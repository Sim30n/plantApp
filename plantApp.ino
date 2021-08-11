// First we include the libraries
#include "DHT.h"


#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define DHTPIN 4    // modify to the pin we connected
#define DHTTYPE DHT21   // AM2301 
#define RELAY1 5
#define RELAY2 6
#define SOIL 8
#define WLEVEL 10


DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(WLEVEL, INPUT);
  pinMode(SOIL, OUTPUT);
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  dht.begin();

  digitalWrite(RELAY2, HIGH); // Switch off the water pump
}
void loop() {
      

    int distance;

    distance = ultrasonic_distance();

    //Serial.println(distance);
    read_temp_hum();
    //control_relay(2, 0);
    //delay(5000);
    //control_relay(2, 1);
    read_light();
    read_wlevel();
    read_soil();
    
}

int ultrasonic_distance(){
    // defines variables
    long duration; // variable for the duration of sound wave travel
    int distance; // variable for the distance measurement
    // Clears the trigPin condition
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance, return cm
    distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back) 
    return distance;
}


void read_temp_hum(){
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    // check if returns are valid, if they are NaN (not a number) then something went wrong!
    if (isnan(t) || isnan(h)) 
    {
        Serial.println("Failed to read from DHT");
    } 
    else 
    {
        Serial.print("Humidity: "); 
        Serial.print(h);
        Serial.print(" %\t");
        Serial.print("Temperature: "); 
        Serial.print(t);
        Serial.println(" *C");
        delay(2000);
    }
}

void control_relay(int relay, int position){
    if(relay == 2 && position == 0){
        // inverted because of relay position
        digitalWrite(RELAY2, HIGH);
    }
    else if (relay == 2 && position == 1)
    {
        // inverted because of relay position
        digitalWrite(RELAY2, LOW);
    }
}

void read_light(){
    int light_value = analogRead(A0);
    Serial.println(light_value);
}

void read_wlevel(){
    int val = digitalRead(WLEVEL);
    Serial.println(val);
}

void read_soil(){
    digitalWrite(SOIL, HIGH);
    delay(3000);
    int soilSensorValue = analogRead(A1);
    Serial.println(soilSensorValue);
    //delay(2500);
    digitalWrite(SOIL, LOW);
}