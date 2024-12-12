from app import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(50), nullable=False)  # Eventbrite, TripAdvisor, Facebook
    image_url = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(50), nullable=True)

    def __init__(self, name, location, date, source, url, image_url=None, price=None):
        self.name = name
        self.location = location
        self.date = date
        self.source = source
        self.url = url
        self.image_url = image_url
        self.price = price

    @property
    def __repr__(self):
        return f"<Activity {self.name} from {self.source}>"
