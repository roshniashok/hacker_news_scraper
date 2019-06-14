from bs4 import BeautifulSoup
from scraper_code.hackerNewsScraper import scraper,main

#Reading sample html to parse
with open("sampleHN.html", encoding="utf-8") as f:
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    res=scraper(soup)
    print(res) 

#Test general working of scraper function
def test_scraperfunction():
    assert res[0]['title'] == "Gorilla Youngsters Seen Dismantling Poachers' Traps"
    assert res[0]['rank'] == '1'

#Test if empty strings are picked up
def test_empty_strings():
    assert res[1]['title'] != ''
    assert res[1]['author'] != ''

#Test if empty strings in points are picked up
def test_empty_authors_scores():
    assert res[1]['author'] =='empty'
    assert res[1]['points'] =='empty'

#Test if values are integer and greater than 0
def test_greater_than_zero_values():
    assert int(res[0]['points']) >= 0
    assert int(res[0]['comments']) >= 0
    assert int(res[0]['rank']) > 0

#Test if it is integer
def test_integer():
    try:
        int(res[0]['points'])
        int(res[0]['comments'])
        int(res[0]['rank'])
        assert True
    except ValueError:
        assert False

#Test if chars more < 256
def test_greaterthan256():
    assert len(res[0]['title']) <= 256
    assert len(res[0]['author']) <= 256


