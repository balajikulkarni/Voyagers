
int8_t answer;
char aux_str[50];

char server[ ]="api.xively.com";
char port[ ]="8081";
String temperature = "2";
String humidity = "5";

String TCP_message ="{\"method\": \"put\",\"resource\": \"/feeds/***********/\",\"params\": {},\"headers\": {\"X-ApiKey\":  \"n49PBBOVhNjACyzWm6T5vuOwLXyudiYhtI5eoaE3pQVdrame\"},\"body\": {\"version\": \"1.0.0\",\"datastreams\": [{\"id\": \"Humidity\",\"current_value\": \"" + humidity + "\"},{\"id\": \"Temperature\",\"current_value\": \"" + temperature + "\"}]}}";

void setup(){
  
    Serial.begin(115200);   
    
    Serial.println("Starting Config");
    power_on();
    
    delay(3000);
    
    // sets the PIN code
    sendATcommand("AT+CPIN", "OK", 2000);
    
    delay(3000);
    
    while( (sendATcommand("AT+CREG?", "+CREG: 0,1", 500) || 
            sendATcommand("AT+CREG?", "+CREG: 0,5", 500)) == 0 );
    
    // sets APN, user name and password
    sendATcommand("AT+CGSOCKCONT=1,\"airtelgprs.com\"", "OK", 2000);
    sendATcommand("AT+CSOCKAUTH=1,1,\"\",\"\"", "OK", 2000);
   

}
void loop(){
    
  char message_TCP [300];
  TCP_message.toCharArray(message_TCP, 300); // converting TCP_message to char inorder for it to pass through AT command

  sprintf(aux_str, "AT+NETOPEN=\"TCP\",%s", port);
  answer = sendATcommand(aux_str, "Network opened", 20000);
    
    if (answer == 1)
    {
        Serial.println("Network opened");
        sprintf(aux_str, "AT+TCPCONNECT=\"%s\",%s", server, port);
        answer = sendATcommand(aux_str, "Connect ok", 20000);
        if (answer == 1)
        {
            Serial.println("Socket opened");
            
            String humidity = "18";
            String temperature = "30";
            String writeAPIKey = "n49PBBOVhNjACyzWm6T5vuOwLXyudiYhtI5eoaE3pQVdrame";
            
            sprintf(aux_str, "AT+TCPWRITE=%d", strlen(message_TCP));
           
            answer = sendATcommand(aux_str, ">", 20000);
              if (answer == 1)
            {
                sendATcommand(message_TCP, "Send OK", 20000);                
            }

            sendATcommand("AT+NETCLOSE", "OK", 20000);

        }
        else
        {
            Serial.println("Error opening the socket");    
        }
    }
    else
    {
        Serial.println("Error opening the network");    
    }

}

void power_on(){

    uint8_t answer=0;
    
    // checks if the module is started
    answer = sendATcommand("AT", "OK", 2000);
    if (answer == 0)
    {
        // waits for an answer from the module
        while(answer == 0){    
            answer = sendATcommand("AT", "OK", 2000);    
        }
    }   
}

int8_t sendATcommand(char* ATcommand, char* expected_answer1,
        unsigned int timeout)
{

    uint8_t x=0,  answer=0;
    char response[100];
    unsigned long previous;

    memset(response, '\0', 100);    // Initialize the string
    
    delay(100);
    
    while( Serial.available() > 0) 
		   Serial.read();    // Clean the input buffer
    
    Serial.println(ATcommand);    // Send the AT command 

    x = 0;
    previous = millis();

    // this loop waits for the answer
    do{
		if(Serial.available() != 0){    
            response[x] = Serial.read();
            x++;
            // check if the desired answer is in the response of the module
            if (strstr(response, expected_answer1) != NULL)    
            {
                answer = 1;
            }
        }
        // Waits for the asnwer with time out
    }while((answer == 0) && ((millis() - previous) < timeout));    

    return answer;
}
