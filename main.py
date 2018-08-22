import requests


def main():
    intro()
    desired_position = find_title()
    location = find_location()
    print("Okay, you are looking for a {} job in {}, right? Calculating skills!".format(desired_position, location))


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


def get_indeed_listings(position, loc):
    pass


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
