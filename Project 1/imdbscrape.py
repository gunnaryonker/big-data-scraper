import requests
from bs4 import BeautifulSoup
import csv

# Start index and step size for pagination
start = 1
step = 1

# Create a list to store the scraped data
anime_data = []

while start <= 19:  # Scrape all 19 pages
    # Create the URL with the appropriate start index
    url = f"https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page={start}&sort=moviemeter,asc"

    # Send a GET request to the webpage
    req = requests.get(url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(req.content, "html.parser")

    # Export HTML content to a text file
    with open("html_content_tableB.txt", "a", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

    # Find the title and rating of each anime
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

        anime_data.append([rank, title_text, rating_text, age_text, runtime_text, year_range, vote_count])
                
    # Update the start index for the next page
    start += step

print(f"Html data saved to html_content_tableB.txt successfully.")

# Define the CSV file path
csv_file = "tableB.csv"

# Write the data to the CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["rank", "title", "rating", "age_rating", "run_time", "year_range", "votes"])  # Write header
    writer.writerows(anime_data)  # Write data rows

print(f"Data saved to {csv_file} successfully.")
