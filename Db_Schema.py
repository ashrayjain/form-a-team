# Google DataStore
from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    skills = ndb.TextProperty()
    event = ndb.StringProperty(required=True)
    team = ndb.StringProperty()


class Team(ndb.Model):
    teamLeader = ndb.StringProperty(required=True)
    event = ndb.StringProperty(required=True)


class Event(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=True)
    organizer = ndb.StringProperty(required=True)
    organizerEmail = ndb.StringProperty(required=True)
    maxTeamSize = ndb.IntegerProperty(required=True)
    minTeamSize = ndb.IntegerProperty(required=True)
    maxParticipants = ndb.IntegerProperty(required=True)

class JoinTeamRequest(ndb.Model):
    userURL = ndb.StringProperty(required=True)
    teamToJoin = ndb.StringProperty(required=True)

class FormTeamRequest(ndb.Model):
    senderURL = ndb.StringProperty(required=True)
    receiverURL = ndb.StringProperty(required=True)
