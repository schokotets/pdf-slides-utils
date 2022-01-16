# pdf-slides-utils
a collection of (linux) utility scripts to deal with pdf presentations at uni

When `nix-shell` is installed, dependencies should be automatically downloaded on script execution. I assume the user has `nix-shell` installed when listing run commands.

## pdfdeanimate-image.py

This utility removes the "animation" (step-by-step reveal) slides from a pdf.

- It takes a pdf file that was exported from a presentation.
- It detects the image difference between two consecutive pages (assuming white background).
- It omits a page if its consecutive page only enhances it.

Run it via: `./pdfdeanimate-image.py pdffile.pdf`

The output will be `stripped-pdffile.pdf`.

## pdf2msvg.sh

This utility converts each page of a pdf into a minimized 720-width svg.

Run it via: `./pdf2msvg pdffile.pdf [program_to_open_svg_with]`

The output will be `pdffile-pages/pdffile-pageNNN.svg`.
