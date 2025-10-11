# import serial
from dummyReader import DummyReader
import requests
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

API_URL = 'https://mypi-lf7.duckdns.org/'


def readUid(ser):
    line = ser.readline()
    if line:
        return line.decode('utf-8', errors='ignore').strip()
    return None


def postUid(uid):
    data = {'uid': uid}
    try:
        response = requests.post(API_URL, json=data)
        print(f"UID {uid} sent successfully (Status: {response.status_code})")
    except Exception as e:
        print(f"Failed to send UID: {e}")

def main():

    print("Starting RFID Attendance Service (Dummy Mode)...")

    reader = DummyReader()
    time.sleep(1)

    try:
        while True:
            line = reader.readline()
            if line:
                uid = line.decode('utf-8').strip()
                print(f"UID read: {uid}")
                postUid(uid)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        reader.close()
        print("Serial connection closed.")


if __name__ == "__main__":
    main()
