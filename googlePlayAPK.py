import scrapy
from scrapy.http.request import Request
import json
import numpy as np
import os, sys
import urllib.parse


link_libs = set()
seemorelinks = set()

apkPackagelist = "/home/r/rajawatg/googleAPKTest/apk_package_list.txt"
if os.path.exists(apkPackagelist):
    os.remove(apkPackagelist)

apk_apidownload_list = "/home/r/rajawatg/googleAPKTest/apk_apidownload_list.txt"
if os.path.exists(apk_apidownload_list):
    os.remove(apk_apidownload_list)

def add_record(recordfile, entry):
    with open(recordfile, "a+") as f:
        f.write(entry+"\n")

class GoogleApkSpider(scrapy.Spider):
    name = "googleplayapk"
    allowed_domains = ["play.google.com", "apkcombo.com"]


    def start_requests(self):
        start_url = "https://play.google.com/store/apps?hl=en_US"
        start_url = urllib.parse.quote(start_url.encode('utf8'), ':/')
        yield scrapy.Request(url=start_url, callback=self.parse_apklist_page)


    def parse_apklist_page(self, response):

        currentpage_links = set()
        base = 'https://play.google.com'

        #Extract all hyper links, there should be way to select specfic patterns   
        links = response.xpath("//a/@href").extract()
        
        for link in links:
            if link.startswith("/store/apps/details?id=") and link not in link_libs:
                
                entry1 = base+link + "," + link.split('=')[1]
                link_libs.add(entry1)
                print("Printing in file\n")
                print(entry1)
                add_record(apkPackagelist, entry1)
                yield scrapy.Request(url=link, callback=self.parse_download_page)

            #get links by category
            #elif link.startswith('/store/apps/category/') and link not in seemorelinks:
             #   seemorelinks.add(link)
              #  currentpage_links.add(base + link)
            '''
            #based on 'see more' button
            elif link.startswith("/store/apps/collection/cluster?clp=") and link not in seemorelinks:
                seemorelinks.add(link)
                currentpage_links.add(base + link)
            '''

        '''
        #Recursively get unvisited pages
        if currentpage_links:
            for link in currentpage_links:
                try:
                    yield scrapy.Request(url=link, callback=self.parse_download_page)
                except:
                    print("===> Invalid link!")
        else:
            print("Finish data crawling.")
        '''
        download_base = 'https://apkcombo.com/apk-downloader/?q='
        for package in link_libs:
            link = download_base + package.split('=')[1]
            yield scrapy.Request(url=link, callback=self.parse_download_page)


    
    def parse_download_page(self, response):
        download_link = response.xpath("//a/@href").extract()
        base = 'https://apkcombo.com'
        apklink = ''
        for link in download_link:
            if link.endswith('/download/apk'):
                apklink = base + link
                break

            yield scrapy.Request(url=apklink, callback=self.download_apk)

    
    def download_apk(self, response):
        api_links = response.xpath("//a/@href").extract()
        api = ''
        for link in api_links:
            if link.startswith('https://play.googleapis.com/download/by-token/download?'):
                api = link 
                break
                
        packageName = response.request.url.split('/')[-3]
        entry2 = packageName + "," + api
        add_record(apk_apidownload_list, entry2)
        yield None


