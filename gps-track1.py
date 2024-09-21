import gps
import time

# Function to convert meters to feet
def meters_to_feet(meters):
    return meters * 3.28084

# Initialize GPS session
session = gps.gps(mode=gps.WATCH_ENABLE)

# Store the previous altitude in feet
previous_altitude_feet = None

while True:
    try:
        # Get the next GPS report
        report = session.next()

        # Check if the GPS report contains altitude data
        if hasattr(report, 'altMSL'):
            current_altitude_meters = report.altMSL
            current_altitude_feet = meters_to_feet(current_altitude_meters)

            # Print the current coordinates and altitude
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                print(f"Latitude: {report.lat}, Longitude: {report.lon}, Altitude: {current_altitude_feet:.2f} feet")

            # Compare with the previous altitude
            if previous_altitude_feet is not None:
                altitude_difference = current_altitude_feet - previous_altitude_feet
                if altitude_difference > 0:
                    print(f"Rose {altitude_difference:.2f} feet")
                elif altitude_difference < 0:
                    print(f"Fell {-altitude_difference:.2f} feet")
                else:
                    print("Altitude unchanged")
            
            # Update previous altitude
            previous_altitude_feet = current_altitude_feet

        # Wait for 3 seconds before the next reading
        time.sleep(3)

    except KeyError:
        # In case of missing data, skip to the next report
        pass
    except KeyboardInterrupt:
        print("Stopping GPS script.")
        break
    except StopIteration:
        session = None
        print("GPSD has terminated.")