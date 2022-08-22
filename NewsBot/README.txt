This Folder contains all the requirements needed to the code fully. 
It contains:
newsbot.py file 
requirements.txt (requirements needed to be uploaded to heroku)
nlk.txt (contains all the nlk elements) 
Procfile (unique to Heroku)

To properly load these files you need:
- Heroku CLI
- Heroku account
- Git


Steps:
1. Type this into cmd: heroku login 
2. heroku create 
3. heroku git:remote (name of server created) ~ You can do this by going to heroku cli or heroku website, this is to set the remote of the heroku cli
4. git add .
5. git commit -am "name of the change"
6. git push heroku master 

At the end, you should be able to load the heroku server up.
