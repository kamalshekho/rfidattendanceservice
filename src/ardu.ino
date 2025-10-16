#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

// LED Pins
#define LED_GREEN 5
#define LED_YELLOW 6
#define LED_BLUE 4

// Buzzer Pin
#define BUZZER 7

// Sector 1 Key B works (FFFFFFFFFFFF)
const byte KEY_FF[6] = { 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF };

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  Serial.println("RFID-Scanner gestartet...");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  // UID
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();

  // Read payload from sector 1 (blocks 4–6)
  String payload = readPayloadSector1();

  // Parse values
  int courseId = -1, userId = -1;
  parseCourseUser(payload, courseId, userId);

  // Send only the comma-separated line to the Pi
  Serial.print(uid);
  Serial.print(",");
  Serial.print(courseId);
  Serial.print(",");
  Serial.println(userId);

  // Wait for Pi response (feedback)
  digitalWrite(LED_BLUE, HIGH);
  unsigned long start = millis();
  String response = "";
  while (millis() - start < 5000) {
    if (Serial.available()) {
      char c = Serial.read();
      response += c;
      if (response.indexOf("Successfully") != -1) {
        handleSuccess();
        break;
      } else if (response.indexOf("DENY") != -1 || response.indexOf("Error") != -1) {
        handleFailure();
        break;
      }
    }
  }
  if (response.indexOf("Successfully") == -1 &&
      response.indexOf("DENY") == -1 &&
      response.indexOf("Error") == -1) {
    handleFailure();
  }

  digitalWrite(LED_BLUE, LOW);
  while (mfrc522.PICC_IsNewCardPresent() || mfrc522.PICC_ReadCardSerial());
  delay(500);
}

/* --- Core logic --- */

String readPayloadSector1() {
  MFRC522::MIFARE_Key key;
  memcpy(key.keyByte, KEY_FF, 6);

  const byte firstBlock = 4, lastDataBlock = 6;
  String result = "";

  MFRC522::StatusCode status =
    mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_B,
                             firstBlock, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    mfrc522.PICC_HaltA(); mfrc522.PCD_StopCrypto1();
    return "";
  }

  for (byte block = firstBlock; block <= lastDataBlock; block++) {
    byte buffer[18]; byte size = sizeof(buffer);
    status = mfrc522.MIFARE_Read(block, buffer, &size);
    if (status != MFRC522::STATUS_OK) continue;

    for (int i = 0; i < 16; i++) {
      char c = (char)buffer[i];
      if (isPrintable(c)) result += c;
    }
  }

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  // Extract payload starting from "courseid"
  int idx = result.indexOf("courseid");
  if (idx >= 0) result = result.substring(idx);
  result.trim();
  return result;
}

void parseCourseUser(const String &s, int &courseId, int &userId) {
  courseId = -1; userId = -1;
  if (!s.length()) return;

  int i = s.indexOf("courseid");
  if (i >= 0) {
    int eq = s.indexOf('=', i);
    if (eq >= 0) courseId = s.substring(eq + 1).toInt();
  }

  i = s.indexOf("userid");
  if (i >= 0) {
    int eq = s.indexOf('=', i);
    if (eq >= 0) userId = s.substring(eq + 1).toInt();
  }
}

/* --- Feedback --- */

void handleSuccess() {
  digitalWrite(LED_BLUE, LOW);
  tone(BUZZER, 1000, 200);
  delay(200);
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_GREEN, HIGH); delay(300);
    digitalWrite(LED_GREEN, LOW); delay(300);
  }
}

void handleFailure() {
  digitalWrite(LED_BLUE, LOW);
  digitalWrite(LED_YELLOW, HIGH);
  delay(3000);
  digitalWrite(LED_YELLOW, LOW);
}
