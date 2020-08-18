const int thermistor_pin = A0;
const int relay_pin = 8;

float set_point = 30.0;
long tot_energy = 0.0;
bool reach_target = false;
double squared_error = 0.0;
double mean_squared_error = 0.0;
double efficiency_metric = 0.0;
int num_samples = 0;

const int num_sensor_readings = 100;
int temp_val[num_sensor_readings];

void setup()
{
  reach_target = false;
  pinMode(thermistor_pin, INPUT);
  pinMode(relay_pin, OUTPUT);
  Serial.begin(9600);
  digitalWrite(relay_pin, HIGH);
}

// Ignoring extreme sensor values
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

  int sum = 0;
  int count = 0;
  
  for (int i = (num_sensor_readings / 3); i < (num_sensor_readings * 2 / 3); i++)
  {
//    Serial.print(i);
//    Serial.print(", ");
//    Serial.print(temp_val[i]);
//    Serial.print(", ");
//    Serial.println(sum);

    sum += temp_val[i];
    count ++;
  }

  return ((sum + 0.0) / count);
}

float get_temp()
{
  float sensor_average = 0;

  for (int i = 0; i < num_sensor_readings; i++)
  {
    int sensor_val = analogRead(thermistor_pin);
    temp_val[i] = sensor_val;
//    Serial.print(i);
//    Serial.print(", ");
//    Serial.println(temp_val[i]);
    delay(1000 / num_sensor_readings);
  }    
  sensor_average = temp_sort_clean();
  
  float voltage = sensor_average * 5.0 / 1024.0;
  float resistance = 10000.0 * (voltage / (5.0 - voltage));
  float temp_reciprocal = 1.0 / 295.15 + log(resistance / 10000.0) / 3950.0;
  float temperature = (1.0 / temp_reciprocal) - 273.15;

  return temperature;
}

float old_temp = 0;
void loop()
{
  num_samples ++;
  float temperature = get_temp();
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(";  Num Samples: ");
  Serial.print(num_samples);
  
  
  old_temp = temperature;

  if (temperature < set_point - 0.1)
  {
    digitalWrite(relay_pin, LOW);
    tot_energy += 255L * 255L;
  }
  if (temperature > set_point + 0.1)
  {
    digitalWrite(relay_pin, HIGH);  
  }
  if (temperature >= set_point)
  {
    reach_target = true;
  }
  
  if (reach_target)
  {
    squared_error += (temperature - set_point) * (temperature - set_point);
  }

  mean_squared_error = squared_error / num_samples;
  efficiency_metric = (0.7 * tot_energy) + (0.3 * mean_squared_error);
  
  Serial.print(";  Total energy: ");
  Serial.print(tot_energy);

  Serial.print(";  Squared error: ");
  Serial.print(squared_error);

  Serial.print(";  Mean squared error: ");
  Serial.print(mean_squared_error);
  
  Serial.print(";  Efficiency metric: ");
  Serial.println(efficiency_metric);
//  delay(1000);
}
