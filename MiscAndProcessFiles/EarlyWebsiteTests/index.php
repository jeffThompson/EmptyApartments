<!doctype html>
<html>

<?php
	$num_cols = 	4;
?>

<head>
	<meta charset="UTF-8">
	<title>Empty Apartments ++ Drift Station</title>

	<style>
		/* CSS RESET */
		/* http://meyerweb.com/eric/tools/css/reset/ */
		a,abbr,acronym,address,applet,article,aside,audio,b,big,blockquote,body,canvas,caption,center,cite,code,dd,del,details,dfn,div,dl,dt,em,embed,fieldset,figcaption,figure,footer,form,h1,h2,h3,h4,h5,h6,header,hgroup,html,i,iframe,img,ins,kbd,label,legend,li,mark,menu,nav,object,ol,output,p,pre,q,ruby,s,samp,section,small,span,strike,strong,sub,summary,sup,table,tbody,td,tfoot,th,thead,time,tr,tt,u,ul,var,video{margin:0;padding:0;border:0;font:inherit;vertical-align:baseline}article,aside,details,figcaption,figure,footer,header,hgroup,menu,nav,section{display:block}body{line-height:1}ol,ul{list-style:none}blockquote,q{quotes:none}blockquote:after,blockquote:before,q:after,q:before{content:'';content:none}table{border-collapse:collapse;border-spacing:0}

		/* IMPORT LATO FONT */
		@import url(http://fonts.googleapis.com/css?family=Lato:100,400,700); */
		@font-face {
		    font-family: 	'Lato';
		    src: 			url('fonts/lato-webfont.eot');
		    src: 			url('fonts/lato-webfont.eot?#iefix') format('embedded-opentype'),
		         			url('fonts/lato-webfont.woff') format('woff'),
		         			url('fonts/lato-webfont.ttf') format('truetype'),
		         			url('fonts/lato-webfont.svg#latoregular') format('svg');
		    font-weight: 	normal;
		    font-style: 	normal;
		}

		/* BORDERS INSIDE ELEMENTS */
		*, *:after, *:before {
			-webkit-box-sizing:	border-box;
 			-moz-box-sizing: 	border-box;
 			box-sizing: 		border-box;
		}

		/* BASICS */
		html, body {
			font-family: 	'Lato', Calibri, Arial, sans-serif;
			color: 			black;
			font-size: 		16px;
			text-align: 	center;
		}
		em {
			font-style:		italic;
		}
		h1 {
			font-size: 		4em;
			line-height: 	0.9em;
			margin-bottom:  0.2em;
			color: 			rgba(0,0,0, 0.5);
		}

		/* LINKS */
		a, a:link, a:visited {
			color: 				rgb(100,100,100);
			text-decoration: 	none;
			outline: 			0;		/* remove dotted line after clicking link */
		}
		a:hover, a:active {
			color: 				rgb(20,150,255);
			text-decoration: 	none;
		}

		/* HEADER */
		header {
			width: 				100%;
			height: 			auto;
			padding: 			20px;
			position: 			default;

			-webkit-transition: height 0.3s;
		    -moz-transition: 	height 0.3s;
		    -ms-transition: 	height 0.3s;
		    -o-transition: 		height 0.3s;
		    transition: 		height 0.3s;
		}
		header a:hover, footer a:hover {
			text-decoration: 	underline;
		}
		header h1 {
			-webkit-transition: all 0.3s;
		    -moz-transition: 	all 0.3s;
		    -ms-transition: 	all 0.3s;
		    -o-transition: 		all 0.3s;
		    transition: 		all 0.3s;
		}
		header p {
			line-height: 		1.5em;
		}

		header.smaller {
			height: 			2.5em;
			padding: 			10px 20px 20px 20px;

			overflow: 			hidden;
			position: 			fixed;
			top: 				0;
			left: 				0;
			z-index: 			999;
			background-color: 	white;
		}
		header.smaller h1 {
			font-size: 			1.2em;
			float: 				left;
		}
		header.smaller h1:hover {
			cursor: 			pointer;
		}
		header.smaller h1:hover:before {
			content: 			"\2191\00a0\00a0";	/* up arrow */
		}
		header.smaller p {
			text-align: 		right;
			float: 				right;
		}
		header:after {
			clear: 				both;
		}
		.spacer {
			color: 				rgb(200,200,200);
		}

		/* CITY LISTINGS */
		#cities {
			line-height: 			0;
			-webkit-column-count: 	<?php echo $num_cols ?>;
			-webkit-column-gap: 	10px;
			-moz-column-count: 		<?php echo $num_cols ?>;
			-moz-column-gap: 		10px;
			column-count: 			<?php echo $num_cols ?>;
			column-gap: 			10px;
		}
		.city img {
			width: 			100% !important;
			height: 		auto !important;
			margin-bottom: 	10px;
			border: 		1px solid rgb(200,200,200);
		}
		.city img:hover {
			cursor:  		pointer;
		}
		.city:hover .cityName {
			display: 		block;
		}
		.cityName {
			display: 		none;
			text-transform: uppercase;
			color: 			black !important;
			font-size: 		1.5em;
			line-height: 	1em;
			margin-bottom: 	10px;
			/*margin: 		-4em 0 3em 0;*/
		}

		/* BIG IMAGE OVERLAY */
		.overlay {
			position: 			fixed;
			top: 				0;
			left: 				0;
			width: 				100%;
			height: 			100%;
			z-index: 			99999;
			cursor: 			pointer;
			background-color: 	rgba(0,0,0, 0.9);
			padding-top: 		5%;
		}
		.overlay img {
			width: 				90%;
			height: 			90%;
			object-fit: 		contain;
			object-position: 	50% 50%;
		}

		/* FOOTER */
		footer {
			width: 			60%;
			min-width: 		320px;
			margin: 		60px auto 40px auto;
		}
		footer p {
			margin-bottom: 	2em;
			line-height:	1.3em;
		}
		#more {
			width: 90%;
			margin: 0 auto 30px auto;
			padding: 10px;
			border: 1px solid rgb(200,200,200);
		}
		#more:hover {
			background-color: rgb(0,150,255);
			color: white;
			border: 1px solid white;
		}

		/* RESIZE COLUMNS ON SMALL SCREENS */
		@media screen and (max-width:460px) {
			header h1 {
				font-size: 				3em;
			}
			#cities {
				-webkit-column-count:	1;
			    -moz-column-count: 		1;
			    column-count: 			1;
			}
		}
		@media screen and (min-width:460px) and (max-width:680px) {
			header h1 {
				font-size: 				3em;
			}
			#cities {
				-webkit-column-count:	2;
			    -moz-column-count: 		2;
			    column-count: 			2;
			}
		}
		@media screen and (min-width:680px) and (max-width:1000px) {
			#cities {
				-webkit-column-count:	3;
			    -moz-column-count: 		3;
			    column-count: 			3;
			}
		}
	</style>

	<!-- LOAD JQUERY -->
	<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
</head>

<body>

	<!-- HEADER -->
	<header>
		<h1>EMPTY APARTMENTS</h1>
		<p id="dsLink">A project by <a href="http://www.driftstation.org">Drift Station</a> for the <a href="http://www.kemperart.org">Kemper Museum of Contemporary Art</a></p>
		<p id="infoLink"><a href="#info">More info</a></p>
	</header>

	<!-- CITY LISTINGS -->
	<section id="cities">
	<?php
		function map($value, $low1,$high1, $low2,$high2) {
			return $low2 + ($high2 - $low2) * ($value - $low1) / ($high1 - $low1);
		}
		ini_set('auto_detect_line_endings', true);

		// get list of cities from CSV file
		$cities = array();
		if (( $handle = fopen('Craigslist_USCitiesWithLatLon.csv', 'r')) !== FALSE) {
			while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
				$cities[] = $data;
			}
		}

		// display one image per, in location
		foreach ($cities as $city) {
			$cl_name =  $city[0];
			$location = $city[1];
			$lat = 		$city[2];
			$lon = 		$city[3];

			$images = glob('images/' . $cl_name . '/*.jpg');
			$image = $images[array_rand($images)];
			// echo '<a href="' . $cl_name . '.php">';
			echo '<div class="city">';
			echo '	<img src="' . $image . '" onclick="setOverlay(\'' . $image . '\')">' . PHP_EOL;
			echo '	<p class="cityName">' . $location . '</p>' . PHP_EOL;
			echo '</div>';
			// echo '</a>';
		}
	?>
	</section> <!-- end images -->

	<!-- FOOTER -->
	<footer>
		<!-- <div id="more">Load more images</div> -->
		<p>This project was developed for the exhibition <em>The Center Is A Moving Target</em> at Kemper Museum of Contemporary Art in Kansas City, Missouri, USA. A set of ~160,500 images of available apartments were pulled from Craigslist postings around the US using custom software.</p>

		<p>All images copyright their authors. Everything else <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/">CC BY-NC-SA</a>.
	</footer>
	<a name="info"></a>

	<!-- JS -->
	<script>

		// bigger image overlay
		function setOverlay(img) {
			var overlay = document.createElement("div");
			overlay.setAttribute("id", "overlay");
			overlay.setAttribute("class", "overlay");
			overlay.innerHTML = '<img src="' + img + '">';
			overlay.onclick = removeOverlay;
			document.body.appendChild(overlay);
		}
		function removeOverlay() {
			document.body.removeChild(document.getElementById("overlay"));
		}
		document.onkeydown = function(e) {
			removeOverlay();
			e.preventDefault();
		}

		// shrink menu at top on scroll
		$(window).scroll( function() {
			if ($(window).scrollTop() > 10) {
				$('header').addClass('smaller');
				$('#dsLink').html('<a href="http://www.driftstation.org">Drift Station</a><span class="spacer"> / </span><a href="#info">Info</a>');
				$('#infoLink').html('');
			}
			else {
				$('header').removeClass('smaller');
				$('#dsLink').html('A project by <a href="http://www.driftstation.org">Drift Station</a> for <a href="http://www.kemperart.org">Kemper Museum of Contemporary Art</a>');
				$('#infoLink').html('<a href="#info">More info</a>');
			}
		});

		// scroll up to top
		$('header h1').on('click', function() {
        	$('html, body').animate({ scrollTop: 0 }, 800);
    	});

    	// load more images
    	// var cities = <?php echo json_encode($cities); ?>;
    	// var index = 1;
    	// $('#more').click( function() {
    	// 	for (var i=index; i<cities.length; i++) {
    	// 		var images = [];
    	// 		var city = cities[i][0];
    	// 		$.ajax({
    	// 			url: 'images/' + city,
    	// 			success: function(data) {
    	// 				$(data).find('a:contains(' + '.jpg' + ')').each( function() {
    	// 					var filename = this.href.replace(window.location, '').replace('http:///', '');
    	// 					images.push(filename);
    	// 				});
    	// 			}
    	// 		});
    	// 		// $('body').append($('<img src="images/' + city + '/' + images[index] + '">'));
    	// 	}
    	// 	index += 1;
    	// });

	</script>

</body>
</html>

