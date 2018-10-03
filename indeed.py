import requests
from bs4 import BeautifulSoup
from languages import *


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


def get_indeed_listings(position, loc):
	loc = loc.replace(" ", "%20")
	position = position.replace(" ", "+")
	counter = 0
	lpn = 0
	for i in range(0, 5):
		listings_page = "https://www.indeed.com/jobs?q={}&l={}&start={}".format(position, loc, lpn)
		print(listings_page)
		response = requests.get(listings_page)
		lps = BeautifulSoup(response.content, 'html.parser')
		box = lps.find_all(attrs={"data-tn-component" : "organicJob"})
		for result in box:
			print(result.children)
			y = result.h2.a['href']
			listing_page = y
			new_req = requests.get("https://www.indeed.com{}".format(listing_page))
			new_soup = BeautifulSoup(new_req.content, 'html.parser')
			try:
				description = new_soup.find(attrs={'class' : 'jobsearch-JobComponent-description'}).get_text()
			except AttributeError:
				description = new_soup.find(attrs={'class' : 'jobsearch-JobComponent'})
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

get_indeed_listings("Software Developer", "Salt Lake City")


