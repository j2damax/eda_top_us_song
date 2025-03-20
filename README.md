# Exploratory Data Analysis on Top Global Movies

This project performs exploratory data analysis (EDA) on top global movies from IMDb, analyzing trends in the movie industry from 1950 to 2020. The dataset covers attributes such as release year, box office revenue, rating, genre, director(s), and lead actors.


## Project Setup

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (compatible with your Chrome browser version)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/j2damax/eda_top_us_song.git
   cd eda_global_movies


2. Set Up a Virtual Environment
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

3. Install Dependencies
    pip install -r requirements.txt

4. Download ChromeDriver

    Visit ChromeDriver Downloads and download the version that matches your Chrome browser.
    Move the chromedriver binary to a directory in your system's PATH, or place it in the drivers directory within the project.
    
    mv path/to/chromedriver drivers/

## Project Structure
```

eda_global_movies/
├── data/
│   ├── imdb_top_movies_cleaned.csv
│   └── imdb_top_movies.csv
├── notebooks/
│   └── eda_global_movies.ipynb
├── src/
│   ├── data_scraper.py
├── [requirements.txt]
└── [README.md]
```

## Environment Requirements
```

Requirements:
    pandas
    beautifulsoup4
    requests
    selenium
    webdriver-manager
    jupyter

```
Notes:
Ensure that the ChromeDriver version matches your installed Chrome browser version.
If you encounter issues with ChromeDriver, refer to the ChromeDriver Documentation for troubleshooting.
