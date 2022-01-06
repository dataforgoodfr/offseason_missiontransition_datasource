# offseason_missiontransition

Scrap all the aids from the API : https://aides-territoires.beta.gouv.fr/api/aids/

For each one gives the information of :
- name
- url
- if error on orig url and the type
- if error on app url and the type
- list of pdfs if available on url
- Whether a pdf contains a word from the list given here

`CRITERIA_WORDS = ["conditions", "critères", "éligible", "éligibilité"]`

## Install

```
pip install .
python scripts/scrap_pdf_files.py
```
