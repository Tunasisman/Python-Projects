import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import requests
import threading

API_KEY = 'fca_live_SCAc75FDh5S0KSe2IqntK1yFC4EhApZt4U9xkzi0'
BASE_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}'

CURRENCIES = [
    'EUR', 'USD', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 
    'SEK', 'CHF', 'ISK', 'NOK', 'HRK', 'RUB', 'TRY', 'AUD', 'BRL', 'CAD', 
    'CNY', 'HKD', 'IDR', 'ILS', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 
    'SGD', 'THB', 'ZAR'
]

def convert_currency(base, currencies, callback):
    def run():
        try:
            url = f'{BASE_URL}&base_currency={base}&currencies={",".join(currencies)}'
            response = requests.get(url)
            data = response.json()["data"]
            callback(data, None)
        except Exception as e:
            callback(None, e)
    
    threading.Thread(target=run).start()

def show_conversion(data, error):
    if error:
        result_text.config(text=f"Error: {error}")
        return
    if not data:
        result_text.config(text="No data.")
        return
    result = "\n".join([f"{currency}: {rate}" for currency, rate in data.items()])
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.INSERT, result)

def on_convert_button_click():
    base_currency = base_currency_var.get()
    selected_currencies = [currency for currency, var in currency_vars.items() if var.get()]
    if not selected_currencies:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.INSERT, "No currency selected.")
        return
    convert_currency(base_currency, selected_currencies, show_conversion)

root = tk.Tk()
root.title("Currency Converter")

base_currency_var = tk.StringVar(value='USD')
base_currency_label = tk.Label(root, text="Select base currency:")
base_currency_label.grid(row=0, column=0, columnspan=2)
base_currency_dropdown = ttk.Combobox(root, textvariable=base_currency_var, values=CURRENCIES)
base_currency_dropdown.grid(row=1, column=0, columnspan=2)

currency_vars = {}
for i, currency in enumerate(CURRENCIES):
    row = 2 + (i // 5)
    column = i % 5
    var = tk.BooleanVar(value=False)
    currency_vars[currency] = var
    chk = tk.Checkbutton(root, text=currency, var=var)
    chk.grid(row=row, column=column, sticky='w')

convert_button = tk.Button(root, text="Convert", command=on_convert_button_click)
convert_button.grid(row=12, column=0, columnspan=2)

# Scrollable text area for results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
result_text.grid(row=13, column=0, columnspan=5)

root.mainloop()
