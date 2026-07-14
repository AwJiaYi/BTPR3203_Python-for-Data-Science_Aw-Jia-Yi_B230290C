import os
from datetime import datetime

river_stations = {
    'Sungai Klang KL': {'state': 'Selangor', 'wqi': 68.3, 'status': ''},
    'Sungai Muar':     {'state': 'Johor',    'wqi': 54.1, 'status': ''},
    'Sungai Pahang':   {'state': 'Pahang',   'wqi': 82.5, 'status': ''},
    'Sungai Kinabatangan': {'state': 'Sabah', 'wqi': 95.0, 'status': ''}
}

reading_log = []

def get_class_status(wqi):
    """Converts a WQI value into the correct class label."""
    if wqi > 92.7:
        return "Class I (Clean)"
    elif 76.5 < wqi <= 92.7:
        return "Class II (Slightly Polluted)"
    elif 51.9 < wqi <= 76.5:
        return "Class III (Moderately Polluted)"
    elif 31.0 < wqi <= 51.9:
        return "Class IV (Polluted)"
    else:
        return "Class V (Heavily Polluted)"

def classify_all_stations():
    """Iterates through all entries, updates status, and prints a formatted table."""
    print("\n--- River Quality Classification ---")
    print(f"{'Station Name':<25} | {'State':<15} | {'WQI':<6} | {'Status'}")
    print("-" * 80)
    
    for station, data in river_stations.items():
        data['status'] = get_class_status(data['wqi'])
        print(f"{station:<25} | {data['state']:<15} | {data['wqi']:<6.1f} | {data['status']}")
    print("-" * 80)

def add_update_station():
    """Prompts user to add or update a station and re-classifies."""
    print("\n--- Add / Update Station ---")
    name = input("Enter station name: ").strip()
 
    while True:
        try:
            wqi = float(input("Enter WQI value (0-100): "))
            if 0 <= wqi <= 100:
                break
            else:
                print("Error: WQI value must be between 0 and 100.")
        except ValueError:
            print("Error: Please enter a valid numeric value for WQI.")

    if name in river_stations:
        river_stations[name]['wqi'] = wqi
        print(f"Station '{name}' updated with new WQI: {wqi}")
    else:
        state = input("Enter state: ").strip()
        river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
        print(f"New station '{name}' added.")
    
    for stat, data in river_stations.items():
        data['status'] = get_class_status(data['wqi'])

def log_monitoring_reading():
    """Logs a new reading, checks for alerts, and prints history."""
    print("\n--- Log Monitoring Reading ---")
    name = input("Enter station name to log: ").strip()
    
    if name not in river_stations:
        print(f"Error: Station '{name}' not found.")
        return

    while True:
        try:
            wqi = float(input("Enter WQI reading (0-100): "))
            if 0 <= wqi <= 100:
                break
            else:
                print("Error: WQI value must be between 0 and 100.")
        except ValueError:
            print("Error: Please enter a valid numeric value for WQI.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reading_log.append((timestamp, name, wqi))
    river_stations[name]['wqi'] = wqi
    river_stations[name]['status'] = get_class_status(wqi)
    print(f"Reading logged successfully for {name}.")
    print("\n--- Alert Check ---")
    alerts = False
    for stat, data in river_stations.items():
        if data['wqi'] <= 51.9:
            print(f"[!] ALERT: {stat} in {data['state']} is {data['status']} (WQI: {data['wqi']}).")
            alerts = True
    
    if not alerts:
        print("All monitored rivers are within acceptable quality levels.")

    print("\n--- Reading Log History ---")
    if not reading_log:
        print("No readings have been logged yet.")
    else:
        for entry in reading_log:
            print(f"[{entry[0]}] Station: {entry[1]:<20} | WQI: {entry[2]:<5.1f}")

class RiverStation:
    def __init__(self, name, state, wqi):
        self.name = name
        self.state = state
        self.wqi = wqi
        
    def get_class_label(self):
        return get_class_status(self.wqi)
        
    def print_summary(self):
        print(f"{self.name} | {self.state} | WQI: {self.wqi} | {self.get_class_label()}")

def trend_analysis():
    print("\n--- Trend Analysis ---")
    print("\n[RiverStation Class Instances]")
    stations_list = list(river_stations.keys())
    if len(stations_list) >= 2:
        s1_name = stations_list[0]
        s2_name = stations_list[1]
        rs1 = RiverStation(s1_name, river_stations[s1_name]['state'], river_stations[s1_name]['wqi'])
        rs2 = RiverStation(s2_name, river_stations[s2_name]['state'], river_stations[s2_name]['wqi'])
        rs1.print_summary()
        rs2.print_summary()
        
    print("\n[Average WQI by State]")
    state_totals = {}
    state_counts = {}
    for data in river_stations.values():
        state = data['state']
        state_totals[state] = state_totals.get(state, 0) + data['wqi']
        state_counts[state] = state_counts.get(state, 0) + 1
        
    state_averages = {state: state_totals[state]/state_counts[state] for state in state_totals}
    sorted_states = sorted(state_averages.items(), key=lambda x: x[1], reverse=True)
    for state, avg in sorted_states:
        print(f"{state:<15}: {avg:.1f} WQI")

    print("\n[Improvement & Decline Analysis]")
    station_readings = {}
    for ts, name, wqi in reading_log:
        if name not in station_readings:
            station_readings[name] = []
        station_readings[name].append((ts, wqi))

    trend_data = {}
    for name, readings in station_readings.items():
        if len(readings) >= 2:
            readings.sort(key=lambda x: x[0]) 
            improvement = readings[-1][1] - readings[0][1]
            trend_data[name] = improvement

    if not trend_data:
        print("Insufficient data for trend analysis. Please log more readings.")
    else:
        best_station = max(trend_data, key=trend_data.get)
        worst_station = min(trend_data, key=trend_data.get)
        print(f"Greatest Improvement: {best_station} ({trend_data[best_station]:+.1f} WQI)")
        print(f"Least Improvement/Greatest Decline: {worst_station} ({trend_data[worst_station]:+.1f} WQI)")

    print("\n[Class Distribution Summary]")
    class_counts = {"Class I": 0, "Class II": 0, "Class III": 0, "Class IV": 0, "Class V": 0}
    
    for data in river_stations.values():
        status = data['status']
        if "Class I " in status or status.startswith("Class I("): class_counts["Class I"] += 1
        elif "Class II " in status or status.startswith("Class II("): class_counts["Class II"] += 1
        elif "Class III " in status or status.startswith("Class III("): class_counts["Class III"] += 1
        elif "Class IV " in status or status.startswith("Class IV("): class_counts["Class IV"] += 1
        elif "Class V " in status or status.startswith("Class V("): class_counts["Class V"] += 1

    for cls, count in class_counts.items():
        print(f"{cls:<10}: {count} station(s)")

def export_report():
    """Writes the current contents of river_stations to a text file."""
    filename = "river_report.txt"
    try:
        with open(filename, 'w') as file:
            for name, data in river_stations.items():
                status = data['status'] if data['status'] else get_class_status(data['wqi'])
                file.write(f"{name},{data['state']},{data['wqi']},{status}\n")
        print(f"\nSuccess: Data exported successfully to {filename}.")
    except PermissionError:
        print("\nError: Permission denied. Cannot write to the file.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def load_report():
    """Reads a text file and repopulates river_stations."""
    filename = input("\nEnter filename to load (e.g., river_report.txt): ").strip()
    try:
        with open(filename, 'r') as file:
            river_stations.clear() 
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    state = parts[1].strip()
                    wqi = float(parts[2].strip())
                    river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
        
        print("\nSuccess: Data loaded successfully.")
        classify_all_stations()
        
    except FileNotFoundError:
        print(f"\nError: The file '{filename}' does not exist.")
    except ValueError:
        print("\nError: File contains invalid (non-numeric) WQI data.")
    except PermissionError:
        print("\nError: Permission denied. Cannot read the file.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def main():
    for stat, data in river_stations.items():
        data['status'] = get_class_status(data['wqi'])

    while True:
        print("\n======= Main Menu =======")
        print("1. Classify All Stations")
        print("2. Add / Update Station")
        print("3. Log Monitoring Reading")
        print("4. Trend Analysis")
        print("5. Export Report")
        print("6. Load Report")
        print("0. Exit")
        print("=========================")
        
        choice = input("Select an option (0-6): ").strip()
        
        if choice == '1':
            classify_all_stations()
        elif choice == '2':
            add_update_station()
        elif choice == '3':
            log_monitoring_reading()
        elif choice == '4':
            trend_analysis()
        elif choice == '5':
            export_report()
        elif choice == '6':
            load_report()
        elif choice == '0':
            print("Exiting River Quality Monitoring System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 0 to 6.")

if __name__ == "__main__":
    main()