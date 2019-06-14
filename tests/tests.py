from bs4 import BeautifulSoup
from scraper_code.hackerNewsScraper import scraper,soup

with open("sampleHN.html", encoding="utf-8") as f:
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    res=scraper(soup)
    print(res) 

def test_scraperfunction():
    assert res[0]['title'] == "Gorilla Youngsters Seen Dismantling Poachers' Traps"
    assert res[0]['rank'] == '1'


def test_empty_strings():
    assert res[1]['title'] != ''
    assert res[1]['author'] != ''

def test_empty_authors_scores():
    assert res[26]['author'] =='empty'
    assert res[26]['points'] =='empty'

def test_greater_than_zero_values():
    assert int(res[0]['points']) >= 0
    assert int(res[0]['comments']) >= 0
    assert int(res[0]['rank']) > 0

def test_integer():
    try:
        int(res[0]['points'])
        int(res[0]['comments'])
        int(res[0]['rank'])
        assert True
    except ValueError:
        assert False

def test_greaterthan256():
    assert len(res[0]['title']) <= 256
    assert len(res[0]['author']) <= 256


