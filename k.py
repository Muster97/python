import re

"""Todo"""
# Unbekannt Entfernen
# andere Dateien einlesen
# Kategorie Zuweisung
# Betrag in Zahl konviertieren
# Übersicht erstellen
    # Monat
    # Jahr
    # Gesamter Zeitraum
    # Diagramme?
# Kategorien überlegen

def is_transaction_line(text):
    """
    Prüft, ob eine Zeile einen Geldbetrag am Ende enthält.
    """
    return re.search(r'\d{1,3}(?:\.\d{3})*,\d{2}$', text) is not None

def extract_amount(text):
    """
    Extrahiert den Geldbetrag am Ende der Zeichenkette.
    """
    match = re.search(r'\d{1,3}(?:\.\d{3})*,\d{2}$', text)
    return match.group(0) if match else ""

def remove_date_and_amount(text):
    """
    Entfernt das Datum und den Geldbetrag aus dem Text.
    """
    # Entferne das Datum (angenommen es ist immer im Format dd.mm.yyyy am Anfang)
    text_without_date = re.sub(r'^\d{2}\.\d{2}\.\d{4}\s+', '', text)
    # Entferne den Geldbetrag am Ende
    text_without_amount = re.sub(r'\s*\d{1,3}(?:\.\d{3})*,\d{2}$', '', text_without_date)
    return text_without_amount.strip()

def process_lines(lines):
    """
    Verarbeitet die Zeilen, kombiniert sie entsprechend der Vorgaben und filtert die Ergebnisse.
    """
    processed_lines = []
    current_line = ""
    current_text = ""
    current_amount = ""
    
    for line in lines:
        # Zerlege die Zeile in ihre Bestandteile
        date, text, additional_text = eval(line)

        if is_transaction_line(text):
            # Wenn es sich um eine Transaktionszeile handelt, speichere die bisherige Zeile
            if current_line:
                combined_text = f"{current_text.strip()} {additional_text.strip()}, {current_amount}"
                processed_lines.append(f"('{current_line}', '{combined_text}')")
            
            # Starte eine neue Zeile
            current_line = date
            current_text = remove_date_and_amount(text)  # Buchungstext ohne Datum und Betrag
            current_amount = extract_amount(text)  # Extrahiere den Betrag

        else:
            # Wenn es sich um eine Fortsetzungszeile handelt, füge sie zum aktuellen Text hinzu
            current_text += " " + remove_date_and_amount(text)  # Text ohne Datum und Betrag

    # Letzte Zeile hinzufügen
    if current_line:
        combined_text = f"{current_text.strip()} {additional_text.strip()}, {current_amount}"
        processed_lines.append(f"('{current_line}', '{combined_text}')")

    return processed_lines

# Beispielinhalt der Datei (normalerweise würde man die Datei einlesen)
# lines = [
#     "('01.01.2024', '01.01.2024 Das ist ein Buchungstext 5,00', 'Unbekannt')",
#     "('01.01.2024', '01.01.2024 Das ist ein Buchungstext', 'aus der folgenden Zeile ohne Geldbetrag')",
#     "('02.01.2024', '01.01.2024 Das ist ein anderer Buchungstext 2.000,00', 'Unbekannt')",
#     "('02.01.2024', '01.01.2024 Ein weiterer Buchungstext', 'aus der folgenden Zeile Ohne Geldbetrag')"
# ]

with open('res2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Verarbeitung der Zeilen
processed_lines = process_lines(lines)

# Write the processed lines to an output file
with open('output.txt', 'w', encoding='utf-8') as output_file:
    for line in processed_lines:
        output_file.write(line + '\n')

# Ausgabe der verarbeiteten Zeilen
#for line in processed_lines:
 #   print(line)
