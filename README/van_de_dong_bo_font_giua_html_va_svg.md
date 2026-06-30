Mục tiêu chính của mình:
- Xuất SVG từ TikZ (vẽ hình toán học) dùng font STIX từ thư mục assets/fonts/.
- Đồng bộ font giữa SVG và HTML: SVG phải dùng cùng font với trang web.
Những gì mính đang có bao gồm:
1. Thư mục chứa fonts cần dùng:
DELL@DESKTOP-FDUACVV MINGW64 /e/zo-math (master)
$ tree assets/fonts
assets/fonts
|-- STIXTwoMath.otf
|-- STIXTwoMath.woff2
|-- STIXTwoText-Bold.otf
|-- STIXTwoText-Bold.woff2
|-- STIXTwoText-BoldItalic.otf
|-- STIXTwoText-BoldItalic.woff2
|-- STIXTwoText-Italic.otf
|-- STIXTwoText-Italic.woff2
|-- STIXTwoText-Medium.otf
|-- STIXTwoText-Medium.woff2
|-- STIXTwoText-MediumItalic.otf
|-- STIXTwoText-MediumItalic.woff2
|-- STIXTwoText-Regular.otf
|-- STIXTwoText-Regular.woff2
|-- STIXTwoText-Semibold.otf
|-- STIXTwoText-Semibold.woff2
|-- STIXTwoText-SemiboldItalic.otf
`-- STIXTwoText-SemiboldItalic.woff2

2. Tệp tikz đang ở đây E:\zo-math\figures\toan-tai-hien\khai-trien-luy-thua-nhi-thuc-thanh-da-thuc\so-do-nhan-phan-phoi-hai-nhi-thuc.tex, và nội dung của nó là
\documentclass{standalone}
\newcommand{\FontPath}{../../../assets/fonts/} 
\input{../../../assets/tex/tikz-preamble.tex}% Dự phòng nếu chưa định nghĩa
\begin{document}
\begin{tikzpicture}%[level distance=1.5cm,sibling distance=2.5cm]
    % Dòng thứ nhất
    \node (d11) at (-1,12) {$1$};
    \node (d12) at (0,12) {$+$};
    \node (d13) at (1,12) {$x$};
    
    % Dòng thứ hai
    \node (d21) at (-2, 10.5) {$1$};
    \node (d22) at (-1, 10.5) {$+$};
    \node (d23) at (0, 10.5) {$2x$};
    \node (d24) at (1, 10.5) {$+$};
    \node (d25) at (2, 10.5) {$x^2$};

    % Các nhị thức tương ứng
    \node (d1l) at (-4,12) {$(1+x)^1$};
    \node (d2l) at (-4,10.5) {$(1+x)^2$};
    \node (d1r) at (4,12) {$p_1$};
    \node (d2r) at (4,10.5) {$p_2$};
    
    % Các đoạn thẳng
    \begin{scope}[every path/.style={color=gray}, every node/.style={color=gray,font=\tiny}]  

    \draw [->] (d11)--(d21) node[midway, left] {$1$};
    \draw [->] (d11)--(d23) node[midway, right] {$x$};
    \draw [->] (d13)--(d23) node[midway, left] {$1$};
    \draw [->] (d13)--(d25) node[midway, right] {$x$};

    \draw [->] (d1l)--(d2l) node[midway,right] {$1+x$};
    \draw [->] (d1r)--(d2r) node[midway,right] {\(1+x\)};
    \end{scope}
    
\end{tikzpicture}
\end{document}

3. Tệp preamble-tikz.tex đang ở đây E:\zo-math\assets\tex\tikz-preamble.tex và nội dung của nó đang là
\RequirePackage{iftex}

% LUÔN dùng font WOFF2 cho SVG/HTML
\ifdefined\HCode
  \RequirePackage{fontspec}
  \providecommand{\FontPath}{../../../assets/fonts/}
  \setmainfont{STIXTwoText}[
    Path = \FontPath,
    Extension = .woff2,
    UprightFont = *-Regular,
    BoldFont = *-Bold
  ]
  \setmathfont{STIXTwoMath}[
    Path = \FontPath,
    Extension = .woff2
  ]
\else
  % Giữ nguyên cấu hình PDF nếu cần
  \RequirePackage{fontspec}
  \setmainfont{STIXTwoText}[
    Path = \FontPath,
    Extension = .otf,
    UprightFont = *-Regular
  ]
\fi

% Cấu hình TikZ
\usetikzlibrary{arrows.meta, positioning}

Bây giờ mình cần làm gì, sửa gì?