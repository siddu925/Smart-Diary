#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>

// DS18B20 Setup
#define ONE_WIRE_BUS 2 // Data wire is connected to GPIO2 (D4 on most ESP8266 boards)
OneWire oneWire(ONE_WIRE_BUS); // Setup oneWire instance
DallasTemperature sensors(&oneWire); // Pass oneWire reference to DallasTemperature

// pH Sensor Setup
float calibration_value = 21.34 - 0.7; // Calibration value for the pH sensor
int phval = 0; 
unsigned long int avgval; 
int buffer_arr[10], temp;
float ph_act;
float voltage;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("ESP8266 DS18B20 Temperature and pH Sensor");

  // Initialize sensors
  sensors.begin();
  Wire.begin();
}

void loop() {
  // Measure temperature
  sensors.requestTemperatures(); // Request temperature readings
  float temperature = sensors.getTempCByIndex(0); // Get temperature in Celsius7

  // Measure pH
  for (int i = 0; i < 10; i++) { 
    buffer_arr[i] = analogRead(A0); // Read analog input from pH sensor
    delay(30);
  }

  // Sort buffer array
  for (int i = 0; i < 9; i++) {
    for (int j = i + 1; j < 10; j++) {
      if (buffer_arr[i] > buffer_arr[j]) {
        temp = buffer_arr[i];
        buffer_arr[i] = buffer_arr[j];
        buffer_arr[j] = temp;
      }
    }
  }

  // Calculate average of the middle 6 values
  avgval = 0;
  for (int i = 2; i < 8; i++)
    avgval += buffer_arr[i];

  voltage = (float)avgval * 3.3 / 1024 / 6; 
  ph_act = -5.70 * voltage + calibration_value;

  // Display results
  Serial.print("Milk Temperature (C): ");
  Serial.println(temperature);

  // Serial.print("Voltage (V): ");
  // Serial.println(voltage, 3); // Display voltage with 3 decimal places

  Serial.print("Milk pH Value: ");
  Serial.println(ph_act);

  delay(1000); // Wait for 1 second before next reading
}
