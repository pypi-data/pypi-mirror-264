# Job Scraper

## Description

Job Scraper is a Python tool designed to scrape job listings from various sources including USAJobs, CIRES, and CIRA. It filters job listings based on specified keywords and can save the results to JSON files for further analysis or processing.

## Installation

Before installing Job Scraper, ensure you have Python and [Poetry](https://python-poetry.org/) installed on your system. You will also need a suitable Chrome WebDriver installed and accessible on your system path.

1. Clone the repository:

   ```bash
   git clone https://github.com/NOAA-GSL/jscraper.git
   cd JobScraper
   ```

1. Install the project dependencies using Poetry:

    ```bash
    poetry install
    ```

This will create a virtual environment and install all necessary dependencies.

## Configuration
#### Credentials

Before running the scraper, you need to provide your user agent and API authorization key for USAJobs. These should be stored in a credentials file located at ~/.jscraper/credentials. The file should have the following format:

```bash
USER_AGENT=your_user_agent_here
AUTHORIZATION_KEY=your_authorization_key_here
```

Replace your_user_agent_here and your_authorization_key_here with your actual credentials. The user agent is a string that identifies your web browser to servers, while the authorization key is a specific key provided by USAJobs for accessing their API. API keys can be requested at https://developer.usajobs.gov/apirequest/

## Command-line Arguments

The Job Scraper tool can be configured using command-line arguments:

    --usajobs-keyword: Keyword for filtering USAJobs listings.
    --cires-keyword: Keyword for filtering CIRES job listings.
    --cira-keyword: Keyword for filtering CIRA job listings.
    --usajobs-json-file: Path to save the fetched USAJobs listings.
    --cires-json-file: Path to save the fetched CIRES listings.
    --cira-json-file: Path to save the fetched CIRA listings.
    --verbose: Enable verbose logging.

## Usage

Activate the Poetry virtual environment and run the main.py script with the desired command-line arguments. Here are some example usages:

Scrape federal job listings with a specific keyword:

```bash
poetry run python main.py --usajobs-keyword "Data Scientist"
```

Scrape CIRES job listings and save to a JSON file:

```bash
poetry run python main.py --cires-keyword "Climate" --cires-json-file "cires_jobs.json"
```

For more information on available command-line options, use:

```bash
poetry run python main.py --help
```
