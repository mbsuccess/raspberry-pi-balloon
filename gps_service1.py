from flask import Flask, jsonify
import gps
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Store GPS data globally
gps_data = {
    "latitude": None,
    "longitude": None,
    "altitude": None,
    "lastFetch": None
}

# Function to update GPS data
def update_gps_data():
    global gps_data
    session = gps.gps(mode=gps.WATCH_ENABLE)
    
    while True:
        try:
            report = session.next()
            
            # Update GPS data if available
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                gps_data["latitude"] = report.lat
                gps_data["longitude"] = report.lon
            if hasattr(report, 'altMSL'):
                gps_data["altitude"] = report.altMSL

            # Update the last fetch timestamp
            gps_data["lastFetch"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        except KeyError:
            pass
        except StopIteration:
            session = None
            print("GPSD has terminated.")
            break
        time.sleep(1)

# Background thread to continuously fetch GPS data
def start_gps_thread():
    gps_thread = threading.Thread(target=update_gps_data)
    gps_thread.daemon = True
    gps_thread.start()

# API endpoint to get the current GPS data
@app.route('/gps', methods=['GET'])
def get_gps_data():
    return jsonify(gps_data)

# Start the GPS data fetching thread before the server runs
if __name__ == "__main__":
    start_gps_thread()
    app.run(host='0.0.0.0', port=5000)