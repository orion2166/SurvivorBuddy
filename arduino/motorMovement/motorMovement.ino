#include <VarSpeedServo.h>

//Control and Feedback Pins
//regular 180 servos
int leftBasePin = 9; 
int rightBasePin = 10; 
int leftBaseFeedback = A0; 
int rightBaseFeedback = A1; 

//360 servo
int turnTablePin = 3;
int turnTableFeedback  = 11;

//180 mini servo
int phoneMountPin =6;
int phoneMountFeedback = A4;

int ledPin = 2;

// Position constants
const int RIGHT_BASE_DOWN = 55; //REDUNDANT LW
const int RIGHT_BASE_UP = 138; //REDUNDANT LW
const int LEFT_BASE_DOWN = 110; //GOOD LW
const int LEFT_BASE_UP = 40; //GOOD LW
const int PHONEMOUNT_LANDSCAPE = 98;
const int PHONEMOUNT_MAX_TILT = 20; //NEED CONSTANT LW
const int TABLETOP_OFFSET = 65; //GOOD LW
const int TABLETOP_FRONT = 90; //GOOD LW
const int TABLETOP_LEFT = 180+TABLETOP_OFFSET; //GOOD LW
const int TABLETOP_RIGHT = 0+TABLETOP_OFFSET; //GOOD LW

// Feedback constants
const int RIGHT_BASE_FB_DOWN = 186; //NEED CONSTANT LW
const int RIGHT_BASE_FB_UP = 369; //NEED CONSTANT LW
const int LEFT_BASE_FB_DOWN = 415; //NEED CONSTANT LW
const int LEFT_BASE_FB_UP = 235; //NEED CONSTANT LW
const int PHONEMOUNT_FB_PORTRAIT = 0; //REDUNDANT LW
const int PHONEMOUNT_FB_LANDSCAPE = 0; //NEED CONSTANT LW


//Create VarSpeedServo objects 
VarSpeedServo leftBaseServo;
VarSpeedServo rightBaseServo;
VarSpeedServo tabletopServo;
VarSpeedServo phoneMountServo;

enum Command {PITCH, YAW, ROLL, CLOSE, OPEN, PORTRAIT, 
              LANDSCAPE, NOD, SHAKE, TILT, SHUTDOWN};

/*******************************************************************/
/*Phone Mount Functions*/
//void portrait(){ //phoneMountServo moves phone to portrait position
//    phoneMountServo.write(PHONEMOUNT_PORTRAIT, 40, true);
//}

void landscape(){ //phoneMountServo moves phone to landscape position
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE, 40, true);
}

void tilt() {
  int currAngle = phoneMountServo.read();
  for(int i =0; i < 3; i++){
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE+PHONEMOUNT_MAX_TILT, 60, true);
    delay(500);
    phoneMountServo.write(PHONEMOUNT_LANDSCAPE-PHONEMOUNT_MAX_TILT, 60, true);
    delay(500);
  }
  phoneMountServo.write(currAngle, 60, true);
}

/*
 * Get current position of Phone Mount Servo
*/
int getPositionPM(){
  int potVal = analogRead(phoneMountFeedback);
  return map(potVal, PHONEMOUNT_FB_PORTRAIT, PHONEMOUNT_FB_LANDSCAPE, 0, 90);
}
/*******************************************************************/
/*Base Motor Functions*/
/*
 * Get current position of Base Servos
*/
int getPositionBM(){
//  int potValLeft = analogRead(leftBaseFeedback);
//  int leftAngle = map(potValLeft, LEFT_BASE_FB_DOWN, LEFT_BASE_FB_UP, 0, 90);
  int potValRight = analogRead(rightBaseFeedback);
  int rightAngle = map(potValRight, RIGHT_BASE_FB_DOWN, RIGHT_BASE_FB_UP, 0, 90);
  return rightAngle;
}

// 360 parallax constants
const unsigned long unitsFC = 360; // 360 degrees in a circle
const unsigned long dcMin = 29;
const unsigned long dcMax = 971;
const unsigned long dutyScale = 1000;
// not constants, but don't want to have to declare them a lot
unsigned long tCycle, tHigh, tLow, dc;
unsigned long theta;

int getPositionTabletop(){
  int tCycle = 0;
  int tHigh, tLow, theta, dc;
  while (1) {
    tHigh = pulseIn(turnTableFeedback, HIGH);
    tLow = pulseIn(turnTableFeedback, LOW);
    tCycle = tHigh + tLow;
    if ((tCycle > 1000) && (tCycle < 1200)) {
      break;
    }
  }
  dc = (dutyScale * tHigh) / tCycle;
  theta = ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  if (theta < 0) {
    theta = 0;
  }
  else if (theta > (unitsFC - 1)) {
    theta = unitsFC - 1;
  }
  
  if(theta < 180){
      theta = map(theta, TABLETOP_RIGHT, 0, 0, TABLETOP_RIGHT);
      if( theta < 0){
        theta = 0;
      }
      if( theta > TABLETOP_RIGHT){
        theta = TABLETOP_RIGHT;
      }
  }
  else if (theta > 180){
    theta = map(theta, 359, TABLETOP_LEFT, TABLETOP_RIGHT+1, 180);
    if(theta < TABLETOP_RIGHT +1){
      theta = TABLETOP_RIGHT +1;
    }
    if( theta > 180)
      theta = 180;
  }
  
  return theta;
}

void up(){
  leftBaseServo.write(LEFT_BASE_UP, 40);
  rightBaseServo.write(RIGHT_BASE_UP, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void down(){
  leftBaseServo.write(LEFT_BASE_DOWN, 40);
  rightBaseServo.write(RIGHT_BASE_DOWN, 40);
  leftBaseServo.wait();
  rightBaseServo.wait();
}
void nod(){
  //up down, arm nods twice
  int currAngleLeft = leftBaseServo.read();
  int currAngleRight = rightBaseServo.read();
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  rightBaseServo.write(70, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(70, 60);
  rightBaseServo.write(70, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  delay(100);
  leftBaseServo.write(LEFT_BASE_UP, 60);
  rightBaseServo.write(RIGHT_BASE_UP, 60);
  leftBaseServo.wait();
  rightBaseServo.wait();
  leftBaseServo.write(currAngleLeft, 60, true);
  rightBaseServo.write(currAngleRight, 60, true);
}
/*******************************************************************/
/*Turn Table Motor Functions*/
void shake(){
  int currPos = getPositionTabletop();
  for(int i = 0; i < 3; i++){
    setYaw(45);
    delay(100);
    setYaw(45+90);
    delay(100);
  }
  setYaw(currPos);
}

void _shutdown() {
  setYaw(TABLETOP_FRONT);
  landscape();
  delay(100);
  down();
  delay(100);
  // blink LED then off
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPin, LOW);
    delay(500);
    digitalWrite(ledPin, HIGH);
    delay(500);
  }
  sendPosition();
  //stop all motor movement. will need to unplug and plug back in to move again
  //while(true) {}
}

/*Emergency Shut Down*/
void emergencyShutdown(){
  //stop all motor movement. will need to unplug and plug back in to move again
  while(true) {}
}

void setPitch(char val) {
  int leftVal = map(val, 0, 90, LEFT_BASE_DOWN, LEFT_BASE_UP);
  int rightVal = map(val, 0, 90, RIGHT_BASE_DOWN, RIGHT_BASE_UP);
  leftBaseServo.write(leftVal, 40);
  rightBaseServo.write(rightVal, 40);
}

void setYaw(int val) {
//  int offset = 0;
  int currPos = getPositionTabletop();
  if (val > currPos) {
    tabletopServo.writeMicroseconds(1555);
    while (val > currPos + 10) {
      currPos = getPositionTabletop();
    }
    tabletopServo.writeMicroseconds(1540);
    while (val > currPos+2) {
      currPos = getPositionTabletop();
    }
  }
  else if (val < currPos) {
    
    tabletopServo.writeMicroseconds(1430);
    while (val < currPos - 10) {
      currPos = getPositionTabletop();
    }
    tabletopServo.writeMicroseconds(1440);
    while (val < currPos-2) {
      currPos = getPositionTabletop();
    }
  }
  tabletopServo.writeMicroseconds(1500);
}

void setRoll(char val) {
  int pos = map(val, 0, 90, PHONEMOUNT_LANDSCAPE - PHONEMOUNT_MAX_TILT, PHONEMOUNT_LANDSCAPE + PHONEMOUNT_MAX_TILT);
  phoneMountServo.write(pos, 40, true);
}

void sendPosition() {
  char pos[3]; // [pitch, yaw, roll]
  pos[0] = map(leftBaseServo.read(), LEFT_BASE_DOWN, LEFT_BASE_UP, 0, 90);
  pos[1] = map(getPositionTabletop(), 0, 180, 0, 180); //[REDUNDANT]
  pos[2] = map(phoneMountServo.read(), PHONEMOUNT_LANDSCAPE-PHONEMOUNT_MAX_TILT, PHONEMOUNT_LANDSCAPE+PHONEMOUNT_MAX_TILT, 0, 90);
  Serial.write(pos, 3);
}

void test() {
  shake();
  delay(1000);
}

/*******************************************************************/
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // feedback pins
  pinMode(leftBaseFeedback, INPUT);
  pinMode(rightBaseFeedback, INPUT);
  pinMode(turnTableFeedback, INPUT);
  pinMode(phoneMountFeedback, INPUT);
  
  // attaches the servo on pin to the servo object
  tabletopServo.attach(turnTablePin);
  setYaw(TABLETOP_FRONT);
  leftBaseServo.attach(leftBasePin);  
  leftBaseServo.write(LEFT_BASE_DOWN, 60, true);
  rightBaseServo.attach(rightBasePin);
  phoneMountServo.attach(phoneMountPin);
  phoneMountServo.write(PHONEMOUNT_LANDSCAPE);
}

//Serial Data
unsigned char serialData[128];
unsigned long numLoops = 0;
int lastYaw = TABLETOP_FRONT;

void loop() {
  // try to keep tabletopServo from jerking
//  setYaw(lastYaw);
//  tabletopServo.writeMicroseconds(1510);
//  test();
  
  numLoops++;
  if (Serial.available() > 0) {//serial is reading stuff 
    Serial.readBytes(serialData, 2); 
    if (serialData[0] == 0x00) { // set pitch
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setPitch(serialData[1]);
      }
    }
    else if (serialData[0] == 0x01) { // set yaw
      if (0 <= serialData[1] && serialData[1] <= 180) {
        lastYaw = map(serialData[1], 0, 180, 0, 180); //#####REDUNDANT#####
        setYaw(lastYaw);
      }
    }
    else if (serialData[0] == 0x02) { // set roll
      if (0 <= serialData[1] && serialData[1] <= 90) {
        setRoll(serialData[1]);
      }
    }
    else if(serialData[0] == 0x03){ // close 
      down();
    }
    else if (serialData[0] == 0x04){ // open
      up();
    }
//    else if(serialData[0] == 0x05){ // portrait
//      portrait();
//    }
    else if (serialData[0] == 0x06){ // landscape
      landscape();
    } 
    else if(serialData[0] == 0x07){ // nod
      nod();
    }
    else if (serialData[0] == 0x08){ // shake
      lastYaw = TABLETOP_FRONT;
      shake();
    }
    else if(serialData[0] == 0x09){ // tilt
      tilt();
    }
    else if (serialData[0] == 0x10) { // shutdown
      _shutdown();
    }
  }
  if (numLoops % 100 == 0) {
    setYaw(lastYaw);
    sendPosition();
    numLoops = 0;
  }
  
  delay(10);
} //end loop

//void loop() {
//  //setYaw(0);
//  Serial.print(" ");
//  Serial.print(getPositionTabletop());
//  delay(2000);
//}