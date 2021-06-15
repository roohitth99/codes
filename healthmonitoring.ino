#include "DHT.h"                   // Data ---> D3 VCC ---> 3V3 GND ---> GND
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
// WiFi parameters
#define WLAN_SSID       "name"
#define WLAN_PASS       "password"
// Adafruit IO
#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME  "username"
#define AIO_KEY       "key"
int pinDHT11=5;
int pinsoil=0;
#define DHTTYPE DHT11
WiFiClient client;
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
Adafruit_MQTT_Publish Temperature = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/temperature");
Adafruit_MQTT_Publish Humidity = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/humidity");
Adafruit_MQTT_Publish soil= Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/soil moisture");
Adafruit_MQTT_Publish heatindex= Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/feels like");
DHT dht(pinDHT11, DHTTYPE);
void setup() {
  Serial.begin(9600);
  pinMode(pinsoil,OUTPUT);
  Serial.println(F("Adafruit IO Example"));
  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  delay(10);
  Serial.print(F("Connecting to "));
  Serial.println(WLAN_SSID);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.println();
  Serial.println(F("WiFi connected"));
  Serial.println(F("IP address: "));
  Serial.println(WiFi.localIP());

  // connect to adafruit io
  connect();

}

// connect to adafruit io via MQTT
void connect() {
  Serial.print(F("Connecting to Adafruit IO... "));
  int8_t ret;
  while ((ret = mqtt.connect()) != 0) {
    switch (ret) {
      case 1: Serial.println(F("Wrong protocol")); break;
      case 2: Serial.println(F("ID rejected")); break;
      case 3: Serial.println(F("Server unavail")); break;
      case 4: Serial.println(F("Bad user/pass")); break;
      case 5: Serial.println(F("Not authed")); break;
      case 6: Serial.println(F("Failed to subscribe")); break;
      default: Serial.println(F("Connection failed")); break;
    }

    if(ret >= 0)
      mqtt.disconnect();

    Serial.println(F("Retrying connection..."));
    delay(10000);
  }
  Serial.println(F("Adafruit IO Connected!"));
}

void loop() {
  // ping adafruit io a few times to make sure we remain connected
  if(! mqtt.ping(3)) {
    // reconnect to adafruit io
    if(! mqtt.connected())
      connect();
  }
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);
  float s = analogRead(pinsoil);
  float content=map(s,1024,0,0,100);
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
    
  }

  // Compute heat index in Fahrenheit (the default)
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
  Serial.println("Air Temperature");
  Serial.print(t); Serial.println(" *C");
  Serial.println("Relative Humidity"); 
  Serial.print(h); Serial.println(" %");
  Serial.println("Moisture Content in the soil");
  Serial.print(content); Serial.println(" %");
  Serial.println("Feels like:");
  Serial.print(hic);Serial.println(" *C");
  delay(5000);
   if (! Temperature.publish(t)) {                     //Publish to Adafruit
      Serial.println(F("Temperature Failed"));
    } 
       if (! Humidity.publish(h)) {                     //Publish to Adafruit
      Serial.println(F("Humidity Failed"));
    }
    if (! soil.publish(s)) {                     //Publish to Adafruit
      Serial.println(F("Soil Failed"));
    }
    if (! heatindex.publish(hic)){
      Serial.println(F("Heat Index Failed"));
    }
    else {
      Serial.println(F("Sent!"));
    }
    delay(10000);
}
