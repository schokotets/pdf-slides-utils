#!/usr/bin/env python3
#!nix-shell -i python3 -p poppler_utils pdftk python38 python38Packages.numpy python38Packages.pillow

import subprocess
import os
import glob
import numpy
from PIL import Image
import sys

def process_pdf(pdffile):
    pdffile_name = pdffile.rsplit(".", 1)[0]
    pgmdir_name = pdffile_name + "-pgm"
    pgmfile_name = pgmdir_name + "/" + pdffile_name

    try:
        os.mkdir(pgmdir_name)
        subprocess.run(["pdftoppm", "-gray", pdffile, pgmfile_name], stderr=subprocess.DEVNULL)
        print(f"converted {pdffile} to pgm files")
    except FileExistsError:
        print("assuming pdf is already converted to pgm")

    lastpix = None
    haslastpix = False
    containpages = []
    currenthold = -1

    filelist = glob.glob(os.path.join(pgmdir_name, '*.pgm'))
    for filename in sorted(filelist, key=lambda s: s.lower()):
        pagenr = filename.rsplit("/", 1)[-1].rsplit(".", 1)[0].rsplit("-", 1)[-1]
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

    containpages.append(currenthold)
    print(f"reduced {len(filelist)}-page PDF to {len(containpages)} pages")
    subprocess.run(["pdftk", pdffile, "cat"] + containpages + ["output", "stripped-" + pdffile])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process PDF files specified as command line arguments
        for pdffile in sys.argv[1:]:
            process_pdf(pdffile)
    else:
        # Process all PDF files in the current directory
        for pdffile in glob.glob('*.pdf'):
            process_pdf(pdffile)
