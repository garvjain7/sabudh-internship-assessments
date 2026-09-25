import os
import re
import time
import random

import requests
import pandas as pd
from bs4 import BeautifulSoup

HOME_URL = "https://indianexpress.com/"
MAX_ARTICLES = 25
INTERN_NAME = "Garv Jain"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NewsScraperBot/1.0)"}
ARTICLE_URL_PATTERN = re.compile(r"https?://indianexpress\.com/article/.+-\d+/?$")  # matches IE article URLs


def get_soup(url, session, retries=2, timeout=10):
    # fetches a page and parses it, retrying once on network failure
    for attempt in range(retries):
        try:
            resp = session.get(url, headers=HEADERS, timeout=timeout)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except requests.exceptions.RequestException:
            if attempt == retries - 1:
                return None
            time.sleep(1)


def get_top_story_links(soup, limit=MAX_ARTICLES):
    # pulls unique, article-shaped links off the homepage, skipping nav/short-text links
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("?")[0]
        text = a.get_text(strip=True)
        if href in seen or len(text) < 20:
            continue
        if ARTICLE_URL_PATTERN.match(href):
            seen.add(href)
            links.append((text, href))
        if len(links) >= limit:
            break
    return links


def extract_title(soup):
    # prefers the on-page h1, falls back to the og:title meta tag
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    og_title = soup.find("meta", property="og:title")
    return og_title["content"].strip() if og_title else ""


def extract_full_text(soup):
    # tries known IE content containers first, then falls back to <article> or whole page
    for selector in ({"id": "pcl-full-content"}, {"class": "full-details"}, {"class": "story_details"}):
        container = soup.find("div", selector)
        if container:
            break
    else:
        container = soup.find("article") or soup

    paragraphs = [p.get_text(strip=True) for p in container.find_all("p")]
    paragraphs = [p for p in paragraphs if p and "Also Read" not in p and "Advertisement" not in p]  # drop boilerplate
    return " ".join(paragraphs)


def scrape():
    session = requests.Session()
    home_soup = get_soup(HOME_URL, session)
    if home_soup is None:
        print("Could not load homepage — aborting.")
        return pd.DataFrame(columns=["NEWS_TITLE", INTERN_NAME.replace(" ", "_").upper(), "NEWS_LINK", "FULL_SCRAPED_TEXT"])

    records = []
    for headline_text, link in get_top_story_links(home_soup):
        time.sleep(random.uniform(1, 2))  # polite delay between requests
        article_soup = get_soup(link, session)
        if article_soup is None:
            continue  # skip articles that failed to load

        title = extract_title(article_soup) or headline_text
        full_text = extract_full_text(article_soup)
        if not full_text:
            continue  # skip pages we couldn't extract usable text from

        records.append({
            "NEWS_TITLE": title,
            "Intern Name": INTERN_NAME,
            "NEWS_LINK": link,
            "FULL_SCRAPED_TEXT": full_text,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = scrape()
    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "indian_express_news.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} articles to {out_path}")