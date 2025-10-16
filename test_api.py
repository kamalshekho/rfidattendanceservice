import requests

API_URL = 'http://localhost:8080/mod/rfidattendance/api.php'
VERIFY_SSL = False

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
    test_uid = '33b6d836'
    test_courseid = 2
    test_userid = 3
    print(f"Testing with UID: {test_uid}, CourseID: {test_courseid}, UserID: {test_userid}")
    post_uid(test_uid, test_courseid, test_userid)

if __name__ == "__main__":
    main()