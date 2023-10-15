from flask import Flask, render_template, request
import urllib.parse
import os

os.environ['GOOGLE_MAPS_API_KEY'] = 'AIzaSyDu-0LziMypXD4KGf0Q0lkid57Yj7KYxHo'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        location = request.args['location']
        encoded_location = urllib.parse.quote(location)
        return render_template('results.html', location=location, encoded_location=encoded_location)

if __name__ == '__main__':
    app.run(debug=True)