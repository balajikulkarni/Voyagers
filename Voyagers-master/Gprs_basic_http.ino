#include "SIM900.h"
 
#include <SoftwareSerial.h>
 
#include "inetGSM.h"
 
InetGSM inet;
 
int k=0;
 
int j=0;
 
char str[]="Date: ";
 
char msg[50];
 
boolean found=false;
 
char data;
 
int numdata;
 
char inSerial[50];
 
int i=0;
 
boolean started=false;
 
void setup()
 
{
 
//Serial connection.
 
Serial.begin(9600);
 
if (gsm.begin(2400)){
 
  Serial.println("\nstatus=READY");
 
  started=true;  
 
}
 
else Serial.println("\nstatus=IDLE");
 
if(started){
 
  if (inet.attachGPRS("internet.wind", "", ""))
 
    Serial.println("status=ATTACHED");
 
  else Serial.println("status=ERROR");
 
  delay(1000);
 
  numdata=inet.httpGET("www.google.com", 80, "/", msg, 50);
 
}
 
};
 
void loop()
 
{
 
data=gsm.read();
 
if(data>0){
 
  Serial.print(data);
 
  if(data==str[k]){
 
    k++;
 
    if(k+1==strlen(str)){
 
      found=true;
 
      msg[0]='\0';
 
      j=0;
 
    }
 
  }else{
 
    k=0;
 
  }
 
}
 
if(found){
 
  if(data!='\n'){
 
    if(data>0){
 
      msg[j]=data;
 
      j++;
 
    }
 
  }else{
 
    msg[j]=data;
 
    msg[j+1]='\0';
 
    found=false;
 
    Serial.print("DATA: ");
 
    Serial.println(msg);
 
  }
 
}
 
};
