import pywikibot
import requests
from typing import List
from datetime import datetime
import yaml

# Pageviews API constants
PAGEVIEWS_BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents"
PAGEVIEWS_QUERY_START = datetime(2020, 10, 1, 0)
PAGEVIEWS_QUERY_END = datetime(2020, 11, 1, 0)
PAGEVIEWS_QUERY_GRANULARITY = 'MONTHLY'


def generate_wiki_page_from_title(title: str) -> pywikibot.Page:
    """
    Gets the wikipedia page referencing the given title.

    Args:
        title (str): title of the wikipedia page to search for.

    Returns:
        pywikibot.Page: an interface to the wikipedia page of interest.
    """

    # Interface for MediaWiki sites
    site = pywikibot.Site('en', 'wikipedia')

    # A MediaWiki page
    page = pywikibot.Page(site, title)

    return page


def generate_wiki_page_from_url(url: str) -> pywikibot.Page:
    """
    A wrapper around `get_wikipedia_page_from_title`. Accepts a URL for a wikipedia page from which the title is extracted.

    Args:
        url (str): URL of wikipedia page.

    Returns:
        pywikibot.Page: an interface to the wikipedia page of interest.
    """

    # Extract title
    title = url.split('/')[-1]

    return generate_wiki_page_from_title(title)


def retrieve_outgoing_links(page: pywikibot.Page) -> List[pywikibot.Page]:
    """
    Retrieve all outgoing links from the provided wiki page.

    Args:
        page (pywikibot.Page): the page containing outgoing links.

    Returns:
        List[pywikibot.Page]: a list of pages linked from the original page.
    """

    return [link for link in page.linkedPages() if link.namespace() == 0]


def retreive_pageviews(page: pywikibot.Page,
                       pv_config_path: str) -> List[int]:
    """
    Retreive page views for a wiki page.

    Args:
        page (pywikibot.Page): wiki page to retreive views for.
        pv_config_path (str): path to the .yaml file configurations for pageviews API.

    Raises:
        Exception: path to pageviews configuration is invalid.
        Exception: request may fail.

    Returns:
        List[int]: returns page views per month.
    """

    try:
        # Load configurations.
        with open(pv_config_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)

            website = config["PERSONAL_WEBSITE"]
            email = config["EMAIL_ADDRESS"]
    except FileNotFoundError:
        raise Exception(
            "wikiapi.retreive_pageviews: Please provide valid path to YAML configurations.")

    # Headers for the API request.
    headers = {"Accept": "application/json",
               "User-Agent": f"WikiWormhole/1.0 ({website}; {email})"}

    # Format datetimes as timestamps.
    start_ts = _generate_timestamp(PAGEVIEWS_QUERY_START)
    end_ts = _generate_timestamp(PAGEVIEWS_QUERY_END)

    # Generate the URL for the pageviews API.
    uri_title = page.title().replace(' ', '_')
    generated_url = f"{PAGEVIEWS_BASE_URL}/{uri_title}/{PAGEVIEWS_QUERY_GRANULARITY}/{start_ts}/{end_ts}"

    # Retrieve JSON data from the API.
    response = requests.get(generated_url, headers=headers)

    # Did the request fail.
    if response.status_code != 200:
        raise Exception(
            f"PWikiAPI.get_page_views: invalid for URL request: {generated_url}")

    # Extract page views from JSON.
    return [d['views'] for d in response.json()['items']]


def _generate_timestamp(dt: datetime) -> str:
    """
    Generates a timestamp string from the provided datetime.

    Args:
        dt (datetime): datetime to be converted to string.

    Returns:
        str: resultant timestamp.
    """

    # Ensure digits are two characters long.
    def fmt(v: int) -> str:
        return str(v) if v >= 10 else f"0{v}"

    # Extract components of datetime
    year = dt.year
    month, day, hour = fmt(dt.month), fmt(dt.day), fmt(dt.hour)

    return f"{year}{month}{day}{hour}"
