/*
Original code from:    
GSM Shield for Arduino    
www.open-electronics.org    
this code is based on the example of Arduino Labs.    
*/



#include "SIM900.h"
#include <SoftwareSerial.h>
#include "inetGSM.h"


InetGSM inet;

char msg[50];
int numdata;
char inSerial[50];
int i = 0;
boolean started = false;
long feedId = 226801;
char datastreamId[] = "1";
char sentMsg[50];

// ThingSpeak Settings
char thingSpeakAddress[] = "api.thingspeak.com";
char writeAPIKey[] = "CJATIDHMDEJD18U8";


void setup()
{
  Serial.begin(9600);
  Serial.println("GSM Shield testing.");
 
  startupGSM900();
    
}

void thingspeakPost() {

  char end_c[2];
  char itoaBuffer[8];
  end_c[0] = 0x1a;
  end_c[1] = '\0';


if (inet.connectTCP(thingSpeakAddress, 80)) {

   Serial.println("connected to thingspeak");

    gsm.SimpleWrite("POST /update HTTP/1.1\r\n");
    gsm.SimpleWrite("Host: api.thingspeak.com\r\n");
    gsm.SimpleWrite("Connection: close\r\n");
    gsm.SimpleWrite("X-THINGSPEAKAPIKEY: ");
    gsm.SimpleWrite(writeAPIKey);
    gsm.SimpleWrite("\r\n");
    gsm.SimpleWrite("Content-Type: application/x-www-form-urlencoded\r\n");
    gsm.SimpleWrite("Content-Length: ");
    sprintf(sentMsg, "Gprs=Balaji2");
    itoa(strlen(sentMsg), itoaBuffer, 10);

    gsm.SimpleWrite(itoaBuffer);

    gsm.SimpleWrite("\r\n\r\n");

    gsm.SimpleWrite(sentMsg);

    gsm.SimpleWrite("\r\n\r\n");

    gsm.SimpleWrite(end_c);

  }
  else
  {
  Serial.println("failed");
    startupGSM900();
  }
}



void startupGSM900() 
{ 
  if(gsm.begin(2400)) {
      Serial.println("\nstatus=READY");
      started = true;
  }
 else 
     Serial.println("\nstatus=IDLE");

 if(started) {
    gsm.SimpleWrite("AT");
    delay(1000);
    //GPRS attach, put in order APN, username and password.
    //If no needed auth let them blank.

    if (inet.attachGPRS("airtelgprs.com", "", ""))
        Serial.println("status=ATTACHED");
    else 
        Serial.println("status=ERROR");
    
    delay(1000);

    //Read IP address.
    gsm.SimpleWriteln("AT+CIFSR");

    delay(5000);

    //Read until serial buffer is empty.
    gsm.WhileSimpleRead();

  }
  
}

void loop()
{
  thingspeakPost();
  serialswread();
  delay(6000);
}

void serialswread(){
gsm.SimpleRead();
 
}
