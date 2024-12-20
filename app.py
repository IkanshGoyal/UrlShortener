from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

BITLY_API_KEY = os.getenv("BITLY_API_KEY")
BITLY_API_URL = "https://api-ssl.bitly.com/v4/shorten"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        long_url = request.form.get('long_url')
        if not long_url:
            return render_template('home.html', error="Please enter a valid URL.")

        headers = {"Authorization": f"Bearer {BITLY_API_KEY}"}
        data = {"long_url": long_url}
        response = requests.post(BITLY_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            short_url = response.json().get("link")
            return render_template('result.html', short_url=short_url)
        else:
            error_message = response.json().get("message", "An error occurred.")
            return render_template('home.html', error=f"Error: {error_message}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500