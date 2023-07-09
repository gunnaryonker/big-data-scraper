import requests
from bs4 import BeautifulSoup
import csv

# Start index step by 1 for each page on the url
start = 1
step = 1

# Create a list for the data
anime_data = []

while start <= 19:  # Scrape all 19 pages that are on the site
    # Create a url with the start index
    url = f"https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page={start}&sort=moviemeter,asc"

    # Send a get request
    req = requests.get(url)

    # Create BeautifulSoup
    soup = BeautifulSoup(req.content, "html.parser")

    # Export html data to a text document
    with open("html_content_tableC.txt", "a", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

    # Find the rankid, title, rating, age rating, runetime, year range, and votes for each entry
    anime_entries = soup.find_all("div", class_="lister-item-content")
    for entry in anime_entries:
        rankid = entry.find("h3", class_="lister-item-header")
        title = entry.find("h3", class_="lister-item-header")
        rating = entry.find("div", class_="ratings-bar")
        age_rating = entry.find("span", class_="certificate")
        runtime = entry.find("span", class_="runtime")
        years = entry.find("span", class_="lister-item-year text-muted unbold")
        votes = entry.find("span", attrs={"name": "nv"})

        rank = rankid.span.get_text().replace(".", "") if rankid is not None else ""
        title_text = title.a.get_text() if title is not None else ""
        rating_text = rating.strong.get_text() if rating is not None and rating.strong is not None else ""
        age_text = age_rating.get_text() if age_rating is not None else ""
        runtime_text = runtime.get_text() if runtime is not None else ""
        year_range = years.get_text() if years is not None else ""
        vote_count = votes["data-value"] if votes is not None else ""

        anime_data.append([str(rank) + 'c', title_text, rating_text, age_text, runtime_text, year_range, vote_count])
                
    # Update the start index for the next page
    start += step

# Define the name of the csv file
csv_file = "tableC.csv"

# Write the data to the csv file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["rank", "title", "rating", "age_rating", "run_time", "year_range", "votes"])
    writer.writerows(anime_data)

print(f"Data saved to {csv_file} successfully.")
