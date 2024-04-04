#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python38 python38Packages.numpy

import sys
import numpy
from pathlib import Path
from pypdfium2 import PdfDocument

input_pdf_path = Path(sys.argv[1])
input_pdf_doc = PdfDocument(input_pdf_path)

lastpix = None
containpages = []

for page_i, page in enumerate(input_pdf_doc):
    pix = page.render(grayscale=True).to_numpy()

    if lastpix is not None:
        isconsecutive = numpy.all(lastpix >= pix)
        if not isconsecutive:
            containpages.append(page_i - 1)

    lastpix = pix
containpages.append(page_i)

print(f"reduced {len(input_pdf_doc)}-pages pdf to {len(containpages)}-pages pdf")
output_pdf_doc = PdfDocument.new()
output_pdf_doc.import_pages(input_pdf_doc, containpages)
output_pdf_doc.save(input_pdf_path.with_name("stripped-" + input_pdf_path.name))
