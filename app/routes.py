from flask import Blueprint, render_template
from flask import jsonify
from app import db
from app.models import Activity
from app.scraper.eventbrite_scraper import scrape_eventbrite
from app.scraper.facebook_scraper import scrape_facebook
from app.scraper.tripadvisor_scraper import scrape_tripadvisor

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return "Welcome to the activity search engine near Montpellier!"

@main.route('/scrape', methods=['POST'])
def scrape_data():
    try:
        # Clear the table
        Activity.query.delete()
        db.session.commit()
        # Scrape data from the various sources
        scrape_eventbrite()
        scrape_tripadvisor()
        scrape_facebook()
        return {"success": True, "message": "Data scraped successfully!"}, 200
    except Exception as e:
        return {"success": False, "message": str(e)}, 500

@main.route('/scraped-data', methods=['GET'])
def get_scraped_data():
    activities = Activity.query.all()
    result = [
        {
            "id": activity.id,
            "name": activity.name,
            "location": activity.location,
            "date": activity.date,
            "source": activity.source,
            "image_url": activity.image_url,
            "url": activity.url,
            "price": activity.price,
        }
        for activity in activities
    ]
    return jsonify(result)


@main.route('/scraped-saved-data', methods=['GET'])
def show_scraped_data():
    # Query the database for all scraped data
    activities = Activity.query.all()

    # Render an HTML template with the data passed in
    return render_template("scraped_data.html", activities=activities)