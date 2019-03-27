//Code written by Jesper Wædeled Henriksen for master thesis project at Aalborg University, 2019
//This code measures heartrate and sends it to serial port.

void setup ( )
{
  pinMode(A0, INPUT); //HR
  pinMode(A2, INPUT); //GSR
  analogReference(DEFAULT);
  Serial.begin (9600);
}

float hr  = 0;
float GSR = 0;
void loop ()
{  
  hr = analogRead (A0);
  GSR = analogRead(A2);
  delay(50);
  //Serial.println(GSR);
  Serial.println(String(GSR)+','+String(hr));
}
