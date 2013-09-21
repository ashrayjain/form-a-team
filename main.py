import webapp2
import jinja2
import os
from Db_Schema import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       autoescape=True)
class Handler(webapp2.RequestHandler):
    """Handler Class with Utility functions for Templates"""

    def __write__(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def __render_str__(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.__write__(self.__render_str__(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("index.html", Event="test")


createEventAttributes = [
    "eventName",
    "eventOrganiser",
    "eventOrganiserEmail",
    "eventDesc",
    "eventParticipantCount",
    "eventTeamRangeLow",
    "eventTeamRangeHigh"
]
class CreateEventHandler(Handler):
    def post(self):
        eventAttributes = {}
        for attribute in createEventAttributes:
            eventAttributes[attribute] = self.request.get(attribute)

    def createEvent(self, eventAttributes):
        event = Event(
            name=eventAttributes["eventName"],
            description=eventAttributes["eventDesc"],
            organizer=eventAttributes["eventOrganiser"],
            organizerEmail=eventAttributes["eventOrganiserEmail"],
            maxTeamSize=eventAttributes["eventTeamRangeHigh"],
            minTeamSize=eventAttributes["eventTeamRangeLow"],
            maxParticipants=eventAttributes["eventParticipantCount"]
        )
        event.put()


joinEventAttributes = [
    "userName",
    "userEmail",
    "userSkills",
    "eventUrl"
]
class JoinEventHandler(Handler):
    def post(self):
        joinAttributes = {}
        for attribute in joinEventAttributes:
            joinAttributes[attribute] = self.request.get(attribute)

    def joinEvent(self, joinAttributes):
        newUser = User(
            name=joinAttributes["userName"],
            email=joinAttributes["userEmail"],
            skills=joinAttributes["userSkills"],
            event=joinAttributes["eventUrl"],
        )
        newUser.put()

class FormTeamHandler(Handler):
    def post(self):
        return

class JoinTeamHandler(Handler):
    def post(self):
        return

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/ajax/createEvent', CreateEventHandler),
    ('/ajax/joinEvent', JoinEventHandler),
    ('/ajax/ft', FormTeamHandler),
    ('/ajax/jt', JoinTeamHandler),
], debug=True)
