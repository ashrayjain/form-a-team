// JavaScript Document

var eventData = new Array("eventName","eventOrganiser","eventOrganiserEmail","eventDesc","eventParticipantCount","eventTeamRangeLow","eventTeamRangeHigh");
var userJoinAnEventData = new Array("userName","userEmail","userSkills");

function createAnEvent()
{
    var validData = validateAnEventData();
    if(validData)
    {
        var postPackage = generateCreateAnEventPostPackage();
        $.post("/ajax/createEvent", postPackage, function (data){
			if(data.response == false)
			{
				alert(data.responseStr);
			}
			else
			{
	            $('#event-data-holder').html("<p class = 'eventServerResponse'> Your event has been created! Here is the exclusive url for your event: </p><br><p class='eventServerResponseURL'>"+window.location.protocol+"://"+window.location.host+data.responseStr+"</p>");
			}
        });
    }
    return false;
}

function validateAnEventData()
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

function generateCreateAnEventPostPackage()
{
    var data = {};
    var length = eventData.length;
    for(var i =0; i < length; i++)
    {
        data[eventData[i]]= $('#'+eventData[i]).val();
    }
    return data;
}

function joinAnEvent()
{
    var validData = validateUserJoinAnEventData();
    if(validData)
    {
        var postPackage = generateUserJoinAnEventPostPackage();
        $.post("/ajax/joinEvent", postPackage,function success(data){
			console.log(data);
			if(data.response == true)
			{
				alert("You have been added to this event. Your unique url has been sent to your email.");
				var path = document.location.pathname;
				path = path.substr(0,path.lastIndexOf("\\")+1);
				path = path.replace(/\//gi, "");
				path = path.replace(/%20/gi, " ");
				path = path.replace(/\\/gi, "\/");
				window.location = path+data.responseStr;
			}
		});
    }
    return false;
}

function validateUserJoinAnEventData()
{
    var length = userJoinAnEventData.length;
    var flag = true;
    for(var i =0; i< length;i++)
    {
        if($('#'+userJoinAnEventData[i]).val() == "")
        {
            //$('#'+fieldsToValidate[i]+"feedback").val("This field cannot be empty!");
            flag = false;
        }
    }

    return flag;
}

function generateUserJoinAnEventPostPackage()
{
    var data = {};
    var length = userJoinAnEventData.length;
    for(var i =0;i<length;i++)
    {
        data[userJoinAnEventData[i]]= $('#'+userJoinAnEventData[i]).val();
    }
    data["eventUrl"] = currentEvent;
    return data;
}

function joinTeam(teamId)
{
    if(confirm("Are you sure you want to request to join the team with id "+teamid+"?"))
    {
        var postPackage = generateUserJoinTeamPostPackage(teamId);
        $.post(postPackage,postPackage,function success(data){
			if(data.response == "false")
			{
				alert(data.responseStr);
			}
			else
			{
            	alert("The request has been sent to the team leader of this team. Please wait for the response from them.");
			}
        });
    }
}

function generateUserJoinTeamPostPackage(teamId)
{
    data = {};

    data["userURL"] = currentURL;
    data["teamID"] = teamId;

    return data;
}

function leaveTeam()
{
    if(confirm("Are you sure you want to leave the current team you are in?"))
    {
        var postPackage = generateUserLeaveTeamPostPackage();

        $.post("/ajax/leaveTeam",postPackageData,function success(data){
            alert("You have been removed from the team!");
        });
    }
}

function generateUserLeaveTeamPostPackage()
{
    data = {};
    data["userURL"] = currentURL;
    return data;
}

function jumpTeam(teamId)
{
	var postPackageLeaveTeamData = generateUserLeaveTeamPostPackage();
	$.post("/ajax/leaveTeam",postPackageLeaveTeamData);
	var postPackageJoinTeamData = generateUserJoinTeamPostPackage(teamId);
	$.post("/ajax/joinTeam",postPackageJoinTeamData,function success(data){
		alert("You have been successfully removed from your previous team, and a new request has been sent over to your new team leader. Please wait for the response from your new leader.");
	});
}

function formTeam()
{
	var postPackageFormTeamData = generateUserFormTeamPostPackage();
	$.post("/ajax/formTeam",postPackageFormTeamData,function success(data){
		alert("A request has been sent to the person regarding the formation of a new team. Please wait for his reply.");
	});
}

function generateUserFormTeamPostPackage(otherUserURL)
{
	data = {};
	
	data["senderURL"] = document.URL;
	data["receiverURL"] = otherUserURL;
	
	return data;
}
