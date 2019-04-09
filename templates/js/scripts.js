$(function() {

	$.urlParam = function(name){
		var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
		if(results) {
			return results[1]
		} else {
			return null;
		}
	}

	var token = $.urlParam('oauth_token');
	var verifier = $.urlParam('oauth_verifier');

	if(token && verifier) {

		$("#bubbles").removeClass("hidden");

		var start_time = new Date().getTime();

		var ids = $("#ids");

		var len = ids.children().length;

		ids.children("span").each(function(index) {
			var id = $(this).html();
			$.ajax({
				method: "GET",
				url: "/toxicity/" + id + "/",
				data: {
					"token": token,
					"verifier": verifier
				},
				beforeSend: function() {
					$("#intro").addClass("hidden");
					$("#sign-in").addClass("hidden");

					setTimeout(function() {
						$(".loading-wrapper").removeClass("hidden").addClass("pulse");

					}, 100);
				},
				error: function(result) {
					console.log(result);
				},
				success: function(result) {

					var request_time = new Date().getTime() - start_time;
					console.log("fetched " + id + " loaded in " + request_time + " ms");

					console.log("name: " + result.name + " toxicity: " + result.toxicity);

					createBubble(result.name, result.toxicity);

				}
			});

			if(index === (len - 1)) {
				showFinalResults();
			}
		});

    	window.history.replaceState('', '', window.location.href.split("?")[0]);
	} else {
		window.location.replace("/");
	}

	function launchBeta() {
		$("#bubbles").removeClass("hidden");

		var sizes = [90, 200, 170, 120, 80, 140, 70, 120, 90, 120, 80];
		var names = ["@POTUS", "@HairForceOne", "@HoVa86", "@mac_attack_", "@_youhadonejob1", "@Cojsemto", "@aritHeta", "@measure_one", "@pleasedth", "@thankunxt", "@JonathanIve"];
		console.log(names);

		var timeout = 3000;

		for(var i = 0; i < sizes.length; i++) {

			createBubble(names[i], sizes[i], timeout);

			timeout = timeout + randBetween(1000, 2000);
		}

		timeout = timeout + 8000;

		setTimeout(function(){
			showFinalResults();
		}, timeout);
	}

	function showFinalResults() {
		$("#intro").hide();
		$("#sign-in").hide();
		$("#twitter-nickname-form").hide();
		$(".loading-wrapper").hide();
		$("#result").removeClass("hidden").css("z-index", 5);
		$("#bubbles").css("opacity", ".1").css("z-index", 1);
		$("#bubbles div").css("color", "transparent");
	}

	function createBubble(name, size, timeout = 100) {
		var div = document.createElement("div");
		var top = 100 + randBetween(0,50);

		div.innerHTML = name;
		div.style.left = randBetween(0, 90) + "%";
		div.style.top = top + "%";
		div.style.width = size + "px";
		div.style.height = size + "px";
		div.setAttribute("class", "animated jello slow")

		setTimeout(function() {
			document.getElementById("bubbles").appendChild(div);
		}, timeout);
		
	}

	/*
	function runTensor(name, tweets) {
		const threshold = 0.55;
		const labelsToMatch = ["toxicity", "insult", "severe_toxicity", "threat"];

		toxicity.load(threshold, labelsToMatch).then(model => {
		  	model.classify(tweets).then(predictions => {

		  		console.log(name);
		  		console.log(tweets);
		    	console.log(predictions);

			    // var values = [];

			    // predictions[0]["results"].forEach(function(item) {
			    // 	// values[] = item.
			    // });
			    
		    	createBubble(name);
		  	});
		});
	} */

	function randBetween(min, max) {
		return Math.floor(Math.random() * (max - min + 1) + min)
	}
});



