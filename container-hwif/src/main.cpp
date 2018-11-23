#include <Arduino.h>
#include <WiFiManager.h>
#include <Adafruit_VL53L0X.h>
#include <PubSubClient.h>

const char* mqtt_server = "broker.mqtt-dashboard.com";
const char* mqtt_topic = "awesome_bin";
const int sensor_id = 0;

Adafruit_VL53L0X sensor_tof;
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];

void callback(char* topic, byte* payload, unsigned int length);
void reconnect();

void setup()
{
  Serial.begin(115200);

  WiFiManager wifiManager;
  wifiManager.autoConnect("AwesomeContainer");

  pinMode(15, OUTPUT); digitalWrite(15, LOW); // sensor GND
  pinMode(27, OUTPUT); digitalWrite(27, HIGH); // sensor VIN

  sensor_tof.begin();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop()
{

  if (!client.connected())
  {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;

    VL53L0X_RangingMeasurementData_t measure;
    sensor_tof.rangingTest(&measure, true); // pass in 'true' to get debug data printout!

    snprintf (msg, 50, "%d_%ld_%d\n", sensor_id, measure.RangeMilliMeter, measure.RangeStatus);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish(mqtt_topic, msg);
  }

}