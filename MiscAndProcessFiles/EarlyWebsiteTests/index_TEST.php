<!doctype html>
<html>
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

		html, body {
			font-family: 	'Lato', Calibri, Arial, sans-serif;
			color: 			black;
			font-size: 		16px;
			text-align: 	center;
		}

		h1 {
			font-size: 		6em;
			line-height: 	1.1em;
			color: 			rgba(0,0,0, 0.5);
		}

		a, a:link, a:visited {
			color: 				rgb(100,100,100);
			text-decoration: 	none;
			outline: 			0;		/* remove dotted line after clicking link */
		}
		a:hover, a:active {
			color: 				rgb(20,150,255);
			text-decoration: 	none;
		}

		#wrapper {
			width: 			90%;
			min-width:  	320px;
			margin:			30px auto 60px auto;
		}

		header {
			margin-bottom:  30px;
		}

		.thumb {
			display: 		inline-block;
			height: 		200px;
			width: 			200px;
			padding: 		10px;
			vertical-align: middle;
		}
		.thumb img {
			max-height: 	200px;
			max-width: 		200px;
		}
		.thumb img:hover {
			cursor: 		pointer;
		}

		.overlay {
			position: 			fixed;
			top: 				0;
			left: 				0;
			width: 				100%;
			height: 			100%;
			z-index: 			10;
			cursor: 			pointer;
			background-color: 	rgba(0,0,0, 0.9);
			padding-top: 		30px;
		}
		.overlay img {
			width: 				80%;
			height: 			80%;
			object-fit: 		contain;
			object-position: 	50% 50%;
		}

	</style>

</head>

<body>
	<div id="wrapper">

		<?php
			$i = 0;
			ini_set('auto_detect_line_endings', true);

			// get list of cities from CSV file
			$cities = array();
			if (( $handle = fopen('Craigslist_USCitiesWithLatLon.csv', 'r')) !== FALSE) {
				while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
					$cities[] = $data;
				}
			}

			// get data into easier format
			$cl_name =  $cities[$i][0];
			$location = $cities[$i][1];
			$lat = 		$cities[$i][2];
			$lon = 		$cities[$i][3];

			// display city name and info
			echo '<header>';
			echo '	<h1><a href="http://' . $cl_name . '.craigslist.org" target="_blank">' . $location . '</a></h1>';
			echo '	<p><a href="https://www.google.com/maps/place/' . $lat . ',' . $lon . '" target="_blank">' . $lat . '&deg;/' . $lon . '&deg;</a></p>';
			echo '</header>';

			// display images
			echo '<section id="images">';
			$images = glob("images/" . $cl_name . '/*.jpg');
			foreach($images as $image) {
				echo '	<div class="thumb">';
				echo "		<img src=\"" . $image . "\" onclick=\"setOverlay('" . $image . "')\">";
				// echo "		<img src=\"" . $image . "\" onclick=\"setOverlay(this)\">";
				echo '	</div>';
			}
			echo '</section>';
		?>

	</div> <!-- end wrapper -->


	<!-- overlay image when clicked -->
	<script>
		function setOverlay(img) {
			var overlay = document.createElement("div");
			overlay.setAttribute("id", "overlay");
			overlay.setAttribute("class", "overlay");
			// overlay.style.backgroundImage = "url('" + img + "')";
			overlay.innerHTML = '<img src="' + img + '">';
			overlay.onclick = removeOverlay;
			document.body.appendChild(overlay);

			// var p = img.parentNode;
			// p.style.width = '100%';
			// p.style.height = '500px';
			// img.style.width = '100%';
			// img.style.height = '100%';
		}
		function removeOverlay() {
			document.body.removeChild(document.getElementById("overlay"));
		}

		// esc to exit too
		document.onkeydown = function(e) {
			e = e || window.event;
			if (e.keyCode == 27) {
				removeOverlay();
			}
		}
	</script>

</body>
</html>



























