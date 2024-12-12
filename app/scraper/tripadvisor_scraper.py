import requests
from bs4 import BeautifulSoup
from app import db
from app.models import Activity
import logging

logger = logging.getLogger(__name__)

def scrape_tripadvisor():
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
        logger.error(f"Error fetching Eventbrite page: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    activities = soup.find_all('section', class_='iAHKl')
    logger.info(f"Found {len(activities)} activities on the Tripadvisor page.")

    for activity in activities:
        try:
            activity_url = activity.find('a', class_='BMQDV')
            activity_url = activity_url['href'] if activity_url else None
            # logger.info(f"ACTIVITY_URL {activity_url} .")

            image_url = activity.find('img', {'data-automation': 'productsShelfProductCardImage'})
            image_url = image_url['src'] if image_url else None
            # logger.info(f"IMAGE {image_url} .")
            #
            # details = activity.find('section', class_='event-card-details')
            # if not details:
            #     logger.warning("No details found, skipping activity.")
            #     continue

            name = activity.find('h3', class_='biGQs._P.fiohW.alXOW.EEXWj.GzNcMBYtua UTQMg alvrA fOtGX')
            name = name.get_text(strip=True) if name else None
            logger.info(f"NAME {name} .")

            paragraphs = details.find_all('p')
            date = paragraphs[0].get_text(strip=True) if len(paragraphs) > 0 else None
            location = paragraphs[1].get_text(strip=True) if len(paragraphs) > 1 else None
            price = paragraphs[2].get_text(strip=True) if len(paragraphs) > 2 else None

            # Log the scraped data
            logger.info(f"Scraped data - Name: {name}, Date: {date}, Location: {location}, Price: {price}, Image URL: {image_url}, URL: {activity_url}")

            # Skip if required fields are missing
            if not name or not date:
                logger.warning("Missing required fields (name or date), skipping activity.")
                continue

            # Check if the activity already exists
            existing_activity = Activity.query.filter_by(name=name, date=date).first()
            if existing_activity:
                logger.info(f"Activity already exists: {name} on {date}, skipping.")
                continue

            # Save to the database
            new_activity = Activity(
                name=name,
                location=location,
                date=date,
                source='Eventbrite',
                url=activity_url,
                image_url=image_url,
                price=price
            )
            db.session.add(new_activity)

            # Log after adding to the session
            logger.info(f"Added activity to session: {new_activity}")
        except Exception as e:
            logger.error(f"Error processing activity: {e}")

    try:
        db.session.commit()
        logger.info("Database commit successful.")
    except Exception as e:
        logger.error(f"Error committing to the database: {e}")
    finally:
        db.session.remove()

# def scrape_tripadvisor():
#     url = 'https://www.tripadvisor.com/Attractions-g187153-Activities-Montpellier_Herault_Occitanie.html'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     activities = soup.find_all('div', class_='listing_title')
#
#     for activity in activities:
#         name = activity.get_text(strip=True)
#         location = "Montpellier, Occitanie"
#         date = "Not specified"  # TripAdvisor may not have dates
#         activity_url = 'https://www.tripadvisor.com' + activity.find('a')['href']
#
#         # Save to the database
#         new_activity = Activity(name=name, location=location, date=date, source='TripAdvisor', url=activity_url)
#         db.session.add(new_activity)
#
#     db.session.commit()
