import requests
import json
import matplotlib.pyplot as plt

nbu_response = requests.get("https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250512&end=20250518&valcode=usd&sort=exchangedate&order=desc&json")

converted_response = json.loads(nbu_response.content)

exchange_dates = []
exchange_rates = []

print("Курс долара США за період 12.05.2025 – 18.05.2025:")
for item in converted_response:
    print(f"{item['exchangedate']}: {item['rate']} грн")
    exchange_dates.append(item['exchangedate'])
    exchange_rates.append(item['rate'])

exchange_dates.reverse()
exchange_rates.reverse()

plt.plot(exchange_dates, exchange_rates)
plt.xlabel("Дата")
plt.ylabel("Курс USD")
plt.title("Курс долара за попередній тиждень")
plt.show()
