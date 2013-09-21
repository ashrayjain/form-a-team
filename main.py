import webapp2
import jinja2
import os
from Db_Schema import *
from google.appengine.api import mail
import util


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
        self.render("teamform.html", Event="test")


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
        self.response.headers['Content-Type'] = "application/json"
        responseJSON = {
            "response": False,
            "responseStr": "Email not valid!"
        }
        if (mail.is_email_valid(eventAttributes["eventOrganiserEmail"]))
        self.createEvent(eventAttributes)
        responseJSON["response"] = True
        responseJSON["responseStr"] = ""

        self.response.out.write(json.dumps(responseJSON))

    def createEvent(self, eventAttributes):
        event = Event(
            name=eventAttributes["eventName"],
            description=eventAttributes["eventDesc"],
            organizer=eventAttributes["eventOrganiser"],
            organizerEmail=eventAttributes["eventOrganiserEmail"],
            maxTeamSize=int(eventAttributes["eventTeamRangeHigh"]),
            minTeamSize=int(eventAttributes["eventTeamRangeLow"]),
            maxParticipants=int(eventAttributes["eventParticipantCount"])
            id = util.getRandomEventURL()            
        )
        print event
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
        self.response.headers['Content-Type'] = "application/json"

        responseJSON = {
            "response": False,
            "responseStr": "Email not valid!"
        }
        if (mail.is_email_valid(joinAttributes["userEmail"]))
        self.joinEvent(joinAttributes)
        responseJSON["response"] = True
        responseJSON["responseStr"] = ""

        self.response.out.write(json.dumps(responseJSON))

    def joinEvent(self, joinAttributes):
        newUser = User(
            name=joinAttributes["userName"],
            email=joinAttributes["userEmail"],
            skills=joinAttributes["userSkills"],
            event=joinAttributes["eventUrl"],
            id=util.getRandomUserURL()            
        )
        newUser.put()

class FormTeamHandler(Handler):
    def post(self):
        formTeamRequest = FormTeamRequest(
            senderURL = self.request.get("senderURL"),
            receiveURL = self.request.get("receiveURL"),
            id=getRandomFormTeamURL()            
        )
        formTeamRequest.put()
        self.executeFormTeamRequest(receiveURL)

    def executeFormTeamRequest(self, receiveURL):
        if not mail.is_email_valid()        

class JoinTeamHandler(Handler):
    def post(self):
        joinTeamRequest = FormTeamRequest(
            userURL=self.request.get("userURL"),
            teamToJoin=self.request.get("teamID"),
            id=util.getRandomJoinTeamURL()            
        )
        joinTeamRequest.put()

class LeaveTeamHandler(Handler):
    def post(self):
        return


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/ajax/createEvent', CreateEventHandler),
    ('/ajax/joinEvent', JoinEventHandler),
    ('/ajax/formTeam', FormTeamHandler),
    ('/ajax/joinTeam', JoinTeamHandler),
    ('/ajax/leaveTeam', LeaveTeamHandler)
], debug=True)
