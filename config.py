import random
import os
import main

basedir = os.path.abspath(os.path.dirname(__file__))

#URLS
cat_url = main.get_cat_url(kitty_url = 'http://aws.random.cat/meow')
dog_url = 'http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true'
fox_url = 'https://randomfox.ca/images/'+str(random.randrange(1, 122, 1))+'.jpg'
####





