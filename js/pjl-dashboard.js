


//*******************************************************************************************
//   DASHBOARDS
//*******************************************************************************************



var Dashboard = Dashboard || {
	docXML: null,



	initPage: function() {
		Dashboard.loadXML();
	},



	loadXML: function() {  //load the XML document holding all the lab records (see global var for XML URL)
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
	    	if (this.readyState == 4 && this.status == 200) {
	            Dashboard.docXML = this.responseXML;
	            console.log("XML loaded")
	    	}
	  	};
	  	xhttp.open("GET", siteroot + mainxmlpath, true);
	  	xhttp.send();
	},



	populateAutoSearch: function() {

	},



	clearForm: function() {

	},



	fillForm: function() {

	},



	getLabNames: function(xml) {

	},



	zipAndDeliver: function(filepathlist, outputfilename, progressbar, failfunction) {
		if (!progressbar) {
			var progressbar;
		}
		if (!failfunction) {
			var failfunction = function(){};
		}

		var zip = new JSZip();
		var promises = [];
		var progresscount = 0;
		var progress = function(i) {
			return i/files.length;
		};
	}




}







$(document).ready(Dashboard.initPage);








