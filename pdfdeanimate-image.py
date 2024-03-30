#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p poppler_utils pdftk python38 python38Packages.numpy python38Packages.pillow

import subprocess
import sys
import os
import glob
import numpy
from pathlib import Path
from PIL import Image, ImageOps

pdffile = Path(sys.argv[1])
pdffile_name = os.path.splitext(pdffile.name)[0]

pgmdir_name = pdffile.parent/(pdffile_name+"-pgm")
pgmfile_name = pgmdir_name/pdffile_name

try:
    os.mkdir(pgmdir_name)
    subprocess.run(["pdftoppm", "-gray", pdffile, pgmfile_name], stderr=subprocess.DEVNULL)
    print("converted pdf to pgm files")
except FileExistsError:
    print("assuming pdf is already converted to pgm")


lastpix = None
haslastpix = False

containpages = []
currenthold = -1

filelist = glob.glob(os.path.join(pgmdir_name, '*.pgm'))
for filename in sorted(filelist, key=lambda s: s.lower()):
    pagenr = filename.rsplit("/",1)[-1].rsplit(".",1)[0].rsplit("-",1)[-1]

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

print(f"reduced {len(filelist)}-pages pdf to {len(containpages)}-pages pdf")
output_pdffile = pdffile.parent/("stripped-"+pdffile.name)
subprocess.run(["pdftk", pdffile, "cat"] + containpages + ["output", output_pdffile])
