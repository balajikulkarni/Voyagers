#include<SoftwareSerial.h>
#define RxPin  2
#define TxPin  3
  
const int PushButton_InputPin = 7;  /* PushButton Input Switch connection */
  
/* Initialize the GPS String Array */
char inBuffer[300]="";
char GPS_RMC[100]="";
char GPS_GGA[100]="";
  
/* Configure Tx and Rx of the GPS connection*/
SoftwareSerial gps = SoftwareSerial(RxPin, TxPin);
  
void setup(){
/* Set up the serial Monitor Baud Rate */
Serial.begin(9600);
/* wait till the communication is set up */
while(!Serial);
                          
/* Set up the GPS communication Baud Rate 
   Baud Rates will change based on the GPS types used
   The below Baud rate is applicable for the Neo -6M GPS Module */

gps.begin(9600);
/* Initialize the Internal Pull-Ups for the Pushbutton digital input to avoid unnecessary voltage fluctuations
   Caution : Don't provide voltages below ground or voltage above the positive voltage reference of the Arduino Board(5V/3.3 V) */
pinMode(PushButton_InputPin, INPUT_PULLUP);
delay(1000);
}
  
void loop() {
/* Here two scenarios can happen :
1. User button press time is greater than the loop() function execution time, this will result in continous LOW read for multiple times(more than one loop() functions called during User press)
   and thus the GPS data may get repeated.
2. User button press time is less than Loop() function single runtime, in that manner it should be able to read only once.

An alternative approach here could be setting the User Input as Interrupt Input onn Falling edge of the Voltage pulse due to the User Button Press */  
  
if(LOW == digitalRead(PushButton_InputPin)){ /* Detect a button press */
 
  if(gps.available()){/* Check GPS availability */ 
    Serial.write(gps.read());
    /* TODO : Sending the data to the cloud for further action.
              Computing the overall runtime of one such Uset request */
  }
  else{
    /* Add code here for GPS Not Available */
  }
}
}
