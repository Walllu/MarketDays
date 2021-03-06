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
data_path = base_dir[:-21] + "/population_resource/data/"
data_path = data_path.replace("\\", "/")

import django
from django.contrib.auth.hashers import make_password
from django.core.files import File
django.setup()
# from market.models import Category, Page, UserProfile, Item
from market.models import UserProfile, Item, User, Session, SessionParticipants, Offer, OfferContent
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max

def populate():
    # Mock data files are generated using the jupyter notebook scripts in
    # the /population_resources/generators folders.
    # Image credits to:
    # http://www.vision.caltech.edu/Image_Datasets/Caltech101/
    # http://www.vision.caltech.edu/Image_Datasets/Caltech_10K_WebFaces/

    se_names = [ "Oedipus", "Narcissus", "Minerva" ]

    # Create 3 sessions
    for i in range(3):
        details = [None, None, None]
        details[0] = se_names[i]
        details[1] = i * 4 + 17 # somewhat random numbers
        details[2] = i * 3 + 13
        add_session(i, details)

    # create a user for every line in users.txt
    f = open("./population_resource/data/users.txt")
    i = 1
    for line in f:
        details = line.split("\t")
        add_user(i, details)
        i += 1
    f.close()

    # create an item for every line in items.txt
    f = open("./population_resource/data/items.txt")
    i = 1
    for line in f:
        details = line.split("\t")
        add_item(i, details)
        i += 1
    f.close()

    # Populate each session with 11 users
    for i in range(3):
        pop_session(i)

    # Populate each session with 1 offer
    # Does not work as intended, and instead only produces a single offer
    for sid in range(3):
        for i in range(11):
            uid1 = sid * 11 + i
            try:
                it1 = Item.objects.filter(claimantID=uid1).first()
            except Item.DoesNotExist:
                it1 = None

            if it1 != None:
                for j in range(uid1 + 1, 11):
                    uid2 = sid * 11 + j
                    try:
                        it2 = Item.objects.filter(claimantID=uid2).first()
                    except Item.DoesNotExist:
                        it2 = None

                    if it2 != None:
                        add_offer(it1, it2, uid1, uid2)
                        break
                break



# Create user object. Takes 3 strings.
def add_sub_user(username, email, password):
    user = User.objects.create(username=username)
    user.email = email
    user.password = make_password(password)
    user.save()

    return user

# Create a UserProfile. Takes an int and a list of strings
def add_user(id, details):
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

    # Open an image file, load to DB, then save
    up.picture.save(str(id) + ".jpg", open(profile_pic + str(id) + ".jpg", "rb"), save=True)

    return up

def add_item(id, details):
    possessor = UserProfile.objects.get(userID = int(details[1]))
    claimant = UserProfile.objects.get(userID = int(details[2]))

    it = Item.objects.create(itemID = id, possessorID = possessor, claimantID = claimant)

    it.itemName = details[0]
    it.itemDescription = details[3]
    it.itemDatePosted = datetime.now()

    item_pic = data_path + "item_pictures/"
    
    # Open an image file, load to DB, then save
    it.picture.save(str(id) + ".jpg", open(item_pic + str(id) + ".jpg", "rb"))

    return it

def add_session(id, details):
    next_week = timezone.now() + timedelta(weeks=1)
    se = Session.objects.create(sessionID=id, sessionName=details[0], sessionEnd=next_week)
    se.xCords = details[1]
    se.yCords = details[2]

    se.save()
    return se

def add_session_participant(se, up):
    sp = SessionParticipants.objects.create(sessionID=se, participantID=up)
    sp.save()
    return sp

# Put some users in each session
def pop_session(id):
    se = Session.objects.get(sessionID=id)
    for i in range(11):
        up = UserProfile.objects.get(userID=id*11 + i + 1)
        add_session_participant(se, up)
        se.participants = int(se.participants) + 1

    se.save()
    return se

# Fill one line of the offer contents table.
# Used as part of add_offer
def add_offer_contents(offer, fid, tid, oid, it, offered):
    contents = OfferContent.objects.create(callerID=fid, calleeID=tid, itemID=it, offerID=oid, offered=offered)
    contents.save()
    return contents

# Take 2 items, 2 users, register an offer
def add_offer(it1, it2, uid1, uid2):
    fid = UserProfile.objects.get(userID=uid1)
    tid = UserProfile.objects.get(userID=uid2)
    id = Offer.objects.all().aggregate(Max('offerID'))
    try:
        oid = id['offerID__max'] + 1
    except:
        oid = 0
    msg = "Bla bla"

    offer = Offer.objects.create(offerID=oid, fromID=fid, toID=tid, message=msg)
    offer.save()

    add_offer_contents(offer, fid, tid, offer, it1, True)
    add_offer_contents(offer, fid, tid, offer, it2, False)

    return offer


if __name__=='__main__':
    print("Starting MarketDays population script...")
    populate()
