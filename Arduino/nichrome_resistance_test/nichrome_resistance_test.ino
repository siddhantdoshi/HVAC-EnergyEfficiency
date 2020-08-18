const int nichrome_pin = A0;
int counter = 0;
float average_resistance = 0.0;
float average_voltage = 0.0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  float nichrome_voltage = analogRead(nichrome_pin) * 5.0/1024.0;
  float resistance = 22 * (nichrome_voltage / (5.0 - nichrome_voltage));

  average_voltage += nichrome_voltage;
  average_resistance += resistance;
  counter ++;

  if (counter % 5 == 0) {
    average_voltage /= 5.0;
    average_resistance /= 5.0;
    
    Serial.print("Voltage: ");
    Serial.print(average_voltage);
    Serial.print(",Resistance: ");
    Serial.print(average_resistance);
    Serial.print("\n");

    average_voltage = 0;
    average_resistance = 0;
  }
}
