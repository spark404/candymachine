/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int startled = 2;
int numberofleds = 9;
int numberofrows = 3;
int numberofcolumns = 3;
// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  int led = startled;
  while (led <= (startled+numberofleds)) {
    pinMode(led, OUTPUT);     
    led++;
 }
}

// the loop routine runs over and over again forever:
void loop() {
  //digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  outin(500);
  outin(200);
  outin(150);
  for (int x=0; x<25 ;x++)
    outin(100);
  delay (1000);
  inout();
  inout();
  inout();
  
  ledrun ();
  verticalwave();
  verticalwave();
  verticalwave();
  horizontalwave();
//    shinebitleds(x);
//    delay(100);               // wait for a second
//    dimleds();    // turn the LED off by making the voltage LOW
//    delay(100);               // wait for a second
  
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
