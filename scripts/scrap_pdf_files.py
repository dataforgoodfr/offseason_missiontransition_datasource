"""Executes a script to retrieve pdf from given url in
an aid on aides-territoires.beta.gouv.fr API
"""
import json
import re
from io import BytesIO
from urllib.parse import urlparse

import pandas as pd
import PyPDF2

from datasource.io import get_data_from_url
from datasource.utils import get_logger


API_URL = "https://aides-territoires.beta.gouv.fr/api/aids/"
CRITERIA_WORDS = ["conditions", "critères", "éligible", "éligibilité"]
logger = get_logger("SCRAP_PDF_FROM_API")


def is_url_working(url, logger):

    logger.info("%s" % url)
    try:
        resp = get_data_from_url(url)
    except Exception as e:
        logger.error(e)
        return False, None

    if resp.status_code != 200:
        logger.error("Status code not 200, instead %i" % resp.status_code)
        return False, None

    if resp.url != url:
        logger.error("url changed to %s" % resp.url)
        return False, None

    return True, resp


def get_pdf_content_from_url(pdf_url):

    if not pdf_url.endswith(".pdf"):
        raise ValueError("pdf_url must ends with '.pdf'")

    response = get_data_from_url(pdf_url)
    my_raw_data = response.content

    full_text = ""

    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfFileReader(data)

        for page in range(read_pdf.getNumPages()):
            full_text += " " + read_pdf.getPage(page).extractText().lower()

    return full_text


def scrap_pdf_in_url(url, logger):

    if not url.startswith("http"):
        return []

    is_ok, resp = is_url_working(url, logger)

    if not is_ok:
        return []

    # pdf_urls = re.findall(r"http.*\.pdf", resp.text)
    pdf_urls = re.findall(r"(?:(?!\").)*?\.pdf", resp.text)

    if len(pdf_urls) == 0:
        return []

    pdf_with_criterias = []

    for pdf_url in set(pdf_urls):
        if pdf_url.startswith("/"):
            domain = urlparse(url).netloc
            pdf_url = "http://" + domain + pdf_url

        logger.info("PDF Analyse : %s" % pdf_url)
        txt = get_pdf_content_from_url(pdf_url)

        find_word = []

        for w in CRITERIA_WORDS:
            if w in txt:
                find_word.append(w)

        if len(find_word) != 0:
            logger.info("CRITERIAS FOUND with %s" % (" ".join(find_word)))
            pdf_with_criterias.append(pdf_url)

    return pdf_with_criterias


def get_one_aide_data(aide, logger):
    name = aide["name"]
    aide_url = aide["url"]
    orig_url = aide["origin_url"]
    app_url = aide["application_url"]

    logger.info("Analyse %s" % (aide_url))
    current_aide = {"name": name, "url": aide_url}

    pdfs = []

    # check orig_url
    pdfs += scrap_pdf_in_url(orig_url, logger)

    # check app_url
    pdfs += scrap_pdf_in_url(app_url, logger)

    current_aide["pdfs"] = pdfs
    current_aide["pdf_avec_criteres"] = False
    if len(pdfs) != 0:
        current_aide["pdf_avec_criteres"] = True

    return current_aide


def get_data_aides_results(data, logger):

    aides_list = []

    for aide in data["results"]:
        current_aide = get_one_aide_data(aide, logger)
        aides_list.append(current_aide)

    return aides_list


def scrap_current_api_page(url, logger=None):
    """Scrap current API page from aides territoires API.

    Returns the next page if there is one else it returns None
    """
    logger.info("Scrap URL : %s" % url)
    data = get_data_from_url(url)
    next_url = None

    if data.status_code != 200:
        logger.info(
            "Status code different from 200 (HTTP %i instead)" % data.status_code
        )
        return None, []

    # Convert to json object
    data = json.loads(data.text)

    # Whether the url has a next step or not
    if "next" in data:
        next_url = data["next"]

    aides_list = get_data_aides_results(data, logger)

    return next_url, aides_list


def srap_pdf():
    aides_list = []

    url, aides = scrap_current_api_page(API_URL, logger=logger)
    aides_list += aides

    while url is not None:
        url, aides = scrap_current_api_page(url, logger=logger)
        aides_list += aides

        break

    df = pd.DataFrame(aides_list)
    df.to_csv("aides.csv", index=False)


if __name__ == "__main__":
    srap_pdf()
