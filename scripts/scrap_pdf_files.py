"""Executes a script to retrieve pdf from given url in
an aid on aides-territoires.beta.gouv.fr API
"""
import json
import os
import re
from urllib.parse import urlparse

import pandas as pd

from datasource.io import get_data_from_url
from datasource.utils import get_logger

# DEFINING GLOBAL VARIABLES
from scripts.read_pdf_files import get_pdf_content_from_url

API_URL = "https://aides-territoires.beta.gouv.fr/api/aids/"
CRITERIA_WORDS = ["conditions", "critères", "éligible", "éligibilité"]
logger = get_logger("SCRAP_PDF_FROM_API")
NUM_SCRAP = 1


def is_url_working(url, logger):
    """Checks that url is working or not.

    Controls:
    - url start with http
    - Status code not 200
    - Url redirect into another one
    - also catch unexpected error

    Parameters
    ----------
    url : str
        Url to check
    logger : Logger
        logger to display information

    Returns
    -------
    bool
        Whether the url is valid or not
    str
        string explaining the problem
    """

    if not url.startswith("http"):
        return False, "url not starting with http"

    # logger.info("%s" % url)

    try:
        resp = get_data_from_url(url)
    except Exception as e:
        logger.error(e)
        return False, "Unknown error"

    if resp.status_code != 200:
        logger.error("Status code not 200, instead %i" % resp.status_code)
        return False, "Status %i" % resp.status_code

    if resp.url != url:
        logger.error("url changed to %s" % resp.url)
        return False, "url changed to %s" % resp.url

    return True, resp


def scrap_pdf_in_url(resp):
    """Find all pdf in a html page and scrap them

    Parameters
    ----------
    resp :
        requests response of an url

    Returns
    -------
    list
        List of pdf find in an url
    """

    # pdf_urls = re.findall(r"http.*\.pdf", resp.text)
    pdf_urls = re.findall(r"(?:(?!\"|').)*?\.pdf", resp.text)

    if len(pdf_urls) == 0:
        return []

    pdf_with_criterias = []

    for pdf_url in set(pdf_urls):
        if pdf_url.startswith("/"):
            parsed_url = urlparse(resp.url)
            domain = parsed_url.netloc
            pdf_url = "http://" + domain + pdf_url

        # logger.debug("PDF Analyse : %s" % pdf_url)
        try:
            txt = get_pdf_content_from_url(pdf_url)

            find_word = []

            for w in CRITERIA_WORDS:
                if w in txt:
                    find_word.append(w)

            if len(find_word) != 0:
                # logger.debug("CRITERIAS FOUND with %s" % (" ".join(find_word)))
                pdf_with_criterias.append(pdf_url)
        except:
            continue

    return pdf_with_criterias


def get_one_aide_data(aide, logger):
    """Retrieves all information about one "aide"
    from the API defined in global

    Parameters
    ----------
    aide : dict
        One "aide" from the Mission transition API
    logger :
        Logger to display all informations

    Returns
    -------
    dict
        Result of the "aide" analysis
    """
    global NUM_SCRAP
    name = aide["name"]
    aide_id = aide["id"]
    aide_url = aide["url"]
    orig_url = aide["origin_url"]
    app_url = aide["application_url"]

    logger.info("[%i] - Analyse %s" % (NUM_SCRAP, aide_url))
    NUM_SCRAP = NUM_SCRAP + 1

    current_aide = {"name": name, "url": aide_url, "id": aide_id}

    pdfs = []

    # check orig_url

    is_ok, resp = is_url_working(orig_url, logger)
    current_aide["error_orig"] = is_ok
    if is_ok:
        pdfs += scrap_pdf_in_url(resp)
    else:
        current_aide["type_error_orig"] = resp

    # check app_url
    is_ok, resp = is_url_working(app_url, logger)
    current_aide["error_app"] = is_ok
    if is_ok:
        pdfs += scrap_pdf_in_url(resp)
    else:
        current_aide["type_error_app"] = resp

    current_aide["pdfs"] = pdfs
    current_aide["pdf_avec_criteres"] = False
    if len(pdfs) != 0:
        current_aide["pdf_avec_criteres"] = True

    return current_aide


def get_data_aides_results(data, logger):
    """Analyse all "aides" from the data given
    by the API

    Parameters
    ----------
    data : dict
        Return from the Mission transition API
    logger :
        Logger to display all informations

    Returns
    -------
    [type]
        [description]
    """

    aides_list = []

    for aide in data["results"]:
        try:
            current_aide = get_one_aide_data(aide, logger)
            aides_list.append(current_aide)
        except Exception as e:
            logger.error(e)
            raise e

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


def srap_pdf(
        directory: str,
        csv: str,
):
    """Main script to scrap and find pdfs given the differents url"""
    aides_list = []

    url, aides = scrap_current_api_page(API_URL, logger=logger)
    aides_list += aides

    while url is not None:
        url, aides = scrap_current_api_page(url, logger=logger)
        aides_list += aides

    df = pd.DataFrame(aides_list)
    df.to_csv(os.path.join(directory, csv), index=False)


if __name__ == "__main__":
    srap_pdf(
        directory="data",
        csv="aides_v2.csv"
    )
