import pandas as pd
from ast import literal_eval
from scrap_pdf_files import get_pdf_content_from_url

data = pd.read_csv("../data/aides_v2.csv")
print(data.columns)
data_with_pdf = data[data['pdfs'] != '[]']

aide = data_with_pdf.sample().iloc[0] # aide prise au hasard pour l'exemple
aide_name = aide['name'] # nom de l'aide
pdfs_list = literal_eval(aide['pdfs']) # liste des urls des pdfs associés à l'aide
first_pdf_content = get_pdf_content_from_url(pdfs_list[0])

print(aide_name)
print(pdfs_list)
print(first_pdf_content)