int pulse=0; 
int value=0; 
// pulse 1000 30cm
  void setup()  
  { 
   pinMode(6, OUTPUT); //Enable 
   pinMode(5, OUTPUT); //Step 
   pinMode(4, OUTPUT); //Direction 
  
   digitalWrite(6,LOW); 
   Serial.begin(9600);
   Serial.setTimeout(1);
  } 

void loop()  
{ 
  if (Serial.available())
  {
   value = Serial.parseInt();
   pulse = (value*100)/3
   if(pulse > 0)
   {
    digitalWrite(4,HIGH); 
    
    for(pulse ; pulse > 0; pulse--) 
    { 
      digitalWrite(5,HIGH); 
      delayMicroseconds(500); 
      digitalWrite(5,LOW); 
      delayMicroseconds(200); 
     }
    
   }

    if (pulse <0)
    {
     digitalWrite(4,LOW); 
     for(pulse ; pulse < 0; pulse++) 
     { 
      digitalWrite(5,HIGH); 
      delayMicroseconds(500); 
      digitalWrite(5,LOW); 
      delayMicroseconds(200); 
     }
    }
  }
  
  } 

