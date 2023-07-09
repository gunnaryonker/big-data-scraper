import requests
from bs4 import BeautifulSoup
import csv

# Start index and step size for pagination
start = 0
step = 50

# Create a list to store the scraped data
anime_data = []

while start < 1000:  # Scrape 1000 titles (20 pages)
    # Create the URL with the appropriate start index
    url = f"https://myanimelist.net/topanime.php?limit={start}"

    # Send a GET request to the webpage
    req = requests.get(url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(req.content, "html.parser")

    # Export HTML content to a text file
    with open("html_content_tableA.txt", "a", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

    # Find the title and rating of each anime
    anime_entries = soup.find_all("tr", class_="ranking-list")
    for entry in anime_entries:
        rankid = entry.find("td", class_="rank ac")
        title = entry.find("h3", class_="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3")
        rating = entry.find("div", class_="js-top-ranking-score-col di-ib al")
        anime_type = entry.find("div", class_="information di-ib mt4")

        rank = rankid.span.get_text().replace(".", "") if rankid is not None else ""
        title_text = title.a.get_text() if title is not None else ""
        rating_text = rating.span.get_text() if rating is not None else ""

        information = entry.find("div", class_="information")
        if information is not None:
            lines = information.get_text().split("\n")
            show_type_and_episodes = lines[1].strip()
            show_type = show_type_and_episodes.split("(")[0].strip()
            episodes = show_type_and_episodes.split("(")[1].split(" ")[0]
            runtime = lines[2].strip()
            member_count = lines[3].strip().split(" ")[0].replace(",", "")

            anime_data.append([rank, title_text, rating_text, show_type, episodes, runtime, member_count])

    # Update the start index for the next page
    start += step

print(f"Html data saved to html_content_tableA.txt successfully.")

# Define the CSV file path
csv_file = "tableA.csv"

# Write the data to the CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["rank", "title", "rating", "show_type", "episodes", "run_time", "member_count"])  # Write header
    writer.writerows(anime_data)  # Write data rows

print(f"Data saved to {csv_file} successfully.")
