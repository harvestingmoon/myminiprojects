
from re import L
from readline import replace_history_item
from tkinter import CURRENT
from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, MessageAutoDeleteTimerChanged,
                      Update, callbackquery, replykeyboardmarkup, user)
from telegram.constants import UPDATE_CHANNEL_POST
from telegram.ext import (Updater,
                          CommandHandler,
                          Filters,
                          MessageHandler,
                          ConversationHandler,
                          CallbackQueryHandler,
                          CallbackContext)
#All of this code is written in python 

print("Bot testing")

FIRST,SECOND,BMI_MENU,CAL,HEIGHT,WEIGHT,BMI = range(7)
ONE,TWO,THREE,FOUR,FIVE = range(5)


def startcommand(update: Update,_: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Calorie Calculator", callback_data = str(ONE))], 
        [InlineKeyboardButton("BMI Calculator",callback_data= str(THREE))],
        [InlineKeyboardButton("Calories For The Day",callback_data = str(FIVE))]
        
    ]

    reply_markup = InlineKeyboardMarkup(keyboard )
    update.message.reply_text("This Bot Tracks Calories As Well As BMI", reply_markup = reply_markup)
    
    return FIRST 

def back(update: Update,_: CallbackContext) -> int: 
    query = update.callback_query 
    query.answer()
    keyboard = [
         [InlineKeyboardButton("Calorie Calculator", callback_data = str(ONE))], 
        [InlineKeyboardButton("BMI Calculator",callback_data= str(THREE))],
        [InlineKeyboardButton("Calories For The Day", callback_data =str(FIVE))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("This Bot Tracks Calories As Well As BMI",reply_markup = reply_markup)
    return FIRST 

def calorie_cal(update:Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(" Breakfast ", callback_data = str(TWO))],
        [InlineKeyboardButton(" Lunch ",callback_data= str(THREE))], 
        [InlineKeyboardButton(" Dinner ",callback_data = str(FOUR))],
        [InlineKeyboardButton(" Exit ",callback_data = str(ONE))]


    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text("What Are You Having Now?", reply_markup = reply_markup)
    return SECOND 

#Ask for the user inputs
def breakfast(update: Update,_: CallbackContext): 
    query = update.callback_query
    query.answer() 
    query.edit_message_text("Please Key In The Amount Of Calories You Had For Breakfast")
    return CAL

def lunch(update: Update,_: CallbackContext): 
    query = update.callback_query
    query.answer() 
    query.edit_message_text("Please Key In The Amount Of Calories You Had For Lunch")

    return CAL

def dinner(update: Update,_: CallbackContext): 
    query = update.callback_query
    query.answer() 
    query.edit_message_text("Please Key In The Amount Of Calories You Had For Dinner")

    return CAL

#Portion where the calories are being input
def calorie_input(user_input):
    try: 
        user_int = int(user_input)
        cal.append(user_int)
    except ValueError: 
        false_answer = "This Is Not A Number"
        return false_answer
    answer = "You Have Keyed In " + user_input + " Calories! Click Back To Go Back To The Main Menu"
    
    return answer
    
#Storing Data in a class 

cal = []

# calculates total cals
def cal_calculator(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Back", callback_data = str(ONE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    
    
    query.edit_message_text(f'You Have Consumed {str(sum(cal))} Calories Today!',reply_markup = reply_markup)
    return SECOND

#Portion where calories are being received 

def calorie_reply(update: Update,_ : CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Back", callback_data = str(ONE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_input = update.message.text 
    update.message.reply_text(calorie_input(user_input),reply_markup = reply_markup)
    return SECOND
    
#Area where bmi is being stored 
w = [] # weight data
h = [] #height data 
current_bmi = []
def bmi_choice(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Current BMI",callback_data = str(ONE))],
        [InlineKeyboardButton("New BMI", callback_data = str(TWO))]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f'Welcome to BMI Menu, What Would You Like To Do?',reply_markup = reply_markup)

    return BMI_MENU
def recorded_bmi(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    a = bool(current_bmi)
    if a is False:
            keyboard = [
            [InlineKeyboardButton("Yes",callback_data = str(TWO))],
            [InlineKeyboardButton("No, Bring Me To Main Menu",callback_data = str(THREE))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("You Have Not Input Your BMI. Would You Like To Do It?", reply_markup = reply_markup)
            return BMI_MENU
    else:
            keyboard = [
                [InlineKeyboardButton("Main Menu", callback_data= str(THREE))],
                [InlineKeyboardButton("Update BMI",callback_data = str(TWO))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(f'Your BMI Is Currently {str(current_bmi[-1])} Would You Like To Change Your BMI?',reply_markup= reply_markup)
            return BMI_MENU

   

def body(update:Update,_: CallbackContext):
    query = update.callback_query 
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Exit",callback_data = str(ONE))]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text("Please Key In Your Height In Centimetres!", reply_markup = reply_markup)
    return HEIGHT
    #Height input reply
def height_input(user_input):
    try: 
        user_int = float(user_input)
        user_val = user_int/100
        h.append(user_val * user_val)
    except ValueError: 
        false_answer = "This Is Not A Number"
        return false_answer
    answer = "You Have Keyed In " + str(user_val) + "m As Your Height! Please Key In Your Weight In Kilograms (To The Nearest 1 Decimal Place)!"
    
    return answer
    #Height reply 
def height_reply(update: Update,_ : CallbackContext):
    user_input = update.message.text 
    update.message.reply_text(height_input(user_input))
    return WEIGHT

def weight_input(user_input): 
    try: 
        user_int = float(user_input)
        w.append(user_int)
    except ValueError:
        false_answer = "This Is Not A Number"
        return false_answer
    answer = "You Have Keyed In " + str(user_int) + "kg As Your Weight! Press Next For Your BMI"
    return answer

def weight_reply(update: Update,_: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Next",callback_data  = str(ONE))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_input = update.message.text
    update.message.reply_text(weight_input(user_input),reply_markup =reply_markup)
    return BMI

def bmi_calculator(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Exit",callback_data = str(ONE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    final_bmi = w[-1]/h[-1]
    final_bmi = str(round(final_bmi,2))
    current_bmi.append(final_bmi)
    query.edit_message_text(f'Your BMI Is  {final_bmi}!',reply_markup=reply_markup)
    return SECOND 



def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main(): 
    #Insert your API Key Here! 
    API_KEY = ""
    updater = Updater(API_KEY, use_context=True)
    main_conv = ConversationHandler(
        entry_points= [CommandHandler('start',startcommand)], 
        states= {
            FIRST: [
                #Calorie count
                CallbackQueryHandler(calorie_cal, pattern = '^' + str(ONE) + '$'
                ),
                #BMI calculator
                CallbackQueryHandler(bmi_choice, pattern = '^' + str(THREE) + '$'
                ),
                #Total Calories Consumed
                CallbackQueryHandler(cal_calculator,pattern = '^' + str(FIVE) + '$')
            ],

            SECOND: [
                CallbackQueryHandler(back, pattern = '^' + str(ONE) + '$'), 
                CallbackQueryHandler(breakfast, pattern = '^' + str(TWO) + '$'),
                CallbackQueryHandler(lunch, pattern = '^' + str(THREE) + '$'),
                CallbackQueryHandler(dinner, pattern = '^' + str(FOUR) + '$')



            ],
#BMI Calculator: 
            BMI_MENU: [
                CallbackQueryHandler(body,pattern = '^' + str(TWO) + '$'),
                CallbackQueryHandler(recorded_bmi, pattern = '^' + str(ONE) + '$'),
                CallbackQueryHandler(back,pattern = '^' + str(THREE) + '$')

            ],
            CAL: [
                MessageHandler(Filters.text,calorie_reply) 
            ], 

            HEIGHT: [
                MessageHandler(Filters.text,height_reply),
                CallbackQueryHandler(back,pattern = '^' + str(ONE) + '$')
            ],
            WEIGHT: [
                MessageHandler(Filters.text, weight_reply)
            ],
            BMI: [
                CallbackQueryHandler(bmi_calculator, pattern = '^' + str(ONE) + '$')
            ]

            
        }, 
        fallbacks= [CommandHandler("start",startcommand)],


    )
    dp = updater.dispatcher
    dp.add_handler(main_conv)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    