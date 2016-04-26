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

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Greeting(ndb.Model):
    """Models a Guestbook entry with an author, content, avatar, and date."""
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    avatar = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


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
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')


class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')

        avatar = self.request.get('img')
        if avatar:
            avatar = images.resize(avatar, 256, 256)
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
        self.render('front.html')

    def post(self):
        #These dropdowns must be error checked

        subject = self.request.get('playerName')
        sorting = self.request.get('sortingTag')
        if (sorting != 'None') and (subject != 'None'):
            posts = Post.all().filter('subject =', subject).order('-%s' % sorting)
        if (subject == 'None') and (sorting == 'None'):
            posts = Post.all().order('-created')
        elif subject == 'None':
            posts = Post.all().order('-%s' % sorting)
        elif sorting == 'None':
            posts = Post.all().filter('subject =', subject).order('-created')
        self.render('front.html', posts = posts, subjectTag = subject, sortingTag = sorting)  

app = webapp2.WSGIApplication([('/', Front),
                            ('/upload', MainPage),
                            ('/img', Image),
                            ('/sign', Guestbook)],
                            debug=True)