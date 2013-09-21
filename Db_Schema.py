# Google DataStore
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    skills = ndb.TextProperty()
    #userURL = ndb.KeyProperty()
    event = ndb.StringProperty(required=True)
    team = ndb.StringProperty()


class Team(ndb.Model):
    teamLeader = ndb.StringProperty(required=True)
    membersList = ndb.StringProperty(repeated=True)
    event = ndb.StringProperty(required=True)


class Event(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    organizer = ndb.StringProperty(required=True)
    organizerEmail = ndb.StringProperty(required=True)
    maxTeamSize = ndb.IntegerProperty(required=True)
    minTeamSize = ndb.IntegerProperty(required=True)
    maxParticipants = ndb.IntegerProperty(required=True)
    teamsList = ndb.StringProperty(repeated=True)
    #eventURL = ndb.KeyProperty()

class JoinTeamRequest(ndb.Model):
    userURL = ndb.StringProperty(required=True)
    teamToJoin = ndb.IntegerProperty(required=True)
    requestURL = ndb.KeyProperty()

class FormTeamRequest(ndb.Model):
    initiatorURL = ndb.StringProperty(required=True)
    passiveUserURL = ndb.StringProperty(required=True)
    eventURL = ndb.StringProperty(required=True)
    requestURL = ndb.KeyProperty()
