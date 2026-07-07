// Cấu hình cho MathJax
window.MathJax = {
  tex: {
    tags: "ams", // Sử dụng kiểu đánh số của gói amsmath
    tagSide: "right", // Đặt số hiệu ở bên phải
    tagIndent: "0em", // Khoảng cách từ công thức đến số hiệu
  },
};

// Tạo và thêm polyfill script
var polyfillScript = document.createElement("script");
polyfillScript.src = "https://polyfill.io/v3/polyfill.min.js?features=es6";
document.head.appendChild(polyfillScript);

// Tạo và thêm MathJax script
var mathjaxScript = document.createElement("script");
mathjaxScript.id = "MathJax-script";
mathjaxScript.async = true;
mathjaxScript.src =
  "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js";
document.head.appendChild(mathjaxScript);
//----------------------------------------

// Dữ liệu tài liệu
var bibData = {
  ref1: {
    author: "Edwards, A. W. F.",
    title: "Pascal's Arithmetical Triangle: The Story of a Mathematical Idea",
    year: "2019",
    publisher: "Dover Publications, Inc",
    edition: "Dover edition",
    address: "Mineola, New York",
    isbn: "ISBN: 9780486832791",
    lccn: "LCCN: 2018052526",
    note: "Note: Originally published: London: C. Griffin; New York: Oxford University Press, 1987. Reissued: Baltimore, Maryland: Johns Hopkins University Press, 2002. A republication of the 2002 version by Johns Hopkins University Press. Includes bibliographical references and index",
  },
  // Thêm các tài liệu khác ở đây
};

// Hàm để render danh mục tài liệu
function renderBibliography() {
  var bibliographyDiv = document.getElementById("bibliography");
  for (var key in bibData) {
    if (bibData.hasOwnProperty(key)) {
      var item = bibData[key];
      var entry = document.createElement("div");
      entry.innerHTML = `<p><strong>${item.author}</strong> (${item.year}). <em>${item.title}</em>. ${item.edition}. ${item.note}. ${item.address}. ${item.publisher}. ${item.lccn}. ${item.isbn}.</p>`;
      bibliographyDiv.appendChild(entry);
    }
  }
}

// Gọi hàm để hiển thị danh mục tài liệu khi trang tải xong
document.addEventListener("DOMContentLoaded", function () {
  renderBibliography();
});
//----------------------------------------

