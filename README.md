# pdf-slides-utils
a collection of (linux) utility scripts to deal with pdf presentations at uni

## pdfdeanimate-image.py

This utility removes the "animation" (step-by-step reveal) slides from a pdf.

- It takes a pdf file that was exported from a presentation.
- It detects the image difference between two consecutive pages (assuming white background).
- It omits a page if its consecutive page only enhances it.

Run it via: `./pdfdeanimate-image.py pdffile.pdf`
