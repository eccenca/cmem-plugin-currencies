"""ChatGPT generated (and fixed) code from the following prompt:

Please give a CSV table with the following rows, a product name (product, string),
a price (price, float), a currency (currency, string, ISO currency ID) and a date.

The currencies should be selected randomly between the main 20 used currencies.
The date can be selected randomly from yesterday until 1999-01-04.

I want to have 1000 different products from real world.
"""
# ruff: noqa: S311, DTZ001, DTZ005, INP001

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# List of top 20 used currencies in ISO format
currencies = [
    "USD",
    "EUR",
    "JPY",
    "GBP",
    "AUD",
    "CAD",
    "CHF",
    "CNY",
    "SEK",
    "NZD",
    "MXN",
    "SGD",
    "HKD",
    "NOK",
    "KRW",
    "TRY",
    "INR",
    "RUB",
    "BRL",
    "ZAR",
]

# List of real-world product names (sample selection)
products = [
    "Apple iPhone 14",
    "Samsung Galaxy S21",
    "Sony WH-1000XM4",
    "Dell XPS 13",
    "Apple MacBook Pro",
    "Microsoft Surface Pro 7",
    "Google Pixel 6",
    "Amazon Echo Dot",
    "HP Spectre x360",
    "Bose QuietComfort 35",
    "Nikon D3500",
    "Canon EOS Rebel T7",
    "Fitbit Charge 5",
    "Garmin Forerunner 245",
    "LG OLED TV",
    "Samsung QLED TV",
    "PlayStation 5",
    "Xbox Series X",
    "Nintendo Switch",
    "Dyson V11 Vacuum",
    "Instant Pot Duo",
    "KitchenAid Stand Mixer",
    "Roomba i7+",
    "Nespresso Vertuo",
    "JBL Flip 5",
    "Beats Solo3",
    "GoPro HERO9",
    "Oculus Quest 2",
    "Razer Blade 15",
    "Alienware m15",
    "Sony A7 III",
    "Panasonic Lumix GH5",
    "DJI Mavic Air 2",
    "Ring Video Doorbell",
    "Arlo Pro 3",
    "Anker PowerCore",
    "Logitech MX Master 3",
    "Apple AirPods Pro",
    "Samsung Galaxy Buds+",
    "Tile Pro",
    "Eero 6 Mesh Wi-Fi",
    "Nest Learning Thermostat",
    "August Smart Lock",
    "Weber Spirit II",
    "Traeger Pro 575",
    "Philips Hue Bulbs",
    "LIFX Smart Bulbs",
    "Sonos One",
    "Yamaha YAS-209",
    "Polk Audio Signa S2",
    "Vizio SB36512-F6",
    "Marshall Stanmore II",
    "Fender Stratocaster",
    "Yamaha P-125",
    "Korg B2",
    "Roland TD-1DMK",
    "Casio Privia PX-160",
    "Nord Stage 3",
    "Moog Subsequent 37",
    "Kawai ES110",
    "Alesis Recital Pro",
    "Arturia KeyLab 88",
    "Novation Launchpad",
    "Native Instruments Maschine",
    "Akai MPK Mini",
    "Ableton Push 2",
    "Pioneer DJ DDJ-1000",
    "Numark Mixtrack Pro FX",
    "Hercules DJControl Inpulse 500",
    "Denon DJ SC6000M",
    "Rane Twelve MKII",
    "Technics SL-1200MK7",
    "Sennheiser HD 25",
    "Audio-Technica ATH-M50x",
    "Beyerdynamic DT 770 PRO",
    "Shure SM7B",
    "Rode NT1-A",
    "Blue Yeti",
    "Focusrite Scarlett 2i2",
    "Universal Audio Apollo Twin",
    "PreSonus AudioBox USB 96",
    "Mackie CR3-X",
    "KRK Rokit 5 G4",
    "Adam Audio T5V",
    "JBL Professional 305P MKII",
    "IK Multimedia iLoud Micro",
    "Yamaha HS5",
    "Neumann KH 120",
    "Genelec 8010A",
    "IK Multimedia iRig Pro Duo",
    "Zoom H5",
    "Tascam DR-40X",
    "Behringer Xenyx Q502USB",
    "M-Audio M-Track Solo",
    "Alesis V49",
    "Akai Professional MPD218",
    "Arturia MicroFreak",
    "Elektron Digitakt",
    "Korg Volca FM",
    "Novation Circuit Tracks",
    "Roland MC-101",
    "Teenage Engineering OP-1",
    "Moog Mother-32",
]


def random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random date between yesterday and 1999-01-04"""
    return start + timedelta(days=random.randint(0, (end - start).days))


start_date = datetime(1999, 1, 4)
end_date = datetime.now() - timedelta(days=1)

# Generate 1000 unique product names (randomly selecting from the list with some repetitions)
product_names = random.choices(products, k=1000)

# Create CSV
file_path = Path("product-prices.csv")
with file_path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["product", "price", "currency", "date"])

    for product in product_names:
        price = round(random.uniform(1, 2000), 2)
        currency = random.choice(currencies)
        date = random_date(start_date, end_date).strftime("%Y-%m-%d")
        writer.writerow([product, price, currency, date])
