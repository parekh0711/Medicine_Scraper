import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve
import os

chrome_options = Options()
chrome_options.add_argument("--headless")


input_file = "input.txt"
fptr = open("input.txt", "r")
f1 = fptr.readlines()
for url in f1:
    driver = webdriver.Chrome("chromedriver", options=chrome_options)
    print(url.strip("\n"))
    while 1:
        try:
            driver.get(url.strip("\n"))
            break
        except:
            pass
    print("done")
    name = driver.find_element_by_tag_name("h1").text
    try:
        img = driver.find_element_by_class_name("style__loaded___22epL")
        src = img.get_attribute("src")
        os.system("cls")
        print(src)
    except:
        os.system("cls")
        print("NOT FOUND IMAGE")
        continue
    try:
        os.mkdir(name)
    except FileExistsError:
        driver.close()
        continue
    while 1:
        try:
            urlretrieve(src, name + "/" + name + str(src[-4:]))
            break
        except:
            pass
    driver.close()
fptr.close()
