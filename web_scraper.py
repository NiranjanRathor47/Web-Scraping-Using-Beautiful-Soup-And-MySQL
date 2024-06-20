import requests
from bs4 import BeautifulSoup
import mysql.connector
import json
import time

# Constants for retry and timeout settings
MAX_RETRIES = 3
WAIT_TIME = 5  # Initial wait time before retrying, in seconds
TIMEOUT = 10  # Timeout for requests, in seconds

# Function to establish database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sangod@123',
        database='web_scraping'
    )
    return connection

# Function to extract meta title and description from BeautifulSoup object
def extract_meta_info(soup):
    title = soup.find('title').get_text() if soup.find('title') else 'N/A'
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else 'N/A'
    return title, description

# Function to extract social media links from BeautifulSoup object
def extract_social_media_links(soup):
    social_media_links = {}
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'facebook.com' in href:
            social_media_links['facebook'] = href
        elif 'twitter.com' in href:
            social_media_links['twitter'] = href
        elif 'linkedin.com' in href:
            social_media_links['linkedin'] = href
        elif 'instagram.com' in href:
            social_media_links['instagram'] = href
    return social_media_links

# Function to extract technology stack from BeautifulSoup object
def extract_tech_stack(soup):
    tech_stack = []
    if 'WordPress' in soup.text:
        tech_stack.append('WordPress')
    if 'Joomla' in soup.text:
        tech_stack.append('Joomla')
    if 'Drupal' in soup.text:
        tech_stack.append('Drupal')
    # Add more checks as necessary
    scripts = soup.find_all('script')
    for script in scripts:
        if script.get('src'):
            src = script['src']
            if 'jquery' in src:
                tech_stack.append('jQuery')
            elif 'react' in src:
                tech_stack.append('React')
            elif 'angular' in src:
                tech_stack.append('Angular')
            # Add more checks as necessary
    return tech_stack

# Function to extract payment gateways from BeautifulSoup object
def extract_payment_gateways(soup):
    payment_gateways = []
    if 'PayPal' in soup.text:
        payment_gateways.append('PayPal')
    if 'Stripe' in soup.text:
        payment_gateways.append('Stripe')
    if 'Razorpay' in soup.text:
        payment_gateways.append('Razorpay')
    return payment_gateways

# Function to categorize website based on meta title and description
def categorize_website(meta_title, meta_description):
    categories = {
        'ecommerce': ['shop', 'buy', 'product', 'sale'],
        'education': ['learn', 'course', 'tutorial'],
        'news': ['news', 'update', 'breaking'],
        'real estate': ['real estate', 'property', 'housing'],
        # Add more categories and keywords as needed
    }
    combined_text = (meta_title + ' ' + meta_description).lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in combined_text:
                return category
    return 'Uncategorized'

# Function to scrape website given a URL
def scrape_website(url):
    retries = MAX_RETRIES
    wait_time = WAIT_TIME
    for i in range(retries):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            meta_title, meta_description = extract_meta_info(soup)
            social_media_links = extract_social_media_links(soup)
            tech_stack = extract_tech_stack(soup)
            payment_gateways = extract_payment_gateways(soup)
            website_language = soup.find('html')['lang'] if soup.find('html').has_attr('lang') else 'N/A'
            category = categorize_website(meta_title, meta_description)

            return {
                'url': url,
                'social_media_links': json.dumps(social_media_links),
                'tech_stack': json.dumps(tech_stack),
                'meta_title': meta_title,
                'meta_description': meta_description,
                'payment_gateways': json.dumps(payment_gateways),
                'website_language': website_language,
                'category': category
            }
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {e}")
            if i < retries - 1:
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  # exponential backoff
            else:
                return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None

# Function to save scraped data into MySQL database
def save_to_db(data):
    if data:
        connection = get_db_connection()
        cursor = connection.cursor()

        add_website_info = ("CALL AddWebsiteInfo(%s, %s, %s, %s, %s, %s, %s, %s)")

        cursor.execute(add_website_info, (
            data['url'],
            data['social_media_links'],
            data['tech_stack'],
            data['meta_title'],
            data['meta_description'],
            data['payment_gateways'],
            data['website_language'],
            data['category']
        ))

        connection.commit()
        cursor.close()
        connection.close()

# Main function to initiate scraping for all URLs
def main():
    urls = [
'https://www.google.com', 
'https://www.youtube.com', 
'https://www.facebook.com', 
'https://www.wikipedia.org', 
'https://www.twitter.com', 
'https://www.instagram.com', 
'https://www.reddit.com', 
'https://www.duckduckgo.com', 
'https://www.amazon.com', 
'https://www.yahoo.com', 
'https://www.tiktok.com', 
'https://www.weather.com', 
'https://www.yahoo.co.jp', 
'https://www.bing.com', 
'https://www.fandom.com', 
'https://www.whatsapp.com', 
'https://www.yandex.ru', 
'https://www.openai.com', 
'https://www.archiveofourown.org', 
'https://www.microsoftonline.com', 
'https://www.twitch.tv', 
'https://www.microsoft.com', 
'https://www.linkedin.com', 
'https://www.live.com', 
'https://www.netflix.com', 
'https://www.quora.com', 
'https://www.t.me', 
'https://www.pixiv.net', 
'https://www.office.com', 
'https://www.vk.com', 
'https://www.livedoor.jp', 
'https://www.bit.ly', 
'https://www.globo.com', 
'https://www.webpkgcache.com', 
'https://www.imdb.com', 
'https://www.animeflv.net', 
'https://www.youtu.be', 
'https://www.aliexpress.com', 
'https://www.cnn.com', 
'https://www.nytimes.com', 
'https://www.pinterest.com', 
'https://www.github.com', 
'https://www.uol.com.br', 
'https://www.ebay.com', 
'https://www.amazon.co.jp', 
'https://www.discord.com', 
'https://www.marca.com', 
'https://www.apple.com', 
'https://www.spotify.com', 
'https://www.msn.com', 
'https://www.sharepoint.com', 
'https://www.espn.com', 
'https://www.dailymail.co.uk', 
'https://www.booking.com', 
'https://www.wordpress.com', 
'https://www.slideshare.net', 
'https://www.change.org', 
'https://www.telegram.me', 
'https://www.4shared.com', 
'https://www.cbsnews.com', 
'https://www.office.com', 
'https://www.estadao.com.br', 
'https://www.amazon.co.uk', 
'https://www.myaccount.google.com', 
'https://www.tinyurl.com', 
'https://www.mail.google.com', 
'https://www.hugedomains.com', 
'https://www.pixabay.com', 
'https://www.aliexpress.com', 
'https://www.photos.google.com', 
'https://www.cpanel.net', 
'https://www.yahoo.com', 
'https://www.mail.ru', 
'https://www.google.co.jp', 
'https://www.cnn.com', 
'https://www.myspace.com', 
'https://www.weebly.com', 
'https://www.dropbox.com', 
'https://www.gravatar.com', 
'https://www.who.int', 
'https://www.line.me', 
'https://www.archive.org', 
'https://www.forbes.com', 
'https://www.forms.gle', 
'https://www.mirror.co.uk', 
'https://www.marketingplatform.google.com', 
'https://www.wp.com', 
'https://www.bbc.com', 
'https://www.reuters.com', 
'https://www.scribd.com', 
'https://www.usatoday.com', 
'https://www.booking.com', 
'https://www.discord.gg', 
'https://www.nature.com', 
'https://www.huffingtonpost.com', 
'https://www.buydomains.com', 
'https://www.issuu.com', 
'https://www.ig.com.br', 
'https://www.rakuten.co.jp', 
'https://www.networkadvertising.org'

    ]

    for url in urls:
        data = scrape_website(url)
        save_to_db(data)
        if data:
            print(f"Data for {url} saved successfully.")
        else:
            print(f"Failed to scrape data from {url}")

if __name__ == "__main__":
    main()
