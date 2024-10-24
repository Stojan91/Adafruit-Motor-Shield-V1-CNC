#include <Arduino.h>
#include "GCodeParser.h"
#include "MotorControl.h"
#include "Config.h"

void processGCode(String command) {
    if (command.startsWith("G0") || command.startsWith("G1")) {
        processLinearMove(command);
    } else if (command.startsWith("G2") || command.startsWith("G3")) {
        processArcMove(command); // Teraz poprawnie zadeklarowane i dostępne
    } else if (command.startsWith("G20")) {
        setUnitsInches();
    } else if (command.startsWith("G21")) {
        setUnitsMetric();
    } else if (command.startsWith("G28")) {
        moveHome();
    } else if (command.startsWith("G74")) {
        performPeckDrilling(10, 1, 50);
    } else if (command.startsWith("G32") || command.startsWith("G76")) {
        performThreading(1.5, 5, 0.2, 100);
    } else if (command.startsWith("G75")) {
        performGrooving(10, 5, 1, 50);
    } else if (command.startsWith("G71")) {
        performRoughing(5, 5, 100);
    } else if (command.startsWith("G70")) {
        performFinishing(100);
    } else {
        Serial.println("Unknown command: " + command);
    }
}
