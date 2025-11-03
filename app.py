from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Simulated book database (RFID scanned books)
book_db = {
    "BOOK001": {"location": "Shelf A1", "timestamp": "2025-11-03T18:45:00"},
    "BOOK002": {"location": "Shelf B2", "timestamp": "2025-11-03T18:47:30"},
    "BOOK003": {"location": "Shelf C3", "timestamp": "2025-11-03T18:50:15"},
}

# RSSI-to-location mapping
def estimate_location_from_rssi(rssi):
    if rssi <= -80:
        return "Shelf C3"
    elif rssi <= -65:
        return "Shelf B2"
    else:
        return "Shelf A1"

@app.route('/search')
def search_book():
    tag_id = request.args.get("tag_id")
    rssi = random.randint(-90, -30)
    timestamp = datetime.now().isoformat()

    if tag_id in book_db:
        return jsonify({
            "found": True,
            "tag_id": tag_id,
            "location": book_db[tag_id]["location"],
            "timestamp": book_db[tag_id]["timestamp"],
            "rssi": rssi
        })
    else:
        # BLE fallback: simulate location even if RFID not scanned
        location = estimate_location_from_rssi(rssi)
        return jsonify({
            "found": False,
            "tag_id": tag_id,
            "location": location,
            "timestamp": timestamp,
            "rssi": rssi
        })

if __name__ == '__main__':
    app.run()
