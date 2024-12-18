import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from EDA import ExploratoryDataAnalysis
import serial
import time
from datetime import datetime
# Configure the serial connection
serial_port = "COM3"  # Replace with your port (e.g., COM3 on Windows)
baud_rate = 115200  # Should match the baud rate in your ESP8266 code
timeout = 1  # Timeout in seconds


st.title("SMART IOT-BASED MILK QUALITY MANAGEMENT SYSTEM: REAL-TIME MONITORING OF PH AND TEMPERATURE")
st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: {"#d2e8fd"};
            color: {"#dd6565"};
        }}
        </style>
        """,
        unsafe_allow_html=True)



# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.session_state["readings"] = {"temperature": [], "pH": []}


def read_serial_data():
    last_reading = None  # To track the last valid reading
    try:
        with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
            st.info(f"Connected to {serial_port} at {baud_rate} baud.")
            time.sleep(1)  # Allow time for the device to reset
            st.info("Reading data from the serial monitor...")

            while len(st.session_state["readings"]["temperature"]) < 10:
                raw_line = ser.readline()
                try:
                    # Decode the data
                    line = raw_line.decode('utf-8', errors='replace').strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Check for temperature and pH data
                    if "Milk Temperature" in line:
                        temp = float(line.split(':')[1].strip().split()[0])  # Extract temperature value
                        st.session_state["readings"]["temperature"].append(temp)

                    elif "Milk pH Value" in line:
                        ph = float(line.split(':')[1].strip())  # Extract pH value
                        st.session_state["readings"]["pH"].append(ph)

                        # Avoid duplicate readings
                        current_reading = (st.session_state["readings"]["temperature"][-1], ph)
                        if current_reading == last_reading:
                            st.session_state["readings"]["temperature"].pop()  # Remove the duplicate temperature
                            st.session_state["readings"]["pH"].pop()  # Remove the duplicate pH
                            continue
                        last_reading = current_reading

                        st.write(f"Reading: {line}")  # Display the valid pH reading

                    # Stop after 10 readings
                    if len(st.session_state["readings"]["temperature"]) == 10 and len(st.session_state["readings"]["pH"]) == 10:
                        break

                except Exception as e:
                    st.warning(f"Error parsing line: {line}. Skipping...")
                    continue

            # Calculate and display averages
            temp_avg = sum(st.session_state["readings"]["temperature"]) / len(st.session_state["readings"]["temperature"])
            ph_avg = sum(st.session_state["readings"]["pH"]) / len(st.session_state["readings"]["pH"])
            st.success(f"Average Temperature: {temp_avg:.2f}°C")
            st.success(f"Average pH: {ph_avg:.2f}")

            # Save data to CSV
            save_user_data_to_csv(st.session_state["user"], temp_avg, ph_avg)

    except serial.SerialException as e:
        st.error(f"Serial error: {e}")



import pandas as pd
import os
from datetime import datetime
import streamlit as st


import pandas as pd
import os
from datetime import datetime
import streamlit as st

def save_user_data_to_csv(user, avgph, avgtemp):
    # Current date and time
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare the data in the specified format
    data = {
        "ID": user[0],
        "Name": user[1],
        "Farm Name": user[2],
        "Breed": user[3],
        "Place": user[4],
        "Phone Number": user[5],
        "Distance from Farm": user[7],
        "date and time": date_time,
        "avgph": avgph,
        "avgtemp": avgtemp
    }

    # Convert the data to a DataFrame
    df = pd.DataFrame([data])

    # File path for the CSV file
    file_path = 'Final_milk_management_users.csv'

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing file
        existing_df = pd.read_csv(file_path)

        # Combine new data with existing data and remove duplicates
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df = updated_df.drop_duplicates(subset=["ID", "Name", "date and time"], keep='last')
    else:
        # If the file doesn't exist, use the new DataFrame
        updated_df = df

    # Save the updated DataFrame to the CSV file
    try:
        updated_df.to_csv(file_path, index=False)
        st.success(f"Data successfully saved to {file_path}.")
    except Exception as e:
        st.error(f"Error saving data: {e}")



# st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-color: {"#56c6e2"};
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
# )
st.image("Image/coverpage.png")
import streamlit as st

st.sidebar.title("MILK QUALITY TESTING")
st.sidebar.image("Image/s2.jpg")
st.sidebar.markdown("""
## Technical Details
### 1. IoT Sensors
- **Temperature Sensor:** Measures milk temperature with high accuracy.
- **pH Sensor:** Detects changes in pH to identify spoilage or contamination.

### 2. Microcontroller
- Utilizes an Arduino or Raspberry Pi for processing sensor data and transmitting it to the cloud.

### 3. Communication Protocol
- Data is sent to the cloud via Wi-Fi, LoRaWAN, or GSM for reliable connectivity in various environments.

### 4. Cloud Platform
- Stores and processes data using platforms like AWS IoT, Google Cloud IoT, or Azure IoT Hub.

### 5. User Interface
- A web-based dashboard provides a user-friendly interface for visualizing data and configuring alerts.
- Mobile applications available for Android and iOS for on-the-go monitoring.

---
""")
st.markdown("""

## Introduction
The dairy industry faces significant challenges in maintaining milk quality during storage and transportation. Milk is a perishable product, and its quality is influenced by factors such as temperature, pH, and microbial activity. To address these challenges, this project introduces a **Smart IoT-Based Milk Quality Management System** that leverages the power of IoT devices to provide real-time monitoring of pH and temperature.

This system is designed to ensure milk quality and safety by enabling dairy farmers, milk processors, and distributors to track critical parameters remotely. By utilizing IoT sensors and cloud-based analytics, the system offers actionable insights to optimize milk storage conditions and reduce spoilage.

---

## Features of the System
1. **Real-Time Monitoring:**
   - Continuous tracking of milk temperature and pH levels using advanced IoT sensors.
   - Immediate detection of deviations from optimal conditions.

2. **Cloud Integration:**
   - Data collected from sensors is transmitted to a cloud server for storage and analysis.
   - Accessible via a web-based dashboard and mobile application.

3. **Alerts and Notifications:**
   - Instant alerts sent via SMS or email when parameters exceed safe thresholds.
   - Prevents delays in corrective actions.

4. **Data Analytics and Reporting:**
   - Visualize historical data trends for informed decision-making.
   - Download detailed reports for quality assurance and compliance purposes.

5. **Remote Accessibility:**
   - Monitor milk quality from anywhere using a secure online portal.
   - Supports multi-user access for large-scale operations.

6. **Energy Efficiency:**
   - Low-power IoT devices ensure sustainable and cost-effective operations.
   - Designed to operate in both urban and rural settings.

---

## Use Cases
### 1. Dairy Farms
- Ensure the health of milk directly from the source by tracking pH and temperature in real-time.
- Identify issues such as mastitis in cattle, which can alter milk pH.

### 2. Milk Transportation
- Monitor conditions during transit to ensure milk quality remains intact.
- Alert drivers and logistics teams about potential issues.

### 3. Processing Plants
- Validate milk quality before processing to prevent contamination.
- Automate quality checks and integrate data into production workflows.

### 4. Retail and Distribution
- Assure customers of milk quality by maintaining consistent storage conditions.
- Enhance trust and satisfaction with verifiable quality data.

---

## Benefits of the System
### 1. Improved Milk Safety
- Real-time alerts allow for immediate action, reducing the risk of spoiled or contaminated milk.

### 2. Reduced Waste
- Proactively address issues before milk quality deteriorates, minimizing waste and loss.

### 3. Enhanced Operational Efficiency
- Automate quality monitoring tasks, saving time and labor costs.

### 4. Better Decision-Making
- Leverage historical data trends for strategic improvements in milk storage and transportation.

### 5. Scalability
- The system can be scaled to handle operations of all sizes, from small dairy farms to large processing plants.

---



## Future Enhancements
1. **Machine Learning Integration:**
   - Predict potential spoilage using AI models trained on historical data.
   - Optimize storage and transportation conditions dynamically.

2. **Blockchain for Traceability:**
   - Use blockchain to create a tamper-proof record of milk quality data.
   - Enhance transparency and trust in the dairy supply chain.

3. **Multi-Parameter Monitoring:**
   - Expand the system to monitor additional parameters like microbial activity, fat content, and lactose levels.

4. **IoT Edge Computing:**
   - Process data locally on IoT devices for faster alerts and reduced cloud dependency.

---

## Conclusion
The **Smart IoT-Based Milk Quality Management System** represents a significant leap forward in ensuring milk quality and safety. By leveraging IoT technology, this system empowers stakeholders across the dairy supply chain to maintain the highest standards of quality, reduce waste, and enhance efficiency.

Whether you are a small-scale farmer or a large dairy processor, this system is designed to meet your needs and help you deliver the best quality milk to consumers. With real-time monitoring, actionable insights, and scalable architecture, the future of dairy quality management is here.

---
""")

# SQLite Database Connection
conn = sqlite3.connect('milk_management.db', check_same_thread=False)
c = conn.cursor()

# Hashing password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Create users table
def create_users_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    farm_name TEXT,
                    breed TEXT,
                    place TEXT,
                    phone_number TEXT,
                    password TEXT,
                    distance_from_farm TEXT)''')
    conn.commit()

# Insert new user
def add_user(name, farm_name, breed, place, phone_number, password, distance_from_farm):
    c.execute('''INSERT INTO users (name, farm_name, breed, place, phone_number, password, distance_from_farm) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (name, farm_name, breed, place, phone_number, password, distance_from_farm))
    conn.commit()
    save_to_csv()

# Save database content to CSV
def save_to_csv():
    c.execute('SELECT id, name, farm_name, breed, place, phone_number, distance_from_farm FROM users')
    data = c.fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Farm Name", "Breed", "Place", "Phone Number", "Distance from Farm"])
    df.to_csv('milk_management_users.csv', index=False)

# Authenticate user
def authenticate_user(name, password):
    hashed_password = hash_password(password)
    c.execute('SELECT * FROM users WHERE name = ? AND password = ?', (name, hashed_password))
    return c.fetchone()

# Fetch user details
def get_user_details(name):
    c.execute('SELECT * FROM users WHERE name = ?', (name,))
    return c.fetchone()

def evaluate_risk_and_recommendation(temp_avg, ph_avg):
    """
    Evaluate the risk level and provide a detailed recommendation for milk usage
    based on average temperature and pH.
    """
    risk = ""
    recommendation = ""

    # Define thresholds for risk evaluation and detailed recommendations
    if temp_avg > 4.0 and ph_avg < 6.4:
        risk = "High Risk"
        recommendation = (
            "The milk has a high risk of spoilage and microbial contamination due to elevated temperature and low pH. "
            "Such milk is not safe for human consumption. It is recommended to discard the milk or repurpose it "
            "for non-food industrial processes, such as fertilizer production or biogas generation."
        )
    elif 4.0 <= temp_avg <= 10.0 and 6.4 <= ph_avg <= 6.8:
        risk = "Moderate Risk"
        recommendation = (
            "The milk is at a moderate risk of spoilage. While it may still be consumable, it requires immediate "
            "pasteurization to eliminate harmful bacteria and extend shelf life. It is suitable for making processed dairy products, "
            "such as cheese or yogurt, after pasteurization."
        )
    elif temp_avg < 4.0 and 6.5 <= ph_avg <= 6.8:
        risk = "Low Risk"
        recommendation = (
            "The milk is in optimal condition with low risk of spoilage. It is safe for direct human consumption and can be used "
            "for producing high-quality dairy products like fresh milk, cream, and butter. Ensure the milk is stored in a "
            "refrigerated environment to maintain its quality."
        )
    else:
        risk = "Unknown Risk"
        recommendation = (
            "The milk does not meet standard quality parameters or falls outside the acceptable thresholds for pH and temperature. "
            "Further laboratory testing is required to assess its suitability for any type of usage. "
            "Do not use this milk for any purpose until further testing is completed."
        )

    return risk, recommendation

# Streamlit UI
create_users_table()

# Page configuration
st.title("Milk Management System")

# Navigation options
menu = st.sidebar.selectbox("Menu", ["Register", "Login", "Admin"])

if menu == "Register":
    st.header("Register New User")
    name = st.text_input("Name")
    farm_name = st.text_input("Farm Name")
    breed = st.text_input("Breed of Cattle")
    place = st.text_input("Place")
    phone_number = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    distance_from_farm = st.text_input("Distance from Farm (in km)")

    if st.button("Register"):
        if name and farm_name and breed and place and phone_number and password and distance_from_farm:
            hashed_password = hash_password(password)
            add_user(name, farm_name, breed, place, phone_number, hashed_password, distance_from_farm)
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Please fill all the fields.")

# Login functionality
elif menu == "Login":
    st.header("Login")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(name, password)
        if user:
            st.success(f"Welcome, {user[1]}!")
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
        else:
            st.error("Invalid credentials. Please try again.")

if st.session_state["logged_in"]:
    user = st.session_state["user"]
    st.subheader("User Details")
    st.write(f"**Name:** {user[1]}")
    st.write(f"**Farm Name:** {user[2]}")
    st.write(f"**Breed of Cattle:** {user[3]}")
    st.write(f"**Place:** {user[4]}")
    st.write(f"**Phone Number:** {user[5]}")
    st.write(f"**Distance from Farm:** {user[7]} km")
    st.image("Image/ph.png")

    # Button to start reading serial data
    if st.button("Start Reading Milk Data"):
        read_serial_data()

    # Calculate and display averages
    if len(st.session_state["readings"]["temperature"]) == 10:
        temp_avg = sum(st.session_state["readings"]["temperature"]) / 10
        ph_avg = sum(st.session_state["readings"]["pH"]) / 10

        # st.write(f"Average pH: {ph_avg:.2f}")
        # st.write(f"Average Temperature: {temp_avg:.2f}")

        # Save data to CSV
        # save_user_data_to_csv(user, temp_avg, ph_avg)

        # Reset readings
        st.session_state["readings"] = {"temperature": [], "pH": []}

        # Evaluate risk and recommendation
        risk, recommendation = evaluate_risk_and_recommendation(temp_avg, ph_avg)

        # Display risk and recommendation
        st.warning(f"**Risk Level:** {risk}")
        st.info(f"**Recommendation:** {recommendation}")

        # Save data to CSV
        save_user_data_to_csv(user, temp_avg, ph_avg)

        # Reset readings
        st.session_state["readings"] = {"temperature": [], "pH": []}

elif menu == "Admin":
    data_paths = {
        "MILK Quality": "Final_milk_management_users.csv",
        "USERS": "milk_management_users.csv"
    }
    eda = ExploratoryDataAnalysis(data_paths)
    eda.run()