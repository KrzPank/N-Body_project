## Wymagania

- **Python 11.x** (wymagany – projekt wykorzystuje biblioteke dostępną tylko w tej wersji),
- requirements.txt


# N-Body Simulation

Aplikacja zawiera symulację układów n-body z detekcją kolizji w czasie rzeczywistym.

## Sterowanie

- **W / A / S / D** – poruszanie się kamerą w poziomie
- **Spacja** – ruch kamery w górę
- **Lewy Ctrl** – ruch kamery w dół
- **Przytrzymanie lewego przycisku myszy** – obracanie kamery

## GUI

W interfejsie graficznym dostępne są trzy predefiniowane przykłady symulacji:

- **Earth-Moon** – symulacja Ziemi i Księżyca
- **Mini Solar System** – uproszczony model małego układu planetarnego
- **Three Body Figure-8** – klasyczny układ trzech ciał poruszających się po trajektorii w kształcie ósemki

Można również modyfikować parametry fizyczne symulacji takie jak grawitacja, prędkość symulacji oraz sprężystość odbicia (1 - idealnie elastyczne odbicie, 0 - brak odbicia) w czasie rzeczywistym.

## Tryb własnych obiektów

Za pomocą paska nawigacyjnego można przejść do drugiego widoku, w którym możliwe jest ręczne wprowadzenie wartości i ustawienie własnych ciał do symulacji.

