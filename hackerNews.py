import urllib.request
from bs4 import BeautifulSoup
import json
import click
import urllib3

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
                article_title=titleURL.string.strip()
                rank=result2.td.span.string.strip()
                #comment=result.select('a')[3].get_text()
                #if (comment==None): comment='empty'
                #else : comment=result.select('a')[3].get_text(strip=True)
                if (author==None) : author_name='empty'
                else: author_name=result.a['href']
                if(score==None) : article_score ='empty'
                else: article_score=result.span.string.strip()
                rec = {
                                'title':article_title,
                                'uri':title_url,
                                'author': author_name,
                                'points': article_score,
                                'rank': rank,
                        }
                items.append(rec)
        return items

if __name__ == "__main__":
    soup()