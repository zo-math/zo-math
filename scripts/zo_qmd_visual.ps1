param(
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot,

    [Parameter(Mandatory = $true)]
    [string]$Target,

    [int]$Height = 1000
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# Machine-owned viewport evidence for QMD review-ready.
# The script measures the already-rendered HTML at canonical mobile and desktop
# viewports through the same MathJax-ready path, captures screenshots, and records
# runtime dimensions + SHA-256.

$VisualMeasurementVersion = 2
$RequiredMobileWidths = @(390, 430)
$RequiredDesktopWidths = @(1440)
$RequiredWidths = @($RequiredMobileWidths + $RequiredDesktopWidths)
$Root = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd('\', '/')
$RootPrefix = $Root + [System.IO.Path]::DirectorySeparatorChar
$TargetPath = [System.IO.Path]::GetFullPath((Join-Path $Root $Target))
if (-not $TargetPath.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Target lies outside repository: $Target"
}
if ([System.IO.Path]::GetExtension($TargetPath).ToLowerInvariant() -ne '.qmd') {
    throw 'visual-check only accepts one .qmd target.'
}
if (-not (Test-Path -LiteralPath $TargetPath -PathType Leaf)) {
    throw "QMD target not found: $TargetPath"
}

$TargetRelative = $TargetPath.Substring($RootPrefix.Length).Replace('\', '/')
$TargetRelativeHtml = [System.IO.Path]::ChangeExtension($TargetRelative, '.html')
$HtmlPath = Join-Path $Root (Join-Path 'docs' ($TargetRelativeHtml -replace '/', '\'))
if (-not (Test-Path -LiteralPath $HtmlPath -PathType Leaf)) {
    throw "Rendered HTML missing; run QMD render first: $HtmlPath"
}

$Slug = [System.IO.Path]::GetFileNameWithoutExtension($TargetPath)
$VisualDir = Join-Path $Root (Join-Path '_audit' "${Slug}_visual")
New-Item -ItemType Directory -Path $VisualDir -Force | Out-Null
$ReportPath = Join-Path $VisualDir 'html_mobile_measurements.json'

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Find-ChromiumBrowser {
    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($candidate in @(
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
        "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
        "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe",
        "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
        "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
    )) {
        if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            $candidates.Add($candidate)
        }
    }
    foreach ($name in @('msedge.exe', 'msedge', 'chrome.exe', 'google-chrome', 'chromium')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($command -and $command.Source) {
            $candidates.Add($command.Source)
        }
    }
    if ($candidates.Count -eq 0) {
        throw 'No supported Chromium browser (Microsoft Edge / Chrome) was found.'
    }
    return $candidates[0]
}

$CdpId = 0
function Receive-WebSocketText {
    param([System.Net.WebSockets.ClientWebSocket]$Socket)
    $stream = New-Object System.IO.MemoryStream
    try {
        do {
            $buffer = New-Object byte[] 65536
            $segment = [System.ArraySegment[byte]]::new($buffer)
            $result = $Socket.ReceiveAsync(
                $segment,
                [System.Threading.CancellationToken]::None
            ).GetAwaiter().GetResult()
            if ($result.MessageType -eq [System.Net.WebSockets.WebSocketMessageType]::Close) {
                throw 'Chromium DevTools WebSocket closed unexpectedly.'
            }
            if ($result.Count -gt 0) {
                $stream.Write($buffer, 0, $result.Count)
            }
        } while (-not $result.EndOfMessage)
        return [System.Text.Encoding]::UTF8.GetString($stream.ToArray())
    }
    finally {
        $stream.Dispose()
    }
}

function Invoke-Cdp {
    param(
        [System.Net.WebSockets.ClientWebSocket]$Socket,
        [string]$Method,
        [hashtable]$Params = @{}
    )
    $script:CdpId += 1
    $id = $script:CdpId
    $payload = @{
        id = $id
        method = $Method
        params = $Params
    } | ConvertTo-Json -Compress -Depth 40

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $segment = [System.ArraySegment[byte]]::new($bytes)
    $Socket.SendAsync(
        $segment,
        [System.Net.WebSockets.WebSocketMessageType]::Text,
        $true,
        [System.Threading.CancellationToken]::None
    ).GetAwaiter().GetResult() | Out-Null

    while ($true) {
        $text = Receive-WebSocketText -Socket $Socket
        $message = $text | ConvertFrom-Json
        if (($message.PSObject.Properties.Name -contains 'id') -and [int]$message.id -eq $id) {
            if ($message.PSObject.Properties.Name -contains 'error') {
                throw "CDP $Method failed: $($message.error | ConvertTo-Json -Compress)"
            }
            return $message
        }
    }
}

function Invoke-RuntimeValue {
    param(
        [System.Net.WebSockets.ClientWebSocket]$Socket,
        [string]$Expression,
        [bool]$AwaitPromise = $false
    )
    $reply = Invoke-Cdp -Socket $Socket -Method 'Runtime.evaluate' -Params @{
        expression = $Expression
        returnByValue = $true
        awaitPromise = $AwaitPromise
    }
    if ($reply.result.PSObject.Properties.Name -contains 'exceptionDetails') {
        throw "Runtime.evaluate exception: $($reply.result.exceptionDetails | ConvertTo-Json -Compress -Depth 10)"
    }
    return $reply.result.result.value
}

function Wait-DocumentReady {
    param([System.Net.WebSockets.ClientWebSocket]$Socket)
    for ($i = 0; $i -lt 100; $i++) {
        try {
            if ((Invoke-RuntimeValue -Socket $Socket -Expression 'document.readyState') -eq 'complete') {
                return
            }
        }
        catch {}
        Start-Sleep -Milliseconds 100
    }
    throw 'Timed out waiting for document.readyState=complete.'
}

$MeasureScript = @'
(async () => {
  if (window.MathJax && MathJax.startup && MathJax.startup.promise) {
    try { await MathJax.startup.promise; } catch (_) {}
  }
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));

  const de = document.documentElement;
  const body = document.body;
  const vw = de.clientWidth;
  const eps = 1;
  const root = document.querySelector('main.content, main, #quarto-content') || body;

  function selector(el) {
    if (!el || el.nodeType !== 1) return null;
    const tag = el.tagName.toLowerCase();
    if (el.id) return `${tag}#${el.id}`;
    const cls = Array.from(el.classList || []).slice(0, 5)
      .map(x => x.replace(/[^a-zA-Z0-9_-]/g, '_'));
    return cls.length ? `${tag}.${cls.join('.')}` : tag;
  }

  function visible(el) {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
  }

  function info(el) {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return {
      selector: selector(el),
      left: +r.left.toFixed(2),
      right: +r.right.toFixed(2),
      width: +r.width.toFixed(2),
      clientWidth: el.clientWidth,
      scrollWidth: el.scrollWidth,
      overflowX: s.overflowX,
      whiteSpace: s.whiteSpace,
      text: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 180)
    };
  }

  const content = root ? [root, ...Array.from(root.querySelectorAll('*'))].filter(visible) : [];
  const offenders = content
    .filter(el => {
      const r = el.getBoundingClientRect();
      return r.right > vw + eps || r.left < -eps;
    })
    .map(info)
    .sort((a, b) => Math.max(b.right - vw, -b.left) - Math.max(a.right - vw, -a.left))
    .slice(0, 30);

  return {
    windowInnerWidth: window.innerWidth,
    documentClientWidth: de.clientWidth,
    documentScrollWidth: de.scrollWidth,
    bodyClientWidth: body ? body.clientWidth : null,
    bodyScrollWidth: body ? body.scrollWidth : null,
    horizontalOverflow: de.scrollWidth > de.clientWidth + eps,
    overflowPx: de.scrollWidth - de.clientWidth,
    offenderCount: offenders.length,
    offenders
  };
})()
'@

$Browser = Find-ChromiumBrowser
$BrowserProcess = $null
$Socket = $null
$Profile = Join-Path ([System.IO.Path]::GetTempPath()) ("zo-qmd-visual-" + [guid]::NewGuid().ToString('N'))
$Port = Get-Random -Minimum 12000 -Maximum 19000
$Records = New-Object System.Collections.Generic.List[object]
$HadFailure = $false

try {
    New-Item -ItemType Directory -Path $Profile -Force | Out-Null
    $browserArgs = @(
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        '--force-device-scale-factor=1',
        '--allow-file-access-from-files',
        '--remote-allow-origins=*',
        "--remote-debugging-port=$Port",
        "--user-data-dir=$Profile",
        'about:blank'
    )
    $BrowserProcess = Start-Process -FilePath $Browser -ArgumentList $browserArgs -PassThru -WindowStyle Hidden

    $targets = $null
    for ($i = 0; $i -lt 100; $i++) {
        try {
            $targets = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/json" -TimeoutSec 1
            if ($targets) { break }
        }
        catch {}
        Start-Sleep -Milliseconds 100
    }
    if (-not $targets) {
        throw 'Could not connect to Chromium DevTools endpoint.'
    }
    $page = $targets | Where-Object { $_.type -eq 'page' } | Select-Object -First 1
    if (-not $page -or -not $page.webSocketDebuggerUrl) {
        throw 'No debuggable Chromium page target was found.'
    }

    $Socket = New-Object System.Net.WebSockets.ClientWebSocket
    $Socket.ConnectAsync(
        [Uri]$page.webSocketDebuggerUrl,
        [System.Threading.CancellationToken]::None
    ).GetAwaiter().GetResult() | Out-Null
    Invoke-Cdp -Socket $Socket -Method 'Page.enable' | Out-Null
    Invoke-Cdp -Socket $Socket -Method 'Runtime.enable' | Out-Null

    $FileUrl = 'file:///' + ($HtmlPath -replace '\\', '/')
    foreach ($Width in $RequiredWidths) {
        Invoke-Cdp -Socket $Socket -Method 'Emulation.setDeviceMetricsOverride' -Params @{
            width = [int]$Width
            height = [int]$Height
            deviceScaleFactor = 1
            mobile = $false
            screenWidth = [int]$Width
            screenHeight = [int]$Height
        } | Out-Null

        Invoke-Cdp -Socket $Socket -Method 'Page.navigate' -Params @{ url = $FileUrl } | Out-Null
        Wait-DocumentReady -Socket $Socket
        Start-Sleep -Milliseconds 250
        $measurement = Invoke-RuntimeValue -Socket $Socket -Expression $MeasureScript -AwaitPromise $true

        $ViewportClass = $(if ($RequiredDesktopWidths -contains [int]$Width) { 'desktop' } else { 'mobile' })
        $ScreenshotName = "html_${ViewportClass}_${Width}.png"
        $ScreenshotPath = Join-Path $VisualDir $ScreenshotName
        Invoke-RuntimeValue -Socket $Socket -Expression 'window.scrollTo(0, 0); true' | Out-Null
        $shot = Invoke-Cdp -Socket $Socket -Method 'Page.captureScreenshot' -Params @{
            format = 'png'
            fromSurface = $true
            captureBeyondViewport = $false
        }
        [System.IO.File]::WriteAllBytes(
            $ScreenshotPath,
            [Convert]::FromBase64String($shot.result.data)
        )

        $Passed = (
            [int]$measurement.windowInnerWidth -eq [int]$Width -and
            [int]$measurement.documentClientWidth -eq [int]$Width -and
            [int]$measurement.documentScrollWidth -le [int]$measurement.documentClientWidth -and
            -not [bool]$measurement.horizontalOverflow
        )
        if (-not $Passed) { $HadFailure = $true }

        $Records.Add([ordered]@{
            viewport_class = $ViewportClass
            requested_width = [int]$Width
            requested_height = [int]$Height
            window_inner_width = [int]$measurement.windowInnerWidth
            document_client_width = [int]$measurement.documentClientWidth
            document_scroll_width = [int]$measurement.documentScrollWidth
            horizontal_overflow = [bool]$measurement.horizontalOverflow
            overflow_px = [int]$measurement.overflowPx
            offender_count = [int]$measurement.offenderCount
            offenders = @($measurement.offenders)
            screenshot = $ScreenshotPath.Substring($RootPrefix.Length).Replace('\', '/')
            screenshot_sha256 = Get-Sha256Lower -Path $ScreenshotPath
            passed = [bool]$Passed
        })
    }
}
finally {
    if ($Socket) {
        try {
            $Socket.CloseAsync(
                [System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure,
                'done',
                [System.Threading.CancellationToken]::None
            ).GetAwaiter().GetResult() | Out-Null
        }
        catch {}
        $Socket.Dispose()
    }
    if ($BrowserProcess -and -not $BrowserProcess.HasExited) {
        try { Stop-Process -Id $BrowserProcess.Id -Force } catch {}
    }
    if (Test-Path -LiteralPath $Profile) {
        Remove-Item -LiteralPath $Profile -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$Payload = [ordered]@{
    visual_measurement_version = $VisualMeasurementVersion
    generator = 'scripts/zo_qmd_visual.ps1'
    target = $TargetRelative
    rendered_html = $HtmlPath.Substring($RootPrefix.Length).Replace('\', '/')
    rendered_html_sha256 = Get-Sha256Lower -Path $HtmlPath
    required_mobile_viewports = @($RequiredMobileWidths)
    required_desktop_viewports = @($RequiredDesktopWidths)
    measurements = $Records.ToArray()
    automated_result = $(if ($HadFailure) { 'FAIL' } else { 'PASS' })
    exit_code = $(if ($HadFailure) { 1 } else { 0 })
}

$Json = $Payload | ConvertTo-Json -Depth 40
[System.IO.File]::WriteAllText(
    $ReportPath,
    $Json + [Environment]::NewLine,
    (New-Object System.Text.UTF8Encoding($false))
)

Write-Host "VISUAL REPORT: $ReportPath"
foreach ($Record in $Records) {
    $Status = $(if ($Record.passed) { 'PASS' } else { 'FAIL' })
    $Line = 'viewport={0}px inner={1} client={2} scroll={3} overflow={4}px result={5}' -f $Record.requested_width, $Record.window_inner_width, $Record.document_client_width, $Record.document_scroll_width, $Record.overflow_px, $Status
    Write-Host $Line
}
Write-Host "AUTOMATED RESULT: $($Payload.automated_result) | EXIT=$($Payload.exit_code)"
exit [int]$Payload.exit_code
