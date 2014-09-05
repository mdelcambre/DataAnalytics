/**
 * Makes the AJAX call to the rps server to play rock paper scisors.
 * @returns void - elements are displayed in HTML as part of exceution
 * @author Mark Delcambre (mark@delcambre.com)
**/


// Setup a few global varriables used to maintain state
var uuid, name;
var waiting = false;
var threw;

// Setup scoreboard varriables
var wins = 0;
var ties = 0;
var loss = 0;

// Creat lookup table.
var plays = {};
plays['rock']=0;
plays['paper']=1;
plays['scissors']=2;

// Defines the primary rps function that handles the jquerry request
function rps(action,hand){
	//Need the date for the log below
	var d = new Date();	

	// Check if the button is being spammed
	if ((action == 'play') && waiting) {
		return;	
	}	

	// If we are playing a new game, redefine the state varriables
	if (action == 'play'){
		uuid = guid();
		name = document.getElementById('name').value	
		threw = hand;
		waiting = true;
	}

	// If we are not waiting on a response, do not querry the server
	if (!waiting){
		return;
	}
	// State has been defined abvoe, time to querry the server.
	$.ajax({
		type: "POST",
		url: "rps.php",
		data: {'name':name,'uuid':uuid,'throw':threw},
		dataType: "json",
		success: function(data) {
			// If the server didn't tell us to wait, we have the action of the other player
			if (!data.wait) {
				// Server told us not to wait anymore.
				waiting = false;
				
				// Check if we won, tied, or lost
				var diff = plays[data.throw] - plays[threw];	
				if (diff == 0){
					var outcome = ". You Tied.";
					ties++;
				} else if (diff == 1 || diff == -2){
					var outcome = ". You Lost.";
					loss++;
				} else {
					var outcome = ". You Won.";
					wins++;
				}
				
				// Update the scoreboard
				document.getElementById('scoreboard').innerHTML = "W: ".concat(wins," T: ",ties, " L: ",loss); 
				

				// Contruct the Message and display
				var message = "You threw ".concat(threw,". ",data.name," threw ",data.throw,outcome);
				document.getElementById('message').innerHTML = message;
				
				// Using the message above put this at the front of the log
				message = "[".concat(d.toTimeString().substring(0,8),"] ",message)
				var log = document.getElementById('log').innerHTML;
				document.getElementById('log').innerHTML = message.concat("<br/>",log); 
			} else {
				// Server told us to wait, display the message.
				var message = "Waiting on another Player";
				document.getElementById('message').innerHTML = message;
				waiting = true;
			}//else
		}//ajax function	
	});//ajax jquerry	
}//rps function


/**
 * Generates a GUID string.
 * @returns {String} The generated GUID.
 * @example af8a8416-6e18-a307-bd9c-f2c947bbb3aa
 * @author Slavik Meltser (slavik@meltser.info).
 * @link http://slavik.meltser.info/?p=142
 */
function guid() {
    function _p8(s) {
        var p = (Math.random().toString(16)+"000000000").substr(2,8);
        return s ? "-" + p.substr(0,4) + "-" + p.substr(4,4) : p ;
    }
    return _p8() + _p8(true) + _p8(true) + _p8();
}
