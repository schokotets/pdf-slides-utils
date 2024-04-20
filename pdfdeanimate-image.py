#!/usr/bin/env python3
import subprocess
import os
import glob
import numpy
from PIL import Image
import sys
from pathlib import Path

def process_pdf(pdffile_path):
    pdffile_path = Path(pdffile_path)
    pdffile_name = pdffile_path.stem
    pgmdir_name = pdffile_name + "-pgm"
    pgmfile_name = pgmdir_name + "/" + pdffile_name

    try:
        os.mkdir(pgmdir_name)
        subprocess.run(["pdftoppm", "-gray", str(pdffile_path), pgmfile_name], stderr=subprocess.DEVNULL)
        print(f"converted {pdffile_path} to pgm files")
    except FileExistsError:
        print("assuming pdf is already converted to pgm")

    lastpix = None
    haslastpix = False
    containpages = []
    currenthold = 0

    filelist = glob.glob(os.path.join(pgmdir_name, '*.pgm'))
    total_pages = len(filelist)

    for filename in sorted(filelist, key=lambda s: s.lower()):
        pagenr = int(filename.rsplit("/", 1)[-1].rsplit(".", 1)[0].rsplit("-", 1)[-1])
        img = Image.open(filename)
        pix = numpy.array(img)
        img.close()

        if haslastpix:
            isconsecutive = numpy.all(lastpix >= pix)
            if not isconsecutive:
                containpages.append(currenthold)

        lastpix = pix
        haslastpix = True
        currenthold = pagenr

    if currenthold <= total_pages:
        containpages.append(currenthold)

    print(f"reduced {total_pages}-page PDF to {len(containpages)} pages")
    containpages_str = [str(page) for page in containpages]  # Convert page numbers to strings without incrementing
    subprocess.run(["pdftk", str(pdffile_path), "cat"] + containpages_str + ["output", "stripped-" + pdffile_path.name])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process PDF files specified as command line arguments
        for pdffile_path in sys.argv[1:]:
            process_pdf(pdffile_path)
    else:
        # Process all PDF files in the current directory
        for pdffile_path in Path.cwd().glob('*.pdf'):
            process_pdf(str(pdffile_path))