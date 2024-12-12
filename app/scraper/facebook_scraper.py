from selenium import webdriver
from app import db
from app.models import Activity

def scrape_facebook():
    driver = webdriver.Chrome()  # Adjust path to your ChromeDriver if needed
    url = 'https://www.facebook.com/events/102678582172773/'
    driver.get(url)

    # Extract activity details (simplified example)
    name = driver.find_element_by_class_name('notranslate').text
    location = driver.find_element_by_class_name('x1bb57kw').text
    date = driver.find_element_by_class_name('x1h7jr4j').text
    activity_url = driver.current_url  # Facebook event URL

    # Save to the database
    new_activity = Activity(name=name, location=location, date=date, source='Facebook', url=activity_url)
    db.session.add(new_activity)
    db.session.commit()

    driver.quit()
