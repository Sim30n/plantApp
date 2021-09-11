// First we include the libraries
#include "DHT.h"

/* pin setup */
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define DHTPIN 4    // modify to the pin we connected
#define DHTTYPE DHT21   // AM2301 
#define RELAY3 6
#define RELAY4 5 // water pump
#define RELAY5 7 // fertilizer pump 1
#define RELAY6 11 // fertilizer pump 2
#define RELAY7 12 // fertilizer pump 3
#define RELAY8 13 // fertilizer pump 4
#define SOIL 8
#define WLEVEL 10

/* integers */
int light_value;
int distance;
int soilSensorValue;
int water_level;
int soil_moisture;
int pump_n_int;

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
String pump_n;


DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(RELAY3, OUTPUT);
  pinMode(RELAY4, OUTPUT);
  pinMode(RELAY5, OUTPUT);
  pinMode(RELAY6, OUTPUT);
  pinMode(RELAY7, OUTPUT);
  pinMode(RELAY8, OUTPUT);
  pinMode(WLEVEL, INPUT);
  pinMode(SOIL, OUTPUT);
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  dht.begin();

  digitalWrite(RELAY3, HIGH);
  digitalWrite(RELAY4, HIGH); // Switch off the water pump
  digitalWrite(RELAY5, HIGH);
  digitalWrite(RELAY6, HIGH);
  digitalWrite(RELAY7, HIGH);
  digitalWrite(RELAY8, HIGH);
}

/* 
 * Main loop. Wait for serial commands.
 */
void loop() {

    // reply only when you receive data:
    if (Serial.available() > 0) {
        val = Serial.readStringUntil('\n');
        if(val == "read_sensors")
        {
            read_sensors(); 
        }
        else if (val.substring(0,14) == "run_water_pump")
        {
            run_water_pump(val);            
        }
        else if (val.substring(0,19) == "run_fertilizer_pump")
        {
            run_fertilizer_pump(val);
        }
    }
}

/* 
 * Function for mesuring the distance of water level from the top of the tank
 */
int ultrasonic_distance()
{
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

/* 
 * Read soil moisture from sensor. 
 */
int read_soil()
{
    digitalWrite(SOIL, HIGH);
    delay(3000);
    soilSensorValue = analogRead(A1);
    digitalWrite(SOIL, LOW);
    return soilSensorValue;
}

/* 
 * Function for running the fertilizer pump. The water pump will stop
 * after given seconds. Example command: run_fertilizer_pump07120
 * run fertilizer pump number 7 for 120 seconds.
 */
void run_fertilizer_pump(String val)
{
    pump_n = val.substring(19,21);
    pump_n_int = pump_n.toInt();
    run_time = val.substring(21,24);
    run_time_int = run_time.toInt();
    startMillis = millis();        
    interval = run_time_int * 1000; 
    stopMills = interval + startMillis;
    digitalWrite(pump_n_int, LOW); // fertilizer pump on, 4 possible pumps
    while(true){
        currentMillis = millis();
        if (currentMillis >= stopMills) 
        {
            digitalWrite(pump_n_int, HIGH); // fertilizer pump off
            break;
        }
    }
}

/* 
 * Function for running the water pump. The water pump will stop
 * after given seconds or when the water level reaches to the high level sensor.  
 */
void run_water_pump(String val)
{
    run_time = val.substring(14,17);
    run_time_int = run_time.toInt();
    startMillis = millis();        
    interval = run_time_int * 1000; 
    stopMills = interval + startMillis;
    digitalWrite(RELAY4, LOW); // water pump on
    
    while(true){
        currentMillis = millis();
        water_level = digitalRead(WLEVEL); // high level sensor
        if (currentMillis >= stopMills || water_level == 1) {
            digitalWrite(RELAY4, HIGH); //water pump off
            break;
        }
    }
}

/* 
 * Function for reading latest sensor data. Prints values to serial  
 */
void read_sensors(){
    distance = ultrasonic_distance();
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    light_value = analogRead(A0);
    water_level = digitalRead(WLEVEL);
    soil_moisture = read_soil();

    Serial.print(distance);
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
