#include "SIM900.h"
#include <SoftwareSerial.h>
#include "sms.h"

SMSGSM sms;
boolean started = false;
void setup()
{
  Serial.begin(9600);
  Serial.println("GSM Testing to send SMS");
  if (gsm.begin(2400)){
  Serial.println("\nstatus=READY");
  started=true;
  }
  else Serial.println("\nstatus=IDLE");
  
  if(started){
    if (sms.SendSMS("+91**********", "Arduino SMS Testing")){// number to which you want to send the sms and the sms text//
    //Serial.println("\nSMS sent OK at %d",time);
    }
  }
}

void loop()
{  
}
