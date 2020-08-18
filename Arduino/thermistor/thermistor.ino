const int thermistor_pin = A0;
int counter = 0;
float sensor_average = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int sensor_val = analogRead(thermistor_pin);
  sensor_average += sensor_val;
  counter++;

  if (counter % 2 == 0) {
    sensor_average /= 2.0;
    
    float voltage = sensor_average * 5.0 / 1024.0;
    float resistance = 10000.0 * (voltage / (5.0 - voltage));
    float temp_reciprocal = 1.0 / 295.15 + log(resistance / 10000.0) / 3950.0;
    float temperature = (1.0 / temp_reciprocal) - 273.15;

    Serial.print("Sensor reading: ");
    Serial.print(sensor_average);
    Serial.print(", Voltage: ");
    Serial.print(voltage);
    Serial.print(", Resistance: ");
    Serial.print(resistance);
    Serial.print(", Temperature: ");
    Serial.print(temperature);
    Serial.print("\n");

    sensor_average = 0;
  }

   delay(5);
}
