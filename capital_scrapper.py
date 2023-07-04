import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime


URL = "https://www.capitalethiopia.com/category/capital/page/"

filename = "localnews.csv"
with open(filename, 'a', newline='') as f:
    w = csv.DictWriter(f,['Index','Title','Link','DatePublished','Body'])
    #w.writeheader()

    pager=369
    count=1472

    for page in range(pager,581):
        #579 Real value
        # Making a GET request
        r = requests.get(URL + str(page) + '/')
        
        # check status code for response received
        # success code - 200
        print(r)
        pager+=1    
        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        #Find the news container
        newscontainer = soup.find("div", class_ = "td-pb-span8 td-main-content")
        # Find relevant items
        titles = newscontainer.find_all("h3", class_="entry-title td-module-title")
        dates = newscontainer.find_all("span", class_="td-post-date")
        
        #Create an empty list of headlines and count variable
        headlines=[]
        for index, title in enumerate(titles):
            d={}
            datestr = dates[index].text
            date = datetime.strftime(datetime.strptime(datestr,"%B %d, %Y"), "%m-%d-%Y")
            link = title.a.get('href')
            title = title.text
            #print(title)
            #print(link)
            d['Index'] = count
            count+=1
            d['Title'] = title
            d['Link'] = link
            r = requests.get(link)
            # check status code for response received
            # success code - 200
            print("Link for Body ---", end=" ")
            print(r)
            
            # Parsing the HTML
            soup = BeautifulSoup(r.content, 'html.parser')
            #Find the news container
            bodycontainer = soup.find("div", class_ = "td-post-content")
            # Find relevant items
            paragraphs = bodycontainer.find_all("p")
            
            body = ""
            for paragraph in paragraphs:
                #print(f"Article {count} contains {len(paragraphs)} paragraphs")
                body += paragraph.text
                               
            d['Body'] = body
            d["DatePublished"] = date
            headlines.append(d)   
        w.writerows(headlines)
        print('Page '+str(pager-1)+' Done')
print(count+1, end=" ")
print("Titles successfully Wrote!")
