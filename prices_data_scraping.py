from requests import get
from bs4 import BeautifulSoup
from pandas import DataFrame


url = "https://kb.pl/cenniki/produkty/cennik-mcdonalds-aktualne-ceny-w-menu/"


if __name__ == "__main__":
    req = get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    offers = soup.find_all("tr", {"class": "sub-row"})

    names = []
    prices = []
    for offer in offers:
        offer_name = offer.find("th").get_text()
        print(offer_name)
        names.append(offer_name)

        offer_price = float(offer.find("td").get_text()[:-3].replace(",", "."))
        print(offer_price)
        prices.append(offer_price)

        print()

    df = DataFrame({'name': names, 'price': prices})
    df.to_excel('prices.xlsx', sheet_name='sheet1', index=False)
