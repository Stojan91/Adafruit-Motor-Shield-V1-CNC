#ifndef CONFIG_H
#define CONFIG_H

// Konfiguracja silników
#define STEPS_PER_REVOLUTION 200  // Liczba kroków na pełen obrót silnika krokowego
#define DEFAULT_SPEED_X 50        // Domyślna prędkość osi X (RPM)
#define DEFAULT_SPEED_Y 50        // Domyślna prędkość osi Y (RPM)
#define UNITS_PER_STEP 0.01       // Milimetry na jeden krok (dostosuj do swojego silnika)

// Prędkości różnych operacji
#define RAPID_SPEED 200           // Prędkość dla szybkich ruchów (G0)
#define HOME_POSITION_STEPS 1000  // Przykładowa liczba kroków do pozycji home

#endif
