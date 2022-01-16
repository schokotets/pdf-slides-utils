# pdf-slides-utils

a collection of (linux) utility scripts to deal with pdf presentations at uni

Feel free to contribute: send pull request / open up issues. While these utils were created for my personal use, I thought others (e.g. uni students) could make use of them as well. The better the feature set and system support, the better the aid :)

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

It was created for embedding single pdf pages into Notion, in order to add text notes between pages. If you're looking for a simple image viewer to open the svgs in that has drag-and-drop support, I can recommend [Eye of GNOME (`eog`)](https://wiki.gnome.org/Apps/EyeOfGnome).

Run the utility via: `./pdf2msvg.sh pdffile.pdf [program_to_open_svg_with]`

The output will be `pdffile-pages/pdffile-pageNNN.svg`.
