
from telegram import * 
from telegram.ext import *
from yahoofinancials import YahooFinancials #impt
import finnhub #impt
import random # needed to randomize your customize random news
import wikipedia # random info about the company
from datetime import datetime # converting unix tiem stamp into utc

from reformat_stock import summary_list
API_KEY =  # actual bot api key
finnhub_client = finnhub.Client(api_key =  ) #finnhub api client key
bot = Bot(token = API_KEY)
#range datasets
ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT = range(8) 
A,B,C,D,E = range(5)
def startcommand(update: Update,_:CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Find Stock",callback_data =  str(ONE) )],
    [InlineKeyboardButton("News",callback_data = str(EIGHT))],
    [InlineKeyboardButton("Exit",callback_data= str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(update.effective_chat.id,"https://cdn1.iconfinder.com/data/icons/business-and-safety-liconica-color/128/mobile-bank-app-finance-2-512.png")
    update.message.reply_text("Welcome To Stock Bot! Choose The Options below!",reply_markup = reply_markup)
    return A
#returns back to main menu after starting
def main_menu(update: Update,_:CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Find Stock", callback_data = str(ONE))],
        [InlineKeyboardButton("News",callback_data = str(EIGHT))],
        [InlineKeyboardButton("Exit",callback_data = str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Welcome To Stock Bot! Choose the Options Below!", reply_markup = reply_markup)
    return A

#temporarily stores general news data for the day
general_news = []

## news filtering time
def news_filter():
    news = finnhub_client.general_news('general',min_id = 0)
    if not general_news:
        for i in news:
                if i["category"] == "top news":
                    general_news.append(i)        
    else:
        return None

#returns the formatted news at the start menu (very important)
def news_format(random_news):
    ts = datetime.utcfromtimestamp(random_news["datetime"]).strftime('%Y-%m-%d %H:%M:%S')
    headline = random_news["headline"]
    source = random_news["source"]
    summary = random_news["summary"]
    return (f'Headlines: {headline}\n'
    f'Time: {ts}\n'
    f'Summary: {summary}\n'
    f'source: {source}')


#returns news
def news(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    news_filter()
    #picks sample w/o duplicates
    s = random.sample(general_news,3)
    #news1,2 and 3 
    n1 = news_format(s[0])
    n2 = news_format(s[1])
    n3 = news_format(s[2])
    # returns the full news
    final_print_out = f'{n1}\n\n\n{n2}\n\n\n{n3}'
    keyboard = [
        [InlineKeyboardButton("Exit",callback_data= str(TWO)), InlineKeyboardButton("Main Menu", callback_data= str(THREE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(final_print_out
    ,reply_markup = reply_markup)
    return A

#kills the conversation
def end(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("This Bot will now exit. Thank you for using it! Use /start to start again!")
    return ConversationHandler.END

stock = [] #temporarily stores data of the stock ticker symbol


#users request for stock choice
def find_stock(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Please key In The Stock Of Choice! (TICKER SYMBOLS ONLY)\n Else the data you received is None")
    return D

#checks if users stock exists , None = does not exist inside the system
def stock_lever(user_input):
    a = str(user_input)
    yahoo_financials = YahooFinancials(a.upper())  
    if str(yahoo_financials.get_current_price()) == str(None):
        return False
    return True
#true set for existance of user storck
def stock_inputtrue(user_input):
    a = str(user_input)
    yahoo_financials = YahooFinancials(a.upper())
    return f'Stock Price of {a.upper()} is currently at {yahoo_financials.get_current_price()}.\n Daily High Of: {yahoo_financials.get_daily_high()}\n Daily Low Of: {yahoo_financials.get_daily_low()}\n Click on other buttons to find more about the stock!'
#false
def stock_inputfalse(user_input):
    a = str(user_input).upper()
    return f'The Stock you have placed: {a} does not exist!'
#reply of user
def stock_reply(update: Update,_:CallbackContext):
    user_input = update.message.text
    lev = stock_lever(user_input)
    if lev is True:
        a = str(user_input)
        stock.append(a.upper())
        company_info = finnhub_client.company_profile2(symbol = a.upper())
        comp_logo = company_info["logo"]
        bot.send_photo(update.effective_chat.id, comp_logo)
        keyboard = [
            [InlineKeyboardButton("About", callback_data = str(SIX))],
            [InlineKeyboardButton("Summary Data",callback_data = str(FOUR)),
            InlineKeyboardButton("Dividends",callback_data = str(FIVE))],
            [InlineKeyboardButton("P/E", callback_data = str(SEVEN)),
            InlineKeyboardButton("Main Menu", callback_data = str(ONE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(stock_inputtrue(user_input),reply_markup = reply_markup)
        return E
    elif lev is False:
        keyboard = [
            [InlineKeyboardButton("Key Stock Again", callback_data = str(ONE))],
            [InlineKeyboardButton("Main Menu", callback_data = str(THREE))],
            [InlineKeyboardButton("Exit",callback_data = str(TWO))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(stock_inputfalse(user_input),reply_markup = reply_markup)
        return A

#summary data , reformatting is done in reformat stock 
def formatting(user_input): #reformatting the summary details (basic)
    yahoo_financials = YahooFinancials(user_input)
    a = yahoo_financials.get_summary_data()
    summary_vals = list(a[user_input].values())
    i = 0
    summary_keys = summary_list()
    new_list = []
    del stock[0]
    while i < len(summary_vals):
        new_list.append(f'{summary_keys[i]}: {summary_vals[i]}\n')
        i += 1
    return ''.join(new_list)
    


#returns summary of the stock, however main formatting is namely done in the formatting function
def summary(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Main Menu", callback_data = str(THREE)),
        InlineKeyboardButton("Exit",callback_data = str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        f'Non-Exhaustive Summary Details of {stock[0]}\n\n{formatting(stock[0])}',reply_markup = reply_markup
    )
    return A

#dividends
def div(user_input):
    yahoo_financials = YahooFinancials(user_input)
    div_yield = yahoo_financials.get_dividend_yield()
    div_yield_annum = yahoo_financials.get_annual_avg_div_yield()
    div_yield_5 = yahoo_financials.get_five_yr_avg_div_yield()
    
    div_rate = yahoo_financials.get_dividend_rate()
    div_rate_annum = yahoo_financials.get_annual_avg_div_rate()

    del stock[0]
    return ( f' Dividend Yield: {div_yield}\n Yearly Average: {div_yield_annum}\n 5 Year Average: {div_yield_5}\n'
             f' Dividend Rate: {div_rate}\n Yearly Average: {div_rate_annum}')

def dividend(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Main Menu", callback_data = str(THREE)),
        InlineKeyboardButton("Exit", callback_data = str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(div(stock[0]),reply_markup=reply_markup)
    return A



#figuring out companies info using wikipedia
def company_about(user_input): #where information of the company is being sent to
    company_info = finnhub_client.company_profile2(symbol = user_input)
    comp_name = company_info['name']
    del stock[0]
    return f'{wikipedia.summary(comp_name,sentences = 3)}'

def about(update: Update,_: CallbackContext): #sends the info (inclusive of logo and about)
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Exit", callback_data = str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(company_about(stock[0]),reply_markup = reply_markup)

    return A
#price equity
def pe(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    yahoo_financials = YahooFinancials(stock[0])
    del stock[0]
    keyboard = [
        [InlineKeyboardButton("Exit",callback_data = str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f'P/E Ratio:{yahoo_financials.get_pe_ratio()}',reply_markup = reply_markup)
    return A

#any error raised will be printed out here, alternatively this can also be deployed to heroku with slight modifications
def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(API_KEY, use_context=True)
    main_conv = ConversationHandler(
        entry_points= [CommandHandler('start',startcommand)],
        states = {
           A: [ CallbackQueryHandler(find_stock,pattern = '^' + str(ONE) + '$'),
            CallbackQueryHandler(end, pattern = '^' + str(TWO) + '$'),
            CallbackQueryHandler(main_menu, pattern = '^' + str(THREE) + '$'),
            CallbackQueryHandler(news, pattern = '^' + str(EIGHT) + '$')
            ], 
            D: [
                MessageHandler(Filters.text, stock_reply)
            ],
            E: [
                CallbackQueryHandler(main_menu,pattern = '^' + str(ONE) + '$'),
                CallbackQueryHandler(end, pattern = '^' + str(TWO) + '$'),
                CallbackQueryHandler(summary,pattern = '^' + str(FOUR) + '$'),
                CallbackQueryHandler(dividend,pattern = '^' + str(FIVE) + '$'),
                CallbackQueryHandler(about, pattern = '^' + str(SIX) + '$'),
                CallbackQueryHandler(pe, pattern = '^' + str(SEVEN) + '$')
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

