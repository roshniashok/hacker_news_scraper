#For scraping web page
from bs4 import BeautifulSoup
#For JSON capabilities for the ouput generation
import json
#For creation of the command line utility
import click
#For accessing url to fetch hmtl
import urllib3
#For regex utilities to strip characters from string
import re
#For validating uri
from validator_collection import validators, checkers


#ignores any SSL certificate warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Click used for creating CLI application using decorators
@click.command()
@click.option('--posts',type=click.IntRange(1, 100))

#Main function - starting point
def main(posts):
        pageInit=0 
        totalPosts=[] 
        #Getting total number of pages for appending to URL
        totalPageCounter=countURL(pageInit,posts)
        
        while (totalPageCounter>0):
                
                pageInit=pageInit+1 

                #Appending pagenumber to the url
                url = 'https://news.ycombinator.com/?p='+str(pageInit) 
                http = urllib3.PoolManager()
                r = http.request("GET", url)
                
                #Parsing the retrieved HTML
                soup = BeautifulSoup(r.data, "html.parser") 
                totalPageCounter=totalPageCounter-1

                #Adding results from scraper function 
                totalPosts=totalPosts + scraper(soup) 

        #Limiting results to the number of posts entered in cli
        total=totalPosts[:posts]

        #Displaying output as JSON
        final_json=json.dumps(total,indent=4) 
        
        print(final_json)
                
#Function that returns total no of pages based on the the no of posts entered. Example p=1 (30 posts), p=2(31-60..)
def countURL(pageInit,posts):
        if(posts%30!=0):
                totalPages=(posts/30)+1
                return int(totalPages)
        else:
                totalPages=posts/30
                return int(totalPages)

#Scraper function that scrapes the soup to get desired tags
def scraper(soup):
        
        results = soup.find_all("td", class_="subtext") #Parsing parent tags
        results2 = soup.find_all("tr", class_="athing")
        items=[]
        
        for result,result2 in zip(results,results2):
                
                #Fetching the desired tags using find function of soup from the parent tags
                author=result.find("a",class_="hnuser")
                score=result.find("span",class_="score")
                ranking=result2.find("span",class_="rank")
                titleURL=result2.find("a",class_="storylink")
                title_url=titleURL['href']
                
                #Checking for valid uri
                validURL=checkers.is_url(title_url) 
                if validURL==True: 
                        url=title_url 
                else: 
                        url='Invalid URI'
                
                #Checking for chars more than 256 in title
                article_title=titleURL.string.strip()
                if len(article_title) > 256: 
                        article_title=article_title[:256]
                
                
                rank=result2.td.span.string.strip('.') 

                #Getting "comment" as a child tag from "result" parent tag
                children = result.findChildren()
                for i, child in enumerate(children):
                        if i == 6:
                                comment=child.text

                #removing unicode chars
                comments=re.sub("\u00a0comments|\xa0comments|discuss|\xa0comment","",comment) 
                title_name=re.sub("\u201c|\u201d|\u2013|\u2019","",article_title)

                #checking for chars more than 256 in author 
                if (author==None) : 
                        author_name='empty'
                else: 
                        author_name=result.a['href']
                        if len(author_name) > 256:
                                author_name=author_name[:256]


                #Checking for empty score tags
                if(score==None) : article_score ='None'
                else: article_score=result.span.string.replace("points","")


                #Checking rank,comments,points integers and greater than 0
                if not article_score: article_score = '0'
                elif article_score=='None': article_score='empty'
                elif int(article_score) < 0: article_score = '0'
                if not comments: comments = '0'
                elif int(comments) < 0: comments = '0'
                if not rank: rank = '0'
                elif int(rank) < 0: rank = '0'
                
                #Building the resultset
                rec = {
                                'title':title_name,
                                'uri':url,
                                'author': author_name.replace("user?id=",""),
                                'points': article_score,
                                'comments' : comments,
                                'rank': rank     
                        }
                items.append(rec)
        return items

if __name__ == "__main__":
    main()