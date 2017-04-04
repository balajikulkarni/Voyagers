#include <SoftwareSerial.h>
#include <String.h>
 
SoftwareSerial mySerial(2, 3);


float temp=0.0;
int  DEBUG= 1;
void setup()
{
  mySerial.begin(9600);               // the GPRS baud rate   
  Serial.begin(9600);    // the GPRS baud rate 
 
  delay(1000);
}
 
void loop()
{
      temp=analogRead(A0);
      temp=temp*0.4887;  
      delay(2);          
       Send2Pachube();
   
  if (mySerial.available())
    Serial.write(mySerial.read());
}
void Send2Pachube()
{
  mySerial.println("AT");
  Serial.println("AT");
  delay(1000);

  mySerial.println("AT+CPIN?");
  Serial.println("AT+CPIN?");
  delay(1000);

  mySerial.println("AT+CREG?");
  delay(1000);

  mySerial.println("AT+CGATT?");
  delay(1000);

  mySerial.println("AT+CIPSHUT");
  if(DEBUG)
    Serial.println("AT+CIPSHUT");
  
  
  
  delay(1000);

  mySerial.println("AT+CIPSTATUS");
  if(DEBUG)
    Serial.println("AT+CIPSTATUS");
  delay(2000);

  mySerial.println("AT+CIPMUX=0");
  if(DEBUG)
    Serial.println("AT+CIPMUX=0");
  
  delay(2000);
 
  ShowSerialData();
 
  mySerial.println("AT+CSTT=\"airtelgprs.com\"");//start task and setting the APN,
  if(DEBUG)
    Serial.println("AT+CSTT=\"internet\"");

  delay(1000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIICR");//bring up wireless connection
  if(DEBUG)
    Serial.println("AT+CIICR");

  delay(3000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIFSR");//get local IP adress
  if(DEBUG)
    Serial.println("AT+CIFSR");
  
  delay(2000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSPRT=0");
  delay(3000);
 
  ShowSerialData();
  
  mySerial.println("AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"");//start up the connection
  if(DEBUG)
    Serial.println("AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"");
  delay(6000);
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSEND");//begin send data to remote server
  if(DEBUG)
    Serial.println("AT+CIPSEND");

  delay(4000);
  ShowSerialData();
  
  String str="GET http://api.thingspeak.com/update?api_key=LV3MK01BLC5HQ363&field1=" + String(temp);
  if(DEBUG)
    Serial.println("GET http://api.thingspeak.com/update?api_key=LV3MK01BLC5HQ363&field1=");
  mySerial.println(str);//begin send data to remote server
  delay(4000);
  ShowSerialData();

  mySerial.println((char)26);//sending
  
  delay(5000);//waitting for reply, important! the time is base on the condition of internet 
  mySerial.println();
 
  ShowSerialData();
 
  mySerial.println("AT+CIPSHUT");//close the connection
  Serial.println("AT+CIPSHUT");
  delay(100);
  ShowSerialData();
} 
void ShowSerialData()
{
  while(mySerial.available()!=0)
    Serial.write(mySerial.read());
}
