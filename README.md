# Anki CLP


## Get Anki to build the cards

Install [pdf2svg](https://github.com/dawbarton/pdf2svg) and [LibRSVG](https://wiki.gnome.org/Projects/LibRsvg) using your package manager of choice to build LaTeX as svg.

Install [Edit LaTeX build process](https://ankiweb.net/shared/info/937148547) from AnkiWeb.

Copy the following to the configuration of `Edit LaTeX build process` under `Tools->Add-Ons`.

```
{
    "pngCommands": [
        [
            "latex",
            "-interaction=nonstopmode",
            "tmp.tex"
        ],
        [
            "dvipng",
            "-D",
            "200",
            "-T",
            "tight",
            "tmp.dvi",
            "-o",
            "tmp.png"
        ]
    ],
    "svgCommands": [
        [
            "xelatex",
            "-interaction=nonstopmode",
            "tmp.tex"
        ],
        [
            "pdf2svg",
            "tmp.pdf",
            "tmp-unscaled-svg"
        ],
        [
            "rsvg-convert",
            "--zoom=2",
            "--format=svg",
            "tmp-unscaled-svg",
            "-o",
            "tmp.svg"
        ]
    ]
}
```
