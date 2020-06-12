const int thermistor_pin = A0;
const int relay_pin = 8;

float set_point = 30.0;

void setup()
{
  pinMode(thermistor_pin, INPUT);
  pinMode(relay_pin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(relay_pin, HIGH);
}

float get_temp()
{
  float sensor_average = 0;

  for (int i = 0; i < 2; i++)
  {
    int sensor_val = analogRead(thermistor_pin);
    sensor_average += sensor_val;
  }  
  sensor_average /= 2.0;
  
  float voltage = sensor_average * 5.0 / 1024.0;
  float resistance = 10000.0 * (voltage / (5.0 - voltage));
  float temp_reciprocal = 1.0 / 295.15 + log(resistance / 10000.0) / 3950.0;
  float temperature = (1.0 / temp_reciprocal) - 273.15;

  return temperature;
}

void loop()
{
  float temperature = get_temp();
  Serial.print("Temperature: ");
  Serial.println(temperature);

  if (temperature < set_point - 0.1)
  {
    digitalWrite(relay_pin, LOW);
  }
  if (temperature > set_point + 0.1)
  {
    digitalWrite(relay_pin, HIGH);  
  }

  delay(300);
}
