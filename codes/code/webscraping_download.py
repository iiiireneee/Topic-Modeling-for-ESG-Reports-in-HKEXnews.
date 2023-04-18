import requests
import pandas as pd
import time, re

def download(link,name):
    r = requests.get(link, allow_redirects=True)
    open(name, 'wb').write(r.content)

def get_df(year):
    df = pd.read_csv("/Users/irene/PycharmProjects/webscraping/ESG/ESG/sample_annual_report/报告信息/hkexesg_" + str(year) + ".csv", dtype={" stock_code":'str'})
    return df


def create_name_and_get_links(df, row):
    pub_year = re.search(r"\d{4}", df["release_time"][row]).group(0)
    stock_code=str(df[" stock_code"][row]).split("/")[0]
    doc_name="_".join([pub_year,stock_code])
    doc_name=doc_name+".pdf"
    doc_size = str(df[" report_type"][row]).split(" ")[-1]

    doc_link=df[" report_url"][row]

    return doc_link, doc_name, doc_size


if __name__ == "__main__":

    df=get_df(2023)

    for row in range(len(df)):

        doc_link, doc_name1, doc_size= create_name_and_get_links(df, row)
        doc_name="/Volumes/Longlive/Research_Assistant/ESG_report/HKEX/Reports/2023/"+doc_name1
        download(doc_link,doc_name)

        print('下载进度：', f'{row}/{len(df)}')
        print("The current processing file is " + str(doc_name1) + ", whose size is " + str(doc_size))
        print("-" * 20)

        time.sleep(3)
