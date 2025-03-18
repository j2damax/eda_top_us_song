from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import requests

# Define IMDb Top 250 URL
BASE_URL = "https://www.imdb.com/chart/top/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_imdb_movies_with_selenium():
    # Set up Selenium WebDriver (Make sure you have ChromeDriver installed)
    service = Service("/usr/local/bin/chromedriver")  # Full path to the chromedriver binary
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    time.sleep(3)  # Wait for the page to load

    # Change the view type to "list-view-option-detailed"
    try:
        # Locate the "chart-layout-view-options" container
        view_options = driver.find_element(By.CLASS_NAME, "chart-layout-view-options")
        
        # Find the button or dropdown for "list-view-option-detailed"
        detailed_view_button = view_options.find_element(By.ID, "list-view-option-detailed")
        
        # Click the button to change the view
        detailed_view_button.click()
        time.sleep(2)  # Wait for the page to update
    except Exception as e:
        print(f"Failed to change view type: {e}")

    # Scroll to the bottom of the page to load all content (if lazy-loaded)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the fully loaded page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close the browser

    # Extract movie data
    movies_data = []
    movie_rows = soup.select(".ipc-metadata-list-summary-item")  # Updated selector for movie rows

    
    if not movie_rows:
        print("No movie data found. Check the HTML structure.")
        return None
    
    movies_data = []
    
    for movie in movie_rows:
        # Extract movie title
        title_element = movie.select_one("h3")
        title = title_element.text.strip() if title_element else "Unknown"
        
        # Extract release year
        year_element = movie.select(".sc-f30335b4-7 jhjEEd dli-title-metadata-item")
        year = year_element[0].text.strip() if year_element else "Unknown"
        
        # Extract IMDb rating
        rating_element = movie.select_one(".ipc-rating-star--imdb")
        rating = rating_element.text.strip() if rating_element else "Unknown"
        
        # Extract movie link
        movie_link_element = movie.select_one("a.ipc-title-link-wrapper")
        movie_link = "https://www.imdb.com" + movie_link_element["href"] if movie_link_element else ""
        
        # Initialize extra details
        genre, directors, box_office_revenue, lead_actors = "Unknown", "Unknown", "Unknown", "Unknown"
        
        # Fetch individual movie page for more details
        if movie_link:
            movie_response = requests.get(movie_link, headers=HEADERS)
            if movie_response.status_code == 200:
                movie_soup = BeautifulSoup(movie_response.text, "html.parser")
                
                # Extract genre
                genre_elements = movie_soup.select(".ipc-chip-list__scroller a")
                genre = ", ".join([g.text.strip() for g in genre_elements]) if genre_elements else "Unknown"
                
                # Extract directors (Avoid duplication)
                director_elements = movie_soup.select(".ipc-metadata-list-item__content-container a[href*='/name/']")
                directors_set = {d.text.strip() for d in director_elements}  # Use a set to avoid duplicates
                directors = ", ".join(directors_set) if directors_set else "Unknown"
                
                # Extract box office revenue
                box_office_element = movie_soup.select_one(".ipc-metadata-list__item:-soup-contains('Gross worldwide')")
                box_office_revenue = box_office_element.text.strip().split(":")[-1] if box_office_element else "Unknown"
                
                # Extract lead actors (Avoid duplication)
                stars_heading = movie_soup.select_one("span:contains('Stars')")  # Locate 'Stars' heading
                print(stars_heading)
                if stars_heading:
                    # Find all sibling elements with the class for actor names
                    actor_elements = stars_heading.find_next_siblings("span", class_="sc-d49a611d-2.iPIqIX")
                    print(actor_elements)
                    if actor_elements:
                        lead_actors_set = {actor.text.strip() for actor in actor_elements}  # Use a set to avoid duplicates
                        lead_actors = ", ".join(lead_actors_set) if lead_actors_set else "Unknown"
                    else:
                        lead_actors = "Unknown"
                else:
                    lead_actors = "Unknown"
                    
        movies_data.append({
            "Title": title,
            "Year": year,
            "Rating": rating,
            "Genre": genre,
            "Director(s)": directors,
            "Box Office Revenue": box_office_revenue,
            "Lead Actors": lead_actors,
        })

    # Save to a DataFrame
    df = pd.DataFrame(movies_data)
    df.shape  # (250, 3)
    df.head()


    # Save the data to a CSV file
    df.to_csv("imdb_top_movies.csv", index=False)
    print(f"Scraping complete. Data saved.")

if __name__ == "__main__":
    scrape_imdb_movies_with_selenium()