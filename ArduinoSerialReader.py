
import serial
import time

# Configure the serial connection
serial_port = "/dev/cu.usbserial-57660175631"  # Replace with your port (e.g., COM3 on Windows)
baud_rate = 115200  # Should match the baud rate in your ESP8266 code
timeout = 1  # Timeout in seconds


def read_serial_data():
    try:
        # Initialize serial connection
        with serial.Serial(serial_port, baud_rate, timeout=timeout) as ser:
            print(f"Connected to {serial_port} at {baud_rate} baud.")

            # Give the ESP8266 time to reset
            time.sleep(2)

            print("Reading data from the serial monitor...\n")

            while True:
                # Read a line of data from the serial port
                line = ser.readline().decode('utf-8').strip()

                if line:  # Check if the line is not empty
                    print(line)

    except serial.SerialException as e:
        print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    read_serial_data()
