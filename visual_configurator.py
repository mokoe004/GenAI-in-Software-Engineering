# zeigt aktuellen Fortschritt der roadmap an
# GUI Anwendung: Tkinter oder PyQt
import time
import json
import matplotlib.pyplot as plt

# Erfolgsfaktoren mit Gewichtungen
success_factors = {
    "Training der Entwickler": {"value": 50, "weight": 0.4},  # Gewichtung: 40 %
    "Datenqualität": {"value": 70, "weight": 0.3},  # Gewichtung: 30 %
    "Nutzerakzeptanz": {"value": 60, "weight": 0.3},  # Gewichtung: 30 %
}

# Roadmap mit Meilensteinen
roadmap = [
    {"Meilenstein": "Pilotphase starten", "Erfolgsschwelle": 50},
    {"Meilenstein": "Rollout im Team", "Erfolgsschwelle": 60},
    {"Meilenstein": "Optimierung & Skalierung", "Erfolgsschwelle": 70},
]

# Funktionen
def calculate_success(factors):
    """Berechnet den gewichteten Erfolgswert."""
    weighted_success = sum(
        factor["value"] * factor["weight"] for factor in factors.values()
    )
    return round(weighted_success)

def simulate_roadmap(factors, roadmap):
    """Simuliert die Roadmap basierend auf Erfolgsfaktoren."""
    overall_success = calculate_success(factors)
    results = []

    print("\nSimuliere Roadmap...")
    for milestone in roadmap:
        time.sleep(1)  # Fortschritt simulieren
        success = overall_success >= milestone["Erfolgsschwelle"]
        results.append({"Meilenstein": milestone["Meilenstein"], "Erfolg": success})
        print(f"\n{milestone['Meilenstein']}...")
        if success:
            print("✅ Erfolgreich abgeschlossen!")
        else:
            print("❌ Gescheitert - Erfolgsschwelle nicht erreicht.")
            break  # Stoppt Simulation bei Misserfolg

    return results

def display_factors(factors):
    """Zeigt die aktuellen Erfolgsfaktoren an."""
    print("\nAktuelle Erfolgsfaktoren:")
    for factor, data in factors.items():
        print(f"- {factor}: {data['value']}% (Gewichtung: {data['weight'] * 100}%)")

def save_factors(factors):
    """Speichert Erfolgsfaktoren in einer JSON-Datei."""
    with open("factors.json", "w") as file:
        json.dump(factors, file)
    print("\nErfolgsfaktoren wurden gespeichert!")

def load_factors():
    """Lädt Erfolgsfaktoren aus einer JSON-Datei."""
    try:
        with open("factors.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("\nKeine gespeicherten Erfolgsfaktoren gefunden.")
        return None

def plot_roadmap(results):
    """Visualisiert die Roadmap mit matplotlib."""
    milestones = [r["Meilenstein"] for r in results]
    success = [r["Erfolg"] for r in results]

    # Farben basierend auf Erfolg (grün/rot)
    colors = ["green" if s else "red" for s in success]

    plt.figure(figsize=(10, 6))
    plt.barh(milestones, [1] * len(milestones), color=colors, edgecolor="black")
    plt.xlabel("Status (Erfolg/Misserfolg)")
    plt.title("Roadmap-Simulation")
    plt.tight_layout()
    plt.show()

def main():
    """Hauptprogramm für den Simulator."""
    global success_factors

    # Erfolgsfaktoren laden, falls vorhanden
    loaded_factors = load_factors()
    if loaded_factors:
        success_factors = loaded_factors
        print("\nGespeicherte Erfolgsfaktoren wurden geladen!")

    print("Willkommen beim erweiterten CoPilot-Implementierungs-Simulator!")
    while True:
        # Zeige Erfolgsfaktoren
        display_factors(success_factors)

        # Benutzer kann Erfolgsfaktoren anpassen
        print("\nMöchten Sie einen Erfolgsfaktor anpassen? (ja/nein)")
        choice = input("Ihre Eingabe: ").lower()
        if choice == "ja":
            factor = input("Welchen Erfolgsfaktor möchten Sie anpassen? ")
            if factor in success_factors:
                try:
                    new_value = int(input(f"Neuer Wert für '{factor}' (0-100): "))
                    if 0 <= new_value <= 100:
                        success_factors[factor]["value"] = new_value
                    else:
                        print("Bitte einen Wert zwischen 0 und 100 eingeben.")
                except ValueError:
                    print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
            else:
                print("Dieser Erfolgsfaktor existiert nicht.")
        else:
            # Starte die Roadmap-Simulation
            results = simulate_roadmap(success_factors, roadmap)

            # Visualisiere die Roadmap
            plot_roadmap(results)

        # Möglichkeit, Erfolgsfaktoren zu speichern
        print("\nMöchten Sie die Erfolgsfaktoren speichern? (ja/nein)")
        if input("Ihre Eingabe: ").lower() == "ja":
            save_factors(success_factors)

        # Möglichkeit, das Programm zu beenden
        print("\nMöchten Sie das Programm beenden? (ja/nein)")
        if input("Ihre Eingabe: ").lower() == "ja":
            print("Vielen Dank für die Nutzung des Simulators!")
            break

# Start des Programms
if __name__ == "__main__":
    main()
