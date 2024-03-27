#!/usr/bin/env python
import argparse
import logging
import shutil
import sys
from pathlib import Path

from .CredentialManager import CredentialManager
from .JobScraper import JobScraper


def setup_arg_parser():
    """
    Set up and return an argument parser for command-line options.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Scrape job listings from various sources based on keywords."
    )

    # Argument definitions
    parser.add_argument(
        "-usajobs-keyword",
        "--usajobs-keyword",
        dest="usajobs_keyword",
        required=False,
        default="'Global Systems Laboratory'",
        help="The keyword string to search for in the USAJobs listings.",
    )

    parser.add_argument(
        "-cires-keyword",
        "--cires-keyword",
        dest="cires_keyword",
        required=False,
        default="'NOAA GSL'",
        help="The keyword string to search for in the CIRES listings.",
    )

    parser.add_argument(
        "-cira-keyword",
        "--cira-keyword",
        dest="cira_keyword",
        required=False,
        default="'Global Systems Laboratory'",
        help="The keyword string to search for in the CIRA listings.",
    )

    # Arguments for saving results to JSON files
    parser.add_argument(
        "-usajobs-json-file",
        "--usajobs-json-file",
        dest="usajobs_json_file",
        required=False,
        help="Filename to store the results from USAJobs.",
    )

    parser.add_argument(
        "-cires-json-file",
        "--cires-json-file",
        dest="cires_json_file",
        required=False,
        help="Filename to store the results from CIRES.",
    )

    parser.add_argument(
        "-cira-json-file",
        "--cira-json-file",
        dest="cira_json_file",
        required=False,
        help="Filename to store the results from CIRA.",
    )

    parser.add_argument(
        "-user-agent",
        "--user-agent",
        dest="user_agent",
        default=None,
        help="The username used with the USAJobs API.",
    )

    parser.add_argument(
        "-authorization-key",
        "--authorization-key",
        dest="authorization_key",
        default=None,
        help="The API key used with the USAJobs API.",
    )

    # Verbose logging flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    return parser


def initialize_credential_manager(expected_keys):
    """
    Initialize the CredentialManager with credentials from the ~/.rtvideo/credentials file,
    and check for the presence of expected keys.

    Args:
        expected_keys (list of str): A list of expected keys to be found in the credentials.

    Returns:
        CredentialManager: An instance of the CredentialManager loaded with credentials.

    Raises:
        FileNotFoundError: If the credentials file is not found.
        KeyError: If any of the expected keys are missing.
    """
    home_directory = Path.home()
    credentials_file = home_directory / ".jscraper" / "credentials"

    # Ensure credentials file exists
    if not credentials_file.exists():
        raise FileNotFoundError(f"Credentials file not found at {credentials_file}")

    # Initialize CredentialManager with the credentials file
    credential_manager = CredentialManager(str(credentials_file))
    credential_manager.read_credentials(expected_keys=expected_keys)

    # Additionally, check if all expected keys are available as environment variables
    # as a fallback or supplement
    for key in expected_keys:
        if not credential_manager.get_credential(key):
            raise KeyError(f"Missing expected key: {key}")

    return credential_manager


def main():
    """
    Main function to execute script logic.
    """
    # Constants used for scraping
    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

    # Set up command-line arguments and logging
    parser = setup_arg_parser()
    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        # Retrieve secrets from credentials file
        expected_keys = ["USER_AGENT", "AUTHORIZATION_KEY"]
        credential_manager = initialize_credential_manager(expected_keys)

        # If certain arguments were not provided, update them with credentials
        args.user_agent = args.user_agent or credential_manager.get_credential(
            "USER_AGENT"
        )
        args.authorization_key = (
            args.authorization_key
            or credential_manager.get_credential("AUTHORIZATION_KEY")
        )

    except KeyError as e:
        logging.error(f"Missing credential: {e}")
        sys.exit(1)

    # Check for chromedriver installation
    if shutil.which("chromedriver") is None:
        logging.error(
            "chromedriver is not installed. Please install it using your system's package manager."
        )
        sys.exit(1)

    # Initialize the JobScraper and fetch job listings
    scraper = JobScraper(args.user_agent, args.authorization_key, CHROMEDRIVER_PATH)

    # Process jobs from different sources
    # For USAJobs
    federal_jobs = scraper.fetch_federal_jobs(
        args.usajobs_keyword, args.usajobs_json_file
    )
    if federal_jobs:
        for job in federal_jobs:
            job_details = scraper.extract_federal_job_details(job)
            logging.info(f"Matching USA Job: {job_details['title']}")
    else:
        logging.info(
            f"No federal job listings available for keyword {args.usajobs_keyword}."
        )

    # For CIRES
    cires_jobs = scraper.fetch_cires_jobs(args.cires_keyword, args.cires_json_file)
    if cires_jobs:
        for job in cires_jobs:
            logging.info(f"Matching CIRES Job: {job['title']}")
    else:
        logging.info(
            f"No CIRES jobs listings available for keyword {args.cires_keyword}."
        )

    # For CIRA
    cira_jobs = scraper.fetch_cira_jobs(args.cira_keyword, args.cira_json_file)
    if cira_jobs:
        for job in cira_jobs:
            logging.info(f"Matching CIRA Job: {job['title']}")
    else:
        logging.info(
            f"No CIRA jobs listings available for keyword {args.cira_keyword}."
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
