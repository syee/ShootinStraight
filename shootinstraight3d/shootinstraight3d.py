import os
import re
import random
import hashlib
import hmac
import datetime
import time
from datetime import datetime, timedelta
from string import letters
import cgi
import urllib

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import mail


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

playerList = ["Curry, Stephen", "Bryant, Kobe", "James, Lebron", "Nowitzki, Dirk", "Jordan, Deandre"]
chartTypeList = ["All Shots", "Makes Misses", "Field Goal Percentage", "Raw Points", "Point Frequency"]


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def greetings_key(group = 'default'):
    return db.Key.from_path('greetings', group)

class Greeting(ndb.Model):
    """Models a Guestbook entry with an author, content, avatar, and date."""
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    avatar = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    playerName = ndb.StringProperty()
    chartType = ndb.StringProperty()
    dimensions = ndb.StringProperty()

    @classmethod
    def by_id(cls, cid):
        return Greeting.get_by_id(cid, parent = greetings_key())

    def render(self):
        return render_str("greeting.html", greeting = self)


def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with name."""
    return ndb.Key('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')

        greetings = Greeting.query(
            ancestor=guestbook_key(guestbook_name)) \
            .order(-Greeting.date) \
            .fetch(10)

        for greeting in greetings:
            if greeting.author:
                self.response.out.write(
                    '<b>%s</b> wrote:' % greeting.author)
            else:
                self.response.out.write('An anonymous person wrote:')
            self.response.out.write('<div><img src="/img?img_id=%s"></img>' %
                                    greeting.key.urlsafe())
            self.response.out.write('<blockquote>%s</blockquote></div>' %
                                    cgi.escape(greeting.content))

        self.response.out.write("""
              <form action="/sign?%s"
                    enctype="multipart/form-data"
                    method="post">
                <div>
                  <textarea name="content" rows="3" cols="60"></textarea>
                </div>
                <div><label>Avatar:</label></div>
                <div><input type="file" name="img"/></div>
                <select name="playerName">
                  <option value="None">--------Select a player--------</option>
                  <option value="Curry, Stephen">Stephen Curry</option>
                  <option value="Bryant, Kobe">Kobe Bryant</option>
                  <option value="James, Lebron">Lebron James</option>
                  <option value="Nowitzki, Dirk">Dirk Nowitzki</option>
                  <option value="Jordan, Deandre">Deandre Jordan</option>
                </select>
                <select name="chartType">
                  <option value="None">-----Select a chart type-----</option>
                  <option value="All Shots">All Shots</option>
                  <option value="Makes Misses">Makes and Misses</option>
                  <option value="Field Goal Percentage">Field Goal Percentage</option>
                  <option value="Raw Points">Raw Points</option>
                  <option value="Point Frequency">Point Frequency</option>
                </select>
                <select name="dimensions">
                  <option value="None">-----Select 2D or 3D-----</option>
                  <option value="2D">2D</option>
                  <option value="3D">3D</option>
                </select>
                <div><input type="submit" value="Sign Guestbook"></div>
              </form>
              <hr>
              <form>Guestbook name: <input value="%s" name="guestbook_name">
              <input type="submit" value="switch"></form>
            </body>
          </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                        cgi.escape(guestbook_name)))


class Image(webapp2.RequestHandler):
    def get(self):
        greeting_key = ndb.Key(urlsafe=self.request.get('img_id'))
        greeting = greeting_key.get()
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            # self.response.headers['Content-Type'] = 'image/svg'
            greeting.avatar = images.resize(greeting.avatar, 700, 700)
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        playerName = self.request.get('playerName')
        chartType = self.request.get('chartType')
        dimensions = self.request.get('dimensions')

        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        greeting.playerName = playerName
        greeting.chartType = chartType
        greeting.dimensions = dimensions

        avatar = self.request.get('img')
        if avatar:
            # avatar = images.resize(avatar, 512, 512)
            greeting.avatar = avatar
        greeting.put()

        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    #find user entry with a certain user id and assign it to a "user" objeact
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)

class Front(Handler):
    def get(self):
        greetings1 = Greeting.query(Greeting.playerName == playerList[0]).order(Greeting.date)
        greetings2 = Greeting.query(Greeting.playerName == playerList[1]).order(Greeting.date)
        greetings3 = Greeting.query(Greeting.playerName == playerList[2]).order(Greeting.date)
        greetings4 = Greeting.query(Greeting.playerName == playerList[3]).order(Greeting.date)
        greetings5 = Greeting.query(Greeting.playerName == playerList[4]).order(Greeting.date)
        self.render('front.html', greetings1 = greetings1, greetings2 = greetings2, greetings3 = greetings3, greetings4 = greetings4, greetings5 = greetings5)

    def post(self):
        #These dropdowns could be error checked
        playerName = self.request.get('playerName')
        chartType = self.request.get('chartType')
        dimensions = self.request.get('dimensions')
        if (playerName != 'None') and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName, Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1)
        if (playerName == 'None') and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[1], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings3 = Greeting.query(Greeting.playerName == playerList[2], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings4 = Greeting.query(Greeting.playerName == playerList[3], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings5 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1, greetings2 = greetings2, greetings3 = greetings3, greetings4 = greetings4, greetings5 = greetings5)
        if (playerName != 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName, Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1)
        if (playerName != 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1)
        if (playerName != 'None') and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName, Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1)
        if (playerName == 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0]).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[1]).order(Greeting.date)
            greetings3 = Greeting.query(Greeting.playerName == playerList[2]).order(Greeting.date)
            greetings4 = Greeting.query(Greeting.playerName == playerList[3]).order(Greeting.date)
            greetings5 = Greeting.query(Greeting.playerName == playerList[4]).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1, greetings2 = greetings2, greetings3 = greetings3, greetings4 = greetings4, greetings5 = greetings5)
        if (playerName == 'None') and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[1], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings3 = Greeting.query(Greeting.playerName == playerList[2], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings4 = Greeting.query(Greeting.playerName == playerList[3], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings5 = Greeting.query(Greeting.playerName == playerList[4], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1, greetings2 = greetings2, greetings3 = greetings3, greetings4 = greetings4, greetings5 = greetings5)
        if (playerName == 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[1], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings3 = Greeting.query(Greeting.playerName == playerList[2], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings4 = Greeting.query(Greeting.playerName == playerList[3], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings5 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('front.html', greetings1 = greetings1, greetings2 = greetings2, greetings3 = greetings3, greetings4 = greetings4, greetings5 = greetings5)


class PlayerComparisons(Handler):
    def get(self):
        greetings1 = Greeting.query(Greeting.playerName == playerList[0]).order(Greeting.date)
        greetings2 = Greeting.query(Greeting.playerName == playerList[4]).order(Greeting.date)
        self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)

    def post(self):
        #These dropdowns could be error checked
        playerName1 = self.request.get('playerName1')
        playerName2 = self.request.get('playerName2')
        chartType = self.request.get('chartType')
        dimensions = self.request.get('dimensions')
        if (playerName1 != 'None') and (playerName2 != 'None')and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 != 'None') and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 != 'None') and (playerName2 == 'None') and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType.IN([chartType, 'None']), Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 == 'None') and (chartType != 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.dimensions.IN([dimensions,'None']), Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            # greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType == chartType, Greeting.dimensions == dimensions).order(Greeting.date)
            greetings2 = Greeting.query(ndb.AND(Greeting.playerName == playerList[4], Greeting.dimensions.IN([dimensions,'None']), Greeting.chartType.IN([chartType, 'None']))).order(Greeting.date)
            # greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.dimensions == dimensions, Greeting.chartType == 'Picture').order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
            # self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)


        if (playerName1 != 'None') and (playerName2 != 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 != 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 != 'None') and (playerName2 == 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 == 'None') and (chartType != 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.chartType.IN([chartType, 'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        

        if (playerName1 != 'None') and (playerName2 != 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 != 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0]).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 != 'None') and (playerName2 == 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4]).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 == 'None') and (chartType == 'None') and (dimensions == 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0]).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4]).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)


        if (playerName1 != 'None') and (playerName2 != 'None')and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 != 'None')and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerName2, Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 != 'None') and (playerName2 == 'None')and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerName1, Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)
        if (playerName1 == 'None') and (playerName2 == 'None')and (chartType == 'None') and (dimensions != 'None'):
            greetings1 = Greeting.query(Greeting.playerName == playerList[0], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            greetings2 = Greeting.query(Greeting.playerName == playerList[4], Greeting.dimensions.IN([dimensions,'None'])).order(Greeting.date)
            self.render('playercomparisons.html', greetings1 = greetings1, greetings2 = greetings2)

class FAQ(Handler):
    def get(self):
        self.render('faq.html')

class Resources(Handler):
    def get(self):
        self.render('resources.html')

app = webapp2.WSGIApplication([('/', Front),
                            ('/playercomparisons', PlayerComparisons),
                            ('/img', Image),
                            ('/faq', FAQ),
                            ('/resources', Resources)],
                            debug=True)



# app = webapp2.WSGIApplication([('/', Front),
#                             ('/upload', MainPage),
#                             ('/playercomparisons', PlayerComparisons),
#                             ('/img', Image),
#                             ('/sign', Guestbook)],
#                             debug=True)