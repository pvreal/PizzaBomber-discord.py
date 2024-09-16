import os
import requests
from playwright.async_api import async_playwright
import time as t
import discord
from discord.ext import commands
from discord import app_commands

#SETUP!!
# For hosting this locally use the second option. For hosting this on something like replit use the first but do remember you have to have the env variable set-up.
#TOKEN = os.environ.get('TOKEN')
TOKEN = 'token here'
# For hosting this locally use the second option. For hosting this on something like replit use the first but do remember you have to have the env variable set-up.
#TOMTOMKEY = os.environ.get('TOMTOMKEY')
TOMTOMKEY = 'api key here'
# If you want to restrict the bot to specific channel use this and make sure to uncomment line 115,116,117
# CHANNELID = 1234567890  

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

def geocodead(api_key, address):
    url = f"https://api.tomtom.com/search/2/geocode/{address}.json"
    params = {
        'key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            position = data['results'][0]['position']
            return position['lat'], position['lon']
        else:
            print("Address not valid or found")
            return None, None
    else:
        print(f"Error: {response.status_code}")
        return None, None

def findpizza(api_key, latitude, longitude, radius=13000): # set "radius" to your desired radius. I find 9000-13000 to be the most accurate
    url = "https://api.tomtom.com/search/2/search/pizza.json"
    params = {
        'key': api_key,
        'lat': latitude,
        'lon': longitude,
        'radius': radius,
        'categorySet': '7315',
        'limit': 100
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        return results
    else:
        print(f"Error: {response.status_code}")
        return []
# Note that you may need to change these delays based on your network speed.
async def mainorderer(address, city, state, zip_code):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False) # headless does not work, I guess you can make it work by defining the viewport and such.
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.pizzahut.com")

        await page.click('button:has-text("Delivery")')
        await page.click('div.MuiGrid-root.MuiGrid-container.MuiGrid-justify-content-xs-center div.MuiGrid-root.MuiGrid-item')

        await page.fill('input#w2-address', address)
        await page.fill('input#w2-city', city)
        await page.fill('input#w2-state', state)
        await page.fill('input#w2-zip', zip_code)

        await page.click('span:has-text("Search")')
        t.sleep(1)
        await page.click('span:has-text("Continue")')
        t.sleep(5)
        await page.goto("https://www.pizzahut.com/menu/pizza/builder?id=gUVLRyQ7wZy3oTaoMsBLag")
        t.sleep(2)
        await page.click('p.MuiTypography-root:has-text("large")')
        await page.click('p.MuiTypography-root:has-text("225")')
        t.sleep(1)
        await page.click('span:has-text("add to order")')
        t.sleep(4)
        await page.goto("https://www.pizzahut.com/checkout")
        t.sleep(5)
        await page.fill('input#first-name', 'John')
        await page.fill('input#last-name', 'Doe')
        await page.fill('input#email', 'fakeemail@fake.email')
        await page.fill('input#phone-number', '123-234-5678')

        await page.click('div[data-testid="cash-tab-button"]')

        placeorderbutton = 'button[data-testid="primary-cta-button-place-order"]'

        await page.click(placeorderbutton)

        t.sleep(6)

        await page.click(placeorderbutton)
        t.sleep(4)
        await page.wait_for_selector('text=Order Confirmed', timeout=10000) # Adjust this based on your network speed.
        t.sleep(2)
        await page.screenshot(path='done.png')
        print('Pizza ordered!')
        await browser.close()
# ANYONE CAN VIEW YOUR ADDRESS IF YOUR IN A PUBLIC SERVER USING THIS COMMAND!!!
@client.tree.command(name="orderpizza", description="Order a pizza using PizzaHut")
@app_commands.describe(address="Street Name", city="City", state="State", zip_code="Postal/Zip code")
async def order_pizza(interaction: discord.Interaction, address: str, city: str, state: str, zip_code: str):
    #if interaction.channel_id != CHANNELID:
        #await interaction.response.send_message("Use the correct channel.", ephemeral=True)
        #return

    await interaction.response.defer()


    full_address = f"{address}, {city}, {state}, {zip_code}"
    latitude, longitude = geocodead(TOMTOMKEY, full_address)

    if latitude is not None and longitude is not None:
        pizza_places = findpizza(TOMTOMKEY, latitude, longitude)
        if pizza_places:
            for place in pizza_places:
                name = place.get('poi', {}).get('name', 'No Name')
                if "Pizza Hut" in name:
                    await interaction.followup.send(f"PizaHut location found: {name}. Ordering Pizza")
                    await mainorderer(address, city, state, zip_code)
                    await interaction.followup.send("Pizza Successfully ordered.", file=discord.File('done.png'))
                    return
            await interaction.followup.send("No match found.")
        else:
            await interaction.followup.send("error")
    else:
        await interaction.followup.send("Gecode error.")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    await client.tree.sync()
    print(f'Bot logged in @ {client.user} please dont do illegal or immoral stuff with these pleaseee')

def start():
    client.run(TOKEN)

if __name__ == "__main__":
    start()
