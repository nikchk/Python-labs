import requests as rq
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import re

rates = []
Chousecurrencey = input("Enter currency (USD, EUR): ").lower()
Choosedays = int(input("Enter number of days to analyze (e.g., 7): "))

for i in range(Choosedays):
    date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    url = f"https://minfin.com.ua/ua/currency/banks/{Chousecurrencey}/{date}/"
    res = rq.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    rate_tag = soup.select("table tbody tr")
    for tag in rate_tag:
        cols = tag.find_all("td")
        if len(cols) >= 4:
            rate_t = cols[3].get_text(strip=True).replace(',', '.')
            match = re.search(r'\d+(\.\d+)?', rate_t)   
            if match:
                rate = float(match.group())
                rates.append((date, rate))   
                with open(f"{Chousecurrencey}_data.txt", "a", encoding="utf-8") as f:
                    f.write(f"{date} {Chousecurrencey.upper()} {rate}\n")
                break

rates.sort(key=lambda x: x[0])
x = [datetime.strptime(d, "%Y-%m-%d") for d, _ in rates]
currens = [item[1] for item in rates]

#Лінійна регресія
def predict(lst):
    n = len(lst)
    x = list(range(1, n+1))
    a11 = sum(i**2 for i in x)
    a12 = sum(x)
    a22 = n
    c1 = sum(x[i]*lst[i] for i in range(n))
    c2 = sum(lst)
    det = a11*a22 - a12**2
    k = (c1*a22 - c2*a12)/det
    b = (a11*c2 - a12*c1)/det
    pred = [k*(i+1)+b for i in range(n)]
    next_day = k*(n+1)+b
    return pred, next_day, k, b

pred, predicted, k, b = predict(currens)

t = x[-1] + timedelta(days=1)
print(f"\nTomorrow {Chousecurrencey.upper()} rate: {predicted:.2f} UAH")
print(f"Regression coefficients: k = {k:.3f}, b = {b:.3f}")

plt.figure(figsize=(10, 5))
plt.plot(x, currens, "o-", label="Actual Rates")
plt.plot(x, pred, "--", color="red", label="Predict (Linear Regression)")
plt.plot(t, predicted, "ro", label="Predicted Rate (Tomorrow)")
plt.plot([x[-1], t], [pred[-1], predicted], "--", color="red")

plt.title(f"{Chousecurrencey.upper()} Exchange rate")
plt.xlabel("Date")
plt.ylabel("Rate (UAH)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
