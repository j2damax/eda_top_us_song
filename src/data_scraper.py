import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imdb_top_movies():
    # Example scraping logic (you'll need to adapt this to IMDb's structure)
    url = "https://www.imdb.com/chart/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for row in soup.select('tbody.lister-list tr'):
        title = row.select_one('.titleColumn a').text
        year = row.select_one('.titleColumn span').text.strip('()')
        rating = row.select_one('.imdbRating strong').text
        movies.append({'Title': title, 'Year': year, 'Rating': rating})

    # Save to a DataFrame
    df = pd.DataFrame(movies)
    df.to_csv('../data/raw/imdb_top_movies.csv', index=False)
    print("Scraping complete. Data saved to 'data/raw/imdb_top_movies.csv'.")

if __name__ == "__main__":
    scrape_imdb_top_movies()