#include <SoftwareSerial.h>
SoftwareSerial gprsSerial(2,3);

void setup()
{
  gprsSerial.begin(2400);
  Serial.begin(9600);

  Serial.println("Configuring GSM..");
  delay(2000);
  Serial.println("Done!");
  gprsSerial.flush();
  Serial.flush();

  //Test if Board is Up
  gprsSerial.println("AT");
  delay(100);
  toSerial();
  
  //Test SIM is unlocked
  gprsSerial.println("AT+CPIN?");
  delay(100);
  toSerial();

  //Test Sim registration
  gprsSerial.println("AT+CREG?");
  delay(100);
  toSerial();

  //Test if GPRS Attached
  gprsSerial.println("AT+CGATT?");
  delay(100);
  toSerial();
  
  //Test Signal Strength ( > 9)
  gprsSerial.println("AT+CSQ");
  delay(100);
  toSerial();
  
  //Set connection type to GPRS
  gprsSerial.println("AT+SAPBR=3,1,\"Contype\",\"GPRS\"");
  delay(100);
  toSerial();
  
  
  //Set APN 
  gprsSerial.println("AT+SAPBR=3,1,\"APN\",\"airtelgprs.com\"");
  delay(2000);
  toSerial();

  //Enable GPRS ,this will take time
  gprsSerial.println("AT+SAPBR=1,1");
  delay(100);
  toSerial();

  Serial.println("Set Up Done..!");  
}


void loop()
{
   //Init HTTP
  gprsSerial.println("AT+HTTPINIT");
  delay(200);
  toSerial();
  
  //Set HTTP Profile Identifier
  gprsSerial.println("AT+HTTPPARA=\"CID\",1");
  delay(100);
  toSerial();
 
  //Set HTTP Parameters
  gprsSerial.println("AT+HTTPPARA=\"URL\",\"http://posttestserver.com/post.php\"");
  delay(100);
  toSerial();
  
  Serial.println("Connected to server");
  
  //Set HTTP Post Data size and timeout period
  gprsSerial.println("AT+HTTPDATA=100,10000");
  delay(200);
  toSerial();
  
  Serial.println("Posting Data");
  
  //Set Data to be POSTED
  gprsSerial.println("Hello Voyagers!");
  delay(500);
  toSerial();
  
  //POST the data and wait for response
  gprsSerial.println("AT+HTTPACTION=1");
  delay(500);
  toSerial();
  
  Serial.println("Posting Done.");
  
  //Read the response
  gprsSerial.println("AT+HTTPREAD");
  delay(100);
  toSerial();
  
  //Terminate HTTP Connection
  gprsSerial.println("AT+HTTPTERM");
  delay(100);
  toSerial();
  
  
}
void toSerial()
{
  while(gprsSerial.available()!=0)
  {
    Serial.write(gprsSerial.read());
  }
}
