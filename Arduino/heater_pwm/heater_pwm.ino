#define HEATER_A1_PIN 7 // Driver Board IN1
#define HEATER_B1_PIN 8 // Driver Board IN2
#define HEATER_PWM 5 // Driver Board PWM
#define EN_PIN A0 // Driver Board EN
#define CS_PIN A1 // Driver Board CS
#define THERMISTOR_PIN A2 // Thermistor (temperature sensor)

int count = 0;

float current = 0.0;
float resistance = 3.6;
float max_voltage = 12.0;

float set_point = 30.0;

float error = 0.0;
float prev_error = 0.0;
float derivative = 0.0;
float integral = 0.0;

float kp = 18.0;
float ki = 0.004;
float kd = 10.0;

float output_power = 0.0;
int pwm_output = 0;

const int num_sensor_readings = 100;
int temp_val[num_sensor_readings];

float temp_sort_clean()
{
  int temp = 0;
  for (int i = 0; i < (num_sensor_readings - 1); i++)
  {
    for (int j = 0; j < (num_sensor_readings - 1 - i); j++)
    {
      if (temp_val[j] < temp_val[j + 1])
      {
        temp = temp_val[j];
        temp_val[j] = temp_val[j + 1];
        temp_val[j + 1] = temp;
      }
    }
  }

//  int sum = 0;
//  int count = 0;
//  
//  for (int i = (num_sensor_readings / 3); i < (num_sensor_readings * 2 / 3); i++)
//  {
//    sum += temp_val[i];
//    count ++;
//  }

//  return ((sum + 0.0) / count);

    return temp_val[49];
}

float get_temp()
{
  float sensor_average = 0;

  for (int i = 0; i < num_sensor_readings; i++)
  {
    int sensor_val = analogRead(THERMISTOR_PIN);
    temp_val[i] = sensor_val;
    delay(1000 / num_sensor_readings);
  }
      
  sensor_average = temp_sort_clean();
  
  float voltage = sensor_average * 5.0 / 1024.0;
  float resistance = 10000.0 * (voltage / (5.0 - voltage));
  float temp_reciprocal = 1.0 / 295.15 + log(resistance / 10000.0) / 3950.0;
  float temperature = (1.0 / temp_reciprocal) - 273.15;

  return temperature;
}

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

//  set_point = get_temp() + 10.0;
  prev_error = 10;

  Serial.begin(9600); // Initiates the serial to do the monitoring

//  Serial.println(set_point);
  Serial.println("Timestamp, Temperature (ºC), Error,  Output power (W), PWM output, Current, PWM / Current");
}



void loop() 
{
  float temperature = get_temp();

  if (count == 0)
  {
    set_point = temperature + 10;
    Serial.println(set_point);
    count ++;
  }
  
  error = set_point - temperature;

  current = analogRead(CS_PIN) * 5.0 / (1024 * 0.13) - 0.189;

  derivative = error - prev_error;
  
  if (temperature >= 0.9 * set_point) // and temperature <= set_point)
  {
//    if (derivative <= 0)
//    {
//      integral += error;
//    } else
//    {
//      integral += 0.8 * error;
//    }
      integral += error;
  }
  
  output_power = kp * error + ki * integral + kd * derivative;

  if (output_power < 0)
  {
    pwm_output = 0.0;
  }
  else
  {
    pwm_output = (int) (sqrt(resistance * output_power) + 0.5) * 255.0 / max_voltage;
  }

  if (pwm_output > 255)
  {
    pwm_output = 255;
  }
// Added code
  if (temperature < 30.0){
    analogWrite(HEATER_PWM, 255);  
  }else{
   analogWrite(HEATER_PWM, 0);  
  }
  
// End of added code
  prev_error = error;
  Serial.print(temperature);
  
  Serial.print(", ");
  Serial.print(error);
  
  Serial.print(", ");
  Serial.print(output_power);
  
  Serial.print(", ");
  Serial.print(pwm_output);
  
  Serial.print(", ");
  Serial.print(current);
  
  Serial.print(", ");
  Serial.println(pwm_output / current);

//  delay(200);
}
