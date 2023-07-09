import requests
from bs4 import BeautifulSoup
import csv

# List for stored data to export to csv
anime_data = []

# Send a get request to Anime News Network
url = "https://www.animenewsnetwork.com/encyclopedia/ratings-anime.php?top50=popular&n=1000"
req = requests.get(url)

# Create BeautifulSoup
soup = BeautifulSoup(req.content, "html.parser")

# Export html data to text document for later use
with open("html_content_tableB.txt", "a", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

# Find data such as rankid, title, rating, votes on initial page
anime_table = soup.find("table", class_="encyc-ratings")
anime_entries = anime_table.find_all("tr", bgcolor="#EEEEEE")

for entry in anime_entries:
    rank = entry.find("td", class_="l")
    title = entry.find("td", class_="t").find("a")
    rating = entry.find("td", class_="r").get_text().strip()
    votes = entry.find_all("td", class_="r")[1].get_text().strip()

    rank_text = rank.get_text().strip() if rank is not None else ""
    title_text = title.get_text().strip() if title is not None else ""
    show_type = title_text.split("(")[-1].strip(")") if "(" in title_text else ""
    title_text = title_text.split("(")[0].strip()

    # Open nested url to find runtime and episode count of each anime show
    if title is not None:
        anime_url = "https://www.animenewsnetwork.com" + title["href"]
        anime_req = requests.get(anime_url)
        anime_soup = BeautifulSoup(anime_req.content, "html.parser")

        # Find the runtime(minutes) and episode count
        runtime = ""
        episodes = ""
        infotypes = anime_soup.find_all("div", class_="encyc-info-type")
        for infotype in infotypes:
            if infotype.strong:
                strong_text = infotype.strong.get_text().strip()
                if strong_text == "Running time:":
                    runtime_text = infotype.span.get_text().strip()
                    runtime = runtime_text.split(" ")[0]  # Extract the number of minutes not the whole phrase

                elif strong_text == "Number of episodes:":
                    episodes = infotype.span.get_text().strip()
        
        # Add each entry to item list for export
        anime_data.append([str(rank_text) + 'b', title_text, show_type, rating, votes, runtime, episodes])

# Name of csv file
csv_file = "tableB.csv"

# Write the data to the csv file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["rank_id", "title", "show_type", "rating", "votes", "runtime_minutes", "episodes"])
    writer.writerows(anime_data)

print(f"Data saved to {csv_file} successfully.")
