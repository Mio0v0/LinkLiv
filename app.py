from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import UserProfile
from config import DROPDOWN_1, DROPDOWN_2, DROPDOWN_3, FIELDS_1, FIELDS_2, FIELDS_3
from extensions import db
import os

app = Flask(__name__)

database_uri = os.environ.get('DATABASE_URL', 'postgresql://kailun:kailun@localhost/linklivdb')

# Replace 'postgres://' with 'postgresql://' if it exists in the URI
if database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db.init_app(app)

@app.route('/')
def index():
    if 'uni' not in session:
        return redirect(url_for('login'))

    filter_choices = request.args
    query = UserProfile.query

    for category, values in filter_choices.lists():
        if hasattr(UserProfile, category):
            if category == 'rent':
                rent_filters = []
                for value in values:
                    min_val, max_val = map(int, value.split('-'))
                    rent_filters.append(UserProfile.budget_min >= min_val)
                    rent_filters.append(UserProfile.budget_max <= max_val)
                if rent_filters:
                    query = query.filter(db.and_(*rent_filters))
            else:
                query = query.filter(getattr(UserProfile, category).in_(values))

    all_users = query.all()
    return render_template('index.html', all_users=all_users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uni = request.form.get('uni')
        passcode = request.form.get('passcode')
        user = UserProfile.query.filter_by(uni=uni).first()

        if user and user.passcode == passcode:
            session['uni'] = uni
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('uni', None)
    return redirect(url_for('index'))

@app.route('/profile/show', methods=['GET'])
def profile_show():
    uni = request.args.get('uni')
    if not uni:
        return "User identifier not provided", 400

    user_profile = UserProfile.query.filter_by(uni=uni).first()
    if not user_profile:
        return "User profile not found", 404

    is_own_profile = session.get('uni') == uni
    
    return render_template('show.html', 
                           user_profile=user_profile,
                           is_own_profile=is_own_profile,
                           field_1 = FIELDS_1,
                           field_2 = FIELDS_2)


@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    if request.method == 'GET':
        uni = session.get('uni')
        user_profile = UserProfile.query.filter_by(uni=uni).first()
        
        if not user_profile:
            print("User profile not found for uni:", uni)
            return "User profile not found", 404
        
        return render_template('edit.html', 
                                user_profile=user_profile, 
                                dropdown_1=DROPDOWN_1,
                                dropdown_2=DROPDOWN_2)

    if request.method == 'POST':
        uni = session.get('uni')
        user_profile = UserProfile.query.filter_by(uni=uni).first()

        if not user_profile:
            print("User profile not found for uni:", uni)
            return "User profile not found", 404

        for field in (FIELDS_1 + FIELDS_2):
            print(field, request.form.get(field), getattr(user_profile, field))
            setattr(user_profile, field, request.form.get(field) or getattr(user_profile, field))
        
        user_profile.budget_min = request.form.get('budget_min', type=int)
        user_profile.budget_max = request.form.get('budget_max', type=int)

        db.session.commit()
        print("Debug - User Profile Data:", vars(user_profile))
        return redirect(url_for('profile_show', uni=session['uni']))

@app.route('/compare')
def compare():
    uni = session.get('uni')
    user_profile = UserProfile.query.filter_by(uni=uni).first()

    compare_with_uni = request.args.get('compare_with')
    compare_user_profile = UserProfile.query.filter_by(uni=compare_with_uni).first()

    if not user_profile or not compare_user_profile:
        print("User profile not found for uni:", uni)
        return "User profile not found", 404

    user_profile_2 = {field: getattr(user_profile, field, 'N/A') for field in FIELDS_3}
    compare_user_profile_2 = {field: getattr(compare_user_profile, field, 'N/A') for field in FIELDS_3}

    print(user_profile_2, compare_user_profile_2)
    return render_template('compare.html', 
                            fields_2=FIELDS_3,
                            user_profile=user_profile, 
                            compare_user_profile=compare_user_profile,
                            user_profile_2=user_profile_2,
                            compare_user_profile_2=compare_user_profile_2)

@app.route('/filter')
def filter():
    return render_template('filter.html',
                            dropdown_3=DROPDOWN_3)

@app.route('/add')
def add():
    return render_template('add.html')

def reset_database():
    db.drop_all()
    db.create_all()
    print("Database reset.")

def seed_database():
    user1 = UserProfile(uni='jd1234', 
    passcode='password123', 
    name='John Doe', 
    phone_number='9492198022', 
    building='Harmony Hall',
    room_type='Single',
    
    gender = 'Male',
    budget_min = '200',
    budget_max = '2000',

    cleanliness = 'Casual',
    sleeping_habits = 'Flexible',
    guest_habits = 'Rare Guests',
    party_habits = 'Rarely Parties',
    cooking_habits = 'Never Cooks',
    shared_responsibilities = 'Equally Shared',
    noise_tolerance = 'Average',
    pet_acceptance = 'Other Pets Allowed',
    alcohol_usage = 'Social Drinker',
    cannabis_usage = 'Non-User',
    smoking = 'Heavy Smoker',
    car_ownership = True,
    vegetarian_vegan = True,
    overnight_guests = False,
    financially_stable = True,
    food_sharing = True
    )

    user2 = UserProfile(uni='js1234', 
    passcode='password123', 
    name='Jane Smith', 
    phone_number='9492198022',
    building='Hogan Hall',
    room_type='Double', 
    
    gender = 'Female',
    budget_min = '200',
    budget_max = '2000',
    
    cleanliness = 'Tidy',
    sleeping_habits = 'Morning Person',
    guest_habits = 'Never Hosts',
    party_habits = 'Often Parties',
    cooking_habits = 'Cooks Occasionally',
    shared_responsibilities = 'Mostly Shared',
    noise_tolerance = 'Noise Welcoming',
    pet_acceptance = 'Dogs Allowed',
    alcohol_usage = 'Social Drinker',
    cannabis_usage = 'Occasional User',
    smoking = 'Social Smoker',
    car_ownership = True,
    vegetarian_vegan = False,
    overnight_guests = False,
    financially_stable = True,
    food_sharing = True
    )

    user3 = UserProfile(uni='at1234', 
    passcode='password123', 
    name='Apple Tree', 
    phone_number='1231231111',
    building='47 Claremont Avenue',
    room_type='Single', 
    
    gender = 'Female',
    budget_min = '2000',
    budget_max = '4000',
    
    cleanliness = 'Casual',
    sleeping_habits = 'Flexible',
    guest_habits = 'Occasional Guests',
    party_habits = 'Often Parties',
    cooking_habits = 'Never Cooks',
    shared_responsibilities = 'Minimal Shared',
    noise_tolerance = 'Quiet Tolerant',
    pet_acceptance = 'Dogs Allowed',
    alcohol_usage = 'Frequent Drinker',
    cannabis_usage = 'Frequent User',
    smoking = 'Regular Smoker',
    car_ownership = True,
    vegetarian_vegan = True,
    overnight_guests = True,
    financially_stable = True,
    food_sharing = True
    )

    user4 = UserProfile(uni='ls1234', 
    passcode='password123', 
    name='Lemon Smith', 
    phone_number='1233212222',
    building='River Hall',
    room_type='Double', 
    
    gender = 'Female',
    budget_min = '1000',
    budget_max = '6000',
    
    cleanliness = 'Immaculate',
    sleeping_habits = 'Early Bird',
    guest_habits = 'Occasional Guests',
    party_habits = 'Sometimes Parties',
    cooking_habits = 'Frequent Chef',
    shared_responsibilities = 'Minimal Shared',
    noise_tolerance = 'Average',
    pet_acceptance = 'Small Rodents Allowed',
    alcohol_usage = 'Frequent Drinker',
    cannabis_usage = 'Frequent User',
    smoking = 'Non-Smoker',
    car_ownership = False,
    vegetarian_vegan = False,
    overnight_guests = False,
    financially_stable = False,
    food_sharing = False
    )

    user5 = UserProfile(uni='ps1234', 
    passcode='password123', 
    name='Peach Fruit', 
    phone_number='9492198888',
    building='Woodbridge Hall',
    room_type='Double', 
    
    gender = 'Male',
    budget_min = '1000',
    budget_max = '2000',
    
    cleanliness = 'Tidy',
    sleeping_habits = 'Night Owl',
    guest_habits = 'Frequent Host',
    party_habits = 'Never Parties',
    cooking_habits = 'Frequent Chef',
    shared_responsibilities = 'Minimal Shared',
    noise_tolerance = 'Quiet Tolerant',
    pet_acceptance = 'No Pets Allowed',
    alcohol_usage = 'Moderate Drinker',
    cannabis_usage = 'Regular User',
    smoking = 'Non-Smoker',
    car_ownership = False,
    vegetarian_vegan = False,
    overnight_guests = False,
    financially_stable = False,
    food_sharing = False
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()

    print("Database seeded!")


if __name__ == '__main__':
    with app.app_context():
        reset_database()
        seed_database()
    app.run(debug=True)
