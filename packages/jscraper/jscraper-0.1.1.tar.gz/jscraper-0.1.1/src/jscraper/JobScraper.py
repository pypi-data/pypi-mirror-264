import json
import logging
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class JobScraper:
    """
    A class to scrape job listings from various sources including USAJobs, CIRES, and CIRA.
    """

    def __init__(self, user_agent, authorization_key, chromedriver_path):
        """
        Initializes the JobScraper with necessary credentials and Chrome WebDriver path.

        Args:
            user_agent (str): User agent for HTTP requests.
            authorization_key (str): Authorization key for secured APIs.
            chromedriver_path (str): Filesystem path to the Chrome WebDriver executable.
        """
        self.user_agent = user_agent
        self.authorization_key = authorization_key
        self.chromedriver_path = chromedriver_path

    def setup_driver(self):
        """
        Sets up and returns a headless Selenium WebDriver.

        Returns:
            selenium.webdriver.Chrome: A Chrome WebDriver instance in headless mode.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "--headless"
        )  # Run browser in headless mode for automation.
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model.
        chrome_options.add_argument(
            "--disable-dev-shm-usage"
        )  # Overcome limited resource problems.
        service = Service(executable_path=self.chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def fetch_federal_jobs(self, keywords, save_to_file=None):
        """
        Fetches job listings from the USAJobs API filtered by keywords and optionally saves them to a file.

        Args:
            keywords (str): Keywords to search for within the job listings.
            save_to_file (str, optional): Path where the listings should be saved as a JSON file.

        Returns:
            list: A list of job listings that match the given keywords.
        """
        url = "https://data.usajobs.gov/api/search"
        headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": self.user_agent,
            "Authorization-Key": self.authorization_key,
        }
        params = {"Keyword": keywords}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            job_listings = response.json()["SearchResult"]["SearchResultItems"]
        else:
            logging.error(
                f"Failed with status code {response.status_code}: {response.text}"
            )
            return []

        if save_to_file:
            save_path = Path(save_to_file)
            with save_path.open("w") as f:
                json.dump(job_listings, f, indent=4)
            logging.info(f"USAJobs listings saved to {save_to_file}")

        return job_listings

    def extract_federal_job_details(self, job_listing):
        """
        Extracts and returns detailed information from a single federal job listing.

        Args:
            job_listing (dict): A dictionary representing a single job listing.

        Returns:
            dict: A dictionary containing detailed information about the job.
        """
        # Parsing job details from the job listing
        matched_object_descriptor = job_listing.get("MatchedObjectDescriptor", {})
        user_area = matched_object_descriptor.get("UserArea", {})
        details = user_area.get("Details", {})

        # Extracting specific fields from the job details
        title = matched_object_descriptor.get("PositionTitle", "")
        agency = matched_object_descriptor.get("OrganizationName", "")
        department = matched_object_descriptor.get("DepartmentName", "")
        qualifications = matched_object_descriptor.get("QualificationSummary", "")
        salary = matched_object_descriptor.get("PositionRemuneration", [])
        major_duties = details.get("MajorDuties", [])
        apply_link = matched_object_descriptor.get("PositionURI", "")
        application_close_date = matched_object_descriptor.get(
            "ApplicationCloseDate", ""
        )

        salary_range = [
            s.get("MinimumRange", "") + "-" + s.get("MaximumRange", "") for s in salary
        ]
        salary_text = ", ".join(salary_range)
        major_duties_text = "; ".join(major_duties)

        return {
            "title": title,
            "agency": agency,
            "department": department,
            "qualifications": qualifications,
            "salary": salary_text,
            "major_duties": major_duties_text,
            "apply_link": apply_link,
            "application_close_date": application_close_date,
        }

    # Additional methods like `fetch_cires_jobs`, `extract_cires_job_details`, `fetch_cira_jobs`,
    # `extract_cira_job_details`, and `filter_cira_jobs_by_description` should be similarly documented,
    # explaining their purposes, the arguments they take, the operations they perform, and what they return.

    def fetch_cires_jobs(self, keywords, save_to_file=None):
        """
        Fetches CIRES job listings from their website based on keywords and optionally saves them to a file.

        Args:
            keywords (str): Keywords to search for within the CIRES job listings.
            save_to_file (str, optional): Path where the CIRES listings should be saved as a JSON file.

        Returns:
            list: A list of CIRES job listings that match the given keywords.
        """
        url = "https://cires.colorado.edu/work-with-cires"
        driver = self.setup_driver()
        driver.get(url)
        # # Use BeautifulSoup to parse the page source
        cires_soup = BeautifulSoup(driver.page_source, "html.parser")
        # Remember to close the browser
        driver.quit()

        cires_filtered_job_details = []

        # Extract and print job titles, modify this part based on actual page structure and your needs
        cires_job_listings = cires_soup.find_all("div", {"class": "active:scale-[.98]"})
        # logging.debug(cires_job_listings)
        for cires_job_listing in cires_job_listings:
            logging.debug(cires_job_listing.text.strip())
            job_details = self.extract_cires_job_details(cires_job_listing)
            # Check if the organization includes keywords
            if keywords in job_details["title"]:
                cires_filtered_job_details.append(job_details)

        # Save the job listings to a file if a file path is provided
        if save_to_file:
            save_path = Path(save_to_file)
            with save_path.open("w") as f:
                json.dump(cires_filtered_job_details, f, indent=4)
            logging.info(f"CIRES listings saved to {save_to_file}")

        return cires_filtered_job_details

    def extract_cires_job_details(self, bs_element):
        """
        Extracts and returns details from a single CIRES job listing element.

        Args:
            bs_element (BeautifulSoup): A BeautifulSoup object representing a CIRES job listing.

        Returns:
            dict: A dictionary containing extracted job details.
        """
        job_link = bs_element.find("a")["href"] if bs_element.find("a") else "No link"
        title_element = bs_element.find(
            "p",
            class_="text-current font-sans text-lg lg:text-xl font-semibold dark:text-current",
        )
        category_element = bs_element.find(
            "p",
            class_="text-primary-light dark:text-indigo-300 font-sans uppercase text-[12px] font-bold tracking-wide",
        )
        date_opened_element = bs_element.find("p", {"class": "mt-4"})

        job_link = "https://cires.colorado.edu" + job_link
        title = title_element.text.strip() if title_element else "No title"
        category = (
            category_element.text.strip() if category_element else "Unknown category"
        )
        date_opened = (
            date_opened_element.text.strip().split(": ")[1]
            if date_opened_element
            else "No date"
        )

        return {
            "link": job_link,
            "title": title,
            "category": category,
            "date_opened": date_opened,
        }

    def fetch_cira_jobs(self, keywords, save_to_file=None):
        """
        Fetches and filters CIRA job listings based on the provided keywords.

        Args:
            keywords (str): Keywords to search for in the CIRA job listings.
            save_to_file (str, optional): If provided, saves the listings to the specified JSON file.

        Returns:
            list: A list of filtered CIRA job listings.
        """
        url = "https://www.cira.colostate.edu/welcome-about/jobs/"
        driver = self.setup_driver()
        driver.get(url)
        cira_soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()  # Close the browser

        # Initialize an empty list to store all CIRA job details
        all_cira_job_details = []

        cira_job_listings = cira_soup.find_all(
            "div", {"class": "col-lg-3 col-md-12 col-sm-12"}
        )

        for cira_job_listing in cira_job_listings:
            # Extract details for each CIRA job listing
            cira_job_details = self.extract_cira_job_details(cira_job_listing)

            # Fetch additional information based on the job's apply link
            url = cira_job_details["apply_link"]
            cira_additional_info = self.cira_extract_additional_info(url)

            # Update the job details with additional information
            cira_job_details.update(cira_additional_info)

            # Add the complete job details to the list
            all_cira_job_details.append(cira_job_details)

        # Filter the complete list of job details based on the keyword
        cira_filtered_job_details = self.filter_cira_jobs_by_description(
            all_cira_job_details, keywords
        )

        # Save the job listings to a file if a file path is provided
        if save_to_file:
            save_path = Path(save_to_file)
            with save_path.open("w") as f:
                json.dump(cira_filtered_job_details, f, indent=4)
            logging.info(f"CIRA listings saved to {save_to_file}")

        return cira_filtered_job_details

    def extract_cira_job_details(self, job_listing):
        """
        Extracts and returns details from a single CIRA job listing element.

        Args:
            bs_element (BeautifulSoup): A BeautifulSoup object representing a CIRA job listing.

        Returns:
            dict: A dictionary containing extracted job details.
        """

        # Extract job title
        title = job_listing.find("h4").text.strip()
        logging.debug(f"CIRA Title: {title}")
        # Extract "Apply" link
        apply_link = job_listing.find("a", href=True)["href"]
        logging.debug(f"CIRA Apply Link: {apply_link}")
        # Extract closing date, if available
        closing_date_info = job_listing.find("strong", string="Closes:")
        closing_date = (
            closing_date_info.find_next_sibling(string=True).strip()
            if closing_date_info
            else None
        )
        logging.debug(f"CIRA Closing Date: {closing_date}")

        # Extract position type, if available
        position_type_info = job_listing.find("strong", string="Position Type:")
        position_type = (
            position_type_info.find_next_sibling(string=True).strip()
            if position_type_info
            else None
        )
        logging.debug(f"CIRA Position Type: {position_type}")

        # Return a dictionary with the extracted details
        return {
            "title": title,
            "apply_link": apply_link,
            "closing_date": closing_date,
            "position_type": position_type,
        }

    def filter_cira_jobs_by_description(self, job_listings, keywords):
        """
        Filters a list of job listings by checking if a specific text is present in their 'Description of Work Unit'.

        Args:
            job_listings (list): A list of job listing dictionaries.
            text (str): The text to check for in the 'Description of Work Unit' of each job listing.

        Returns:
            list: A list of job listings that contain the specified text in their 'Description of Work Unit'.
        """
        # logging.debug("Debugging job listings:", job_listings)

        for job in job_listings:
            if isinstance(job, dict):
                description = job.get("Description of Work Unit", "")
                found = keywords.lower() in description.lower()
                logging.debug(f"Checking job: {description} - Keyword Found: {found}")
            else:
                logging.error(f"Unexpected type: {type(job)} - Content: {job}")

        # Keep only those where the specified text is found in the 'Description of Work Unit'
        return [
            job
            for job in job_listings
            if isinstance(job, dict)
            and keywords in job.get("Description of Work Unit", "")
        ]

    def cira_extract_additional_info(self, url):
        """
        Extracts additional details from a CIRA job details page.

        Args:
            url (str): The URL of the CIRA job details page.

        Returns:
            dict: A dictionary containing the extracted job details.
        """

        # Send a GET request to the URL
        response = requests.get(url)
        # Create a BeautifulSoup object from the response text
        cira_details_soup = BeautifulSoup(response.text, "html.parser")
        # Initialize an empty dictionary to store the extracted info
        info_dict = {}
        # Loop through all the table rows in the details page
        for row in cira_details_soup.find_all("tr"):
            # Extract the key from the table header (th) and strip any leading/trailing whitespace
            key = row.find("th").get_text(strip=True)
            # Extract the value from the table data (td) and strip any leading/trailing whitespace
            value = row.find("td").get_text(strip=True)
            if key == "Description of Work Unit":
                logging.debug(f"Description of Work Unit: {value}")
            # Add the key-value pair to the dictionary
            info_dict[key] = value

        # Return the dictionary with the extracted info
        return info_dict
