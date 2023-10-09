import requests
import discord 
from discord.ext import commands

bot=commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot Activated!")

@bot.command()
async def air(ctx, zip: int):
    print('fetching info...')
    
    #Build API request.
    
    base_url = 'https://www.airnowapi.org'
    endpoint = '/aq/observation/zipCode/current/'
    parameters = {
        'format': 'application/json',
        'zipCode': str(zip),
        'distance': '25',
        'API_KEY': '150D1602-6B37-4735-9D6E-A659F17576CF'
    }
    response = requests.get(base_url + endpoint, params=parameters)
    
    if response.status_code == 200:
        try:
            json = response.json()
            print(json)
        
            right_dict = None
            right_one = 0


            #Parses through JSON object to find the value of the highest pollutant.
            for data in json:
                if data['AQI'] > right_one:
                    right_one = data['AQI']
                    right_dict = data

            #Sets each variable to a specific value in the portion of the JSON object that contains the highest pollutant. This will be used to create the embed later.
            else:
                reportingArea = right_dict['ReportingArea']
                aqi = right_dict['AQI']
                category = right_dict['Category']
                status = category['Name']
                pollutant = right_dict['ParameterName']

            
            #Creates initial default embed.

                air_qual_embed = discord.Embed(
                    title="Air Quality Stats",
                    color=discord.Color.green()
                )

            #Determines color based off of AQI score.
                if aqi < 51:
                    air_qual_embed.color=discord.Color.green()
                elif aqi < 101:
                    air_qual_embed.color=discord.Color.yellow()
                elif aqi < 151:
                    air_qual_embed.color=discord.Color.orange()
                elif aqi < 201:
                    air_qual_embed.color=discord.Color.red()
                elif aqi < 301:
                    air_qual_embed.color=discord.Color.purple()
                elif aqi >= 301:
                    air_qual_embed.color=discord.Color.from_rgb(128,0,0)



            #Adds the specific values of the current zip code's AQI into the embed. 
                air_qual_embed.add_field(name="Reporting Area:", value=reportingArea, inline=False)
                air_qual_embed.add_field(name="Highest Pollutant:", value=pollutant, inline=False)
                air_qual_embed.add_field(name="AQI:", value=aqi, inline=False)
                air_qual_embed.add_field(name="Status:", value=status, inline=False)


                print(reportingArea)
                print(aqi)
                print(status)
        
        #Sometimes the AirNow API can have outages. This handles the event in which the sensor in currently unavailable in a specific area or if a user submits an invalid zip code.
        except:
            air_qual_embed = discord.Embed(
            title="Error",
            description="That zip code was not found in AirNow. Try another one.",
            color=discord.Color.red()
        )


    #Sometimes the AirNow API can have outages. This handles the event in which the sensor in currently unavailable in a specific area or if a user submits an invalid zip code.
    else:
        air_qual_embed = discord.Embed(
            title="Error",
            description="That zip code was not found in AirNow. Try another one.",
            color=discord.Color.red()
        )
        
        print('Request failed with status code:', response.status_code)

    
    
    await ctx.send(embed=air_qual_embed)



bot.run('MTExODc0NTEwNDE5NTI2ODcwMQ.GemlIs.dFDUuNSmAnnNyJ2mCnlFfC7EfpulAu3v9S4bU4')