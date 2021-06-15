from telebot import types
import telegram
import geofind
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import telebot
key=<token>
api_key=key
bot=telebot.TeleBot(api_key)
print(bot.get_me())
info=[]
@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message,"Hii")

@bot.message_handler(commands=['start'])
def begin(message):
        bot.send_message(message.chat.id,'I am Groot!\n'+ 'I collect location and name of the trees present in GRIET Campus for Geotagging\n'+
        'To begin this process, I would like to know little about yourself.\n'+'What is your name?\n')

'''#Echo Room
@bot.message_handler(commands=['echo'])
def repeat(message):
    bot.send_message(message.chat.id,"Hii!! I am echo-echo. Talk to me!!")
@bot.message_handler(func=lambda message:message.text is not None)
def repeat(message):
    bot.reply_to(message,message.text)
'''


#Name and issue box
@bot.message_handler(func=lambda message:message.text is not None and '/' not in message.text)
def msg(message):
    name=message.text
    
    if(len(info)==0):
        info.append(name)
        bot.reply_to(message,"Hii "+message.text)
        bot.send_message(message.chat.id,'Thank you and tap /tree for mentioning the name of the tree')
    elif(len(info)==5):
        m=InlineKeyboardMarkup()
        b=InlineKeyboardButton(text='Home',url='https://grietstudent.github.io/GRIETtrees/')
        m.add(b)
        bot.send_message(message.chat.id,"Thanks for coming here!! You can go back to the Home Page",reply_markup=m)    
        info.append(name)
        geofind.worksheet.append_row(info)
        info.clear()
    else:
        bot.send_message(message.chat.id,"Sorry I didn't get you can we start from the beginning?\nTap /start for beginning...")
        info.clear()    

#Tree Box
@bot.message_handler(commands=['tree'])
def get(message):
    bot.reply_to(message,"Select the below trees")
    m=InlineKeyboardMarkup()
    b1=InlineKeyboardButton(text='Mango Tree',callback_data='mango tree')
    b2=InlineKeyboardButton(text='Tamarind Tree',callback_data='tamarind tree')
    b3=InlineKeyboardButton(text='Elephant Ear Tree',callback_data='elephantear tree')
    b4=InlineKeyboardButton(text='Sandalwood Tree',callback_data='sandalwood tree')
    b5=InlineKeyboardButton(text='Almond Tree',callback_data='almond tree')
    b6=InlineKeyboardButton(text='Ashoka Tree',callback_data='ashoka tree')
    b7=InlineKeyboardButton(text='Jackfruit Tree',callback_data='Jackfruit tree')
    b8=InlineKeyboardButton(text='Peepal Tree',callback_data='Peepal Tree')
    m.add(b1,b2)
    m.add(b3,b4)
    m.add(b5,b6)
    m.add(b7,b8)
    bot.send_message(message.chat.id,"Select the tree",reply_markup=m)

#Callback of tree            
@bot.callback_query_handler(func=lambda callback: True)
def call(callback):
    tree=callback.data
    info.append(tree)
    bot.send_message(callback.message.chat.id,"Now tap /locate for sending the location of the tree.")


#Locate-Keyboard
@bot.message_handler(commands=['locate'])
def locating(message):
    print("Initiating location.....")
    markup=telebot.types.ReplyKeyboardMarkup()
    location_keyboard=telegram.KeyboardButton(text="Share the location!!",request_location=True)
    markup.add(location_keyboard)
    bot.send_message(message.chat.id,"Can you please share the location and stand near to the tree for accuracy",reply_markup=markup)


#Taking Location
@bot.message_handler(content_types=['location'])
def find(message):
    lat=message.location.latitude
    lon=message.location.longitude
    print("Printing the co-ordinates")
    info.append(lat)
    info.append(lon)
    bot.send_message(message.chat.id,"Thank you for your contribution "+info[0]+". Your Participation is highly appreciated!!")
    url="https://www.google.com/maps/search/?api=1&query="+str(lat)+","+str(lon)
    info.append(url)
    '''print("Latitude ",lat)
    print("Longitude ",lon)
    print("Now the data is ready...")
    print("Take a look..",info)'''
    bot.send_message(message.chat.id,"Do let me know if the tree has any diseases")
    


#Tree box Earlier
'''@bot.message_handler(func=lambda message:message.text is not None and '/' not in message.text)
def msg(message):
    name_tree=message.text
    info.append(name_tree)
    bot.reply_to(message,message.text)
    bot.send_message(message.chat.id,'Excellent!! Now tap /locate to send the location of the tree')
    print(name_tree)
    print("The list is ",info)
'''


#Photo box
@bot.message_handler(content_types=['photo'])
def img(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.png', 'wb') as new_file:new_file.write(downloaded_file)



#For continuous running
bot.polling()


#Leftover functions..
#updater=Updater(token=api_key)
#dispatcher=updater.dispatcher
#item=['Mango tree','Banyan Tree','X-mas Tree','Almond Tree']
#flag=False
#choice=False
    
