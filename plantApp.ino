// First we include the libraries
#include "DHT.h"


#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define DHTPIN 4    // modify to the pin we connected
#define DHTTYPE DHT21   // AM2301 
#define RELAY1 5
#define RELAY2 6 // water pump
// define RELAY3 x
// define RELAY4 x
// define RELAY5 x
// define RELAY6 x
#define SOIL 8
#define WLEVEL 10

/* integers */
int light_value;
int distance;
int soilSensorValue;
int water_level;
int soil_moisture;

/* floats */
float humidity;
float temperature;

/* long integers */
long run_time_int;
long interval;
unsigned long startMillis;   
unsigned long currentMillis;     
long stopMills;
long duration;

/* strings */
String val;
String run_time;


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

    // reply only when you receive data:
    if (Serial.available() > 0) {
        
        val = Serial.readStringUntil('\n');
        if(val == "read_sensors")
        /* logic for sending sensor values to serial */
        {
            distance = ultrasonic_distance();
            humidity = dht.readHumidity();
            temperature = dht.readTemperature();
            light_value = analogRead(A0);
            water_level = digitalRead(WLEVEL);
            soil_moisture = read_soil();

            Serial.print(20);
            Serial.print(";");
            Serial.print(humidity);
            Serial.print(";");
            Serial.print(temperature);
            Serial.print(";");
            Serial.print(light_value);
            Serial.print(";");
            Serial.print(water_level);
            Serial.print(";");
            Serial.print(soil_moisture);
            Serial.println();
        }

        else if (val.substring(0,14) == "run_water_pump")
        /* 
        Logic for running the water pump. The water pump will stop
        after given seconds or when the water level reaches to the high level sensor.  
        */
        {
            run_time = val.substring(14,17);
            run_time_int = run_time.toInt();
            startMillis = millis();        
            interval = run_time_int * 1000; 
            stopMills = interval + startMillis;
            digitalWrite(RELAY2, LOW); // water pump on
            
            while(true){
                currentMillis = millis();
                water_level = digitalRead(WLEVEL); // high level sensor
                if (currentMillis >= stopMills || water_level == 1) {
                    digitalWrite(RELAY2, HIGH); //water pump off
                    break;
                }
            }
        }
    }
}

int ultrasonic_distance(){
    // defines variables
    duration; // variable for the duration of sound wave travel
    distance; // variable for the distance measurement
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

int read_soil(){
    digitalWrite(SOIL, HIGH);
    delay(3000);
    soilSensorValue = analogRead(A1);
    digitalWrite(SOIL, LOW);
    return soilSensorValue;
}