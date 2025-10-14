# import serial
import requests
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
API_URL = 'http://localhost:8080/mod/rfidattendance/api.php'
VERIFY_SSL = True

def readUid(ser):
    try:
        line = ser.readline()
        if line:
            return line.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        print(f"Error reading UID: {e}")
    return None

def postUid(uid):
    data = {
    'uid': uid,
    'courseid': 1,  
    'userid': 3     
}
    try:
        response = requests.post(API_URL, json=data, verify=VERIFY_SSL)
        if response.ok:
            print(f"UID {uid} sent successfully (Status: {response.status_code})")
        else:
            print(f"Server error: Status {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"Failed to send UID: {e}")

def main():
    print("Starting RFID Attendance Service")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        print("Check available ports with: ls /dev/tty*")
        return

    time.sleep(2)
    print(f"Connected to {SERIAL_PORT} @ {BAUD_RATE} baud")

    try:
        while True:
            uid = readUid(ser)
            if uid:
                print(f"UID read: {uid}")
                postUid(uid)
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        ser.close()
        print("Serial connection closed")

if __name__ == "__main__":
    main()
