// JavaScript Document

var eventData = new array("eventName","eventOrganiser","eventOrganiserEmail","eventDesc","eventParticipantCount","eventTeamRangeLow","eventTeamRangeHigh");
var userJoinEventData = new array("userName","userEmail","userSkills");
var currentURL = document.URL;

function createEvent()
{
	var validData = validateEventData();
	if(validData)
	{
		var postPackage = generateCreateEventPostPackage();
		$.post("../ajax/createEvent",postPackage,function (data){
			$('#event-data-holder').val("<p class = 'eventServerResponse'> Your event has been created! Here is the exclusive url for your event: </p><br><p class='eventServerResponseURL'>"+data+"</p>");
		});
	}
}

function validateEventData()
{
	var length = eventData.length;
	var flag = true;
	for(var i =0; i< length;i++)
	{
		if($('#'+eventData[i]).val() == "")
		{
			//$('#'+fieldsToValidate[i]+"feedback").val("This field cannot be empty!");
			flag = false;
		}
	}
	
	var pattern = /[0-9]+/i;
	if(pattern.test($('#eventParticipantCount')))
	{
		flag = false;
		//$('#eventParticipantCountfeedback').val("This field only accepts integers > 0!");
	}
	
	if(pattern.test($('#eventTeamRangeLow')))
	{
		flag = false;
		//$('#eventTeamRangeLowfeedback').val("This field only accepts integers > 0!");
	}
	
	if(pattern.test($('#eventTeamRangeHigh')))
	{
		flag = false;
		//$('#eventTeamRangeHighfeedback').val("This field only accepts integers > 0!");
	}
	
	if(flag && (parseInt($('#eventTeamRangeHigh').val()) > parseInt($('#eventParticipantCount').val())))
	{
		flag = false;
		//$('#eventTeamRangeHighfeedback').val("This value must be lower than the total participant count1");
	}
	
	if(flag && (parseInt($('#eventTeamRangeHigh').val()) < parseInt($('#eventTeamRangeLow').val())))
	{
		flag = false;
		//$('#eventTeamRangeLowfeedback').val("Lower limit of team size must be lower than the upper limit!");
	}
	
	return flag;
}

function generateCreateEventPostPackage()
{
	var data = {};
	var length = eventData.length;
	for(var i =0;i<length;i++)
	{
		data[eventData[i]]= $('#'+eventData[i]).val();
	}
	return data;	
}

function joinEvent()
{
	var validData = validateUserJoinEventData();
	if(validData)
	{
		var postPackage = generateUserJoinEventPostPackage();
		$.post("../ajax/joinEvent",postPackage);
	}
}

function validateUserJoinEventData()
{
	var length = userJoinEventData.length;
	var flag = true;
	for(var i =0; i< length;i++)
	{
		if($('#'+userJoinEventData[i]).val() == "")
		{
			//$('#'+fieldsToValidate[i]+"feedback").val("This field cannot be empty!");
			flag = false;
		}
	}
	
	return flag;
}

function generateUserJoinEventPostPackage()
{
	var data = {};
	var length = userJoinData.length;
	for(var i =0;i<length;i++)
	{
		data[eventData[i]]= $('#'+eventData[i]).val();
	}
	data["eventURL"] = currentURL;
	return data;
}

function joinTeam()
{
	var postPackage = generateUserJoinTeamPostPackage();
	$.post(postPackage,"");
}

function generateUserJoinTeamPostPackage()
{
	
}