//libraries
#include "SD.h" 

// Definitions
#define DEBUG_MODE false
#define SD_CARD_ATTACHED true
#define CALIBRATION_DONE false

#define WAIT_MILLISECONDS 15000 //840000
#define NUM_READINGS 60

#define POS_NINETY_PIN A0 //red
#define POS_FORTY_PIN A1 //green
#define NEG_FORTY_PIN A2 //blue
#define NEG_NINETY_PIN A3 //yellow
#define RELAY_PIN 5
#define INDICATOR_PIN 3

#if SD_CARD_ATTACHED
  Sd2Card card; //Setting up SD Card
  SdVolume volume;
  SdFile root;
  File DataFile; 
#endif  // SD_CARD_ATTACHED

unsigned long RawSensorSum = 0;
unsigned long PosNinetyVal = 0;
unsigned long NegNinetyVal = 0;
unsigned long PosFortyFiveVal = 0;
unsigned long NegFortyFiveVal = 0;

unsigned long PosNinety = 0;
unsigned long NegNinety = 0;
unsigned long PosForty = 0;
unsigned long NegForty = 0;

unsigned long NinetyVal = 0;
unsigned long FortyFiveVal = 0;

unsigned long Ninety = 0;
unsigned long Forty = 0;

unsigned long PreviousMillis = 0;
unsigned long CurrentMillis = 0;

String name = "APRCAL.txt";
void setup() {
  // put your setup code here, to run once:
#if DEBUG_MODE
  Serial.begin(9600);
  Serial.println("\n\nArduino is ready!"); //printing to serial monitor
  Serial.print("Initializing SD card...");
#endif // DEBUG_MODE
pinMode(RELAY_PIN, OUTPUT);
pinMode(INDICATOR_PIN,OUTPUT);
delay(1000);
digitalWrite(INDICATOR_PIN, HIGH);
delay(2000);
digitalWrite(INDICATOR_PIN, LOW);
#if SD_CARD_ATTACHED
  if (!SD.begin(10)) {
    #if DEBUG_MODE
    Serial.println("initialization failed!");
    #endif
    delay(1000);
    digitalWrite(INDICATOR_PIN, HIGH);
    delay(1000);
    while (1);
  }
  #if DEBUG_MODE
  Serial.println("initialization done.");
  #endif
  DataFile = SD.open(name,FILE_WRITE); //creating a file, ensuring its open and writing to it
  if (DataFile) {
    #if DEBUG_MODE
      Serial.print("Writing to DataFile...");
    #endif
    #if CALIBRATION_DONE
    DataFile.println("\nRelative Time, + 90 Degrees, + 45 Degrees, - 45 Degrees, - 90 Degrees, Raw Sum, Adjusted Turbidity");
    #else
    DataFile.println("\nRelative Time, + 90 Degrees, + 45 Degrees, - 45 Degrees, - 90 Degrees, Raw Sum");
    #endif
    // close the file:
    DataFile.close();
    #if DEBUG_MODE
      Serial.println("done.");
    #endif
  } 
  else {
    // if the file didn't open, print an error:
  #if DEBUG_MODE
      Serial.println("error opening datafile");
      delay(1000);
      digitalWrite(INDICATOR_PIN, HIGH);
  #endif  // DEBUG_MODE
  }
#endif
  digitalWrite(RELAY_PIN, HIGH); //turning LED on
}
void loop() {
  // put your main code here, to run repeatedly:
  float RawSensorAverage = 0;
  float PosNinetyAverage= 0;
  float NegNinetyAverage= 0;
  float PosFortyFiveAverage = 0;
  float NegFortyFiveAverage = 0;

  float NinetyAverage= 0;
  float FortyFiveAverage = 0;
  #if CALIBRATION_DONE
  float NTU = 0;
  #endif
  PosFortyFiveVal = 0;
  NegFortyFiveVal = 0;
  PosNinetyVal = 0;
  NegNinetyVal = 0;

  RawSensorSum = 0;
  FortyFiveVal = 0;
  NinetyVal = 0;

  // Main Analog Data Acquisition Loop ---------
  for (int i = 0; i < NUM_READINGS; i++){
    PosNinety = analogRead(POS_NINETY_PIN);
    NegNinety = analogRead(NEG_NINETY_PIN);
    PosForty = analogRead(POS_FORTY_PIN);
    NegForty = analogRead(NEG_FORTY_PIN);
    PosNinetyVal += PosNinety;
    NegNinetyVal += NegNinety;
    PosFortyFiveVal += PosForty;
    NegFortyFiveVal += NegForty;
    #if DEBUG_MODE
      Serial.println("Ninety: "+ String(PosNinety) + ", " + String(NegNinety) + " FourtyFive: "+ String(PosForty) + ", " + String(NegForty));
    #endif
    delay(500);
  }
  
  RawSensorSum = PosNinetyVal + NegNinetyVal + PosFortyFiveVal + NegFortyFiveVal;
  RawSensorAverage = RawSensorSum / NUM_READINGS;  // This is the single signal data point
  PosNinetyAverage = PosNinetyVal / NUM_READINGS;
  NegNinetyAverage = NegNinetyVal / NUM_READINGS;
  PosFortyFiveAverage = PosFortyFiveVal / NUM_READINGS;
  NegFortyFiveAverage = NegFortyFiveVal / NUM_READINGS;

  PreviousMillis = CurrentMillis;
  CurrentMillis = millis();
  unsigned long ElapsedMillis = CurrentMillis-PreviousMillis;  // This is the timestamp for the duration since the last data point

  #if SD_CARD_ATTACHED 
  DataFile = SD.open(name,FILE_WRITE); //reopening data file
    #if DEBUG_MODE
      if (!DataFile){
        Serial.println("Data File Couldn't Open?");
      }else{
        Serial.println("Data File Open!");
      }
    #endif
  DataFile.print("\n");
  DataFile.print(ElapsedMillis);
  DataFile.print(",");
  DataFile.print(PosNinetyAverage);
  DataFile.print(",");
  DataFile.print(PosFortyFiveAverage);
  DataFile.print(",");
  DataFile.print(NegFortyFiveAverage);
  DataFile.print(",");
  DataFile.print(NegNinetyAverage);
  DataFile.print(",");
  DataFile.print(RawSensorAverage);
  #if CALIBRATION_DONE
  DataFile.print(",");;
  DataFile.print(NTU);
  #endif
  #if DEBUG_MODE
    Serial.print("Time: " + String(ElapsedMillis)+ "," + " Ninety: "+ String(PosNinety) + ", " + String(NegNinety) + " FortyFive: "+ String(PosForty) + ", " + String(NegForty) + ", " + String(RawSensorAverage));
    #if CALIBRATION_DONE
    Serial.print(", " + String(NTU));
    #endif
    Serial.println("/n");
  #endif
  DataFile.close();
  #if DEBUG_MODE
  if (!DataFile){
      Serial.println("Data File Closed!");
      Serial.println("Data Written!");
    }else{
      Serial.println("Data File Couldn't Close?");
    }
  #endif
  #endif 
  delay(WAIT_MILLISECONDS);
}
