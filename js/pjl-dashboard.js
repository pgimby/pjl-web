


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
	            console.log("XML loaded");
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
	},


	xmlToString: function xmlToString(xmlData) {

	    var xmlString;
	    // for IE browser
	    if (window.ActiveXObject){
	        xmlString = xmlData.xml;
	    }
	    // for Mozilla, Firefox, Opera, etc.
	    else{
	        xmlString = (new XMLSerializer()).serializeToString(xmlData);
	    }
	    return xmlString;
	}



}







$(document).ready(Dashboard.initPage);




//MODIFY LABORATORY DATABASE

$(document).on("click", "#lab-select-edit", function(e) {
	$("#lab-db-select").fadeOut("fast", function() {
		$("#edit-lab").fadeIn("fast");
	});
});

$(document).on("click", "#lab-select-new", function(e) {
	$("#lab-db-select").fadeOut("fast", function() {
		$("#new-lab").fadeIn("fast");
	});
});



$(document).on("mouseover", "#lab-select-edit img", function() {
	console.log("hover");
	$("#lab-select-edit h3").css({backgroundColor : "#393939", color : "#fff"});
	$("#lab-select-edit h3").css("boxShadow", "0px 1px 5px 0px #222, 0px 1px 5px 0px #222 inset");
});

$(document).on("mouseout", "#lab-select-edit img", function() {
	console.log("hover");
	$("#lab-select-edit h3").css({backgroundColor : "", color : ""});
	$("#lab-select-edit h3").css("boxShadow", "");
});



$(document).on("mouseover", "#lab-select-new img", function() {
	console.log("hover");
	$("#lab-select-new h3").css({backgroundColor : "#393939", color : "#fff"});
	$("#lab-select-new h3").css("boxShadow", "0px 1px 5px 0px #222, 0px 1px 5px 0px #222 inset");
});

$(document).on("mouseout", "#lab-select-new img", function() {
	console.log("hover");
	$("#lab-select-new h3").css({backgroundColor : "", color : ""});
	$("#lab-select-new h3").css("boxShadow", "");
});







//MODIFY EQUIPMENT DATABASE

$(document).on("click", "#equip-select-edit", function(e) {
	$("#equip-db-select").fadeOut("fast", function() {
		$("#edit-equip").fadeIn("fast");
	});
});

$(document).on("click", "#equip-select-new", function(e) {
	$("#equip-db-select").fadeOut("fast", function() {
		$("#new-equip").fadeIn("fast");
	});
});



$(document).on("mouseover", "#equip-select-edit img", function() {
	console.log("hover");
	$("#equip-select-edit h3").css({backgroundColor : "#393939", color : "#fff"});
	$("#equip-select-edit h3").css("boxShadow", "0px 1px 5px 0px #222, 0px 1px 5px 0px #222 inset");
});

$(document).on("mouseout", "#equip-select-edit img", function() {
	console.log("hover");
	$("#equip-select-edit h3").css({backgroundColor : "", color : ""});
	$("#equip-select-edit h3").css("boxShadow", "");
});



$(document).on("mouseover", "#equip-select-new img", function() {
	console.log("hover");
	$("#equip-select-new h3").css({backgroundColor : "#393939", color : "#fff"});
	$("#equip-select-new h3").css("boxShadow", "0px 1px 5px 0px #222, 0px 1px 5px 0px #222 inset");
});

$(document).on("mouseout", "#equip-select-new img", function() {
	console.log("hover");
	$("#equip-select-new h3").css({backgroundColor : "", color : ""});
	$("#equip-select-new h3").css("boxShadow", "");
});