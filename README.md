
## N-Body Simulation

Aplikacja zawiera symulację układów n-body z detekcją kolizji w czasie rzeczywistym

## Struktura projektu

- **`main.py`** – punkt wejściowy aplikacji, inicjalizuje i uruchamia pętlę symulacji.
- **`Body.py`** – definicja klasy reprezentującej ciało fizyczne oraz generowanie przykładów symulacji.
- **`Physic.py`** – logika fizyki: obliczanie grawitacji, detekcja i obsługa kolizji między ciałami.
- **`Camera.py`** – zarządza pozycją i ruchem kamery w scenie 3D (WASD, obracanie kamery).
- **`Gui.py`** – interfejs graficzny użytkownika: wybór symulacji, zmiana parametrów, tryb własnych obiektów.
- **`Settings.py`** – ustawienia globalne projektu (stałe fizyczne, parametry wyświetlania).
- **`Sphere.py`** – wizualna reprezentacja ciał (generowanie i rysowanie sfery w 3D).

## Sterowanie

- **W / A / S / D** – poruszanie się kamerą w poziomie
- **Spacja** – ruch kamery w górę
- **Lewy Ctrl** – ruch kamery w dół
- **Przytrzymanie Lewego shifta** - przyspieszenie ruchu kamery
- **Przytrzymanie lewego przycisku myszy** – obracanie kamery

## GUI

W interfejsie graficznym dostępne są trzy predefiniowane przykłady symulacji:

- **Earth-Moon** – symulacja Ziemi i Księżyca
- **Mini Solar System** – uproszczony model małego układu planetarnego
- **Three Body Figure-8** – klasyczny układ trzech ciał poruszających się po trajektorii w kształcie ósemki

Można również modyfikować parametry fizyczne symulacji takie jak grawitacja, prędkość symulacji oraz sprężystość odbicia (1 - odbicie idealnie elastyczne, 0 - brak odbicia) w czasie rzeczywistym.

## Tryb własnych obiektów

Za pomocą paska nawigacyjnego można przejść do drugiego widoku, w którym możliwe jest ręczne wprowadzenie wartości i ustawienie własnych ciał do symulacji.

## Wymagania

- **Python 8.x - Python 11.x** (wymagany – projekt wykorzystuje biblioteke dostępną tylko w tych wersjach Python),
- ```pip install -r requirements.txt ```
# Uruchomienie aplikacji
W głównym katalogu projektu uruchom:
```python main.py```

