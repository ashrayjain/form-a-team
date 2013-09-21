import Db_Schema
import uuid

def getRandomUserURL():
	randomUserURL = uuid.uuid4().hex
	sameUserUrl = Db_Schema.User.get_by_id(randomUserURL)
	if(sameUserUrl != None):
		getRandomUserURL()
	return randomUserURL

def getRandomEventURL():
	randomEventURL = uuid.uuid4().hex
	sameEventUrl = Db_Schema.Event.get_by_id(randomEventURL)
	if(sameEventUrl != None):
		getRandomEventURL()
	return randomEventURL

def getRandomJoinTeamURL():
	randomJoinTeamURL = uuid.uuid4().hex
	sameJoinTeamUrl = Db_Schema.Event.get_by_id(randomJoinTeamURL)
	if (randomJoinTeamURL != None):
		getRandomEventURL()
	return randomJoinTeamURL

def getRandomFormTeamURL():
	randomFormTeamURL = uuid.uuid4().hex
	sameFormTeamUrl = Db_Schema.Event.get_by_id(randomFormTeamURL)
	if (randomFormTeamURL != None):
		getRandomFormTeamURL()
	return randomFormTeamURL