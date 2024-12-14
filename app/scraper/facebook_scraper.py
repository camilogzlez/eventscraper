import os
import time
import logging
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from app import db
from app.models import Activity

# Configure logging
logger = logging.getLogger(__name__)

def scrape_facebook():
    # Configure WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    # Initialize WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    # Load environment variables
    load_dotenv()

    # Define URLs
    url_base = 'https://www.facebook.com'
    url_events = 'https://www.facebook.com/events/search/?q=montpellier'

    try:
        # Open Facebook homepage
        driver.get(url_base)

        # Handle cookie banner
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="facebook"]/body/div[3]/div[2]/div/div/div/div/div[3]/div[2]/div/div[2]/div[1]'))
            )
            cookie_button.click()
        except Exception as e:
            logger.warning("No cookie banner detected or unable to click it: %s", e)

        # Login to Facebook
        email = os.getenv('FB_EMAIL')
        password = os.getenv('FB_PASSWORD')

        if not email or not password:
            raise ValueError("Facebook credentials are missing. Check your environment variables.")

        try:
            # Enter email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="royal_email"]'))
            )
            email_input.clear()
            email_input.send_keys(email)

            # Enter password
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="royal_pass"]'))
            )
            password_input.clear()
            password_input.send_keys(password)

            # Click login button
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="royal_login_button"]'))
            )
            login_button.click()

            # Confirm successful login
            logger.info("Login successful.")
        except Exception as e:
            logger.error("Error during login: %s", e)

        try:
            # Ensure login is successful by waiting for a known post-login element
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_4O"]/div/div/div[1]/div/div[2]/div[4]/div/div[1]/div[1]/ul/li[1]/span/div/a'))
            )
            logger.info("Post-login navigation ready.")
        except Exception as e:
            logger.error("Error after login: %s", e)

        # Navigate to events page and scrape activities
        try:
            driver.get(url_events)
            time.sleep(5)  # Adjust this delay based on your internet speed
            # Step 3: Scroll to load all activities
            scroll_pause_time = 2  # Pause time between scrolls
            last_height = driver.execute_script("return document.body.scrollHeight")
            start_time = time.time()

            while True:
                # Scroll down to the bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new content to load
                time.sleep(scroll_pause_time)

                # Check if additional content has loaded
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height or time.time() - start_time > 10:  # Timeout after 20 seconds
                    break
                last_height = new_height

            # Step 4: Parse the fully loaded page
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            activities = soup.find_all('a', class_='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lliihq')
            logger.info("Found %d activities on the Facebook page.", len(activities))
        except Exception as e:
            logger.error("Error loading activities: %s", e)

        # Process each activity
        for activity in activities:
            try:
                activity_url = activity['href'] if activity.has_attr('href') else None
                activity_url = url_base + activity_url if activity_url and activity_url.startswith("/") else activity_url
                # logger.info(f"ACTIVITY_URL {activity_url} .")

                image_url = activity.find('img', class_='x1rg5ohu x5yr21d xl1xv1r xh8yej3')
                image_url = image_url['src'] if image_url else None
                # logger.info(f"IMAGE URL {image_url} .")

                name = activity.find('span', class_='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j')
                name = name.get_text(strip=True) if name else "Name not found"
                # logger.info(f"NAME {name} .")

                location = activity.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft')
                location = location.get_text(strip=True) if location else "Location not found"
                # logger.info(f"LOCATION {location} .")

                date = activity.find('div', class_='xu06os2 x1ok221b')
                date = date.get_text(strip=True) if date else "Date not found"
                # logger.info(f"DATE {date} .")
        #         logger.info("Scraped data - Name: %s, Image URL: %s, URL: %s, Price: %s", activity_name, image_url, activity_url, price)

        #         # Check if the activity already exists
                existing_activity = Activity.query.filter_by(name=name).first()
                if existing_activity:
                    logger.info("Activity already exists: %s, skipping.", activity_name)
                    continue
        #
                # Save to the database
                new_activity = Activity(
                    name=name,
                    source='Facebook',
                    url=activity_url,
                    image_url=image_url,
                    price="Voir lien pour plus d'informations",
                    location=location,
                    date=date
                )
                db.session.add(new_activity)
                logger.info("Added activity to session: %s", new_activity)
            except Exception as e:
                logger.error("Error processing activity: %s", e)
        # Commit to the database
        try:
            db.session.commit()
            logger.info("Database commit successful.")
        except Exception as e:
            logger.error("Error committing to the database: %s", e)

    finally:
        # Clean up resources
        driver.quit()
        db.session.remove()
