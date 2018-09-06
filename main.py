import requests
from bs4 import BeautifulSoup
from languages import *


def main():
    intro()
    desired_position = find_title()
    location = find_location()
    print("Okay, you are looking for a {} job in {}, right? Calculating skills!".format(desired_position, location))
    get_indeed_listings(desired_position, location)


def intro():
    print("\n")
    print(r"         \\\\\\\\\\\\\\\\\\\\\\\\\\Most Sought Tech Skills by Area/////////////////////////////")
    input("Welcome! This script will find the most sought skills for tech jobs in a given area! Press enter to continue.")


def find_title():
    print("What position would you like to look for? Enter a digit between 1 and 4.")
    position = input("Your options are: 1) Software Developer 2) Web Developer 3) Game Developer 4) EXTRA \n")
    positions = {'1': 'Software Developer', '2': 'Web Developer', '3': 'Game Developer', '4': "EXTRA"}
    return positions[position]


def find_location():
    print("For now we will just use your current location via IP. (If you are using a VPN this will be incorrect.)")
    r = requests.get("https://ipapi.co/json").json()
    user_ip = r['ip']
    user_city = requests.get("https://ipapi.co/{}/city/".format(user_ip))
    user_state = requests.get("https://ipapi.co/{}/region_code/".format(user_ip))
    user_loc = ("{}, {}".format(user_city.text, user_state.text))
    return user_loc


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
        box = lps.find_all(attrs={"data-tn-component": "organicJob"})
        for result in box:
            print(result.children)
            y = result.h2.a['href']
            listing_page = y
            new_req = requests.get("https://www.indeed.com{}".format(listing_page))
            new_soup = BeautifulSoup(new_req.content, 'html.parser')
            try:
                description = new_soup.find(attrs={'class': 'jobsearch-JobComponent-description'}).get_text()
            except AttributeError:
                description = new_soup.find(attrs={'class': 'jobsearch-JobComponent'})
                if description is not None:
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


def get_dice_listings(position, loc):
    pass


def get_sof_listings(position, loc):
    pass


def compile_data(data):
    pass


def display_data(data):
    pass


if __name__ == "__main__":
    main()
