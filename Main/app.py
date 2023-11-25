from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

# Replace with your Google Places API key
GOOGLE_MAPS_API_KEY = 'API KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    material = request.args.get('material')
    zip_code = request.args.get('zip')
    distance_miles = float(request.args.get('distance'))

    # Use the Google Geocoding API to get the coordinates for the ZIP code
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={GOOGLE_MAPS_API_KEY}'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    # Check if the geocoding request was successful
    if geocoding_data.get('status') == 'OK':
        # Extract latitude and longitude from the geocoding result
        lat = geocoding_data['results'][0]['geometry']['location']['lat']
        lng = geocoding_data['results'][0]['geometry']['location']['lng']

        # Convert miles to meters
        distance_meters = distance_miles * 1609.34

        # Use the Google Places API to find recycling points
        search_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={material}+recycling&location={lat},{lng}&radius={distance_meters}&key={GOOGLE_MAPS_API_KEY}'
        response = requests.get(search_url)
        data = response.json()

        if data.get('status') == 'OK':
            # Filter places within the specified distance
            filtered_places = []
            for place in data.get('results', []):
                place_lat = place['geometry']['location']['lat']
                place_lng = place['geometry']['location']['lng']
                # Calculate distance between user and place
                place_distance_miles = calculate_distance(lat, lng, place_lat, place_lng)
                if place_distance_miles <= distance_miles:
                    filtered_places.append(place)

            return render_template('map.html', places=filtered_places, zip_code=zip_code, material=material, lat=lat, lng=lng, google_maps_api_key=GOOGLE_MAPS_API_KEY)

    return 'No recycling points found or an error occurred.'

def calculate_distance(lat1, lng1, lat2, lng2):
    # Calculate the Haversine distance between two sets of coordinates
    earth_radius = 6371  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng/2) * math.sin(delta_lng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = earth_radius * c
    distance_miles = distance_km * 0.621371  # Convert to miles
    return distance_miles

if __name__ == '__main__':
    app.run()
