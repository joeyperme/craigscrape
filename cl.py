from bs4 import BeautifulSoup
import requests, sys

class Listing:
	def __init__(self,listing_id,header,header_link,price,location):
		# used to discard multiple listings
		self.listing_id = listing_id
		self.header = header
		self.header_link = header_link
		self.price = price
		self.location = location

# date defaults to rel[evance]
def get_craigslist_source(city="cleveland", sort="date", query="legos"):
	craigslist_url = f"https://{city}.craigslist.org/search/sss?sort={sort}&postedToday=1&query={query}"
	return requests.get(craigslist_url).content

def get_craigslist_soup(city="cleveland", sort="date", query="legos"):
	source = get_craigslist_source(city, sort, query)
	return BeautifulSoup(source, "html.parser")

def get_craigslist_listings(city="cleveland", sort="date", query="legos"):
	soup = get_craigslist_soup(city, sort, query)
	raw_listings = soup.findAll("li", {"class":"result-row"})

	listings = []

	# populate list of Listings
	for rl in raw_listings:
		header = rl.find("a",{"class":"result-title hdrlnk"}).text
		header_link = rl.find("a",{"class":"result-title hdrlnk"})['href']
		# image_url = rl.find("img") # images don't load without JS, not going headless
		price = rl.find("span",{"class":"result-price"}).text
		location = rl.find("span",{"class":"nearby"}).text
		listing_id = header_link.split("/")[-1].split(".")[0]

		listings.append(Listing(listing_id,header,header_link,price,location))

	return listings


listings = get_craigslist_listings("cleveland", "date", "legos")
print(f"{len(listings)} listings")
for li in listings:
	print(f"[{li.price: >{7}}] {li.header}: {li.header_link}")
