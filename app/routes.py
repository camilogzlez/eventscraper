from flask import Blueprint, render_template, request
from flask import jsonify
import os
from google.cloud import dialogflow_v2 as dialogflow
from app import db
from app.models import Activity
from app.scraper.eventbrite_scraper import scrape_eventbrite
from app.scraper.facebook_scraper import scrape_facebook
from app.scraper.tripadvisor_scraper import scrape_tripadvisor
import logging

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


@main.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']

    dialogflow_client = dialogflow.SessionsClient()
    logging.info(f"Request payload: {req}")

    session_id = req.get("session")
    session = dialogflow_client.session_path(os.getenv("GOOGLE_PROJECT_ID"), session_id)

    if intent == 'trouve des activites':
        # Extract parameters from the Dialogflow request
        params = req['queryResult']['parameters']
        name = params.get('name')
        location = params.get('location', None)
        date = params.get('date', None)
        price = params.get('price', None)

        # Start building the query
        query = Activity.query

        if name:
            query = query.filter(Activity.name.ilike(f'%{name}%'))
        if location:
            query = query.filter(Activity.location.ilike(f'%{location}%'))
        if date:
            query = query.filter(Activity.date.ilike(f'%{date}%'))
        if price:
            try:
                price = float(price)
                query = query.filter(Activity.price == price)  # Use `==` for exact price match
            except ValueError:
                return jsonify({
                    "fulfillmentText": "Invalid price provided.",
                    "activities": []
                })

        # Log the query and parameters
        logging.info(f"Query with filters - Name: {name}, Location: {location}, Date: {date}, Price: {price}")

        # Execute the query and get the filtered activities
        filtered_activities = query.all()

        # Log the results
        # logging.info(f"Found activities: {filtered_activities}")

        # Prepare the response
        if filtered_activities:
            activity_details = [
                {
                    "name": activity.name,
                    "location": activity.location,
                    "date": activity.date,
                    "price": activity.price,
                    "image_url": activity.image_url,
                    "url": activity.url,
                    "source": activity.source
                }
                for activity in filtered_activities
            ]
            response_data = {
                "fulfillmentText": "I found the following activities:",
                "activities": activity_details
            }
        else:
            response_data = {
                "fulfillmentText": "I couldn't find any activities matching your query.",
                "activities": []
            }

        # Return the response
        return jsonify(response_data)

    else:
        return jsonify({
            "fulfillmentText": "Sorry, I couldn't process that request."
        })