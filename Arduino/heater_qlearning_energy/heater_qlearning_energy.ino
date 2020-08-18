#define HEATER_A1_PIN 7 // Driver Board IN1
#define HEATER_B1_PIN 8 // Driver Board IN2
#define HEATER_PWM 5 // Driver Board PWM
#define EN_PIN A0 // Driver Board EN
#define CS_PIN A1 // Driver Board CS
#define THERMISTOR_PIN A2 // Thermistor (temperature sensor)

const int delta_T = 5;
const float resistance = 4.5;
float current;
const float max_voltage = 10.72; //9.66;

const unsigned char q_actions[149] = {155, 236, 253, 252, 213, 244, 208, 254, 240, 100, 178, 231, 255, 241, 254, 164, 231, 236, 255, 247, 253, 253, 248, 222, 249, 241, 238, 253, 254, 250, 248, 234, 249, 242, 247, 255, 250, 254, 233, 246, 232, 255, 251, 254, 239, 248, 249, 233, 242, 251, 255, 253, 245, 237, 253, 247, 245, 236, 243, 252, 242, 236, 244, 251, 208, 255, 251, 254, 250, 223, 249, 250, 248, 243, 251, 255, 253, 251, 254, 249, 253, 251, 252, 255, 249, 235, 252, 253, 255, 250, 238, 255, 255, 246, 253, 254, 240, 246, 253, 229, 249, 230, 106, 8, 5, 26, 37, 169, 77, 4, 54, 19, 12, 9, 6, 6, 34, 8, 16, 16, 0, 32, 15, 2, 7, 1, 19, 42, 186, 156, 8, 203, 160, 130, 21, 177, 50, 188, 125, 200, 211, 149, 241, 208, 243, 114, 0, 0, 0};

const int num_sensor_readings = 100;
short int temp_val[num_sensor_readings];

float target_energy = 0.05 * 4180 * delta_T;
int state = 0;

float output_power = 0.0;
int pwm_output = 0;

short int count = 0;

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
    short int sensor_val = analogRead(THERMISTOR_PIN);
    temp_val[i] = sensor_val;
    delay(1000 / num_sensor_readings);
  }
      
  sensor_average = temp_sort_clean();
  
  float voltage = sensor_average * 5.0 / 1024.0;
  float sensor_resistance = 10000.0 * (voltage / (5.0 - voltage));
  float temp_reciprocal = 1.0 / 295.15 + log(sensor_resistance / 10000.0) / 3950.0;
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
  
  Serial.begin(9600);
  Serial.println("Timestamp, Count, Temperature (ºC), State, Output Power, PWM output, Current, PWM / Current");
  // put your setup code here, to run once:

}

void loop()
{
  // put your main code here, to run repeatedly:
  float temperature = get_temp();

  count ++;
  
  pwm_output = q_actions[(int) (state / 10.0 + 0.5)];
  output_power = ((((max_voltage * pwm_output) / 255) * ((max_voltage * pwm_output) / 255)) / resistance);
  state += output_power;
//  state = (int) (state / 10.0 + 0.5);

  analogWrite(HEATER_PWM, pwm_output);
  
  current = analogRead(CS_PIN) * 5.0 / (1024 * 0.13) - 0.189;
  
  Serial.print(count);

  Serial.print(", ");
  Serial.print(temperature);

  Serial.print(", ");
  Serial.print(state);

  Serial.print(", ");
  Serial.print(output_power);

  Serial.print(", ");
  Serial.print(pwm_output);
  
  Serial.print(", ");
  Serial.print(current);

  Serial.print(", ");
  Serial.println(pwm_output / current);
}
