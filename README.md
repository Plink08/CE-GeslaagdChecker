# VWO Slaag/Zak Dashboard

Een interactieve Streamlit web-app waarmee VWO-scholieren direct kunnen berekenen of ze voldaan hebben aan de slaagregeling.

[Streamlit App](https://geslaagdchecker.streamlit.app/)

## Functies
- **Dynamische vakkenlijst**: Voeg vakken toe of pas ze aan.
- **CE-Toggle**: Ondersteuning voor vakken zonder Centraal Examen (zoals Informatica of Maatschappijleer).
- **Profielen**: Snelvullen met profielen zoals N&T, N&G, E&M en C&M.
- **Wettelijke Regels**: Automatische controle op:
  - Gemiddelde CE-cijfer (minimaal 5.5).
  - Kernvakkenregels (Nederlands, Engels, Wiskunde).
  - Algemene onvoldoende-regels en combinatiecijfer.
  - LO status (Voldoende/Goed).

## Bestandsstructuur
- `main.py`: De hoofdcode van de applicatie.
- `requirements.txt`: Bevat de benodigde libraries (`streamlit`).

## Disclaimer
Deze tool is bedoeld als hulpmiddel. Controleer altijd je definitieve uitslag bij je eigen school of via officiële kanalen zoals [Examenblad.nl](https://www.examenblad.nl).

---
Gemaakt met Python en Streamlit.
