//Code written by Jesper Wædeled Henriksen for master thesis project at Aalborg University, 2019
//This code measures heartrate and sends it to serial port.

int output_Pin = A0;                               
double alpha = 0.75;
double change = 0.0;
static double prevValue = 0;

void setup ( )                     
{
  Serial.begin (9600);          
}

void loop ()
{
    int rawValue = analogRead (output_Pin);                          
    double value = alpha * prevValue + (1 - alpha) * rawValue;       

    Serial.print (rawValue);
    Serial.print (",");                                                                                          
    Serial.println (value);
    prevValue = value;
} 
