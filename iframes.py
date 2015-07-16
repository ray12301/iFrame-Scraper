import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import re
import os
import time

urls = []

with open('URLs.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    url_input = next(reader)

for x in url_input:
        urls.append(x)

filedate = time.strftime('%Y%m%d')

#Configures Firefox Browser settings
profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port',9150)
profile.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285')
profile.set_preference("general.acceptlanguage.override","en-GB;q=0.8,en;q=0.6")
profile.set_preference("general.acceptcharset.override","ISO-8859-1,utf-8;q=0.7,*;q=0.3")
profile.set_preference("general.acceptencoding.override","gzip,deflate,sdch")

def lookup(x):
    os.startfile("C:\Users\MAN\Desktop\Python Files\Tor Browser\Browser\Firefox.exe")
    time.sleep(1)
    driver = webdriver.Firefox(profile)
    for x in urls:
        try:
            driver.get('http://www.%s' % x)
            html = driver.page_source
            soup = BeautifulSoup(html,'html5lib')
            soup = soup.prettify().encode('utf-8')
            f = open(x + filedate + '.html', 'w')
            f.write(soup)
            f.close()
        except:
            pass

    driver.close()

def compare(x):
    for x in urls:
        try:
            #Identifies number of iFrames in baseline
            baseline = open(x + ' baseline.html', 'r')
            base_soup = BeautifulSoup(baseline.read())
            base_i = re.findall('(\s*iframe)',str(base_soup))
            print "The baseline", x, "webpage (20150615) has", len(base_i), "iFrames"

            #Identifies number of iFrames in current webpage
            current = open(x + filedate + '.html', 'r')
            current_soup = BeautifulSoup(current.read())
            #Identifies possible hidden or obfusacted iframes in current webpage
            current_i = re.findall('((?i)iframe|(?i)i(\s|\S|\d|\D\w|\W*)f(\s|\S|\d|\D\w|\W*)r(\s|\S|\d|\D\w|\W*)a(\s|\S|\d|\D\w|\W*)m(\s|\S|\d|\D\w|\W*)e)',str(current_soup))
            current_h = re.findall('((?i)width=\S0\S\s*height=\S0\S)',str(current_soup))
            current_o = re.findall('(aWZyYW1l|696672616D65|&#105;&#102;&#114;&#97;&#109;&#101)',str(current_soup))
            print "The current", x, "webpage (", filedate, ") has", len(current_i), "iFrames"
            print ''

            if len(current_h) >= 1 or len(current_o) >= 1:
                print len(current_h) + len(current_o), "possible obfuscated iframe(s) detected"
                print len(current_h), "hidden frame detected"
                print len(current_o), "Base64 or Hex obfuscation detected"
                
        except:
            pass



def main():
    lookup(urls)
    compare(urls)

main()
