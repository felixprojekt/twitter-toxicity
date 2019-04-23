$(function() {

	$("body").removeClass("loading");

	$.urlParam = function(name){
		const results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
		if(results) {
			return results[1]
		} else {
			return null;
		}
	};

	const token = $.urlParam('oauth_token');
	const verifier = $.urlParam('oauth_verifier');

	if(token && verifier) {

		$("#bubbles").removeClass("hidden");

		const ids = $("#ids");

		let len = ids.children("span").length;

		$("#intro").addClass("hidden");
		$("#sign-in").addClass("hidden");

		setTimeout(function() {
			$(".loading-wrapper").removeClass("hidden");

			$("#loading-name").addClass("pulse")
		}, 100);

		let time = 0;

		ids.children("span").each(function() {
			const id = $(this).text();

			setTimeout(function() {
				$.ajax({
					method: "GET",
					url: "/toxicity/" + id + "/",
					data: {
						"token": token,
						"verifier": verifier
					},
					beforeSend: function(result) {

					},
					error: function(result) {
						console.log(result.responseText);
					},
					success: function(result) {

						console.log(result.name + " " + result.toxicity);

						$("#loading-name").html("@" + result.name);

						if(result.toxicity > 120) {
							createBubble(result.name, result.toxicity * 1.8);
						}

						len -= 1;

						if(len < 1) {
							setTimeout(function() {
								showFinalResults();
							}, 3000)
						}
					}
				});
			}, time);

			time += 1000;
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
			url: "/toxicity/insights/",
			error: function(result) {
				console.log(result.responseText)
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

	function createBubble(name, size) {
		const div = document.createElement("div");
		const top = 100 + randBetween(0,65);

		div.innerHTML = name;
		div.style.left = randBetween(0, 90) + "%";
		div.style.top = top + "%";
		div.style.width = size + "px";
		div.style.height = size + "px";
		div.setAttribute("class", "animated jello slow");
		div.setAttribute("data-size", size);

		document.getElementById("bubbles").appendChild(div);
	}

	function randBetween(min, max) {
		return Math.floor(Math.random() * (max - min + 1) + min)
	}

	$(".unfollow-button").click(function() {
	    console.log($(this).data("screen_name"));
    })
});



