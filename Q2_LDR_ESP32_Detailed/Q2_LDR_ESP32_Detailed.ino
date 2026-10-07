const int LDR_PIN = 34;

void setup() {
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);
}

void loop() {
  int ldrValue = analogRead(LDR_PIN);
  float voltage = (ldrValue * 3.3) / 4095.0;
  float lightPercent = (ldrValue / 4095.0) * 100.0;

  Serial.print("ADC: ");
  Serial.print(ldrValue);
  Serial.print(" | Voltage: ");
  Serial.print(voltage, 2);
  Serial.print("V | Light: ");
  Serial.print(lightPercent, 1);
  Serial.println("%");

  delay(1000);
}
