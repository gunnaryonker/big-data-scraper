import requests
from bs4 import BeautifulSoup
import csv

# Create a list for all of the data to export later to csv
anime_data = []

# Send a get request
url = "https://www.animenewsnetwork.com/encyclopedia/ratings-anime.php?top50=popular&n=1000"
req = requests.get(url)

# Create BeautifulSoup
soup = BeautifulSoup(req.content, "html.parser")

# Export html data to text document for later use
with open("html_content_tableB.txt", "a", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())

# Find the rankid, title, rating, and vote data
anime_table = soup.find("table", class_="encyc-ratings")
anime_entries = anime_table.find_all("tr", bgcolor="#EEEEEE")

# Counter to keep track of progress since this is a long process
for i, entry in enumerate(anime_entries):
    rank = entry.find("td", class_="l")
    title = entry.find("td", class_="t").find("a")
    rating = entry.find("td", class_="r").get_text().strip()
    votes = entry.find_all("td", class_="r")[1].get_text().strip()

    rank_text = rank.get_text().strip() if rank is not None else ""
    title_text = title.get_text().strip() if title is not None else ""
    show_type = ""
    title_parts = title_text.split(" (")
    if len(title_parts) > 1:
        show_type = title_parts[-1].strip(")")
    title_text = title_parts[0]

    # Open the nested url for more information on each title
    if title is not None:
        anime_url = "https://www.animenewsnetwork.com" + title["href"]
        anime_req = requests.get(anime_url)
        anime_soup = BeautifulSoup(anime_req.content, "html.parser")

        # Find the runtime(in minutes) and episodes values
        runtime = ""
        episodes = ""
        infotypes = anime_soup.find_all("div", class_="encyc-info-type")
        for infotype in infotypes:
            if infotype.strong:
                strong_text = infotype.strong.get_text().strip()
                if strong_text == "Running time:":
                    runtime_text = infotype.span.get_text().strip()
                    runtime = runtime_text.split(" ")[0]

                elif strong_text == "Number of episodes:":
                    episodes = infotype.span.get_text().strip()

    anime_data.append([str(rank_text) + 'b', title_text, show_type, rating, votes, runtime, episodes])

    print(f"Processed entry {i+1} of {len(anime_entries)}")

# Name the csv file
csv_file = "tableB.csv"

# Write the data to the csv file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["rank_id", "title", "show_type", "rating", "votes", "runtime_minutes", "episodes"])
    writer.writerows(anime_data)

print(f"Data saved to {csv_file} successfully.")
