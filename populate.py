"""
 Walter 20.2.18
    I just generated the "market" app.
    We need to introduce new models, build the database and decide how to populate the database with this script.
"""



import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketDays.settings')

import django
django.setup()
from market.models import Category, Page

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

    users = {}
    items = {}
    sessions = {}
    offers = {}

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

if __name__=='__main__':
    print("Starting MarketDays population script...")
    populate()

