#define HEATER_A1_PIN 7 // Driver Board IN1
#define HEATER_B1_PIN 8 // Driver Board IN2
#define HEATER_PWM 5 // Driver Board PWM
#define EN_PIN A0 // Driver Board EN
#define CS_PIN A1 // Driver Board CS
#define THERMISTOR_PIN A2 // Thermistor (temperature sensor)

const int delta_T = 5;
const float resistance = 3.8;
float current = 0.0;
const float max_voltage = 9.66;

const unsigned char q_actions[448] = {0, 0, 0, 224, 247, 0, 0, 0, 0, 0, 0, 0, 0, 223, 0, 0, 0, 0, 0, 0, 0, 0, 239, 0, 0, 0, 0, 0, 0, 0, 0, 239, 0, 0, 0, 0, 0, 0, 0, 0, 239, 0, 0, 0, 0, 0, 0, 0, 0, 239, 0, 0, 239, 0, 0, 0, 0, 0, 239, 0, 0, 239, 0, 0, 0, 0, 0, 63, 0, 0, 225, 0, 0, 0, 0, 0, 234, 0, 0, 250, 0, 0, 0, 0, 0, 234, 0, 0, 250, 0, 0, 0, 0, 0, 234, 0, 0, 250, 0, 0, 0, 0, 0, 234, 0, 0, 250, 0, 0, 0, 0, 0, 243, 0, 0, 250, 0, 0, 0, 0, 0, 9, 0, 0, 250, 0, 0, 0, 0, 0, 237, 0, 0, 250, 0, 0, 0, 0, 0, 37, 0, 0, 250, 0, 0, 0, 0, 0, 151, 0, 0, 250, 0, 0, 0, 0, 0, 151, 0, 0, 250, 0, 0, 0, 0, 0, 151, 0, 0, 250, 0, 0, 0, 0, 0, 151, 0, 0, 250, 0, 0, 0, 0, 0, 147, 0, 0, 234, 0, 0, 0, 0, 0, 152, 0, 0, 234, 0, 0, 0, 0, 0, 78, 0, 0, 234, 0, 0, 0, 0, 0, 17, 0, 0, 234, 0, 0, 0, 0, 0, 30, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 3, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 109, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 200, 0, 0, 125, 0, 0, 0, 0, 0, 109, 0, 0, 125, 0, 0, 0, 0, 0, 109, 0, 0, 125, 0, 0, 0, 0, 0, 109, 0, 0, 125, 0, 0, 0, 0, 0, 109, 0, 0, 125, 0, 0, 0, 0, 0, 218, 0, 0, 125, 0, 0, 0, 0, 0, 144, 0, 0, 34, 0, 0, 0, 0, 0, 50, 0, 0, 80, 0, 0, 0, 0, 0, 12, 0, 0, 203, 0, 0, 0, 0, 0, 86, 0, 0, 39, 0, 0, 0, 0, 0, 97, 0, 0, 26, 0, 0, 0, 0, 0, 203, 0, 0, 210, 0, 0, 0, 0, 0, 128, 0, 0, 84, 0, 0, 0, 0, 0, 175, 0, 0, 112, 0, 0, 0, 0, 0, 11, 0, 0, 68, 0, 0, 0, 0, 0, 67, 0, 0, 158, 0, 0, 0, 0, 0, 13, 0, 0, 37, 0, 0, 0, 0, 0, 18, 0, 0};

const int num_sensor_readings = 100;
int temp_val[num_sensor_readings];

float set_point;
int state = 0;

float output_power = 0.0;
int pwm_output = 0;

float prev_temp = 0.0;
float prev_velocity = 0.0;

int count = 0;

int action_table_size = 0;


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

  action_table_size = sizeof(q_actions) / sizeof(q_actions[0]);
  
  Serial.begin(9600);
  Serial.println("Timestamp, Temperature (ºC), Setpoint, Error, Velocity, Acceleration, State, PWM output, Current, PWM / Current");
  // put your setup code here, to run once:

}

int getstate(float temp, float delta_temp, float acceleration)
{
  temp = round(temp * 10.0) / 10.0;
  delta_temp = round(delta_temp * 10.0) / 10.0;
  acceleration = round(acceleration * 10.0) / 10.0;

  if (delta_temp > 0.1)
  {
    delta_temp = 0.1;
  }
  else if (delta_temp < -0.1)
  {
    delta_temp = -0.1;
  }
  
  int conjugate = 1000 * temp + 100 * delta_temp + 10 * acceleration + 5011;
  int tmp = floor(conjugate / 10);
  int index = 9 * floor(conjugate / 100) + 3 * (tmp % 10) + (conjugate % 10);

  return index;
}

void loop()
{
  // put your main code here, to run repeatedly:
  float temperature = get_temp();

  float velocity = temperature - prev_temp;
  float acceleration = velocity - prev_velocity;

  if (count == 5)
  {
    set_point = temperature + delta_T;
    Serial.println(set_point);
    count ++;
  }

  state = getstate(temperature - set_point, velocity, acceleration);
  pwm_output = 0;

  if (state < 0)
  {
    pwm_output = 255;
  }

  else if (state < action_table_size)
  {
    pwm_output = q_actions[state];  
  }


  analogWrite(HEATER_PWM, pwm_output);
  
  current = analogRead(CS_PIN) * 5.0 / (1024 * 0.13) - 0.189;

  Serial.print(temperature);

  Serial.print(", ");
  Serial.print(set_point);

  Serial.print(", ");
  Serial.print(temperature - set_point);
  
  Serial.print(", ");
  Serial.print(velocity);

  Serial.print(", ");
  Serial.print(acceleration);
  
  Serial.print(", ");
  Serial.print(state);

  Serial.print(", ");
  Serial.print(pwm_output);
  
  Serial.print(", ");
  Serial.print(current);

  Serial.print(", ");
  Serial.println(pwm_output / current);

  prev_temp = temperature;
  prev_velocity = velocity;
  count ++;
}
