
from telegram import *
import re 
from requests import *
import requests, json
from telegram.ext import *
# bot should be able to provided the day of the weather previously 
# bot should be able to provide metrics in terms of pictures if possible (using the desc from open weather api)
# bot is able to save up to 5 cities 
# bot provides both pictures and description of the weather (through openweatherapi sources)
ONE,TWO,THREE,FOUR,FIVE = range(5) #list assignment for saved cities
A,B,C,D = range(4)
base_url = "https://api.openweathermap.org/data/2.5/weather?" #openweather api
API_KEY = "INSERT YOUR BOT API KEY HERE"
W_KEY = "INSERT YOUR WEATHER API KEY HERE"
bot = Bot(token=API_KEY)

#begin command of a weather bot
def startcommand(update,context):
    keyboard = [[InlineKeyboardButton("Search For City/ Country",callback_data =  str(ONE))],
    [InlineKeyboardButton("Saved Cities",callback_data = str(TWO))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(update.effective_chat.id, "https://www.hellowonderful.co/ckfinder/userfiles/images/weather%20wheel-4.jpg")
    update.message.reply_text("I am Weatherbot, what would you like to do?\n~ Version 1.0.0",reply_markup = reply_markup)
    return A
#in reference back to main menu 
def startcommand2(update,context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Search For City/ Country",callback_data =  str(ONE))],
    [InlineKeyboardButton("Saved Cities",callback_data = str(TWO))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(update.effective_chat.id, "https://www.hellowonderful.co/ckfinder/userfiles/images/weather%20wheel-4.jpg")
    query.message.reply_text("I am Weatherbot, what would you like to do?\n~ Version 1.0.0",reply_markup = reply_markup)
    return A
# requests for weather input by user 
def weather(update: Update,_ :  CallbackContext):
    query = update.callback_query
    query.answer()
    
    query.edit_message_text("Please Input City")
    return B
#Saved Data        
city = []
# temoporarily stores country inside 
temp = []  
#data retrieval format 
def c_input(user_input):
    complete_url = base_url + "appid=" + W_KEY + "&q=" + user_input + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        #store the value of main
        y = x["main"]
        c_temp = y["temp"]
        c_pressure = y["pressure"]
        c_humidity = y["humidity"]
        z = x["weather"]
        desc = z[0]["description"]
        final = " Country/City:" + user_input.capitalize() + "\nTemperature:" + str(c_temp)  + "c\nAtmospheric Pressure:" + str(c_pressure) + "hPa\nHumidity:" + str(c_humidity) + "%\nDescription:" + str(desc)
        temp.append(user_input)
        return final
    else:
        error = "Country/ City does not exist"
        return error
#saved data menu + function
def save(update: Update, context):
    query = update.callback_query
    query.answer()
    city.append(temp[-1])
    ced = str(city[-1])
    country = ced.capitalize() + " has been saved!"
    keyboard = [[InlineKeyboardButton(" New Country/ City",callback_data = str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(country,reply_markup = markup)
    return A
# number of saved cities (max five) , inside the dframe (it is very much possible to make it infinite )
def saved_cities(update: Update, context):
    query = update.callback_query
    query.answer()
    if city != []:
        country_names = city
        keyboard = [[InlineKeyboardButton(n.capitalize(),callback_data= str(i+1))] for i,n in enumerate(country_names)]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Saved Cities \n You can only save up to 5 cities", reply_markup = markup)
        return C
    else:
        keyboard = [[InlineKeyboardButton("New City/Country",callback_data = str(ONE))],
        [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("No City/Country Saved",reply_markup = markup)
        return A

#Saved dataframe
def country_1(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    c1 = city[0]
    keyboard = [[InlineKeyboardButton("Another City/Country",callback_data= str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    reply = c_input(c1)
    query.edit_message_text(reply, reply_markup = markup)
    print(c1)
    return A
def country_2(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    c1 = city[1]
    keyboard = [[InlineKeyboardButton("Another City/Country",callback_data= str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    reply = c_input(c1)
    query.edit_message_text(reply, reply_markup = markup)
    print(c1)
    return A
def country_3(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    c1 = city[2]
    keyboard = [[InlineKeyboardButton("Another City/Country",callback_data= str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    reply = c_input(c1)
    query.edit_message_text(reply, reply_markup = markup)
    print(c1)
    return A
def country_4(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    c1 = city[3]
    keyboard = [[InlineKeyboardButton("Another City/Country",callback_data= str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    reply = c_input(c1)
    query.edit_message_text(reply, reply_markup = markup)
    return A
def country_5(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    c1 = city[-1]
    keyboard = [[InlineKeyboardButton("Another City/Country",callback_data= str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit",callback_data = str(FOUR))]]
    markup = InlineKeyboardMarkup(keyboard)
    reply = c_input(c1)
    query.edit_message_text(reply, reply_markup = markup)
    return A



#gets the icon label
def c_desc(user_input):
    complete_url = base_url + "appid=" + W_KEY + "&q=" + user_input + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    a = x["weather"]
    icon = a[0]["icon"]
    link = "http://openweathermap.org/img/wn/"+ str(icon) + "@2x.png"
    
    return link
    result 
#combines both the data as well as current weather displayed 
def c_reply(update: Update,_:CallbackContext):
    user_input = update.message.text
    p_test = c_input(user_input)
    link = c_desc(user_input)
    bot.send_photo(update.effective_chat.id,link)
    keyboard = [[InlineKeyboardButton("Save City/Country",callback_data =  str(THREE) )],
    [InlineKeyboardButton("Another City/Country",callback_data = str(ONE))],
    [InlineKeyboardButton("Menu",callback_data = str(FIVE))],
    [InlineKeyboardButton("Exit", callback_data = str(FOUR))]]
    reply = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(p_test,reply_markup= reply)
    return A


def error(update,context):
    print(f"Update {update} caused error {context.error}")
def exit(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Exiting...")
    return ConversationHandler.END
# menu conversation handler 
def main():
    updater = Updater(API_KEY, use_context=True)
    main_conv = ConversationHandler(
        entry_points= [CommandHandler('start',startcommand)],
        states = {
            A: [ CallbackQueryHandler(weather,pattern = str(ONE)),
            CallbackQueryHandler(saved_cities, pattern = str(TWO)),
            CallbackQueryHandler(save, pattern = str(THREE)),
            CallbackQueryHandler(exit,pattern = str(FOUR)),
            CallbackQueryHandler(startcommand2,pattern = str(FIVE))
            ], 
            B: [
                MessageHandler(Filters.text, c_reply)
            ],
            #work on callbackqueryhandler
            C: [CallbackQueryHandler(country_1, pattern = str(1)),
            CallbackQueryHandler(country_2, pattern = str(2)),
            CallbackQueryHandler(country_3, pattern = str(3)),
            CallbackQueryHandler(country_4, pattern = str(4)),
            CallbackQueryHandler(country_5, pattern = str(5)),
            CallbackQueryHandler(startcommand2, pattern = str(FIVE))
            ]

        },
      fallbacks= [CommandHandler("start",startcommand)]
    )
    
    dp = updater.dispatcher
    dp.add_handler(main_conv)
    
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()