from flask import Flask, render_template, request
import json, requests

app = Flask(__name__)

# Replace with your Google Places API key
GOOGLE_MAPS_API_KEY = 'API CODE'

@app.route('/')
def index():
    return render_template('index.html')

# Import the JSON module
import json

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
            places = data.get('results', [])

            return render_template('map.html', places=places, zip_code=zip_code, material=material, lat=lat, lng=lng, google_maps_api_key=GOOGLE_MAPS_API_KEY)
    
    return 'No recycling points found or an error occurred.'
