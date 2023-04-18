'''this script is used to transfer the downloaded pdf ESG reports to txt file'''

from PyPDF2 import PdfReader
import pandas as pd
import re
import time
import os


def remove_non_ascii(text):
    '''
    delete non-English characters
    '''
    return "".join(i for i in text if ord(i)<128)

def clean(str):
    '''
    preliminary pre-process
    '''
    str = re.sub(r'\d+',"",str) #remove digits
    str = str.replace("\xa0", " ")
    str = ''.join(str).strip()
    str = str.replace("\n", "")
    return str

def pdf_to_text(pdf_file_path, txt_file_path):
    '''
    PDF2 lib to transform the format
    '''
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page_index in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_index]
            text += page.extract_text()
        text = remove_non_ascii(clean(text)) # clean here
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(text)

pdf_path="/Volumes/Longlive/Research_Assistant/ESG_report/HKEX/Reports/2016"
txt_path="/Volumes/Longlive/Research_Assistant/ESG_report/HKEX/Reports/txt/"

pdfs=os.listdir(pdf_path)
pdfs = [pdf for pdf in pdfs if pdf[0]!="."] # mac generated contents


# final sample generated before
#final_sample=pd.read_csv("/Volumes/Longlive/Research_Assistant/ESG_report/HKEX/Reports_info/sample_info.csv") 
#pdf_list = final_sample["pdf_name"].to_list()

start_time = time.time()
for i in range(len(pdfs)):
    try:
        print("transforming " + str(i) + " file named " + pdfs[i])
        pdf_to_text(pdf_path+"/"+pdfs[i],txt_path+pdfs[i][:-4]+".txt")
    except:
        print("File "+ pdfs[i] +"does not exist")
        pass
print("--- %s seconds ---" % (time.time() - start_time))