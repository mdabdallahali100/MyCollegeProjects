# Import required modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import requests
import datetime as dt

# Converting stuff
class CurrencyConverter:

    def __init__(self, url):
        self.url = 'https://api.exchangerate.host/'
        self.response = requests.get(url)
        self.data = self.response.json()
        self.rates = self.data.get('rates')

    def convert(self, amount, base_currency, des_currency):
        if base_currency != 'EUR':
            amount = amount / self.rates[base_currency]
        # Limiting the result to 2 decimal places
        amount = round(amount * self.rates[des_currency], 2)
        # Add comma every 3 numbers
        amount = '{:,}'.format(amount)
        return amount

    def get_exchange_rate(self, base_currency, des_currency):
        return self.rates[des_currency] / self.rates[base_currency]

    def get_exchange_rate_history(self, base_currency, des_currency, days):
        history_url = f'{self.url}timeseries?start_date={dt.datetime.now() - dt.timedelta(days=days)}&end_date={dt.datetime.now()}&symbols={des_currency}&base={base_currency}'
        response = requests.get(history_url)
        data = response.json()
        rates = data.get('rates')
        return rates
# Main window
class Main(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.geometry('400x500')
        self.config(bg='#3A3B3C')
        self.CurrencyConverter = converter

        # Create title label
        self.title_label = Label(self, text='Currency Converter', bg='#3A3B3C', fg='white',
                                 font=('franklin gothic medium', 20), relief='sunken')
        self.title_label.place(x=200, y=35, anchor='center')

        # Create date label
        self.date_label = Label(self, text=f'{dt.datetime.now():%A, %B %d, %Y}', bg='#3A3B3C', fg='white',
                                font=('calibri', 10))
        self.date_label.place(x=0, y=480, anchor='sw')

        # Create version label
        self.version_label = Label(self, text='v1.0', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.version_label.place(x=400, y=480, anchor='se')
        # Create amount label
        self.amount_label = Label(self, text='Input Amount: ', bg='#3A3B3C', fg='white',
                                  font=('franklin gothic book', 15))
        self.amount_label.place(x=200, y=80, anchor='center')

        # Create amount entry box
        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25)
        self.amount_entry.place(x=200, y=110, anchor='center')

        # Create 'from' label
        self.base_currency_label = Label(self, text='From: ', bg='#3A3B3C', fg='white',
                                         font=('franklin gothic book', 15))
        self.base_currency_label.place(x=200, y=140, anchor='center')

        # Create 'to' label
        self.destination_currency_label = Label(self, text='To: ', bg='#3A3B3C', fg='white',
                                                font=('franklin gothic book', 15))
        self.destination_currency_label.place(x=200, y=200, anchor='center')
        # Create dropdown menus
        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set('USD')
        self.currency_variable2.set('INR')

        self.currency_combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1,
                                               values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox1.place(x=200, y=170, anchor='center')

        self.currency_combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2,
                                               values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox2.place(x=200, y=230, anchor='center')

        # Create 'convert' button
        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=170, y=270, anchor='center')

        # Create 'clear' button
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=230, y=270, anchor='center')
        # Create converted result field
        self.final_result = Label(self, text='', bg='#52595D', fg='white', font=('calibri', 12), relief='sunken',
                                  width=40)
        self.final_result.place(x=200, y=310, anchor='center')

        # Create exchange rate label
        self.exchange_rate_label = Label(self, text='', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.exchange_rate_label.place(x=200, y=340, anchor='center')

        # Create exchange rate history label
        self.history_label = Label(self, text='Exchange Rate History:', bg='#3A3B3C', fg='white',
                                   font=('franklin gothic book', 12))
        self.history_label.place(x=200, y=370, anchor='center')

        # Create history text box
        self.history_text = Text(self, width=35, height=5)
        self.history_text.place(x=200, y=400, anchor='center')

    # Create clear function, to clear the amount field, final result field, and history text box
    def clear(self):
        clear_entry = self.amount_entry.delete(0, END)
        clear_result = self.final_result.config(text='')
        clear_history = self.history_text.delete('1.0', END)
        return clear_entry, clear_result, clear_history 
    # Create a function to perform
    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            given_base_currency = self.currency_variable1.get()
            given_des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, given_base_currency, given_des_currency)

            exchange_rate = self.CurrencyConverter.get_exchange_rate(given_base_currency, given_des_currency)
            self.exchange_rate_label.config(
                text=f'Exchange Rate: 1 {given_base_currency} = {exchange_rate} {given_des_currency}')

            # Add comma every 3 numbers
            given_amount = '{:,}'.format(given_amount)
            self.final_result.config(
                text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

            # Retrieve exchange rate history for the last 7 days
            rates_history = self.CurrencyConverter.get_exchange_rate_history(given_base_currency, given_des_currency, 30)

            # Update the history text box
            self.history_text.delete('1.0', END)
            for date, rate in rates_history.items():
                self.history_text.insert(END, f'{date}: {rate}\n')
        # Create warning message box
        except ValueError:
            convert_error = messagebox.showwarning('WARNING!', 'Please Fill the Amount Field (integer only)!')
            return convert_error

if __name__ == '__main__':
    converter = CurrencyConverter('https://api.exchangerate.host/latest')
    Main(converter)
    mainloop()
