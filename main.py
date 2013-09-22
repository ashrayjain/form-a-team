import webapp2
import jinja2
import os
from Db_Schema import *
from google.appengine.api import mail
import util
import json

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
        self.render("index.html")


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
        if (mail.is_email_valid(eventAttributes["eventOrganiserEmail"])):
            newID = self.createEvent(eventAttributes)
            responseJSON["response"] = True
            responseJSON["responseStr"] = "/events/"+newID
        self.response.out.write(json.dumps(responseJSON))

    def createEvent(self, eventAttributes):
        eventID = util.getRandomEventURL()
        event = Event(
            name=eventAttributes["eventName"],
            description=eventAttributes["eventDesc"],
            organizer=eventAttributes["eventOrganiser"],
            organizerEmail=eventAttributes["eventOrganiserEmail"],
            maxTeamSize=int(eventAttributes["eventTeamRangeHigh"]),
            minTeamSize=int(eventAttributes["eventTeamRangeLow"]),
            maxParticipants=int(eventAttributes["eventParticipantCount"]),
            id = eventID
        )
        event.put()
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(eventAttributes["eventOrganiser"], eventAttributes["eventOrganiserEmail"]),
                       subject="Your Event, {0} has been created".format(eventAttributes["eventName"]),
                       body="""
        Dear {0},

        Your event, "{1}", has been successfully created.

        Form-A-Team Support
        """)
        return eventID



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
        if (mail.is_email_valid(joinAttributes["userEmail"])):
            newID = self.joinEvent(joinAttributes)
            responseJSON["response"] = True
            responseJSON["responseStr"] = "/user/"+newID
        self.response.out.write(json.dumps(responseJSON))

    def joinEvent(self, joinAttributes):
        newID = util.getRandomUserURL()
        newUser = User(
            name=joinAttributes["userName"],
            email=joinAttributes["userEmail"],
            skills=joinAttributes["userSkills"],
            event=joinAttributes["eventUrl"],
            id=newID
        )
        newUser.put()
        theEvent = Event.get_by_id(joinAttributes["eventUrl"])
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(joinAttributes["userName"], joinAttributes["userEmail"]),
                       subject="{0} - Link for Forming Your Team".format(theEvent.name),
                       body="""
                Dear {0},

                Your event, "{1}", has been successfully created.

                Form-A-Team Support
                """)
        return newID

class FormTeamHandler(Handler):
    def post(self):
        newID = util.getRandomFormTeamURL()
        formTeamRequest = FormTeamRequest(
            senderURL = self.request.get("senderURL"),
            receiverURL = self.request.get("receiverURL"),
            id=newID
        )
        formTeamRequest.put()
        user = User.get_by_id(self.request.get("receiverURL"))
        if user != None:
            mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                           to="{0} <{1}>".format(user.name, user.email),
                           subject="",
                           body="""
                            Dear {0},

                            Your event, "{1}", has been successfully created.

                            Form-A-Team Support
                            """)


class JoinTeamHandler(Handler):
    def post(self):
        newID = util.getRandomJoinTeamURL()
        joinTeamRequest = JoinTeamRequest(
            userURL=self.request.get("userURL"),
            teamToJoin=self.request.get("teamID"),
            id=newID
        )
        joinTeamRequest.put()
        theTeam = Team.get_by_id(self.request.get("teamID"))
        self.response.out.write(newID)
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(joinAttributes["userName"], joinAttributes["userEmail"]),
                       subject="{0} - Link for Forming Your Team".format(
                           Event.get_by_id(joinAttributes["eventUrl"]).name),
                       body="""
                        Dear {0},

                        Your event, "{1}", has been successfully created.

                        Form-A-Team Support
                        """)
class LeaveTeamHandler(Handler):
    def post(self):
        userID = self.request.get("userURL")
        userObj = User.get_by_id(userID)
        if userObj != None:
            userObj.team = None
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(joinAttributes["userName"], joinAttributes["userEmail"]),
                       subject="{0} - Link for Forming Your Team".format(
                           Event.get_by_id(joinAttributes["eventUrl"]).name),
                       body="""
                        Dear {0},

                        Your event, "{1}", has been successfully created.

                        Form-A-Team Support
                        """)

class UserPageHandler(Handler):
    def get(self, userID):
        print userID
        user = User.get_by_id(userID)
        print user
        if user is None:
            self.redirect('/')
        else:
            currentEvent = Event.get_by_id(user.event)
            returnObj = {
                "name": currentEvent.name,
                "organiser": currentEvent.organizer,
                "description": currentEvent.description,
                "maxP": currentEvent.maxTeamSize,
                "teams": {},
                "nonteam": []
            }
            teams = Team.query(Team.event == user.event)
            for team in teams:
                teamID = str(team.key.id())
                returnObj["teams"][teamID] = []
                members = User.query(User.team == teamID)
                for member in members:
                    returnObj["teams"][teamID].append({
                        "name": member.name,
                        "email": member.email,
                        "skills": member.skills,
                        "url": member.key.id()
                    })

            print returnObj["teams"]
            for teamID, members in returnObj["teams"].iteritems():
                returnObj["teams"][teamID] = [member for member in members if member["url"]!=userID]
            print returnObj["teams"]

            independentUsers = User.query(ndb.AND(User.event == user.event, User.team == None))
            for independentUser in independentUsers:
                returnObj["nonteam"].append({
                    "name": independentUser.name,
                    "email": independentUser.email,
                    "skills": independentUser.skills,
                    "url": independentUser.key.id()
                })

            print returnObj["nonteam"]
            returnObj["nonteam"] = [member for member in returnObj["nonteam"] if member["url"] != userID ]
            print returnObj["nonteam"]

            self.render("form-team.html", Event=returnObj, User={
                "name": user.name,
                "email": user.email,
                "skills": user.skills,
                "team": "" if user.team == None else user.team,
                "event": user.event,
                "url": userID
            })

class EventPageHandler(Handler):
    def get(self, eventID):
        event = Event.get_by_id(eventID)
        if (event != None):
            self.render("teamform.html", Event={"name": event.name, "organiser": event.organizer, "description": event.description, "url": eventID})
        else:
            self.redirect("/")


class JoinRequestResponseHandler(Handler):
    def get(self, requestID):
        answer = self.request.get("response")
        joinRequest = JoinTeamRequest.get_by_id(requestID)
        if joinRequest != None and (answer == "y" or answer == "n"):
            if answer == "y":
                user = User.get_by_id(joinRequest.userURL)
                user.team = joinRequest.teamToJoin
                user.put()
                self.response.out.write("Team Joining Request Approved! Thanks!")
            else:
                joinRequest.key.delete()
                self.response.out.write("Team Joining Request Declined!")
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(joinAttributes["userName"], joinAttributes["userEmail"]),
                       subject="{0} - Link for Forming Your Team".format(
                           Event.get_by_id(joinAttributes["eventUrl"]).name),
                       body="""
                        Dear {0},

                        Your event, "{1}", has been successfully created.

                        Form-A-Team Support
                        """)


class FormRequestResponseHandler(Handler):
    def get(self, requestID):
        answer = self.request.get("response")
        formRequest = FormTeamRequest.get_by_id(requestID)
        if formRequest != None and (answer=="y" or answer=="n"):
            if answer=="y":
                users = ndb.get_multi([ndb.Key(User, formRequest.senderURL), ndb.Key(User, formRequest.receiverURL)])
                newTeam = Team(teamLeader=users[0].key.id(), event=users[0].event)
                newTeam.put()
                for user in users:
                    user.team = str(newTeam.key.id())
                ndb.put_multi(users)
                self.response.out.write("Team Forming Request Approved! Thanks!")
            else:
                formRequest.key.delete()
                self.response.out.write("Team Forming Request Declined!")
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(joinAttributes["userName"], joinAttributes["userEmail"]),
                       subject="{0} - Link for Forming Your Team".format(
                           Event.get_by_id(joinAttributes["eventUrl"]).name),
                       body="""
                        Dear {0},

                        Your event, "{1}", has been successfully created.

                        Form-A-Team Support
                        """)


app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/ajax/createEvent', CreateEventHandler),
                                  ('/ajax/joinEvent', JoinEventHandler),
                                  ('/ajax/formTeam', FormTeamHandler),
                                  ('/ajax/joinTeam', JoinTeamHandler),
                                  ('/ajax/leaveTeam', LeaveTeamHandler),
                                  ('/user/([0-9a-z]{32})', UserPageHandler),
                                  ('/events/([0-9a-z]{32})', EventPageHandler),
                                  ('/joinRequest/([0-9a-z]{32})', JoinRequestResponseHandler),
                                  ('/formRequest/([0-9a-z]{32})', FormRequestResponseHandler)
                              ], debug=True)
