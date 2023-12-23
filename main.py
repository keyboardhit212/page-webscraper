import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import re


def scrape_headings(url):
    headings = []
    try:
        # Check if the URL has a scheme (http/https), and add one if missing
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = urlunparse(('http',) + parsed_url[1:])

        # Send an HTTP GET request to the specified URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the heading elements (h1, h2, h3, etc.)
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

            # Extract and print the text from the headings
            for heading in headings:
                print(heading.text)
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return headings;


def save_to_csv(headings, filename):
    if len(headings) != 0:
        file = open(filename + ".csv", "w")
        for heading in headings:
            file.write(f"{heading.text}, ")


def main_start():
    if __name__ == "__main__":
        url = input("Enter the URL: ")
        filename = [i for i in re.split(':|/|,', url) if len(i) != 0][-1]
        results = scrape_headings(url)
        save_to_csv(results, filename);
        search_again = input("Do you want to search again? y/n:").lower()
        if search_again == 'y':
            main_start()
        else:
            exit()
        print(f"{filename}")


main_start()
