# Hacker News Web Scraping Application:
A simple command line application of a web scraper for the hackernews website fetching posts based on the input given to the CLI application. The output is in the form of a JSON showing title, URL, author and other details.

## Environment Specifications:
### Python:
Check if you already have a version of python installed on your machine by doing a 
</br>`python -V`.</br>

If you do not have python installed already, then do so by following the instructions on the website : https://realpython.com/installing-python/ </br>

After installing, check whether you have it by doing a </br> `python -V` </br>once more. </br>

It should print the version 3.x.x depending on the version you downloaded. </br>

Then, after cloning the repo install the dependent modules using the requirements.txt file:</br>
`pip install -r requirements.txt`</br>

After installing the dependencies, you can run the application from inside the scraper_code directory : </br>
`python hackerNewsScraper.py  --posts <noofposts>`</br>
Substitue `<noofposts>` to any value between 1-100 to get the scraped results of the articles from the hacker news page in JSON format. </br>

For running the tests, navigate to the tests directory and run :
`pytest tests.py `




