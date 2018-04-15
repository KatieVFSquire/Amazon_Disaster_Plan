'''
This program will parse your emails to find information about your amazon order dates. If you have not
received your shipment after two days, it will send a tweet to Amazon complaining to entice their customer
service to give you a free month of prime.

Disclaimer 1: This program was designed specifically for our situation as we live in an apartment that will send
an email notifications about package delivery.

Disclaimer 2: This program is a work in progress and does not have all the email functionality at the moment.
'''

import re
import datetime as dt
from bs4 import BeautifulSoup
from twitter_utillities import tweet

def parse_email(file_path):
    '''This function will pull expected arrival dates from automated Amazon shipment emails.
    Note: At the moment, a saved email is being pulled and parsed as an html file. Future revisions will incorporate
    ability to login to user's email and search for emails on a regular basis.'''
    fh = open(file_path, 'r')
    soup = BeautifulSoup(fh, "html.parser")
    body = soup.body
    # font' was found to be the easiest parsing criteria to capture a subset of data that contains
    # the expected arrival dates
    b = body.find_all('font')

    year = dt.date.today().strftime("%Y")

    arriving_dates = ""

    for dates in b:
        arriving_dates += dates.contents[0].string

    # Expecting pattern such as 'September 25 '
    pattern = r"[a-zA-Z]+ [0-9]+ "
    match = re.findall(pattern, arriving_dates)

    formated_dates = []

    for date in match:
        formatted_date = dt.datetime.strptime(date + year, '%B %d %Y').date()
        formated_dates.append(formatted_date)

    return formated_dates


def get_older_dates(dates):
    '''This function compares the expected package arrival dates from Amazon to the current date to decide if the
    package is overdue.'''
    today = dt.date.today()
    overdue_dates = []
    for date in dates:
        if today > date:
            overdue_dates.append(date)

    return overdue_dates


def request_pickup():
    '''This function sends the specified tweet via Twitter.'''
    tweet('@_Glynz Hey you! Pick up my package please :)')


def main():
    '''Executes start of code which parses dates from the automated Amazon shipment email,
    checks if the package is past due, and tweets if there are any outstanding packages.'''
    print('Starting Execution...')
    try:
        parsed_dates = parse_email("C:/Users/Michael/Desktop/Amazon_Disaster_Plan/gmail.html")
        dates_of_non_received_packages = get_older_dates(parsed_dates)
        if len(dates_of_non_received_packages) > 0:
            print("New packages are here!")
            request_pickup()
        else:
            print("No new packages =/")

        print('Process Complete!')
    except:
        print("ERROR: Unexpected error while running the program!")


if __name__ == "__main__":
    main()
