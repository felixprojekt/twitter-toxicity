$(function() {

	$("body").removeClass("loading");

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

		var len = ids.children("span").length;

		console.log("length: " + len);

		ids.children("span").each(function() {
			var id = $(this).text();
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
						$(".loading-wrapper").removeClass("hidden");

						$("#loading-name").addClass("pulse")
					}, 100);
				},
				error: function(result) {
					console.log(result);
				},
				success: function(result) {

					var request_time = new Date().getTime() - start_time;
					//console.log("fetched " + id + " loaded in " + request_time + " ms");

					//console.log("name: " + result.name + " toxicity: " + result.toxicity);

					$("#loading-name").html("@" + result.name);

					if(result.toxicity > 580) {
						createBubble(result.name, result.toxicity / 3);
					}

					len -= 1;

					console.log(len);
				}
			});

			if(len < 2) {
				showFinalResults();
			}
		});

    	window.history.replaceState('', '', window.location.href.split("?")[0]);
	} else {
		window.location.replace("/");
	}

	function showFinalResults() {
		$("#intro").hide();
		$("#sign-in").hide();
		$("#twitter-nickname-form").hide();
		$(".loading-wrapper").hide();

		$.ajax({
			method: "GET",
			url: "/toxicity/insights",
			error: function(result) {
				console.log(result)
			},
			success: function(result) {
				console.log(result);
				$("#results-table").html(result)
			}
		});

		$("#result").removeClass("hidden").css("z-index", 5);
		$("#bubbles").css("opacity", ".1").css("z-index", 1);
		$("#bubbles div").css("color", "transparent");
	}

	function createBubble(name, size, timeout = 100) {
		var div = document.createElement("div");
		var top = 100 + randBetween(0,65);

		div.innerHTML = name;
		div.style.left = randBetween(0, 90) + "%";
		div.style.top = top + "%";
		div.style.width = size + "px";
		div.style.height = size + "px";
		div.setAttribute("class", "animated jello slow");
		div.setAttribute("data-size", size);

		setTimeout(function() {
			document.getElementById("bubbles").appendChild(div);
		}, timeout);
		
	}

	function getSizes() {
		var sizes = {};

		$("#bubbles").each(function() {
			sizes[$(this).data("size")] = $(this).text();
		});

		sizes.sort();

		console.log(sizes);

		return sizes;
	}

	function getWorst() {
		var sizes = getSizes();
		var length = sizes.length;

		return sizes.slice(length - 5, length);
	}

	function getBest() {
		var sizes = getSizes();

		return sizes.slice(0, 5);
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



