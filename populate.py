"""
 Walter 20.2.18
    I just generated the "market" app.
    We need to introduce new models, build the database and decide how to populate the database with this script.
"""



import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDays.settings')

import django
django.setup()
# from market.models import Category, Page, UserProfile, Item
from market.models import UserProfile, Item

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
    
    f = open("./population_resource/data/users.txt")
    #with f as open("./population_resource/data/users.txt"):
    i = 1
    for line in f:
        details = line.split("\t")
        add_user(i, details[0], details[1], details[2], details[3], int(details[4]), details[5], details[6], details[7])
        i += 1
    f.close()
    
    f = open("./population_resource/data/items.txt")
    i = 1
    for line in f:
        details = line.split("\t")
        add_item(i, details)
        i += 1
    f.close()
    

# We'll need to implement a few more functions, I don't think we need to worry about "user permissions" when we just shove data into the database    
def add_user(id, uname, fname, lname, email, phone, desc, inter, start):
    #print "Adding user: " + str(id)
    
    u = UserProfile.objects.create(userID = id)
    
    u.userName = uname
    u.firstName = fname
    u.lastName = lname
    u.email = email
    u.userPhoneNumber = phone
    u.userDescription = desc
    u.userInterests = inter
    u.userStartDate = start
    
    u.save()
    return u
    
def add_item(id, details):
    #print "Adding item: " + str(id)
    #print details
    
    possessor = UserProfile.objects.get(userID = int(details[1]))
    claimant = UserProfile.objects.get(userID = int(details[2]))
    
    it = Item.objects.create(itemID = id, possessorID = possessor, claimantID = claimant)
    
    # file: name -> owner -> claimant -> desc -> date
    
    it.itemName = details[0]
    it.itemDescription = details[3]
    it.itemDatePosted = details[4]
    
    it.save()
    return it

if __name__=='__main__':
    print("Starting MarketDays population script...")
    populate()

