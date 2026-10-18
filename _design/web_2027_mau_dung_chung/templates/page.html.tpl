<!DOCTYPE html>
<html lang="vi" data-zo-preferences="zo-web-2027-preview-v1">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>$title · HTML thử nghiệm · ZO Math</title>
  <link rel="icon" href="assets/logos/favicon_color.svg">
  $styles
</head>
<body class="$body_class" data-zo-web-shell>
  <a class="skip" href="#reading">Đến nội dung</a>
  <header class="site-top">
    <a href="$home_href"><img src="assets/logos/horizontal_color.svg" width="112" alt="ZO Math"></a>
    <a class="course-link" href="$home_href">Ôn thi Toán THPT 2027</a>
    <a class="lab-link" href="#reading">HTML thử nghiệm</a>
    $appearance
  </header>
  <div class="workspace">
    <aside class="rail" aria-label="Điều hướng khóa học">
      <div class="rail-heading">
        <a href="$home_href"><img src="assets/logos/horizontal_color.svg" width="148" alt="ZO Math"></a>
        <p class="brand-thought">$brand_thought</p>
      </div>
      <div id="rail-content">$navigation</div>
      <a class="rail-support" href="#ung-ho">Bảo trợ ZO Math ↗</a>
    </aside>
    <main id="reading" tabindex="-1">
      <div class="breadcrumb"><a href="$home_href">Khóa 2027</a><span>/</span>$breadcrumb</div>
      $hero
      $content
      $support
    </main>$site_footer
  </div>
  <button class="mobile-trigger mobile-trigger--icon" type="button" aria-label="Mở mục lục học liệu" aria-haspopup="dialog" aria-controls="mobile-nav" aria-expanded="false"><span aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="M5 6h14M5 12h14M5 18h14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"></path></svg></span><span class="mobile-view" hidden aria-hidden="true">Mục lục học liệu</span></button>
  <dialog id="mobile-nav" aria-labelledby="drawer-title">
    <div class="drawer-top"><strong id="drawer-title">$drawer_title</strong><button class="drawer-close" type="button">Đóng</button></div>
    <div id="drawer-mount"></div>
  </dialog>
  $scripts
</body>
</html>
