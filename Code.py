from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import wget
import pandas as pd
s = Service("C:/Users/PUNEET/Downloads/chromedriver.exe")
driver = webdriver.Chrome()  # service=s)
driver.get("https://www.zalando.co.uk/womens-clothing-tops/")
#time.sleep(5)
while driver.find_elements_by_tag_name("div") is None:
    continue
#WebDriverWait(driver, 55).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfpFfd g88eG_ oHRBzn LyRfpJ _LM JT3_zV g88eG_')))
select_boxx = driver.find_elements_by_tag_name("a")
select_box1=[]
stored_data = {"Brand Name": [],"Model":[], "Product Price": [], "Details":[]}
df = pd.DataFrame(data=stored_data)
count=0
ii=0
path = os.getcwd()
path = os.path.join(path, "Images")
os.mkdir(path)
final_output=[]
while count<1010:
    for image in select_boxx:
        if image.get_attribute("class") == "VfpFfd g88eG_ oHRBzn LyRfpJ _LM JT3_zV g88eG_":
            select_box1.append(image.get_attribute("href"))
    print(len(select_box1), count+1)
    for i in range(len(select_box1)):
        driver1 = webdriver.Chrome()  # service=s)
        driver1.get(select_box1[i])
        #time.sleep(5)
        while driver.find_elements_by_tag_name("div") is None:
            continue
        element = driver1.find_elements_by_tag_name("img")
        element1 = []
        # Data Section Starts
        temp_storage = []
        data = driver1.find_elements_by_tag_name("span")
        for d in data:
            if d.get_attribute("class") == "u-6V88 ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP zN9KaA":
                temp_storage.append(d.get_attribute("textContent"))
        print(count,temp_storage)
        if len(temp_storage)==0:
            stored_data["Details"]="-"
        elif len(temp_storage)==1:
            stored_data["Details"] = temp_storage[0]
        elif len(temp_storage)==2 or len(temp_storage)==3:
            stored_data["Details"] = temp_storage[0] + ", " + temp_storage[1]
        else:
            stored_data["Details"] = temp_storage[0]+", "+temp_storage[1]+", "+temp_storage[3]
        dss = driver1.find_elements_by_tag_name("h1")
        f=0
        for ds in dss:
            if ds.get_attribute("class") == "OEhtt9 ka2E9k uMhVZi z-oVg8 pVrzNP w5w9i_ _1PY7tW _9YcI4f":
                stored_data["Model"]=ds.get_attribute("textContent")
                yy=ds.get_attribute("textContent")
                f=1
                break
        if f==0:
            stored_data["Model"] ="-"
            yy = "-" + str(count) + " "
        f=0
        data2 = driver1.find_elements_by_tag_name("span")
        for d2 in data2:
            if d2.get_attribute("class") == "uqkIZw ka2E9k uMhVZi dgII7d z-oVg8 _88STHx cMfkVL":
                stored_data["Product Price"] = d2.get_attribute("textContent")[1:]
                f=1
                break
            if d2.get_attribute("class") == "uqkIZw ka2E9k uMhVZi FxZV-M z-oVg8 pVrzNP":
                stored_data["Product Price"] = d2.get_attribute("textContent")[1:]
                f=1
                break
        if f==0:
            stored_data["Product Price"] ="-"
        f=0
        data3 = driver1.find_elements_by_tag_name("h3")
        for d3 in data3:
            if d3.get_attribute("class") == "OEhtt9 ka2E9k uMhVZi uc9Eq5 pVrzNP _5Yd-hZ":
                xx=d3.get_attribute("textContent")
                stored_data["Brand Name"] = d3.get_attribute("textContent")
                f=1
                break
        if f==0:
            stored_data["Brand Name"] ="-"
            xx="-"+str(count)+" "
        xx=xx.split(" ")[0]
        yy=yy.split(" ")[0]
        path1 = os.path.join(path, xx +"-"+yy+" "+ str(count+1))
        os.mkdir(path1)
        df = df.append(stored_data, ignore_index=True)
        # Data Section Ends
        # Image Section Starts
        s=1
        for ele in element:
            if ele.get_attribute("class") == "_6uf91T z-oVg8 u-6V88 ka2E9k uMhVZi FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF PZ5eVw":
                try:
                    if ele.get_attribute("src")[-3:] == "800":
                        continue
                    x = ele.get_attribute("src")[:-2] + "800"
                    driver2 = webdriver.Chrome()  # service=s)
                    driver2.get(x)
                    while driver.find_elements_by_tag_name("img") is None:
                        continue
                    save_as = os.path.join(path1, "Picture " + str(s) + ".jpg")
                    s += 1
                    wget.download(x, save_as)
                except:
                    pass
                try:
                    driver2.close()
                except:
                    pass
                if s>4:
                    break
        #Image Section Ends
        count+=1
        try:
            driver1.close()
        except:
            pass
        if count>1010:
            break
        #break
    #driver.close()
    ur="https://www.zalando.co.uk/womens-clothing-tops/?p="+str(ii+2)
    ii=ii+1
    driver = webdriver.Chrome()  # service=s)
    driver.get(ur)
    while driver.find_elements_by_tag_name("div") is None:
        continue
    select_boxx = driver.find_elements_by_tag_name("a")
    select_box1 = []
#print(stored_data)
print(count)

df.to_csv("My_Data.csv",mode='a',index=False)
try:
    driver.close()
except:
    pass
#1:30 277