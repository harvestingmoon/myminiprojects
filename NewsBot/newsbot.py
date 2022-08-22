from telegram import *
from telegram.ext import*
from gnews import GNews
import random
# TODO Implement summary list inside (uses NLP)
# Bot that can provide news across 5 different topics
from newspaper import Article
import os 
import validators
ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT = range(8) 
A,B,C,D = range(4)
API_KEY = #insert your own api key here
bot = Bot(token=API_KEY)
PORT = int(os.environ.get('PORT','8443'))
def topnews():
    a = GNews().get_top_news()
    random_top_news = random.sample(a,1)
    for news in random_top_news:
        headline = news['title']
        return headline
def startcommand(update: Update,_: CallbackContext):
    keyboard = [[InlineKeyboardButton("Summarise News",callback_data =  str(ONE) )],
    [InlineKeyboardButton("News", callback_data= str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'HEADLINES: {topnews()} \n\nWelcome To News Bot! Choose The Options Below!\n\ncreated by ~WY(@harvestingmoon)',reply_markup = reply_markup)
    return A

def main_menu(update: Update,_ : CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Summarise News",callback_data =str(ONE))],
    [InlineKeyboardButton("News",callback_data = str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f'HEADLINES: {topnews()} \n\nWelcome To News Bot! Choose The Options Below!\n\ncreated by ~WY(@harvestingmoon)', reply_markup = reply_markup)
    return A

def end(update: Update,_ : CallbackContext):
    update.message.reply_text("Ending News Bot Immediately... Do /start to begin again")
    return ConversationHandler.END

def news(update: Update,_: CallbackContext):
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(f'Pick a Category: World, Nation, Business, Technology, Entertainment, Sports, Science, Health')
    return C

topics = ['WORLD','NATION','BUSINESS','TECHNOLOGY','ENTERTAINMENT','SPORTS','SCIENCE','HEALTH']

def topic_lever(user_input):
    if user_input.upper() in topics:
        return True
    return False

#TODO ( add your GNEWs JSON formatting shit in here)

def format(user_input):
    user_input = str(user_input).upper()
    news = GNews()
    news = news.get_news_by_topic(user_input)
    sample_news = random.sample(news,3)
    temp_array = []
    for new in sample_news:
        title = new['title']
        description = new['description']
        published_date = new['published date']
        url = new['url']
        msg = f'Title: {title}\nDate: {published_date}\n\nSummary: {description}\n\nLink: {url}'
        temp_array.append(msg)
    return f'{temp_array[0]}\n\n\n{temp_array[1]}\n\n\n{temp_array[2]}'
    
def random_news(update: Update,_:CallbackContext):
    news = GNews()
    news = news.get_top_news()
    sample_news = random.sample(news,1)
    temp_array = []
    for new in sample_news:
        title = new['title']
        description = new['description']
        published_date = new['published date']
        url = new['url']
        msg = f'Title: {title}\nDate: {published_date}\n\nSummary: {description}\n\n\nLink: {url}'
        temp_array.append(msg)
    update.message.reply_text(temp_array[0])
    return ConversationHandler.END
def topic_chosen(update: Update,_: CallbackContext):
    user_input = update.message.text
    topic_lever(user_input)
    if topic_lever(user_input) is True:
        keyboard = [
            [InlineKeyboardButton("Main Menu",callback_data = str(THREE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(format(user_input),reply_markup=reply_markup)
        return A
    else:
        keyboard = [
            [InlineKeyboardButton("Key Again",callback_data = str(TWO))],
            [InlineKeyboardButton("Main Menu",callback_data = str(THREE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("This Is Not A Category!",reply_markup = reply_markup)
        return A
def summarise(update: Update,_ :  CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Paste The Link Of The Newspaper Below! (So That I Can Summarise It For You)")
    return B
def summarise_input(user_input):
    article = Article(str(user_input))
    article.download()
    article.parse()
    article.nlp()
    return str(article.summary)

def valid(user_input):
    return validators.url(user_input)
    
def summarise_reply(update: Update,_:CallbackContext):
    user_input = update.message.text
    if valid(user_input) is True:
        keyboard = [
            [InlineKeyboardButton("Main Menu", callback_data = str(THREE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(summarise_input(user_input),reply_markup = reply_markup)

        return A
    else:
        keyboard = [
            [InlineKeyboardButton("Try Again",callback_data = str(ONE))],
            [InlineKeyboardButton("Main Menu",callback_data = str(THREE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Invalid Link! Try Again",reply_markup = reply_markup)
        return A

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(API_KEY, use_context=True)
    main_conv = ConversationHandler(
        entry_points= [CommandHandler('start',startcommand)],
        states = {
            A: [ CallbackQueryHandler(summarise,pattern = '^' + str(ONE) + '$'),
                CallbackQueryHandler(main_menu, pattern = '^' + str(THREE) + '$'),
                CallbackQueryHandler(news, pattern = '^' + str(TWO) + '$')

            ], 
            B: [
                MessageHandler(Filters.text, summarise_reply)
            ],
            C : [
                MessageHandler(Filters.text,topic_chosen)
            ]
        },
      fallbacks= [CommandHandler("start",startcommand)]
    )
    link = str()#insert your heroku link here
    dp = updater.dispatcher
    dp.add_handler(main_conv)
    dp.add_handler(CommandHandler("end",end))
    dp.add_handler(CommandHandler("random",random_news))
    updater.start_webhook(listen= "0.0.0.0",
    port = PORT,
    url_path = API_KEY,
    webhook_url = link + API_KEY)
    updater.idle()

if __name__ == '__main__':
    main()