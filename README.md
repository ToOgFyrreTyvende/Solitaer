# Gruppe 19 Solitaire løsnings bot
Vores kode er opdelt i client/server mapperne, her skal client bygges for sig selv,
og servers gennem server. Dette trin er allerede gjort på forhånd.

Klienten er skrevet i Vue
Serveren er skrevet i Python med Flask mikro-frameworket

# Kørsel af sever
For at køre serveren der indeholder genkendelseskode og løsnignsalgoritme, anbefaler vi at oprette et 
virtual environment. 
Med Python 3.8 installeret (det burde også virke med 3.7) kør:

På Windows i cmd/powershell i mappen server:
```sh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

På Linux i mappen server:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Nu kan `flask run` køres for at starte webserveren. Default port er 5000, så http://localhost:5000

**Når serveren startes, henter den en 250 mb stor fil** fra vores egen server. Det er vægtene til det neurale netværk som vi har trænet. Det vil fremkomme i terminalen når denne filhenting igangsættes/færdiggøres, og webserveren er ikke tilgængelig indtil dette er færdiggort!

## Troubleshooting af server
- Hvis serveren ikke download vægtene korrekt, altså hvis filen er under 250 mb, anbefaler vi at hente filen selv gennem linket https://lambda.wtf/mem/soli.weights og placere den i mappen server/card_detector/ med det samme navn som fremgår i linket. Hvis linket er utilgængeligt, så er vægtene også uploaded her https://drive.google.com/file/d/1zBiBz00bdo3JQr8Aa8L0CFSTrGb-qZeJ/view

# Selv-byg af klient (Ikke nødvendigt)
Med node version 12+ installeret, gå ind i client mappen
```sh
npm i
npm run build
```
Flyt dernæst indholdet af mappen client/dist/ ind i mappen server/app/

# Hvis i ønsker at prøve appen på telefon
Obs. man kan på de fleste browsere ikke få kamera til at aktivere på hjememside der tilgået direkte fra IP adresse
Derfor skal der bruges en tunnel service der giver et hostname til en lokal webserver.
Vi anbefaler i den anledning at bruge `ngrok` til dette formål.

For at gøre derre skal ngrok installeres, og serveren skal startes på forhånd og kommandoen `ngrok http -region eu 5000` køres. Dette giver en terminal flade med et URL som ekspempelvis: `https://xxxxxxxxxxxx.eu.ngrok.io`
Med dette link kan telefoner tilgå den hostede webserver med understøttelse for telefon kameraet.


Project template: https://github.com/testdrivenio/flask-vue-crud
