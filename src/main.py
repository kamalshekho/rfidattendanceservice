import serial
import requests
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
API_URL = 'http://localhost:8080/mod/rfidattendance/api.php'
VERIFY_SSL = False

def read_uid(ser):
    try:
        line = ser.readline()
        if not line:
            return None, None, None
        parts = line.decode('utf-8', errors='ignore').strip().split(',')
        if len(parts) != 3:
            return None, None, None
        return parts[0].strip(), int(parts[1]), int(parts[2])
    except:
        return None, None, None

def post_uid(uid, courseid, userid):
    data = {'uid': uid, 'courseid': courseid, 'userid': userid}
    try:
        response = requests.post(API_URL, json=data, verify=VERIFY_SSL)
        if response.ok:
            print(f"UID {uid} sent successfully (Status {response.status_code})")
            print(f"Server response: {response.text}")
        else:
            print(f"Server error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to send UID: {e}")

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    time.sleep(1)

    try:
        while True:
            uid, courseid, userid = read_uid(ser)
            if uid and courseid and userid:
                print(f"Read: UID={uid}, CourseID={courseid}, UserID={userid}")
                post_uid(uid, courseid, userid)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
