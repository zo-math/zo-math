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
      <a class="rail-support" href="#ung-ho">Ủng hộ ZO Math ↗</a>
    </aside>
    <main id="reading" tabindex="-1">
      <div class="breadcrumb"><a href="$home_href">Nhà khóa 2027</a><span>/</span>$breadcrumb</div>
      $hero
      $content
      $support
    </main>$site_footer
  </div>
  <button class="mobile-trigger" type="button" aria-haspopup="dialog" aria-controls="mobile-nav" aria-expanded="false"><span aria-hidden="true">☰</span><span class="mobile-view">Mục lục khóa học</span></button>
  <dialog id="mobile-nav" aria-labelledby="drawer-title">
    <div class="drawer-top"><strong id="drawer-title">$drawer_title</strong><button class="drawer-close" type="button">Đóng</button></div>
    <div id="drawer-mount"></div>
  </dialog>
  $scripts
</body>
</html>
