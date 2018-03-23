#	Coded by Medhaja H L on 04-03-2018
#	Designed to scrape rating and review of a product.
#	Goto the page of the product and click "see all **** reviews" and copy the url, paste while running this script.
#	Enter number of pages you want to scrape data from.(Generally in one pages there are around 10 to 12 review of a product)
#	this script is coded to run on Python 2.7.13 :: Anaconda 4.0.0 (64-bit) if you have python is 3.3 or higher,this script doesnt work unless
#	some minor changes
#	Tested on Windows 10 64-bit comp

from bs4 import BeautifulSoup
import requests
import urllib
import json
import validators
import csv
#import pandas as pd
from itertools import izip

def get_soup(url,header):
	return BeautifulSoup(urllib.urlopen(url),'html.parser',from_encoding="iso-8859-1")


query = raw_input("Enter review url:\n")
header={'User-Agent':"Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}

rlist=[]			#review list which contains all the reviews.
rating_list=[]		#rating list which contains all the ratings.
link = query		#query is permanent address which user has entered and link is the url of different pages.it keeps on changing.  
permlink=link		#permlink is permanent address of the starting address.we append the "&&pagenumber=2" in the second iteration and later we change the page number and store it in link.
pages = input("Enter total number of pages you want to traverse \n")+1
num=pages		
total_reviews_collected=0
ex=0				#ex->contain exceptions and data which is in non textual format
for i in xrange(num):#iterates num number of times to collect reviews from num number of pages
	so = get_soup(link,header)
	print("\n")
	print("updated link is\t")
	print(link)
	flag=0
	product = so.find_all("div",class_="a-section review")
	if len(product) != 0:
		review_flag=0
		rating_flag=0
		flag=1
		for rev in product:
			data = rev.find_all("div",class_="a-row")
			rating = str(rev.find_all("span",class_="a-icon-alt"))
			try:
				print("Rating %d - %s" % (i, rating[26:44]))
				rating_flag=1
			except:
				print("couldnot get rating\n")
			for tag in data:
				r = tag.find("span", class_="a-size-base review-text")
				try:
					rev=r.text.decode('ascii')
					print("Review %d - %s" % (i, rev))
					review_flag=1
					total_reviews_collected+=1
					print("\n")
					i+=1
				except Exception as e:
					ex=ex+1
			if(rating_flag==1 and review_flag==1):
				rating_list.append(rating[26:44])
				rlist.append(rev)
			if flag != 1: 
				print("No Reviews Found")
		num=num-1
		if((num+1)==pages):		#if the iteration is the 1st iteration add "&&pagenumber=2" to link and modify the permanent page number.this modification if final.
			link=link+"&&pageNumber=2"
			permlink=permlink+"&&pageNumber="
		else:
			link=permlink[:len(permlink)]+str(pages-num+1)#this statement executes for all the value of i except for the first one.this statement adds
			#the pagenumber to the permlink and assigns it to link.
else:
	print("DONE!!!!")
	print('total Reviews collected is '+str(total_reviews_collected))
	print(ex)
	#my_df = pd.DataFrame(rlist)			#if you want only review then you can use panda.import panda and uncomment these lines and 
	#comment the lines from 80.
	#my_df.to_csv('my_csv.csv', index=False, header=False)
	with open('some.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(izip(rating_list, rlist))
