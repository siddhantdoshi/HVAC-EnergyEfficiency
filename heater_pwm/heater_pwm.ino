#define HEATER_A1_PIN 7 // Driver Board IN1
#define HEATER_B1_PIN 8 // Driver Board IN2
#define HEATER_PWM 5 // Driver Board PWM
#define EN_PIN A0 // Driver Board EN
#define CS_PIN A1 // Driver Board CS
#define THERMISTOR_PIN A2 // Thermistor (temperature sensor)

float current = 0.0;

float set_point = 30.0;

float error = 0.0;
float prev_error = 0.0;
float derivative = 0.0;
float integral = 0.0;

float kp = 15000.0;
float ki = 50.0;
float kd = -500.0;

float output_power = 0.0;
int pwm_output = 0;

void setup()                         
{
  pinMode(HEATER_A1_PIN, OUTPUT);
  pinMode(HEATER_B1_PIN, OUTPUT);
  pinMode(HEATER_PWM, OUTPUT);
  pinMode(EN_PIN, OUTPUT);
  pinMode(CS_PIN, INPUT);

  digitalWrite(EN_PIN, HIGH);
  digitalWrite(HEATER_A1_PIN, LOW);
  digitalWrite(HEATER_B1_PIN, HIGH);
  
  analogWrite(HEATER_PWM, 0); // Sets heater to off

  prev_error = set_point - analogRead(HEATER_PWM);

  Serial.begin(9600); // Initiates the serial to do the monitoring
}

float get_temp()
{
  float sensor_average = 0;

  for (int i = 0; i < 10; i++)
  {
    int sensor_val = analogRead(THERMISTOR_PIN);
    sensor_average += sensor_val;
    delay(5);
  }  
  sensor_average /= 10.0;
  
  float voltage = sensor_average * 5.0 / 1024.0;
  float resistance = 10000.0 * (voltage / (5.0 - voltage));
  float temp_reciprocal = 1.0 / 295.15 + log(resistance / 10000.0) / 3950.0;
  float temperature = (1.0 / temp_reciprocal) - 273.15;

  return temperature;
}

void loop() 
{
  float temperature = get_temp();
  error = set_point - temperature;

  derivative = error - prev_error;
  if (error < 3)
  {
    integral += error;
  }

  output_power = kp * error + ki * integral + kd * derivative;

  if (output_power < 0)
  {
    pwm_output = 0.0;
  }
  else
  {
    pwm_output = (int) (sqrt(output_power) + 0.5);
  }

  if (pwm_output > 255)
  {
    pwm_output = 255;
  }

  current = analogRead(CS_PIN) * 5.0 / (1024 * 0.13);
  analogWrite(HEATER_PWM, pwm_output);

  prev_error = error;
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(";  Error: ");
  Serial.print(error);
  Serial.print(";  Output power: ");
  Serial.print(output_power);
  Serial.print(";  PWM output: ");
  Serial.print(pwm_output);
  Serial.print("; Current: ");
  Serial.print(current);
  Serial.print("; PWM / Current: ");
  Serial.println(pwm_output / current);

  delay(200);
}
