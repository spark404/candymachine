
int startled = 2;
int numberofleds = 9;
int numberofrows = 3;
int numberofcolumns = 3;
int actioninput = 12;
long previousMillis = 0; 
long interval = 1000;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(actioninput, INPUT);
  
  int led = startled;
  while (led <= (startled+numberofleds)) {
    pinMode(led, OUTPUT);     
    led++;
 }
 Serial.begin(9600);
 previousMillis = 0 -interval; //Hack to start blinking right away
}


// the loop routine runs over and over again forever:
void loop() {
  int actionstate = digitalRead(actioninput);
  if (actionstate == HIGH) {
    doaction();
  }
  else {
    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis > interval) {
      previousMillis = currentMillis;   
      switch (random(4)) {  //pick a random action
        case 1:
          inout();
          inout();
          inout();
          break;
        case 2:
          ledrun();
          ledrun();
          ledrun();
          break;
        case 3:
          verticalwave();
          verticalwave();
          verticalwave();
          break;
        case 4:
          outin(200);
          outin(200);
          outin(200);
          break;
        case 0:
          horizontalwave();
          horizontalwave();
          horizontalwave();
          break;
        default:
          horizontalwave();
          horizontalwave();
          horizontalwave();
          break;
        }
      }
  }  
}


void doaction ()
{
  inout();
  inout();
  inout();
  ledrun ();
  verticalwave();
  verticalwave();
  verticalwave();
  horizontalwave();
  outin(200);
  outin(150);
  for (int x=0; x<25 ;x++)
    outin(75);
  int actionstate = digitalRead(actioninput);
  while (actionstate == HIGH) {
    arrow();
    delay(500);
    int actionstate = digitalRead(actioninput);
  }
}


void arrow()
{
  shinebitleds(351);
  delay (500);
  dimleds();
}

void outin (int patternspeed)
{
  shinebitleds(495);
  delay (patternspeed);
  dimleds();
  shinebitleds(16);
  delay (patternspeed);
  dimleds();
  delay(patternspeed);
}

void inout ()
{
  shinebitleds(16);
  delay (200);
  dimleds();
  shinebitleds(495);
  delay (200);
  dimleds();
  delay(200);
}
void horizontalwave()
{
  int y=7;
   for (int x=0; x < (numberofrows); x++) {
   shinebitleds(y);
   delay (200);
   y = y  << 3;
   dimleds();
   
 }
 delay (200);

 y = y >> 3; 
 
 for (int x=numberofrows ; x > 0; x--) {
   shinebitleds(y);
   delay (200);
   y = y  >> 3;
   dimleds();
   
 }
 delay (200);
 
}

void verticalwave()  
{
 int y=73;
 for (int x=0; x < (numberofcolumns); x++) {
   shinebitleds(y);
   delay (200);
   y = y  << 1;
   dimleds();
   
 }
 delay (200);
 y = y >> 1;
 for (int x=numberofcolumns; x >0 ; x--) {
   shinebitleds(y);
   delay (200);
   y = y  >> 1;
   dimleds();
   
 }
 delay (200); 
}

void ledrun() {
  int y=1;
  for (int x=0; x < numberofleds; x++) {
    shinebitleds(y);
    delay (100);
    y = y  << 1;
    dimleds();
  }
}

void shinebitleds (int ledbitmask) {
 for (int led = 0; led < numberofleds; led++) {
   if (ledbitmask & 1)
     digitalWrite ((led+startled), HIGH);
   ledbitmask = ledbitmask >> 1;
 }
}

void dimleds () {
 for (int led = startled; led < (startled+numberofleds); led++) 
     digitalWrite (led, LOW);
}
