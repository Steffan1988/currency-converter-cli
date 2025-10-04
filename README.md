## Currency Converter CLI

**Currency Converter CLI** is een interactieve command-line applicatie geschreven in Python.
Met deze tool kun je valuta omrekenen, wisselkoersen ophalen via een API, en je conversiegeschiedenis bekijken, allemaal rechtstreeks vanuit de terminal met kleurrijke uitvoer.

### Functies

Met Currency Converter CLI kun je:

* Een nieuwe **basisvaluta** instellen (bijv. USD, EUR, GBP)
* Bedragen **converteren** tussen valuta met realtime wisselkoersen
* Je **conversiegeschiedenis** bekijken binnen de sessie
* Een overzicht tonen van **alle beschikbare valuta's**
* Werken met **gekleurde en opgemaakte CLI-uitvoer**
* De **API-key** veilig beheren via een `.env`-bestand

### Gebruikte libraries

* **requests** – om actuele wisselkoersen op te halen via de API
* **pycountry** – voor de officiële valutacodes en namen
* **dotenv** – voor veilige opslag van de API-key in `.env`
* **datetime** – voor datum- en tijdstempels bij conversies
* **os**, **platform**, **random** – standaard Python-modules

### Over dit project

Currency Converter CLI is ontwikkeld als oefenproject binnen de module *Programming Fundamentals* bij NOVI Hogeschool.
Het project richt zich op het combineren van API-gebruik, dataverwerking, foutafhandeling en gebruikersinteractie in een Python CLI-applicatie.

### English summary

*Currency Converter CLI is an educational and interactive Python command-line application. It retrieves live exchange rates from an API, converts between currencies, and tracks conversion history using formatted and colorful CLI output.
