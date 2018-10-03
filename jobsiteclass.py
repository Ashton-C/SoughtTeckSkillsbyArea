import requests
from bs4 import BeautifulSoup
from languages import *


class JobSite:
    def __init__(self, name):
        self.name = name
    def get_listings(self, position, loc):
        loc = loc.replace(",", "%2C+")
        loc = loc.replace(" ", "+")
        position = position.replace(" ", "+")
        counter = 0
        lpn = 0
        if self.name == "stackoverflow":
            range_var = 1
        if self.name == "indeed":
            range_var = 1
        for i in range(0, range_var):
            if self.name == "stackoverflow":
                listings_page = "https://{}.com/jobs?q={}&l={}".format(self.name, position, loc)
            if self.name == "indeed":
                listings_page = "https://{}.com/jobs?q={}&l={}&start={}".format(self.name, position, loc, lpn)
            print(listings_page)
            response = requests.get(listings_page)
            lps = BeautifulSoup(response.content, 'html.parser')
            if self.name == "stackoverflow":
                box = lps.find_all(attrs={"class" : "fs-subheading"})
            if self.name == "indeed":
                box = lps.find_all(attrs={"data-tn-component" : "organicJob"})
            for result in box:
                description = ""
                print(result.children)
                if self.name == "indeed":
                    y = result.h2.a['href']
                if self.name == "stackoverflow":
                    y = result.a['href']
                listing_page = y
                new_req = requests.get("https://www.{}.com{}".format(self.name, listing_page))
                new_soup = BeautifulSoup(new_req.content, 'html.parser')
                try:
                    if self.name == "stackoverflow":
                        page_text = new_soup.find_all(attrs={'class' : 'mb32'})
                        blocks = page_text[3:7]
                        for block in blocks:
                            description += block.get_text()
                    if self.name == "indeed":
                        description = new_soup.find(attrs={'class' : 'jobsearch-JobComponent-description'}).get_text()
                except AttributeError:
                    description = "N/A"
                    continue
                print_results(all_languages, description)
                print_results(all_frameworks, description)
                print_results(all_databases, description)
                print_results(all_platforms, description)
                counter += 1
            lpn += 10
        return counter


def print_results(field, text):
    for word in field:
        if word in text:
            field[word] += 1
