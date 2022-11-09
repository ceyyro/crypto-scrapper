# Crypto Scrapper

#### Video Demo: https://www.youtube.com/watch?v=TiXtyL2K18w

#### Description: It's most common used info of top 10 cryptos scrapper. I used a coinmarketcap API to get the values, which updates every 60 seconds. I chose CustomTkinter library instead of tkinter, because it looks nicer. I made gui app structured as a class. It initializes basic properties and layout with 2x2 grid containing 1 option-menu and 1 button. Option-menu takes values from other function scrape() which is called at the program start. Button on-click runs function scrapebutton() which first gets recent api values then initializes formatted information.

# In order to it to work you need to place your api private key at the top of project.py in key variable
