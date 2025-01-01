from flask import Flask, jsonify, Response
import requests
from datetime import datetime

app = Flask(__name__)

# Constants
BING_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"


def fetch_image():
    """
    Fetch the latest Bing image URL.
    """
    print(f"{datetime.now()} - Fetching the latest Bing image...")
    try:
        # Simulate network errors
        #if os.environ.get("SIMULATE_NETWORK_ERROR") == "1":
        #    raise requests.exceptions.ConnectionError("Simulated network error")

        # Fetch the Bing JSON
        response = requests.get(BING_URL)
        response.raise_for_status()

        # Simulate unexpected JSON structure
        #if os.environ.get("SIMULATE_BAD_JSON") == "1":
        #    return None  # No 'images' key to process

        # Parse JSON and extract image URL
        data = response.json()
        if 'images' not in data or len(data['images']) == 0:
            print("Error: Could not fetch image data from Bing.")
            return None

        image_url = "https://www.bing.com" + data['images'][0]['url']
        return image_url

    except requests.exceptions.ConnectionError as e:
        print(f"Network error: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except ValueError as e:
        print(f"JSON parsing error: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")

    return None


@app.route("/")
def home():
    """
    Fetch the latest Bing image URL and return it as a response.
    """
    image_url = fetch_image()
    if image_url:
        # Redirect to the image URL
        return Response(status=302, headers={"Location": image_url})
    else:
        # Return a blank response with a 200 status code
        return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)