#define HEATER_A1_PIN 7 // Driver Board IN1
#define HEATER_B1_PIN 8 // Driver Board IN2
#define HEATER_PWM 5 // Driver Board PWM
#define EN_PIN A0 // Driver Board EN
#define CS_PIN A1 // Driver Board CS
#define THERMISTOR_PIN A2 // Thermistor (temperature sensor)

const int delta_T = 5;
const float resistance = 3.8;
float current;
const float max_voltage = 9.66;

//const unsigned char q_actions[749] = {128, 127, 241, 196, 230, 228, 249, 253, 245, 253, 218, 241, 230, 252, 225, 246, 251, 249, 241, 236, 253, 253, 255, 235, 254, 247, 249, 234, 240, 245, 244, 239, 178, 242, 237, 246, 243, 224, 247, 233, 241, 250, 249, 251, 253, 251, 253, 248, 244, 254, 251, 231, 241, 251, 250, 252, 245, 252, 250, 231, 247, 226, 217, 252, 255, 253, 243, 240, 239, 239, 253, 255, 209, 255, 231, 239, 247, 238, 231, 243, 253, 246, 241, 245, 242, 253, 249, 240, 252, 236, 251, 250, 250, 224, 249, 215, 244, 255, 231, 252, 238, 253, 251, 242, 247, 216, 250, 246, 248, 255, 250, 255, 236, 239, 255, 247, 255, 227, 255, 249, 250, 255, 224, 251, 253, 248, 252, 243, 247, 246, 231, 250, 224, 191, 252, 238, 250, 208, 254, 237, 235, 254, 255, 255, 250, 252, 251, 246, 225, 214, 231, 231, 240, 229, 253, 248, 252, 243, 251, 243, 253, 240, 229, 229, 233, 242, 230, 244, 241, 252, 255, 246, 211, 249, 245, 254, 253, 215, 249, 251, 239, 237, 229, 235, 248, 251, 234, 225, 254, 253, 246, 229, 240, 249, 251, 232, 241, 233, 239, 163, 151, 236, 244, 222, 220, 249, 247, 241, 249, 253, 235, 236, 248, 245, 254, 240, 252, 254, 239, 197, 252, 237, 238, 244, 249, 252, 224, 249, 245, 237, 229, 227, 249, 250, 248, 253, 242, 236, 241, 228, 223, 221, 241, 211, 239, 219, 248, 251, 242, 243, 210, 236, 243, 255, 252, 249, 238, 251, 231, 254, 248, 236, 238, 253, 244, 252, 255, 250, 240, 230, 249, 252, 242, 232, 223, 230, 244, 249, 251, 255, 246, 234, 255, 248, 220, 199, 242, 234, 249, 223, 249, 255, 215, 247, 215, 222, 244, 238, 253, 250, 225, 241, 255, 247, 249, 252, 246, 250, 253, 252, 249, 250, 245, 252, 222, 221, 253, 179, 253, 225, 251, 243, 241, 242, 250, 243, 247, 202, 252, 250, 255, 231, 255, 245, 221, 236, 236, 167, 254, 250, 255, 242, 248, 244, 254, 234, 209, 253, 255, 222, 248, 239, 250, 233, 213, 255, 232, 251, 243, 224, 192, 230, 253, 253, 245, 252, 250, 245, 242, 242, 244, 245, 244, 241, 240, 239, 242, 204, 252, 254, 247, 237, 247, 236, 174, 245, 227, 245, 232, 214, 234, 217, 254, 255, 255, 253, 220, 236, 245, 247, 219, 240, 248, 219, 238, 233, 253, 250, 248, 250, 252, 219, 227, 239, 241, 249, 246, 200, 252, 254, 246, 249, 235, 248, 235, 246, 222, 215, 243, 212, 211, 230, 249, 245, 244, 254, 236, 229, 243, 240, 233, 192, 223, 241, 236, 222, 145, 233, 245, 245, 232, 107, 234, 155, 246, 248, 228, 246, 219, 237, 100, 242, 195, 228, 255, 143, 108, 164, 153, 238, 212, 130, 140, 114, 153, 113, 123, 95, 62, 129, 98, 228, 142, 36, 127, 111, 141, 102, 34, 38, 47, 121, 73, 16, 33, 64, 61, 93, 92, 34, 14, 53, 91, 138, 9, 2, 3, 56, 34, 10, 67, 53, 9, 6, 5, 5, 7, 26, 0, 4, 55, 15, 3, 21, 40, 60, 57, 4, 10, 28, 94, 254, 13, 200, 14, 169, 34, 103, 220, 68, 14, 45, 47, 167, 42, 27, 36, 120, 185, 121, 196, 12, 135, 23, 72, 28, 118, 140, 121, 184, 79, 88, 42, 189, 56, 91, 45, 48, 28, 239, 123, 27, 226, 132, 97, 37, 43, 6, 144, 20, 195, 21, 163, 3, 79, 220, 163, 91, 232, 73, 122, 127, 18, 27, 29, 99, 137, 19, 49, 186, 230, 21, 129, 193, 102, 6, 173, 135, 5, 153, 224, 202, 25, 104, 114, 190, 26, 7, 40, 122, 153, 103, 30, 47, 20, 133, 140, 27, 29, 46, 83, 157, 175, 200, 168, 243, 26, 227, 119, 250, 233, 233, 237, 244, 245, 251, 223, 250, 95, 94, 253, 248, 240, 226, 235, 249, 252, 252, 234, 222, 232, 250, 255, 249, 250, 255, 247, 185, 235, 251, 246, 240, 245, 246, 39, 192, 202, 119, 109, 90, 244, 249, 246, 253, 210, 244, 246, 245, 248, 238, 207, 189, 145, 150, 128, 103, 131, 95, 151, 111, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//const unsigned char q_actions[74] = {247, 236, 237, 239, 237, 227, 248, 171, 187, 251, 249, 239, 214, 255, 252, 252, 231, 228, 201, 248, 251, 254, 239, 231, 247, 252, 243, 247, 252, 240, 234, 252, 246, 237, 210, 249, 216, 173, 171, 201, 242, 240, 176, 132, 186, 244, 245, 170, 182, 25, 28, 18, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

// action matrix for training simulation 8
//const unsigned char q_actions[174] = {0, 245, 0, 0, 239, 0, 0, 187, 0, 0, 245, 0, 0, 244, 0, 0, 254, 0, 0, 230, 0, 0, 253, 0, 0, 230, 254, 0, 253, 254, 0, 253, 254, 0, 253, 253, 0, 246, 249, 0, 246, 253, 0, 249, 243, 0, 251, 243, 0, 253, 249, 0, 243, 253, 0, 251, 251, 0, 253, 251, 0, 253, 251, 0, 251, 249, 0, 249, 253, 0, 251, 249, 0, 251, 249, 0, 231, 243, 0, 231, 253, 0, 231, 251, 0, 251, 251, 0, 251, 103, 0, 23, 14, 0, 189, 249, 0, 129, 65, 0, 7, 14, 0, 44, 108, 0, 56, 251, 0, 160, 149, 0, 136, 149, 0, 0, 198, 0, 7, 198, 0, 0, 244, 0, 7, 244, 0, 0, 211, 0, 0, 211, 0, 7, 13, 0, 7, 110, 0, 26, 149, 0, 37, 36, 0, 171, 37, 0, 55, 37, 0, 7, 37, 0, 93, 36, 0, 0, 224, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1};

// action matrix for training simulation 9
const unsigned char q_actions[171] = {0, 246, 0, 0, 246, 0, 0, 185, 0, 0, 253, 0, 0, 228, 0, 0, 248, 0, 0, 250, 0, 0, 250, 0, 0, 248, 247, 0, 248, 249, 0, 248, 205, 0, 248, 100, 0, 252, 149, 0, 249, 196, 0, 253, 188, 0, 245, 208, 0, 245, 120, 0, 249, 8, 0, 254, 228, 0, 249, 247, 0, 249, 247, 0, 254, 247, 0, 233, 247, 0, 254, 247, 0, 254, 247, 0, 254, 247, 0, 254, 247, 0, 230, 184, 0, 212, 240, 0, 229, 240, 0, 252, 252, 0, 227, 16, 0, 102, 102, 0, 77, 77, 0, 245, 245, 0, 237, 10, 0, 159, 159, 0, 206, 203, 0, 197, 197, 0, 89, 217, 0, 222, 222, 0, 251, 195, 0, 234, 138, 0, 204, 204, 0, 40, 40, 0, 246, 246, 0, 57, 247, 0, 148, 62, 0, 134, 148, 0, 111, 108, 0, 240, 25, 0, 112, 95, 0, 218, 163, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1};


const int num_sensor_readings = 100;
int temp_val[num_sensor_readings];

float set_point;
int state = 0;

float output_power = 0.0;
int pwm_output = 0;

float prev_temp = 0.0;

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

  action_table_size = sizeof(q_actions)/sizeof(q_actions[0]);
  
  Serial.begin(9600);
  Serial.println("Timestamp, Temperature (ºC), Error, Delta_T, State, PWM output, Current, PWM / Current");
  // put your setup code here, to run once:

}

int getstate(float temp, float delta_temp) {
  temp = round(temp * 10.0) / 10.0;
  delta_temp = round(delta_temp * 10.0) / 10.0;
  
  int conjugate = 1000 * temp + 10 * delta_temp + 5001;
  int index = (floor(conjugate/100) * 3) + (conjugate % 100)  ;

  return index;
}

void loop()
{
  // put your main code here, to run repeatedly:
  float temperature = get_temp();

  float velocity = temperature - prev_temp ;

  if (count == 5)
  {
    set_point = temperature + delta_T - 0.2;
    Serial.println(set_point);
    count ++;
  }

  state = getstate(temperature - set_point + 0.2, velocity);
  pwm_output = 0;
  
//  state = (int) (temperature * 10) - ((set_point - delta_T) * 10);
  if ( state < action_table_size ) {
    pwm_output = q_actions[state];  
  }


  analogWrite(HEATER_PWM, pwm_output);  
  
  
  current = analogRead(CS_PIN) * 5.0 / (1024 * 0.13) - 0.189;

  Serial.print(temperature);

  Serial.print(", ");
  Serial.print(temperature - set_point);
  
  Serial.print(", ");
  Serial.print(velocity);
  
  Serial.print(", ");
  Serial.print(state);

  Serial.print(", ");
  Serial.print(pwm_output);
  
  Serial.print(", ");
  Serial.print(current);

  Serial.print(", ");
  Serial.println(pwm_output / current);

  prev_temp = temperature ;
  count ++;
}
