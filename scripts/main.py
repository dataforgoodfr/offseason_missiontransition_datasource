from typing import Optional

from scripts.read_pdf_content import compute_pdf_content
from scripts.scrap_pdf_files import srap_pdf

# whether the pdf scrapping step should be performed
SCRAP_PDF: bool = False

# input and output directory of the pdf scrapping and content extraction
DATA_DIRECTORY: str = "../data"
# input and output CSV of the pdf scrapping and content extraction
CSV_NAME: str = "aides_v3.csv"

# Nb samples with PDF on which the final content should be computed.
# If None, all PDF content will be computed
NB_SAMPLES: Optional[int] = None
# Boolean indicating whether special not yet removed characters should be printed,
# to ease the identification of these characters to be removed
DEBUG_PRINT: bool = False

if __name__ == "__main__":

    if SCRAP_PDF:
        srap_pdf(
            directory=DATA_DIRECTORY,
            csv=CSV_NAME
        )

    compute_pdf_content(
        directory=DATA_DIRECTORY,
        csv=CSV_NAME,
        nb_samples=NB_SAMPLES,
        debug_print=DEBUG_PRINT
    )
