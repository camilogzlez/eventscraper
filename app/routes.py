from flask import Blueprint, render_template

from app.models import Activity
from app.scraper.eventbrite_scraper import scrape_eventbrite
from app.scraper.facebook_scraper import scrape_facebook
from app.scraper.tripadvisor_scraper import scrape_tripadvisor

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return "Welcome to the activity search engine near Montpellier!"

@main.route('/scrape')
def scrape_data():
    # Scrape data from the various sources
    scrape_eventbrite()
    scrape_tripadvisor()
    scrape_facebook()
    return "Data scraped successfully!"

@main.route('/scraped-data', methods=['GET'])
def show_scraped_data():
    # Query the database for all scraped data
    activities = Activity.query.all()

    # Render an HTML template with the data passed in
    return render_template("scraped_data.html", activities=activities)

@main.route('/debug_template_path')
def debug_template_path():
    return "Template folder: {current_app.template_folder}"
