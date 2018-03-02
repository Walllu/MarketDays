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
    """
    python_pages = [
            {"title":"Official Python Tutorial",
                "url":"https://docs.python.org/2/tutorial/",
                "views":128},
            {"title":"How to Think like a Computer Scientist",
                "url":"http://www.greenteapress.com/thinkpython/",
                "views":100},
            {"title":"Learn Python in 10 Minutes",
                "url":"http://www.korokithakis.net/tutorials/python/",
                "views":200}]
    django_pages = [
            {"title":"Official Django Tutorial",
                "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
                "views":122},
            {"title":"Django Rocks",
                "url":"http://www.djangorocks.com/",
                "views":1000},
            {"title":"How to Tango with Django",
                "url":"htt://www.tangowithdjango.com/",
                "views":103}
            ]

    other_pages = [
            {"title":"Bottle",
                "url":"http://bottlepy.org/docs/dev/",
                "views":1222},
            {"title":"Flask",
                "url":"http://flask.pocoo.org",
                "views":15}
            ]
    cats = {"Python":{"pages":python_pages, "views":128, "likes":64},"Django":{"pages":django_pages, "views":64, "likes":32},"Other Frameworks":{"pages":other_pages, "views":32, "likes":16}}


    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data["views"], likes=cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], views=p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c),str(p)))

    """

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
    i = 1
    for line in f:
        details = line.split("\t")
        add_user(i, details[0], details[1], details[2], details[3], int(details[4]), details[5], details[6], details[7])
        i += 1


# We'll need to implement a few more functions, I don't think we need to worry about "user permissions" when we just shove data into the database
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views=0,likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
    
def add_user(id, uname, fname, lname, email, phone, desc, inter, start):
    print "Adding user: " + str(id)
    
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

if __name__=='__main__':
    print("Starting MarketDays population script...")
    populate()

