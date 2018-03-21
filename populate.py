"""
 Walter 20.2.18
    I just generated the "market" app.
    We need to introduce new models, build the database and decide how to populate the database with this script.
"""


import glob, os
from shutil import copyfile
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDays.settings')
base_dir = os.path.abspath(__file__)  # get current directory
data_path = base_dir[:-12] + "/population_resource/data/"
data_path = data_path.replace("\\", "/")

import django
from django.contrib.auth.hashers import make_password
from django.core.files import File
django.setup()
# from market.models import Category, Page, UserProfile, Item
from market.models import UserProfile, Item, User, Session, SessionParticipants, Offer, OfferContent
from datetime import datetime, timedelta
from django.utils import timezone

def populate():
    users = [
            {"username":"Johnnyy", "fname":"Johhny","lname":"Pun","password":"Johnny", "email":"2329819P@student.gla.ac.uk","phonenumber":"123456789","desc":"","interests":""},
            {"username":"Olee", "fname":"Ole","lname":"Stubben","password":"Ole", "email":"2270838S@student.gla.ac.uk","phonenumber":"123456789","desc":"","interests":""},
            {"username":"Pawell", "fname":"Pawel","lname":"Heldt","password":"Pawel", "email":"2268686H@student.gla.ac.uk","phonenumber":"123456789","desc":"","interests":""},
            {"username":"Wally", "fname":"Walter","lname":"Leinonen","password":"Walter", "email":"2270077L@student.gla.ac.uk","phonenumber":"123456789","desc":"","interests":""},
            {"username":"Rosannaaa", "fname":"Rosanna","lname":"smth","password":"Rosanna", "email":"rosanna@gmail.com","phonenumber":"123456789","desc":"Im a fashion student","interests":"I love clothes!"},
            {"username":"Komorii", "fname":"Komori","lname":"smthsm","password":"Komori", "email":"komori@gmail.com","phonenumber":"123456789","desc":"Im from Japan","interests":"I love to cook!"},
            {"username":"Georgie", "fname":"George","lname":"Thiefman","password":"George", "email":"george@gmail.com","phonenumber":"123456789","desc":"Im a smalltime thief looking to expand","interests":"I like shiny things and money"},
            ]

    items = [
            {"posterID":"1", "phonenumber":"1234567", "pic":None, "desc":"", "interests":"", "startdate":""},
            {},
            {},
            ]
    sessions = []
    offers = []

    se_names = [ "Oedipus", "Narcissus", "Minerva" ]

    for i in range(3):
        details = [None, None, None]
        details[0] = se_names[i]
        details[1] = i * 4 + 17
        details[2] = i * 3 + 13
        print "Adding session: " + str(i)
        add_session(i, details)

    f = open("./population_resource/data/users.txt")
    #with f as open("./population_resource/data/users.txt"):
    i = 1
    for line in f:
        details = line.split("\t")
        add_user(i, details)
        i += 1
    f.close()

    f = open("./population_resource/data/items.txt")
    i = 1
    for line in f:
        details = line.split("\t")
        add_item(i, details)
        i += 1
    f.close()



def add_sub_user(username, email, password):
    user = User.objects.create(username=username)
    user.email = email
    user.password = make_password(password)
    user.save()

    return user


# We'll need to implement a few more functions, I don't think we need to worry about "user permissions" when we just shove data into the database
def add_user(id, details):
    #print "Adding user: " + str(id)

    '''
    details list:
        0: uname
        1: fname
        2: lname
        3: email
        4: phone
        5: bio
        6: interests
        7: password
        8: date
    '''

    user = add_sub_user(details[0], details[3], details[7])

    up = UserProfile.objects.create(userID = id, user = user)

    up.user = user
    up.firstName = details[1]
    up.lastName = details[2]
    up.userPhoneNumber = details[4]
    up.userDescription = details[5]
    up.userInterests = details[6]
    up.userStartDate = datetime.now()

    profile_pic = data_path + "profile_pictures/"
    print profile_pic + str(id) + ".jpg"
    up.picture.save(str(id) + ".jpg", open(profile_pic + str(id) + ".jpg", "rb"), save=True)

    return up

def add_item(id, details):
    #print "Adding item: " + str(id)
    #print details

    possessor = UserProfile.objects.get(userID = int(details[1]))
    claimant = UserProfile.objects.get(userID = int(details[2]))

    it = Item.objects.create(itemID = id, possessorID = possessor, claimantID = claimant)

    # file: name -> owner -> claimant -> desc -> date

    it.itemName = details[0]
    it.itemDescription = details[3]
    it.itemDatePosted = datetime.now()
    
    item_pic = data_path + "item_pictures/"
    it.picture.save(str(id) + ".jpg", open(item_pic + str(id) + ".jpg", "rb"))

    return it

def add_session(id, details):
    next_week = timezone.now() + timedelta(weeks=1)
    se = Session.objects.create(sessionID=id, sessionName=details[0], sessionEnd=next_week)
    se.xCords = details[1]
    se.yCords = details[2]

    se.save()
    return se


if __name__=='__main__':
    print("Starting MarketDays population script...")
    populate()
