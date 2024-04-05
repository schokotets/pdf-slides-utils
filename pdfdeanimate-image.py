#!/usr/bin/env python3

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from numpy import mean
from pathlib import Path
from pypdfium2 import PdfDocument

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("input_pdf_path", help="Path of PDF to remove duplicate pages from")
parser.add_argument(
    "-t",
    "--tolerance",
    default=0,
    help="Max %% lightened pixels between two pages before considered non-duplicates"
)
args = parser.parse_args()

input_pdf_path = Path(args.input_pdf_path)
input_pdf_doc = PdfDocument(input_pdf_path)

PERCENT_TOLERANCE = float(args.tolerance)
assert 0 <= PERCENT_TOLERANCE < 100
PROPORTION_TOLERANCE = PERCENT_TOLERANCE / 100

lastpix = None
containpages = []

for page_i, page in enumerate(input_pdf_doc):
    pix = page.render(grayscale=True).to_numpy()

    if lastpix is not None:
        isconsecutive = mean(pix > lastpix) <= PROPORTION_TOLERANCE
        if not isconsecutive:
            containpages.append(page_i - 1)

    lastpix = pix
containpages.append(page_i)

print(f"reduced {len(input_pdf_doc)}-pages pdf to {len(containpages)}-pages pdf")
output_pdf_doc = PdfDocument.new()
output_pdf_doc.import_pages(input_pdf_doc, containpages)
output_pdf_doc.save(input_pdf_path.with_name("stripped-" + input_pdf_path.name))
