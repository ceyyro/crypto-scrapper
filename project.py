import json
import customtkinter
from tkinter import *
from requests import Session

# Set gui theme
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


def main():
    # Get the API at program start
    scrape()

    # Initialize app
    app = App()

    # App properties
    app.iconbitmap("eth_icon.ico")
    app.deiconify()
    app.mainloop()
    
# Gui
class App(customtkinter.CTk):

    # Window sizes
    WIDTH = 400
    HEIGHT = 240

    def __init__(self):
        super().__init__()

        # Main window properties
        self.title("Crypto Scrapper")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(400, 240)

        # Sets 2x2 grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # First frame for info
        self.frame_up = customtkinter.CTkFrame(master=self, width=300, height=140, corner_radius=10)
        self.frame_up.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nesw")
        
        # Initiate scrape button
        self.button = customtkinter.CTkButton(master=self, text="Scrape", fg_color="#444c74", command=self.scrapebutton)
        self.button.grid(row=1, column=1, padx=(0,20) , pady=(0, 20), sticky="ew")

        # Initiate option-menu
        self.combobox = customtkinter.CTkComboBox(master=self,
                                            values=[*symbols]
                                            )
        self.combobox.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")


    # Gets api values first, then shows values
    def scrapebutton(self):

        # Get formatted api values on-click
        symbol_i = get_i(self.combobox.get())
        name = get_name(symbol_i)
        price = f"${round(get_price(symbol_i), 2):,}"
        market_cap = f"${round(get_market_cap(symbol_i), 2):,}"
        volume_24h = f"${round(get_volume_24h(symbol_i), 2):,}"
        percent_change_1h = f"{round(get_percent_change_1h(symbol_i), 2)}%"
        percent_change_24h = f"{round(get_percent_change_24h(symbol_i), 2)}%"
        
        # Show information
        # Name label
        label_name = customtkinter.CTkLabel(master=self,
                                    text=f"Name:\n{name}",
                                    width=120,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_name.place(relx=0.5, rely=0.5, anchor=customtkinter.W)
        label_name.grid(row=0, column=0, padx=20, pady=(25, 20), sticky="new")

        # Price label
        label_price = customtkinter.CTkLabel(master=self,
                                    text=f"Price:\n{price}",
                                    width=120,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_price.place(relx=0.5, rely=0.5, anchor=customtkinter.W)
        label_price.grid(row=0, column=0, padx=20, pady=(23, 20), sticky="ew")

        # Market cap label
        label_market = customtkinter.CTkLabel(master=self,
                                    text=f"Market cap:\n{market_cap}",
                                    width=120,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_market.place(relx=0.5, rely=0.5, anchor=customtkinter.W)
        label_market.grid(row=0, column=0, padx=20, pady=(0, 25), sticky="sew")

        # Volume 24h label
        label_volume = customtkinter.CTkLabel(master=self,
                                    text=f"Volume 24h:\n{volume_24h}",
                                    width=110,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_volume.place(relx=0.5, rely=0.5, anchor=customtkinter.E)
        label_volume.grid(row=0, column=1, padx=20, pady=(25, 20), sticky="new")

        # Percent change 1h label
        label_change1 = customtkinter.CTkLabel(master=self,
                                    text=f"Percentage change 1h:\n{percent_change_1h}",
                                    width=110,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_change1.place(relx=0.5, rely=0.5, anchor=customtkinter.E)
        label_change1.grid(row=0, column=1, padx=20, pady=(25, 20), sticky="ew")

        # Percent change 24h label
        label_change24 = customtkinter.CTkLabel(master=self,
                                    text=f"Percentage change 24h:\n{percent_change_24h}",
                                    width=110,
                                    height=25,
                                    fg_color="#292929",
                                    bg_color="#292929",
                                    corner_radius=0)
        label_change24.place(relx=0.5, rely=0.5, anchor=customtkinter.E)
        label_change24.grid(row=0, column=1, padx=20, pady=(20, 25), sticky="sew")
        


# Gets API
def scrape():

    # Values url
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    # Get top 10 cryptos (cmc_rank) and convert prices to USD
    parameters = {
        'limit': '10',
        'convert': 'USD',
        'sort_dir': 'desc'
    }

    # API key
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0b387bb2-4030-41e2-8631-d9ad8e0f331d'
    }

    # Request values from API including headers and parameters
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)

    # Create global variable api
    global api
    api = json.loads(response.text)

    # Create list of top 10 cryptos symbols
    global symbols
    symbols = []
    i = 0
    for _ in api['data']:
        symbols.append(api['data'][i]['symbol'])
        i += 1
    
    # Return 0 if everything went good
    if len(symbols) == 10:
        return 0




# Get crypto order in api list
def get_i(symbol):

    # On each recall get recent API
    scrape()
    global api

    # Find order in API based on string symbol
    # for example 'BTC' returns 0, because it's first
    try:
        i = 0
        for _ in api['data'][i]:
            if symbol == api['data'][i]['symbol']:
                symbol_i = i
                return int(symbol_i)
            i += 1
    # Except crypto isn't in the top 10 list
    # raise an IndexError
    except IndexError:
        raise IndexError("Index Error")
    

# Get crypto name based on order in the api list
def get_name(symbol_i):
    try:
        return api['data'][symbol_i]['slug']
    except IndexError:
        raise IndexError("Index Error")


# Get crypto info based on the order in the api list
def get_price(symbol_i):
    return api['data'][symbol_i]['quote']['USD']['price']

def get_symbol(symbol_i):
    return api['data'][symbol_i]['symbol']

def get_market_cap(symbol_i):
    return api['data'][symbol_i]['quote']['USD']['market_cap']

def get_volume_24h(symbol_i):
    return api['data'][symbol_i]['quote']['USD']['volume_24h']

def get_percent_change_1h(symbol_i):
    return api['data'][symbol_i]['quote']['USD']['percent_change_1h']

def get_percent_change_24h(symbol_i):
    return api['data'][symbol_i]['quote']['USD']['percent_change_24h']




if __name__ == "__main__":
    main()