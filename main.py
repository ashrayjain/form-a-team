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
        You may now distribute the following to the participants-

        {1}

        Form-A-Team Support
        """.format(eventAttributes["eventOrganiser"], "http://formateamnow.appspot.com/events/"+eventID))
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

                You may now join or form teams for the event, {1}, at the following url-

                {2}

                Please be advised that this url is specifically created for you and must be kept
                confidential for your own privacy.

                Form-A-Team Support
                """.format(joinAttributes["userName"], theEvent.name, "http://formateamnow.appspot.com/user/"+newID))
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
        sender = User.get_by_id(self.request.get("senderURL"))
        theEvent = Event.get_by_id(user.event)
        if user != None:
            mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                           to="{0} <{1}>".format(user.name, user.email),
                           subject="Someone wants to team up for {0}".format(theEvent.name),
                           body="""
                            Dear {0},

                            {1} would like to team up with you for {2}.

                            {1} is a fellow participant for this event and has the following skills/interests-
                            {3}

                            You can correspond with {1} at {4} to discuss this further.

                            If you would like to accept this request, please click on one of the following links-

                            ACCEPT
                            {5}

                            DECLINE
                            {6}

                            Form-A-Team Support
                            """.format(user.name, sender.name, theEvent.name, sender.skills, sender.email,
                                       "http://formateamnow.appspot.com/formRequest/"+newID+"?response=y",
                                       "http://formateamnow.appspot.com/formRequest/"+newID+"?response=n"))

class JoinTeamHandler(Handler):
    def post(self):
        newID = util.getRandomJoinTeamURL()
        joinTeamRequest = JoinTeamRequest(
            userURL=self.request.get("userURL"),
            teamToJoin=self.request.get("teamID"),
            id=newID
        )
        joinTeamRequest.put()
        user = User.get_by_id(self.request.get("userURL"))
        theTeam = Team.get_by_id(self.request.get("teamID"))
        leader = User.get_by_id(theTeam.teamLeader)
        theEvent = Event.get_by_id(theTeam.event)
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(leader.name, leader.email),
                       subject="Request to join your team for {0}".format(theEvent.name),
                       body="""
                        Dear {0},

                        {1} would like to join you group for {2}.

                        {1} possess the following skills- {3}

                        If you'd like further correspondence, you may contact {1} at
                        {4}

                        Please choose one of the following links to inform us of your choice:


                        ACCEPT
                        {5}

                        DECLINE
                        {6}

                        Form-A-Team Support
                        """.format(leader.name, user.name, theEvent.name, user.skills, user.email,
                           "http://formateamnow.appspot.com/joinRequest/"+newID+"?response=y",
                           "http://formateamnow.appspot.com/joinRequest/"+newID+"?response=n"))

class LeaveTeamHandler(Handler):
    def post(self):
        userID = self.request.get("userURL")
        userObj = User.get_by_id(userID)
        leader = User.get_by_id(Team.get_by_id(userObj.team).teamLeader)
        if userObj != None:
            userObj.team = None
        mail.send_mail(sender="Form-A-Team Support <ashrayj11@gmail.com>",
                       to="{0} <{1}>".format(leader.name, leader.email),
                       subject="One of your team member has left!",
                       body="""
                        Dear {0},

                        {1} has left your team.

                        Form-A-Team Support
                        """.format(leader.name, userObj.name))

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
