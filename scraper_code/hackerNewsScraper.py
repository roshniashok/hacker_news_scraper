import urllib.request 
from bs4 import BeautifulSoup
import json
import click
import urllib3
import re
import requests
from validator_collection import validators, checkers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@click.command()
@click.option('--posts',type=click.IntRange(1, 100))

def soup(posts):
        pageInit=0
        totalPosts=[]
        totalPageCounter=countURL(pageInit,posts)
        while (totalPageCounter>0):
                pageInit=pageInit+1
                url = 'https://news.ycombinator.com/?p='+str(pageInit)
                http = urllib3.PoolManager()
                r = http.request("GET", url)
                soup = BeautifulSoup(r.data, "html.parser")
                totalPageCounter=totalPageCounter-1
                totalPosts=totalPosts + scraper(soup)
                #print(len(totalPosts))
        total=totalPosts[:posts]
        print(len(total))
        final_json=json.dumps(total,indent=4)
        print(final_json)
        return total
        
        
                

def countURL(pageInit,posts):
        if(posts%30!=0):
                totalPages=(posts/30)+1
                return int(totalPages)
        else:
                totalPages=posts/30
                return int(totalPages)

def scraper(soup):
        
        results = soup.find_all("td", class_="subtext")
        results2 = soup.find_all("tr", class_="athing")
        items=[]
        
        for result,result2 in zip(results,results2):
                
                author=result.find("a",class_="hnuser")
                score=result.find("span",class_="score")
                ranking=result2.find("span",class_="rank")
                titleURL=result2.find("a",class_="storylink")
                title_url=titleURL['href']
                
                validURL=checkers.is_url(title_url)
                
                if validURL==True: url=title_url
                else: url='Invalid URI'
                
                article_title=titleURL.string.strip()
                if len(article_title) > 256: article_title=article_title[:256]
                
                rank=result2.td.span.string.strip('.') 
                children = result.findChildren()
                for i, child in enumerate(children):
                        if i == 6:
                                comment=child.text

                comments=re.sub("\u00a0comments|\xa0comments|discuss|\xa0comment","",comment)
                title_name=re.sub("\u201c|\u201d|\u2013|\u2019","",article_title)
                if (author==None) : author_name='empty'
                else: 
                        author_name=result.a['href']
                        if len(author_name) > 256:
                                author_name=author_name[:256]

                if(score==None) : article_score ='None'
                else: article_score=result.span.string.replace("points","")

                if not article_score: article_score = '0'
                elif article_score=='None': article_score='empty'
                elif int(article_score) < 0: article_score = '0'
                if not comments: comments = '0'
                elif int(comments) < 0: comments = '0'
                if not rank: rank = '0'
                elif int(rank) < 0: rank = '0'
                
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
    soup()