import requests
from bs4 import BeautifulSoup
from app import db
from app.models import Activity
import logging

logger = logging.getLogger(__name__)


# Function to extract activity name from the URL
def extract_activity_name(url):
    # Split the URL by hyphen and get the last part before ".html"
    parts = url.split('-')

    # The name should be between the ID and the location part, so we take the middle part
    activity_name = '-'.join(parts[3:-1])  # Skip the first 3 parts (ID, code) and the last part (location)

    # Replace underscores with spaces for better readability
    activity_name = activity_name.replace('_', ' ')

    return activity_name


def scrape_tripadvisor():
    base_url = "https://www.tripadvisor.com"
    url = 'https://www.tripadvisor.com/Attractions-g187153-Activities-Montpellier_Herault_Occitanie.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching Tripadvisor page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    activities = soup.find_all('div', {'data-automation': 'shelfCard'})
    logger.info(f"Found {len(activities)} activities on the Tripadvisor page.")

    for activity in activities:
        try:
            activity_url = activity.find('a', class_='BMQDV')
            activity_url = activity_url['href'] if activity_url else None
            activity_url = base_url+activity_url if activity_url.startswith("/") else activity_url
            if activity_url:
                logger.info(f"ACTIVITY_URL {activity_url} .")

                # Extract the activity name from the URL
                activity_name = extract_activity_name(activity_url)
                logger.info(f"NAME {activity_name} .")

                # Get image URL
                image_url = activity.find('img', {'data-automation': 'productsShelfProductCardImage'})
                image_url = image_url['src'] if image_url else None
                logger.info(f"IMAGE {image_url} .")

                # If needed, you can extract other details here
                # For example, location, price, etc. (you can adapt the following accordingly)
                # location = ...
                price = activity.select_one('div[data-automation="cardProductPrice"] .fiohW.fOtGX')
                price = price.get_text(strip=True) if price else "Voir lien pour plus d'informations"
                logger.info(f"PRICE {price} .")


                # Log the scraped data
                logger.info(f"Scraped data - Name: {activity_name}, Image URL: {image_url}, URL: {activity_url}")

                # Skip if required fields are missing
                if not activity_name:
                    logger.warning("Missing required field (name), skipping activity.")
                    continue

                # Check if the activity already exists
                existing_activity = Activity.query.filter_by(name=activity_name).first()
                if existing_activity:
                    logger.info(f"Activity already exists: {activity_name}, skipping.")
                    continue

                # Save to the database
                new_activity = Activity(
                    name=activity_name,
                    source='Tripadvisor',
                    url=activity_url,
                    image_url=image_url,
                    price=price,
                    location="Montpellier- Voir lien pour plus d'informations",
                    date="Sous reserve"
                )
                db.session.add(new_activity)

                # Log after adding to the session
                logger.info(f"Added activity to session: {new_activity}")
            else:
                logger.warning("Activity URL not found, skipping.")
        except Exception as e:
            logger.error(f"Error processing activity: {e}")

    try:
        db.session.commit()
        logger.info("Database commit successful.")
    except Exception as e:
        logger.error(f"Error committing to the database: {e}")
    finally:
        db.session.remove()
