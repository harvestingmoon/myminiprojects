
from telegram import *
from telegram.ext import *
import pandas as pd
import numpy as np
import pickle
import json
import http.client,urllib.parse
import os
#heroku logs --tail (gives you the req) 
#restaurant bot to utilise machine learning k cluster meaning technique
#restaurant bot to use positionstack api
#restaurant bot to produce meaningful data, aka produce data that is sorted based on ratings and what not... 
centroids = pd.read_csv('centroids.csv')
location_res = pd.read_csv('restaurant_loc.csv')
town_only = pd.read_csv('town_only.csv')
label = pickle.load(open("save.pkl","rb"))

ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN = range(7)
A,B,C,D = range(4)
API_KEY = "#KEY YOUR BOT API KEY HERE!"
PORT = int(os.environ.get('PORT','80'))
bot = Bot(token=API_KEY)
user_coords = [] #to temporarily store user coords
temp = [] #to temporarily store user data

def startcommand(update: Update,_: CallbackContext):
    keyboard = [[InlineKeyboardButton("Find A Restaurant Near Me!",callback_data =  str(ONE) )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome To Restaurant Bot! \n version alpha1.1.0 by harvestingmoon\n Update: Created approx distance b/n user location and restaurant! ",reply_markup = reply_markup)
    return A

def main_menu(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    global user_coords,temp #need to use this in order to change my user coords and temp 
    user_coords,temp = [],[]
    keyboard = [[InlineKeyboardButton("Find A Restaurant Near Me!",callback_data =  str(ONE) )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Welcome To Restaurant Bot! \n version alpha1.1.0 by harvestingmoon\n Update: Created approx distance b/n user location and restaurant! ",reply_markup = reply_markup)
    return A


def user_query(update: Update,_ :  CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Where are you currently?")
    return B

def food_recommendation(user_location):
        conn = http.client.HTTPConnection('api.positionstack.com')
        params = urllib.parse.urlencode({
        'access_key': '#API KEY FROM POSITION STACK', #protect this API please
        'query': f'{user_location}',
        'limit': 1,
        })
        conn.request('GET', '/v1/forward?{}'.format(params))
        res = conn.getresponse()
        data = res.read()
        d = data.decode('utf-8')

        json_data = json.loads(d)
        data = json_data["data"]
        main_data = data[0] 
        coords = [float(main_data['latitude']),float(main_data['longitude'])]
        user_coords.append(coords)
        leftbottom = coords
        leftbottom = np.array(leftbottom)
        distances = np.linalg.norm(centroids-leftbottom, axis=1)
        min_index = np.argmin(distances)+1 #necessary to +1 due to indexing issue
        final_res = location_res[label == min_index][['name','address','rating','lat','lon']].sample(n=5) #constantly shuffles rows
        fin = json.loads(final_res.to_json(orient = 'split'))
        del fin["index"]
        final_json = json.dumps(fin)
        return final_json

#aids to intepret the json into readable lists for python
# immediately send the food recomm data to json interpreter
def json_interpreter(json_string):
    json_file = json.loads(json_string)
    data = json_file["data"]
    return data
def res_transform(user_location,index): #index only 0 to 4 since random sample is 5
    res_list = json_interpreter(food_recommendation(user_location))[index]
    temp.append(res_list)
    return res_list
# approximate distance calculation between user location & restaurant
def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2
    calc = earth_radius * 2 * np.arcsin(np.sqrt(a))
    approx = round(calc,2)
    return approx

def robot_reply(update,context):
    try:
        user_location = update.message.text
        keyboard = [
            [InlineKeyboardButton(f'{res_transform(user_location,0)[0]}',callback_data= str(ONE))],
            [InlineKeyboardButton(f'{res_transform(user_location,1)[0]}',callback_data= str(TWO))],
            [InlineKeyboardButton(f'{res_transform(user_location,2)[0]}',callback_data= str(THREE))],
            [InlineKeyboardButton(f'{res_transform(user_location,3)[0]}',callback_data= str(FOUR))],
            [InlineKeyboardButton(f'{res_transform(user_location,4)[0]}',callback_data= str(FIVE))],
            [InlineKeyboardButton(f'Menu',callback_data = str(SIX))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(f'Here are the restaurants near {user_location.upper()}! \nClick on the buttons below for more info!',reply_markup = reply_markup)

        return C
    except IndexError:
        keyboard = [
            [InlineKeyboardButton("Key Again", callback_data = str(ONE))],
            [InlineKeyboardButton("Exit",callback_data =  str(TWO))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Invalid Location! Try Again!",reply_markup = reply_markup)
        return A
        
#slots to store bot
def s1(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    slot = temp[0]
    reply = f'Store Name: {slot[0]} \nLocation: {slot[1]}\nRating:{slot[2]}\nDistance: {haversine(user_coords[0][0],user_coords[0][1],slot[-2],slot[-1])} km' 
    keyboard = [[InlineKeyboardButton(f'Main Menu',callback_data = str(SIX))],
    [InlineKeyboardButton("Exit",callback_data = str(SEVEN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(reply,reply_markup = reply_markup)
    return D

def s2(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    slot = temp[1]
    reply = f'Store Name: {slot[0]} \nLocation: {slot[1]}\nRating: {slot[2]}\nDistance: {haversine(user_coords[0][0],user_coords[0][1],slot[-2],slot[-1])} km'
    keyboard = [[InlineKeyboardButton(f'Main Menu',callback_data = str(SIX))],
    [InlineKeyboardButton("Exit",callback_data = str(SEVEN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(reply,reply_markup = reply_markup)
    return D

def s3(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    slot = temp[2]
    reply = f'Store Name: {slot[0]} \nLocation: {slot[1]}\nRating: {slot[2]}\nDistance: {haversine(user_coords[0][0],user_coords[0][1],slot[-2],slot[-1])} km'
    keyboard = [[InlineKeyboardButton(f'Main Menu',callback_data = str(SIX))],
    [InlineKeyboardButton("Exit",callback_data = str(SEVEN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(reply,reply_markup = reply_markup)
    return D

def s4(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    slot = temp[3]
    reply = f'Store Name: {slot[0]} \nLocation: {slot[1]}\nRating: {slot[2]}\nDistance: {haversine(user_coords[0][0],user_coords[0][1],slot[-2],slot[-1])} km'
    keyboard = [[InlineKeyboardButton(f'Main Menu',callback_data = str(SIX))],
    [InlineKeyboardButton("Exit",callback_data = str(SEVEN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(reply,reply_markup = reply_markup)
    return D

def s5(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    slot = temp[4]
    reply = f'Store Name: {slot[0]} \nLocation: {slot[1]}\nRating: {slot[2]}\nDistance: {haversine(user_coords[0][0],user_coords[0][1],slot[-2],slot[-1])} km'
    keyboard = [[InlineKeyboardButton(f'Main Menu',callback_data = str(SIX))],
    [InlineKeyboardButton("Exit",callback_data = str(SEVEN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(reply,reply_markup = reply_markup)
    return D

def exit(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Thank you for using this bot! Hope you manage to find your desired restaurant!")
    return ConversationHandler.END
def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(API_KEY, use_context=True)
    main_conv = ConversationHandler(
        entry_points= [CommandHandler('start',startcommand)],
        states = {
            A: [ CallbackQueryHandler(user_query,pattern = '^' + str(ONE) + '$'),
                CallbackQueryHandler(exit, pattern = '^' + str(TWO) + '$')

            ], 
            B: [
                MessageHandler(Filters.text, robot_reply)
            ],
            C: [
                CallbackQueryHandler(s1,pattern = '^' + str(ONE) + '$'),
                CallbackQueryHandler(s2,pattern = '^' + str(TWO) + '$'),
                CallbackQueryHandler(s3,pattern = '^' + str(THREE) + '$'),
                CallbackQueryHandler(s4,pattern = '^' + str(FOUR) + '$'),
                CallbackQueryHandler(s5,pattern = '^' + str(FIVE) + '$'),
                CallbackQueryHandler(main_menu,pattern = '^' + str(SIX)+ '$')
            ],
            D: [
                CallbackQueryHandler(main_menu,pattern = '^' + str(SIX) + '$'),
                CallbackQueryHandler(exit, pattern = '^' + str(SEVEN)+ '$')
            ]

        },
      fallbacks= [CommandHandler("start",startcommand)]
    )
    
    dp = updater.dispatcher
    dp.add_handler(main_conv)
    updater.start_webhook(listen= "0.0.0.0",
    port = PORT,
    url_path = API_KEY,
    webhook_url = '#insert heroku webhook url here' + API_KEY,
    force_event_loop= True)
    updater.idle()

if __name__ == '__main__':
    main()

