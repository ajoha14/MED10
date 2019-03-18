//Code written by Jesper Wædeled Henriksen for master thesis project at Aalborg University, 2019
//This code measures heartrate and sends it to serial port.
int input_HR_Pin = A0;

int output_GSR_Pin = 9;
int input_GSR_Pin = A2;

void setup ( )
{
  pinMode(input_HR_Pin, INPUT);
  Serial.begin (9600);
}

int hr  = 0
int GSR = 0
void loop ()
{
  digitalWrite(output_GSR_Pin, HIGH);
  
  hr = analogRead (input_HR_Pin);
  GSR = analogRead(input_GSR_Pin);'
  
  Serial.print(GSR);
  Serial.print (",");
  Serial.println(hr);
}
