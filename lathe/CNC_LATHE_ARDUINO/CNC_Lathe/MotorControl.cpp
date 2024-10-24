#include <Arduino.h>
#include "MotorControl.h"
#include "Config.h"
#include <math.h>
#include <stdlib.h>

// Definicje silników krokowych
AF_Stepper stepperX(STEPS_PER_REVOLUTION, 1);
AF_Stepper stepperY(STEPS_PER_REVOLUTION, 2);

void initializeMotors() {
    stepperX.setSpeed(DEFAULT_SPEED_X);
    stepperY.setSpeed(DEFAULT_SPEED_Y);
}

void moveLinear(int stepsX, int stepsY, int speed) {
    setSpeed(speed, speed);
    if (stepsX != 0) {
        stepperX.step(abs(stepsX), stepsX > 0 ? FORWARD : BACKWARD, SINGLE);
    }
    if (stepsY != 0) {
        stepperY.step(abs(stepsY), stepsY > 0 ? FORWARD : BACKWARD, SINGLE);
    }
}

void processLinearMove(String command) {
    int xIndex = command.indexOf('X');
    int yIndex = command.indexOf('Y');
    int fIndex = command.indexOf('F');

    int stepsX = 0, stepsY = 0, feedrate = DEFAULT_SPEED_X;

    if (xIndex >= 0) {
        stepsX = command.substring(xIndex + 1).toInt() / UNITS_PER_STEP;
    }

    if (yIndex >= 0) {
        stepsY = command.substring(yIndex + 1).toInt() / UNITS_PER_STEP;
    }

    if (fIndex >= 0) {
        feedrate = command.substring(fIndex + 1).toInt();
    }

    moveLinear(stepsX, stepsY, feedrate);
}

void processArcMove(String command) {
    int xIndex = command.indexOf('X');
    int yIndex = command.indexOf('Y');
    int iIndex = command.indexOf('I');
    int jIndex = command.indexOf('J');

    float xPos = 0, yPos = 0, iPos = 0, jPos = 0;
    int direction = (command.startsWith("G2")) ? 1 : -1;

    if (xIndex >= 0) {
        xPos = command.substring(xIndex + 1).toFloat();
    }

    if (yIndex >= 0) {
        yPos = command.substring(yIndex + 1).toFloat();
    }

    if (iIndex >= 0) {
        iPos = command.substring(iIndex + 1).toFloat();
    }

    if (jIndex >= 0) {
        jPos = command.substring(jIndex + 1).toFloat();
    }

    moveArc(xPos, yPos, iPos, jPos, direction);
}

// Implementacja funkcji moveArc
void moveArc(float xPos, float yPos, float iPos, float jPos, int direction) {
    float centerX = iPos;
    float centerY = jPos;
    float radius = sqrt(pow(centerX, 2) + pow(centerY, 2));
    float startAngle = atan2(-centerY, -centerX);
    float endAngle = atan2(yPos - centerY, xPos - centerX);
    if (direction == -1 && endAngle > startAngle) {
        endAngle -= 2 * M_PI;
    } else if (direction == 1 && endAngle < startAngle) {
        endAngle += 2 * M_PI;
    }

    int segments = 100;
    for (int i = 0; i <= segments; i++) {
        float theta = startAngle + (endAngle - startAngle) * ((float)i / segments);
        float targetX = centerX + radius * cos(theta);
        float targetY = centerY + radius * sin(theta);
        int stepsX = targetX / UNITS_PER_STEP;
        int stepsY = targetY / UNITS_PER_STEP;
        moveLinear(stepsX, stepsY, DEFAULT_SPEED_X);
    }
}

// Pozostałe funkcje bez zmian

void setSpeed(int speedX, int speedY) {
    stepperX.setSpeed(speedX);
    stepperY.setSpeed(speedY);
}

void setUnitsMetric() {
    Serial.println("Units set to mm");
}

void setUnitsInches() {
    Serial.println("Units set to inches");
}

void moveHome() {
    stepperX.step(HOME_POSITION_STEPS, BACKWARD, SINGLE);
    stepperY.step(HOME_POSITION_STEPS, BACKWARD, SINGLE);
    Serial.println("Returning to home position.");
}

void performPeckDrilling(float depth, float retract, int feedRate) {
    for (float currentDepth = 0; currentDepth <= depth; currentDepth += retract) {
        moveLinear(0, currentDepth / UNITS_PER_STEP, feedRate);
        delay(500);
        moveLinear(0, -(retract / UNITS_PER_STEP), feedRate);
    }
    moveLinear(0, -depth / UNITS_PER_STEP, feedRate);
}

void performThreading(float pitch, int passes, float depthPerPass, int feedRate) {
    for (int pass = 0; pass < passes; pass++) {
        float depth = depthPerPass * (pass + 1);
        moveLinear(0, depth / UNITS_PER_STEP, feedRate);
        moveLinear(100 / UNITS_PER_STEP, 0, feedRate * pitch);
        moveLinear(-100 / UNITS_PER_STEP, 0, feedRate * pitch);
    }
}

void performGrooving(float width, float depth, float stepDepth, int feedRate) {
    for (float currentDepth = 0; currentDepth <= depth; currentDepth += stepDepth) {
        moveLinear(0, currentDepth / UNITS_PER_STEP, feedRate);
        moveLinear(width / UNITS_PER_STEP, 0, feedRate);
        moveLinear(-width / UNITS_PER_STEP, 0, feedRate);
    }
}

void performRoughing(float totalDepth, float passes, int feedRate) {
    float depthPerPass = totalDepth / passes;
    for (int i = 0; i < passes; i++) {
        moveLinear(0, depthPerPass * (i + 1) / UNITS_PER_STEP, feedRate);
        moveLinear(100 / UNITS_PER_STEP, 0, feedRate);
        moveLinear(-100 / UNITS_PER_STEP, 0, feedRate);
    }
}

void performFinishing(int feedRate) {
    moveLinear(100 / UNITS_PER_STEP, 0, feedRate);
}
