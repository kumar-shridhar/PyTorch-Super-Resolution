from bs4 import BeautifulSoup
import requests
import re
import urllib
import os
import argparse
import sys
import json

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
# Download full size images for the given query from google

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib(url,headers=header)),'html.parser')

def main(args):
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=50, type=int, help='num images to save')
	parser.add_argument('-d', '--directory', default='./google_images/', type=str, help='save directory')
	args = parser.parse_args()
	query = args.search#raw_input(args.search)
	max_images = args.num_images
	save_directory = args.directory
	image_type="Action"
	query= query.split()
	query='+'.join(query)
	#url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	url='https://www.google.de/search?as_st=y&tbm=isch&hl=en&as_q='+query+'&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:lt,islt:xga'

	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[]# contains the link for Large original images, type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    ActualImages.append((link,Type))
	for i , (img , Type) in enumerate( ActualImages[0:max_images]):
	    try:
	        req = urllib(img, headers={'User-Agent' : header})
	        raw_img = urllib.request.urlopen(req).read()
	        if len(Type)==0:
	            f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
	        else :
	            f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
	        f.write(raw_img)
	        f.close()
	    except Exception as e:
	        print("could not load : "+img)
	        print(e)

if __name__ == '__main__':
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
