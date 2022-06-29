from enum import Enum
from io import BytesIO
from typing import Any

import PyPDF2
import pdftotext as pdftotext
import slate3k as slate

from datasource.io import get_data_from_url


class PdfMethod(Enum):
    PDFTOTEXT = 'pdftotext'
    PYPDF = 'pypdf'
    SLATE = 'slate'


def get_pdf_content_from_url(
        pdf_url: str,
        method: PdfMethod = PdfMethod.PDFTOTEXT
) -> str:
    """Extract all the text from a pdf url

    Parameters
    ----------
    pdf_url : str
        url of the pdf
    method: PdfMethod
        method to extract the PDF content

    Returns
    -------
    str
        string of all the PDF content
    Raises
    ------
    ValueError
        pdf_url must ends with '.pdf'
    """

    if not pdf_url.endswith(".pdf"):
        raise ValueError("pdf_url must ends with '.pdf'")

    response = get_data_from_url(pdf_url)
    my_raw_data = response.content

    if method == PdfMethod.PDFTOTEXT:
        return get_pdf_content_pdftotext(raw_data=my_raw_data)
    elif method == PdfMethod.PYPDF:
        return get_pdf_content_pypdf(raw_data=my_raw_data)
    elif method == PdfMethod.SLATE:
        return get_pdf_content_slate(raw_data=my_raw_data)
    else:
        raise ValueError(f"PdfMethod {method} is not supported")


def get_pdf_content_pypdf(raw_data: Any) -> str:

    full_text = ""

    with BytesIO(raw_data) as data:
        read_pdf = PyPDF2.PdfFileReader(data)

        for page in range(read_pdf.getNumPages()):
            full_text += " " + read_pdf.getPage(page).extractText().lower()

    return full_text


def get_pdf_content_pdftotext(raw_data: Any) -> str:

    full_text = ""

    with BytesIO(raw_data) as data:
        read_pdf = pdftotext.PDF(data)

        for p in read_pdf:
            full_text += " " + p

    return full_text


def get_pdf_content_slate(raw_data: Any) -> str:

    with BytesIO(raw_data) as data:
        extracted_text = slate.PDF(data)

    return '\n\n'.join([t.lower() for t in extracted_text])
