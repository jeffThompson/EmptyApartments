
// settings
var urlPattern = 'tiles/{z}/{x}/{y}.jpg';
var w =          80000;					// dims of your largest set of images
var h = 		 81152;

var mapMinZoom = 0;						// zoom levels
var mapMaxZoom = 3;      				// same if only one

// create base map
var _map = L.map('map', {
	maxZoom: 			mapMaxZoom,
	minZoom: 			mapMinZoom,
	crs: 				L.CRS.Simple,	// square projection
	zoomControl: 		false,			// no zoom controls
	attributionControl: false,			// no attribution box either

	touchZoom: 			false,			// no zooming, please
	scrollWheelZoom: 	false,
	doubleClickZoom: 	false,
	boxZoom: 			false,

	inertia:            false, 			// dragging inertia?

	detectRetina: 		false			// since we don't have several zoom levels
});

// customized attribution
// via: http://stackoverflow.com/a/33079705/1167783
// var attr = _map.attributionControl;
// attr.setPrefix(false);
// attr.addAttribution(
// 	'"Empty Apartments"\
// 	<span class="separator">&bull;</span>\
// 	<a href="http://www.driftstation.org">Drift Station</a>\
// 	<span class="separator">&bull;</span>\
// 	Built with <a href="http://www.leafletjs.com">Leaflet</a>\
// 	<span class="separator">&bull;</span>\
// 	<a href="#about" id="infoLink">Info</a>');
// attr.addAttribution('<a href="#about" id="infoLink">About</a>');

// set bounds to image size
var _mapBounds = new L.LatLngBounds(
	_map.unproject([0, h], mapMaxZoom),
	_map.unproject([w, 0], mapMaxZoom));
	_map.setMaxBounds(_mapBounds);

// center our view and initial zoom based on window width
var windowWidth = document.documentElement.clientWidth;
var initialZoom = mapMaxZoom;
if (windowWidth < 700) {
	initialZoom = mapMinZoom;
}
var _mapCenter = _map.unproject([w/2, h/2], mapMaxZoom);
_map.setView(_mapCenter, initialZoom);

// load custom tiles
var _tileLayer = L.tileLayer(
	urlPattern, {
	minZoom: 		 mapMinZoom,
	maxZoom: 		 mapMaxZoom,
	bounds: 		 _mapBounds,
	continuousWorld: true,			// better for non-maps
	noWrap: 		 false,			// should wrap, but doesn't seem to :(
	tileSize: 		 256,
	detectRetina: 	 false
}).addTo(_map);

// _map.addEventListener('mousemove', function(ev) {
//  			lat = ev.latlng.lat;
//  			lng = ev.latlng.lng;
//  			console.log(lat + ', ' + lng);
// });

// info box
var info =     document.getElementById('info');
var overlay =  document.getElementById('infoOverlay');
var infoLink = document.getElementById('infoLink');
var aboutBox = document.getElementsByClassName('leaflet-control-attribution')[0];

// show/hide info box
function showInfo() {
	info.style.display =        'block';
	overlay.style.display =     'block';
	aboutBox.style.visibility = 'hidden';
}
function hideInfo() {
	info.style.display =        'none';
	overlay.style.display =     'none';
	aboutBox.style.visibility = 'visible';
}
infoLink.onclick = function() {
	showInfo();
}
window.onclick = function(event) {
	if (event.target == info || event.target == overlay) {
		hideInfo();
	}
}

// highlight notes when clicked on
function highlight(id) {
	var note = document.getElementById(id);
	note.className += ' highlight';
}

// use escape key to hide too
// https://stackoverflow.com/a/3369743/1167783
document.onkeydown = function(evt) {
	evt = evt || window.event;
	var isEsc = false;
	if ('key' in evt) {
		isEsc = (evt.key == 'Escape' || evt.key == 'Esc');
	} else {
		isEsc = (evt.keyCode == 27);
	}
	if (isEsc) {
		hideInfo();
	}
}

// add zoom in/out links in menu
var zoomIn = document.getElementById('zoomInLink');
zoomIn.onclick = function() {
	_map.zoomIn();
}
var zoomOut = document.getElementById('zoomOutLink');
zoomOut.onclick = function() {
	_map.zoomOut();
}

// let people link to the info page
// var url = window.location.href;
// if (url.indexOf('#about') !== -1) {
// 	showInfo();
// }


