#define PIN1  26
#define PIN2  25
#define PIN3  34
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}
void loop() {
  Serial.print(0);
  Serial.print(" "); 
  Serial.print(4096);
  Serial.print(" ");
  //Serial.print(millis());
  //Serial.print(" ");
  Serial.print(analogRead(PIN1));
  Serial.print(" ");
  Serial.print(analogRead(PIN2));
  Serial.print(" ");
  Serial.println(analogRead(PIN3));
  delay(1);
}