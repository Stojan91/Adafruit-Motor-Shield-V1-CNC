#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <AFMotor.h>

extern AF_Stepper stepperX;
extern AF_Stepper stepperY;

void initializeMotors();
void moveLinear(int stepsX, int stepsY, int speed);
void moveArc(float xPos, float yPos, float iPos, float jPos, int direction); // Deklaracja jest poprawna
void moveHome();
void setSpeed(int speedX, int speedY);
void setUnitsMetric();
void setUnitsInches();

void processLinearMove(String command);
void processArcMove(String command);

// Specjalne cykle
void performPeckDrilling(float depth, float retract, int feedRate);
void performThreading(float pitch, int passes, float depthPerPass, int feedRate);
void performGrooving(float width, float depth, float stepDepth, int feedRate);
void performRoughing(float totalDepth, float passes, int feedRate);
void performFinishing(int feedRate);

#endif
