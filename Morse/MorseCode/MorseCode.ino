const int button = 7;
const int greenLight = 6;
const int redLight = 5;
int lastTimePushed;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(greenLight, OUTPUT);
  pinMode(redLight, OUTPUT);
}


int lastTimepushed = 0;
int lastTimeReleased = 0;
boolean activated = false;
boolean newLetter = false;
boolean newWord = false;


void loop() {

  if(digitalRead(button) == HIGH){
    digitalWrite(redLight, LOW);
    digitalWrite(greenLight, HIGH);
    activated = true;
    
    if(lastTimePushed == 0){
      lastTimePushed = millis();
      lastTimeReleased = 0;
      newLetter = false;
      newWord = false;
    }
   
  }
  
  else if(digitalRead(button) == LOW && activated){
    
    digitalWrite(redLight, HIGH);
    digitalWrite(greenLight, LOW);
    
    if(lastTimePushed != 0){
      if(millis() - lastTimePushed < 500){
        Serial.print(0);
      }else{
        Serial.print(1);
      }
      lastTimePushed = 0;
      lastTimeReleased = millis();
    }
    if(millis() - lastTimeReleased == 1000 && !newLetter){
      newLetter = true;
      Serial.print(2);
    }else if(millis() - lastTimeReleased == 2500 && !newWord){
      newWord = true;
      Serial.print(3);
    }
  }
  
  
}
