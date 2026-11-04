# --- Fajl: main.py ---

from influx_manager import InfluxManager
from mqtt_to_influx import MqttIngestor

if __name__ == "__main__":
    print("[GLAVNI SERVIS] Pokrećem prijem i upis u bazu...")

    # 1. Inicijalizujemo bazu preko tvoje klase InfluxManager
    db = InfluxManager()

    # 2. Inicijalizujemo MQTT primaoca (povezujemo se na mosquitto broker)
    # Ako je u Dockeru, adresa je obično naziv kontejnera ("mosquitto") ili "localhost"
    slusalica = MqttIngestor(broker_adresa="mosquitto", port=1883)

    # 3. PRAVIMO CALLBACK FUNKCIJU:
    # Ova funkcija se poziva automatski svaki put kada MqttIngestor uhvati poruku na mreži.
    def sacuvaj_u_bazu(tema, poruka):
        if "temperatura" in tema:
            db.upisi_merenje(naziv_merenja="ambijent", naziv_polja="temperatura", vrednost=poruka)
            print("-> Upisana temperatura u bazu.")
        elif "svetlost" in tema:
            db.upisi_merenje(naziv_merenja="ambijent", naziv_polja="svetlost", vrednost=poruka)
            print("-> Upisana svetlost u bazu.")

    # 4. PROSLEĐUJEMO FUNKCIJU U KLAZU:
    # Dajemo slušaču tačno ovu funkciju preko callback metode
    slusalica.postavi_callback(sacuvaj_u_bazu)

    try:
        # 5. Pokrećemo sistem da sluša u beskonačnoj petlji
        slusalica.pokreni()
    except KeyboardInterrupt:
        print("\n[GLAVNI SERVIS] Prekidam rad...")
    finally:
        # Kulturno zatvaramo vezu sa bazom kada se program gasi
        db.zatvori()
        print("[GLAVNI SERVIS] Sistem je uspešno ugašen.")