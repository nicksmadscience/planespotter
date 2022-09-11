
#include <ESP8266WiFi.h>

#include <WiFiClient.h>
WiFiClient client;

    
#include <WiFiUdp.h>
#include "LedControl.h"

uint8_t data  = D1;
uint8_t clk = D3;
uint8_t load  = D2;
uint8_t piezo = D5;
uint8_t numberOfDevices = 6;

LedControl lc=LedControl(data,clk,load, numberOfDevices);

const char* ssid     = "marshmallowPrime";
const char* password = "marshmarsh6";

#define PACKET_LENGTH 33
WiFiUDP Udp;
unsigned int localUdpPort = 1234;
char incomingPacket[PACKET_LENGTH + 2];



  
void setup()
{
  Serial.begin(74800);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Udp.begin(localUdpPort);

  Serial.println("initializing max7219");

  for (uint8_t i = 0; i < numberOfDevices; i++)
  {
    lc.shutdown(i,false);
    lc.setIntensity(i,15);
    lc.clearDisplay(i);
    lc.setScanLimit(i, 7);
  }
  
  Serial.print("Device count: ");
  Serial.println(lc.getDeviceCount());

  pinMode(piezo, OUTPUT);
}


void loop()
{
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    
    int len = Udp.read(incomingPacket, PACKET_LENGTH);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }

    for (uint8_t addr = 0; addr < 4; addr++)
    {
      for (uint8_t col = 0; col < 8; col++)
      {
        for (uint8_t row = 0; row < 8; row++)
        {
          lc.setLed(3 - addr, row, col, bitRead(incomingPacket[(addr * 8) + col], row));
        }
      }
    }

//    for (uint8_t i = 0; i < numberOfDevices; i++)
//    {
//      lc.setIntensity(i,incomingPacket[32]);
//    }

    if (incomingPacket[32] > 128)
    {
      for (uint8_t i = 0; i < 3; i++)
      {
        digitalWrite(piezo, HIGH);
        delay(20);
        digitalWrite(piezo, LOW);
        delay(50);
      }
    }
  }

  
 

}
