document.addEventListener("DOMContentLoaded", function () {
  const tooltips = document.querySelectorAll(".tooltip-zomath");

  tooltips.forEach((tooltip) => {
    tooltip.addEventListener("mouseover", function () {
      const rect = tooltip.getBoundingClientRect();
      const tooltipText = tooltip.querySelector(".tooltiptext");
      const tooltipRect = tooltipText.getBoundingClientRect();
      const windowWidth = window.innerWidth;
      const pageRect = document.body.getBoundingClientRect(); // Lấy kích thước trang

      // Xóa lớp cũ
      tooltip.classList.remove("near-left", "near-right");

      // Kiểm tra tràn lề trái
      if (rect.left - tooltipRect.width / 2 < 20) {
        tooltip.classList.add("near-left");
      }
      // Kiểm tra tràn lề phải
      else if (rect.right + tooltipRect.width / 2 > windowWidth - 20) {
        tooltip.classList.add("near-right");
      }
    });
  });
});
