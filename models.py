from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash

class UserProfile(db.Model):
    uni = db.Column(db.String(10), primary_key=True, unique=True, nullable=False)
    passcode = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    
    gender = db.Column(db.String(50))
    bio = db.Column(db.Text)
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    cleanliness = db.Column(db.String(50))
    sleeping_habits = db.Column(db.String(50))
    guest_habits = db.Column(db.String(50))
    party_habits = db.Column(db.String(50))
    cooking_habits = db.Column(db.String(50))
    shared_responsibilities = db.Column(db.String(50))
    noise_tolerance = db.Column(db.String(50))
    pet_acceptance = db.Column(db.String(50))
    alcohol_usage = db.Column(db.String(50))
    cannabis_usage = db.Column(db.String(50))
    smoking = db.Column(db.String(50))
    car_ownership = db.Column(db.Boolean)
    vegetarian_vegan = db.Column(db.Boolean)
    overnight_guests = db.Column(db.Boolean)
    financially_stable = db.Column(db.Boolean)
    food_sharing = db.Column(db.Boolean)

    def __repr__(self):
        return f'<UserProfile {self.name}>'