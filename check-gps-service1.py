import requests
import time
from datetime import datetime

# Function to calculate time difference in seconds
def calculate_time_difference(previous_time_str, current_time_str):
    fmt = '%Y-%m-%d %H:%M:%S'
    previous_time = datetime.strptime(previous_time_str, fmt)
    current_time = datetime.strptime(current_time_str, fmt)
    return (current_time - previous_time).total_seconds()

# Main function to check GPS service
def check_gps_service():
    previous_altitude = None
    previous_timestamp = None
    
    while True:
        try:
            # Query the GPS service
            response = requests.get('http://localhost:5000/gps')
            if response.status_code == 200:
                gps_data = response.json()
                current_altitude = gps_data["altitude"]
                current_timestamp = gps_data["lastFetch"]
                
                # Print the current altitude
                print(f"Current Altitude: {current_altitude:.2f} feet")

                if previous_altitude is not None and previous_timestamp is not None:
                    # Compare current and previous altitudes
                    altitude_difference = current_altitude - previous_altitude
                    
                    # Calculate time difference between the current and previous GPS fetch times
                    time_difference = calculate_time_difference(previous_timestamp, current_timestamp)
                    
                    if time_difference > 0:  # Avoid division by zero
                        # Calculate feet per second
                        feet_per_second = altitude_difference / time_difference
                        
                        # Determine if rising or falling
                        if feet_per_second > 0:
                            print(f"Rising at {feet_per_second:.2f} feet/second")
                        elif feet_per_second < 0:
                            print(f"Falling at {-feet_per_second:.2f} feet/second")
                        else:
                            print("No altitude change")
                
                # Update previous values for the next iteration
                previous_altitude = current_altitude
                previous_timestamp = current_timestamp

            else:
                print("Failed to retrieve GPS data")

            # Wait for 5 seconds before the next check
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to GPS service: {e}")
            break
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    check_gps_service()
    