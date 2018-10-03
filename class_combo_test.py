import requests
from bs4 import BeautifulSoup
from languages import *


class JobSite:
    def get_listings(self, position, loc):
        loc = loc.replace(",", "%2C+")
        loc = loc.replace(" ", "+")
        position = position.replace(" ", "+")
        counter = 0
        lpn = 0
        for i in range(0, 1):
            listings_page = "https://{}.com/jobs?q={}&l={}".format(self, position, loc)
            print(listings_page)
            response = requests.get(listings_page)
            lps = BeautifulSoup(response.content, 'html.parser')
            if self == "stackoverflow":
                box = lps.find_all(attrs={"class" : "fs-subheading"})
            if self == "indeed":
                box = lps.find_all(attrs={"data-tn-component" : "organicJob"})
            for result in box:
                description = ""
                print(result.children)
                if self == "indeed":
                    y = result.h2.a['href']
                if self == "stackoverflow":
                    y = result.a['href']
                listing_page = y
                new_req = requests.get("https://www.{}.com{}".format(self, listing_page))
                new_soup = BeautifulSoup(new_req.content, 'html.parser')
                try:
                    if self == "stackoverflow":
                        page_text = new_soup.find_all(attrs={'class' : 'mb32'})
                        blocks = page_text[3:7]
                        for block in blocks:
                            description += block.get_text()
                    if self == "indeed":
                        description = new_soup.find(attrs={'class' : 'jobsearch-JobComponent-description'}).get_text()
                except AttributeError:
                    description = "N/A"
                    if description != None:
                        description = description.get_text()
                    continue
                print_results(all_languages, description)
                print_results(all_frameworks, description)
                print_results(all_databases, description)
                print_results(all_platforms, description)
                counter += 1
            lpn += 10


def print_results(field, text):
    for word in field:
        if word in text:
            field[word] += 1


def remove_empty(field):
    to_remove = []
    for word in field:
        if field[word] == 0:
            to_remove.append(word)
    for word in to_remove:
        field.pop(word)


def get_so_listings(position, loc):
    loc = loc.replace(",", "%2C+")
    loc = loc.replace(" ", "+")
    position = position.replace(" ", "+")
    counter = 0
    lpn = 0
    for i in range(0, 1):
        listings_page = "https://stackoverflow.com/jobs?q={}&l={}".format(position, loc)
        print(listings_page)
        response = requests.get(listings_page)
        lps = BeautifulSoup(response.content, 'html.parser')
        box = lps.find_all(attrs={"class" : "fs-subheading"})
        for result in box:
            description = ""
            print(result.children)
            y = result.a['href']
            listing_page = y
            new_req = requests.get("https://www.stackoverflow.com{}".format(listing_page))
            new_soup = BeautifulSoup(new_req.content, 'html.parser')
            try:
                page_text = new_soup.find_all(attrs={'class' : 'mb32'})
                blocks = page_text[3:7]
                for block in blocks:
                    description += block.get_text()
            except AttributeError:
                description = "N/A"
                if description != None:
                    description = description.get_text()
                continue
            print_results(all_languages, description)
            print_results(all_frameworks, description)
            print_results(all_databases, description)
            print_results(all_platforms, description)
            counter += 1
        lpn += 10
    remove_empty(all_languages)
    remove_empty(all_frameworks)
    remove_empty(all_databases)
    remove_empty(all_platforms)
    print(all_languages, all_frameworks, all_databases, all_platforms)

stackoverflow = JobSite()
indeed = JobSite()

stackoverflow.get_listings("Software Developer", "Salt Lake City")
indeed.get_listings("Software Developer", "Salt Lake City")

#get_so_listings("Software Developer", "Salt Lake City")
