import random

categories = {
    "cleanliness": ["Immaculate", "Tidy", "Average", "Casual", "Poor"],
    "sleeping_habits": ["Early Bird", "Morning Person", "Flexible", "Night Owl", "Very Late Nights"],
    "guest_habits": ["Never Hosts", "Rare Guests", "Occasional Guests", "Regular Guests", "Frequent Host"],
    "party_habits": ["Never Parties", "Rarely Parties", "Sometimes Parties", "Often Parties", "Regular Party Host"],
    "cooking_habits": ["Never Cooks", "Seldom Cooks", "Cooks Occasionally", "Cooks Regularly", "Frequent Chef"],
    "shared_responsibilities": ["Fully Shared", "Mostly Shared", "Equally Shared", "Minimal Shared", "No Shared"],
    "noise_tolerance": ["Silence Preferred", "Quiet Tolerant", "Average", "Noise Indifferent", "Noise Welcoming"],
    "pet_acceptance": ["No Pets Allowed", "Dogs Allowed", "Cats Allowed", "Small Rodents Allowed", "Other Pets Allowed"],
    "alcohol_usage": ["Non-Drinker", "Social Drinker", "Moderate Drinker", "Frequent Drinker"],
    "cannabis_usage": ["Non-User", "Occasional User", "Regular User", "Frequent User"],
    "smoking": ["Non-Smoker", "Social Smoker", "Regular Smoker", "Heavy Smoker"],
    "car_ownership": ["Yes", "No"],
    "vegetarian_vegan": ["Yes", "No"],
    "overnight_guests": ["Yes", "No"],
    "financially_stable": ["Yes", "No"],
    "food_sharing": ["Yes", "No"]
}

for category, options in categories.items():
    chosen_option = random.choice(options)
    print(f"{category} = \'{chosen_option}\',")