# ---------------------------------------------------Requirements----------------------------------------------------- #
import pycountry
import requests
import random

# ---------------------------------------------------Date-stamp------------------------------------------------------- #
from datetime import datetime

def get_formatted_timestamp():
    nu = datetime.now()
    if platform.system() == "Windows":
        return nu.strftime("%#d-%#m-%Y %H:%M")
    else:
        return nu.strftime("%-d-%-m-%Y %H:%M")

# ----------------------------------------------Overige instellingen-------------------------------------------------- #
#CLI leegmaken
import os
import platform

def clear_screen():
    try:
        command = 'cls' if platform.system() == "Windows" else 'clear'
        os.system(command)
    except Exception:
        pass
# ----------------------------------------------API-key veilig in de .env--------------------------------------------- #
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

# ---------------------------------------Helpfuncties voor de tekst opmaak-------------------------------------------- #
# Tekstopmaak
vet = '\033[1m'
onderstreept = '\033[4m'

# Standaard tekstkleuren
rood = '\033[31m'
groen = '\033[32m'
geel = '\033[33m'
blauw = '\033[34m'
magenta = '\033[35m'
cyan = '\033[36m'
reset = '\033[0m'

# -----------------------------Helpfunctie omdat humanize alleen met integers werkt----------------------------------- #
def humaniseer_float(getal):
    if getal >= 1_000_000:
        return f"{getal / 1_000_000:.2f} miljoen"
    elif getal >= 10_000:
        return f"{getal / 1_000:.1f} duizend"
    elif getal >= 1_000:
        return f"{getal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return f"{getal:.2f}".replace(".", ",")

# ----------------------------------------------Alle functie's-------------------------------------------------------- #
def get_exchange_data(api_key):
    url = (f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD")
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        print("Er is iets misgegaan")
        print("Statuscode:", response.status_code)
        return None

def random_valuta():
    data = get_exchange_data(api_key)["conversion_rates"]
    genummerde_dict = {i: val for i, val in enumerate(data, start=1)}
    waarde = genummerde_dict[random.randint(1,len(genummerde_dict))]
    return waarde

def base_currency():
    print(f"\n{onderstreept}{vet}Nieuwe basisvaluta instellen{reset}")
    exchange_rate = get_exchange_data(api_key)
    base_currency = input(f"\n{cyan}Welke valuta wil je als basis instellen? "
                          f"(bijv. {random_valuta()}, {random_valuta()}){reset}").upper()
    while base_currency not in exchange_rate["conversion_rates"]:
        print(f"{rood}Fout: {base_currency} wisselkoers niet gevonden{reset}")
        base_currency = input(f"\n{cyan}Welke valuta wil je als basis instellen? "
                              f"(bijv. {random_valuta()}, {random_valuta()}){reset}").upper()
    else:
        standaard_name = pycountry.currencies.get(alpha_3=base_currency).name
        return exchange_rate["conversion_rates"][base_currency], base_currency, standaard_name

def conversion():
    print(f"\n{onderstreept}{vet}Converteer naar een andere valuta{reset}")
    standaard_name = set_standard[2]
    exchange_rate = get_exchange_data(api_key)
    choice_currency = input(f"\n{geel}Naar welke valuta wil je {vet}{groen}{standaard_name}{reset} "
                            f"{geel}omrekenen? (bijv. {random_valuta()}, {random_valuta()}): {reset}").upper()

    while choice_currency not in exchange_rate["conversion_rates"]:
        print(f"{rood}Fout: {choice_currency} wisselkoers niet gevonden{reset}")
        choice_currency = input(f"\n{geel}Naar welke valuta wil je {vet}{groen}{standaard_name}{reset} "
                                f"{geel}omrekenen? (bijv. {random_valuta()}, {random_valuta()}): {reset}").upper()
    else:
        naam_choice_currency = pycountry.currencies.get(alpha_3=choice_currency).name
        convert = exchange_rate["conversion_rates"][choice_currency]
        amount = float(input(f"{geel}Hoeveel {reset}{vet}{groen}{standaard_name}{reset} "
                             f"{geel}wil je omzetten naar {reset}{vet}{groen}{naam_choice_currency}? {reset}"))
        conversie = (amount * (1/set_standard[0])) * (convert)
        print(
            f"\n{vet}{groen}{humaniseer_float(amount)} {standaard_name}{reset} "
            f"is gelijk aan {vet}{groen}{humaniseer_float(conversie)} {naam_choice_currency}{reset}"
        )
        return get_formatted_timestamp(), standaard_name, amount, conversie, naam_choice_currency

def geschiedenis():
    if not history:
        print(f"\n{rood}{vet}Je hebt nog geen conversiegeschiedenis.{reset}")
    else:
        print(f"\n{onderstreept}{vet}Conversiegeschiedenis:\n{reset}")
        for nummer, (tijd, basis_munt, amount, conversie, doel_munt) in enumerate(history, start=1):
            print(
                f"{blauw}{vet}{nummer}. {reset}"
                f"{tijd} - "
                f"{vet}{groen}{humaniseer_float(amount)} {basis_munt}{reset} "
                f"→ {vet}{groen}{humaniseer_float(conversie)} {doel_munt}{reset}"
            )
    return

def list_currencies(set_standard):
    print(f"{onderstreept}{vet}Beschikbare valuta's\n{reset}")
    data = get_exchange_data(api_key)["conversion_rates"]
    temp = {}
    for i in pycountry.currencies:
        temp[i.alpha_3] = i.name
    for nummer, key in enumerate(data, start=1):
        if key in temp:
            print(
                f"{blauw}{vet}│ {nummer:>3} │ {geel}{key}{reset}{blauw} - {cyan}{temp[key]}{reset}{blauw} │ "
                f"{groen}1.00 {set_standard[1]}{reset}{blauw} = "
                f"{magenta}{data[key] / set_standard[0]:.2f} {key}{reset}{blauw}{reset}"
            )
    return

def main():
    print(f"\n{onderstreept}{vet}Hoofdmenu{reset}")
    standaard_name = set_standard[2]
    menu_keuze = int(input(
            f"\n{vet}Welkom bij de Currency Convertor!{reset}"
            f"\n{blauw}Huidige basisvaluta: {reset}'{vet}{groen}{standaard_name}{reset}'"
            f"\n\n{vet}Maak een keuze:{reset}"
            f"\n{geel}1. Nieuwe basisvaluta instellen"
            f"\n2. Converteer naar een andere valuta"
            f"\n3. Bekijk conversiegeschiedenis"
            f"\n4. Toon beschikbare valuta's"
            f"\n5. Afsluiten{reset}"
        ))
    return menu_keuze

# ---------------------------------------------------Overige---------------------------------------------------------- #
# api_key = "[vul hier de API-key in]"
set_standard = (1, "USD", "US dollar")
history = []

# ----------------------------------------------While-loop voor hoofdmenu--------------------------------------------- #
while True:
    clear_screen()
    menu_choice = main()

    if menu_choice ==1:
        set_standard = base_currency()
    elif menu_choice ==2:
        history.append(conversion())
    elif menu_choice ==3:
        geschiedenis()
    elif menu_choice ==4:
        list_currencies(set_standard)
    elif menu_choice ==5:
        break
    else:
        print(f"{rood}{vet}'{menu_choice}' is een ongeldige keuze!{reset}")