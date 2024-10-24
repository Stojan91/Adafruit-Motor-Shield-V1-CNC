#include <Arduino.h>
#include "GCodeParser.h"
#include "MotorControl.h"
#include "Config.h"

void setup() {
    Serial.begin(9600); // Inicjalizacja komunikacji szeregowej
    initializeMotors(); // Inicjalizacja silników krokowych
    Serial.println("CNC Lathe Controller Ready");
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim(); // Usuwa białe znaki z początku i końca
        processGCode(command);
    }
}
