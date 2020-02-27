#import all the necessary libraries.In our case CSV,pandas,selenium,BeautifulSoup

import csv
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

#method to start the webdriver
def use_selenium_automation():
    driver = webdriver.Firefox()
    return driver

#method to crawl through web pages and extract postal codes in a list
def crawl_and_scrap_webpages(driver):
    url="https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_"       #wikipedia page
    web_pages=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']    #wikipedia pages starting with different alphabets
    postal_codes = []                                                         #list to store the postal codes 
    postal_codes.append(["IATA_code","ICAO_code","AIRPORT_NAME"])
    for wp in web_pages:                                                  #crawl through each web page
        driver.get(url+wp)                                                #browse this web page automatically
        extracted_page_source = driver.page_source
        soup = BeautifulSoup(extracted_page_source,"lxml")                #handle the pagesource to beautifulsoup
        table = soup.find('table',{'class':'wikitable sortable'})           #find table with classname 'wikitable sortable' 
        if(table!=None):                                            #if table not found continue
            for table_row in table.find_all('tr'):                          #iterate through each row of table
                columns = table_row.find_all('td')
                postal_code = []
                i=0
                for column in columns:                #iterate through each column and add the 1st ,2nd ,3rd column
                    if i==0  or i==1 or i==2:
                        postal_code.append(column.text)
                    if i==2:
                        break
                    i+=1
                if(len(postal_code)!=0):
                    postal_codes.append(postal_code)
    return postal_codes

#method to store extracted information in pandas dataframe
def create_pandas_dataframe(postal_codes):      
    df = pd.DataFrame(postal_codes[1:], columns =['IACA_CODE','ICAO_code', 'AIRPORT_NAME']) 
    return df
                                   
#method to store extracted information in pandas dataframe
def create_csv_file(postal_codes):
    with open('Airport_Code.csv', 'w', newline='') as f:
        create_csv = csv.writer(f)
        create_csv.writerows(postal_codes)
    return 
                                   
#method to close the driver
def close_driver(driver):
    driver.close()
    return 
                                   
#print the pandas dataframe
def show_pandas_dataframe(df):
    print(df)
    return
                                   
                                   
if __name__=="__main__":
    driver=use_selenium_automation()  #get driver
    postal_codes=crawl_and_scrap_webpages(driver)  #get list of postal codes of airport
    df=create_pandas_dataframe(postal_codes)       #create pandas dataframe
    show_pandas_dataframe(df)                    # print the dataframe
    create_csv_file(postal_codes)                  #create seperate file in csv format 
    close_driver(driver)                           #close the web driver
