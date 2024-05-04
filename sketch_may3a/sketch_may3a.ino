#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#define BUZZER_PIN  18
// #include <Web

const char* ssid = "shayaan.....";
const char* password = "lightyagami";

WebServer server(80);
int objectCount = 0;
bool isExcess = false;
DynamicJsonDocument detectionData(200);

void handleRoot() {
  server.send(200, "text/plain", "Hello, world!");
  Serial.println("Root request handled");
}

void handleJson() {
  StaticJsonDocument<200> doc;
  doc["message"] = "Hello, world!";

  // Serialize the JSON object to a string
  String jsonString;
  serializeJson(doc, jsonString);

  // Send the JSON response
  server.send(200, "application/json", jsonString);
  Serial.println("JSON request handled");
}

void handleDetection() {
  // Check if the request has JSON data
  if (server.hasArg("plain")) {
    // Parse the JSON payload
    DeserializationError error = deserializeJson(detectionData, server.arg("plain"));

    // Check for parsing errors
    if (error) {
      server.send(400, "application/json", "{\"error\": \"Invalid JSON\"}");
      Serial.println("Error no valid json");
      return;
    }

    // Extract data from JSON payload specific to detection
    if (detectionData.containsKey("classes")) {
      objectCount = detectionData["count"].as<int>();
      Serial.println("Received detection data - classes:");
      for (const auto& item : detectionData["classes"].as<JsonArray>()) {
        Serial.println(item.as<String>()); // Printing each class
      }
      Serial.println("Object count: " + String(objectCount));
    }

    // Send a response
    server.send(200, "application/json", "{\"status\": \"detection received\"}");
    Serial.println("Detection request handled");
  } else {
    server.send(400, "application/json", "{\"error\": \"No JSON data received\"}");
    Serial.println("No JSON data received");
  }
}

void handleCount() {
  // Serialize the JSON document to a string
  String response;
  serializeJson(detectionData, response);
  
  // Send the response
  server.send(200, "application/json", response);
}



void handleExcess(){
  digitalWrite(BUZZER_PIN, HIGH); // Turn buzzer on
  delay(4000); // Change the delay to modify the buzz duration
  digitalWrite(BUZZER_PIN, LOW); // Turn buzzer off
  delay(500); // Change the delay to modify the interval between buzzes
  server.send(200, "application/json",  "{\"message\": \"Disturbance in the field\"}");
}

void handleDog(){

}

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/json", handleJson);
  server.on("/detect", HTTP_POST, handleDetection); // Handle detection POST requests
  server.on("/getcount", handleCount);
  server.on("/excess",  handleExcess);
  // server.on("/excessdog", handleDog);
  // server.on("/excesscat", handleCat);
  // server.on("/excesscow", handleCow);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
