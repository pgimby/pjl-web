

//*******************************************************************************************
//   GLOBALS
//*******************************************************************************************

var mainxmlpath = "/data/pjl-lab-database.xml";
var zipoutputfilename = "PJL-lab-docs.zip";
var siteroot = "/pjl-web"





//*******************************************************************************************
//   PAGE INITIALIZATION
//*******************************************************************************************



function initPage() {
	loadXML();
	$("#search-bar").val("");
}









//*******************************************************************************************
//   GENERAL FUNCTIONS
//*******************************************************************************************



function loadXML() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
            docXML = this.responseXML;
            populateRecordList(docXML);
            populateFilters(docXML);
    	}
  	};
  	xhttp.open("GET", siteroot + mainxmlpath, true);
  	xhttp.send();
} 



function getCurrentRecords() {  //returns currently displayed lab records as array of jquery objects
	var list = [];
	var lablist = $(".lab-record-flex");
	for (var i = lablist.length - 1; i >= 0; i--) {
		if($(lablist[i]).css("display") != "none") {
			list.push($(lablist[i]));
		}
	}
	return list;
}



function getAllRecords() {  //returns all lab records as array of jquery objects
	var list = [];
	var lablist = $(".lab-record-flex");
	for (var i = lablist.length - 1; i >= 0; i--) {
		list.push($(lablist[i]));
	}
	return list;
}



function countNumRecords() {
	var currentrecords = getCurrentRecords();
	return currentrecords.length;
}



function getCurrentFilter() {
	var selects = $("select");
	var filter = {};
	for (var i = selects.length - 1; i >= 0; i--) {
		if (selects[i].value) {
			filter[$(selects[i]).parent().attr("id")] = $(selects[i]).val();
		} else {
			filter[$(selects[i]).parent().attr("id")] = [];
		}
	}
	return filter;
}



function getLabId(lab) {
	return lab.getAttribute("LABID");
}



function mayISeeYourSillyWalk() {
	var itsnotparticularlysillyisit = "The right leg isn't silly at all and the left leg merely does a forward aerial half turn every alternate step.";
	$(".search-icon").attr("src","./img/silly-walk.png");
	$(".search-icon").css({height: "45px", width: "35px", top: "-49px", right: "-35px"})
	$("#search-bar").attr("placeholder", itsnotparticularlysillyisit);
	$("#search-bar").css("font-size", "11px");
	$("#search-bar").val("");
	setTimeout(function() {
		$(".search-icon").attr("src","./img/search-icon.png");
		$(".search-icon").css({height: "40px", width: "40px", top: "-45px", right: "-35px"})
		$("#search-bar").attr("placeholder", "Keyword, topic, course...");
		$("#search-bar").css("font-size", "1rem");
		$("#search-bar").val("");		
	}, 6000);

}



function getLabTopicsList(lab) {
	var list = [];
	var topics = lab.getElementsByTagName("topic");
	for (var i = topics.length - 1; i >= 0; i--) {
		list.push(topics[i].childNodes[0].nodeValue);
	}
	return list;
}



function getLabDisciplinesList(lab) {
	var list = [];
	var disciplines = lab.getElementsByTagName("discipline");
	for (var i = disciplines.length - 1; i >= 0; i--) {
		list.push(disciplines[i].childNodes[0].nodeValue);
	}
	return list;
}



function getLabEquipmentList(lab) {
	var list = [];
	var equipment = lab.getElementsByTagName("item");
	// console.log(equipment)
	for (var i = equipment.length - 1; i >= 0; i--) {
		list.push(equipment[i].getAttribute("name"));
	}
	return list;
}



function getCourseList(lab) {
	var list = [];
	var courses = lab.getElementsByTagName("course");
	for (var i = courses.length - 1; i >= 0; i--) {
		list.push(courses[i].childNodes[0].nodeValue);
	}
	return list;
}



function getExtraLabDocs(lab) {
	var list = [];
	var docs = lab.getElementsByTagName("doc");
	// console.log(docs)
	for (var i = docs.length - 1; i >= 0; i--) {
		list.push({name: docs[i].getAttribute("type"), url: docs[i].childNodes[0].nodeValue});
	}
	// console.log(docs.length)
	return list;
}



function iCameHereForAnArgument() {
	var i = 0;
	$(".search-icon").attr("src","./img/silly-walk.png");
	$(".search-icon").css({height: "45px", width: "35px", top: "-49px", right: "-35px"})
	$("#search-bar").val("");
	var id = setInterval(function() {
		if (i == argument.length - 1) {
			clearInterval(id);
			$(".search-icon").attr("src","./img/search-icon.png");
			$(".search-icon").css({height: "40px", width: "40px", top: "-45px", right: "-35px"});
			$("#search-bar").val("");
			$("#search-bar").attr("placeholder", "Keyword, topic, course...");
			return;
		}
		$("#search-bar").attr("placeholder", argument[i]);
		i++;
	}, 1000);
}



function getVersionList(lab) {
	var versionlist = [];
	var list = lab.getElementsByTagName("version");
	for (var i = list.length - 1; i >= 0; i--) {
		versionlist.push({path: list[i].getElementsByTagName("path")[0].childNodes[0].nodeValue, 
						  semester: list[i].getElementsByTagName("semester")[0].childNodes[0].nodeValue, 
						  year: list[i].getElementsByTagName("year")[0].childNodes[0].nodeValue});
	}
	return versionlist;
}



function getValidFilterOptions(docXML, type) {
	var nodelist = docXML.getElementsByTagName(type);
    var valueslist = [];
    for (var i = 0; i < nodelist.length; i ++) {
	    var value = nodelist[i].childNodes[0].nodeValue;
	    valueslist.push(value);
    }
    return Array.from(new Set(valueslist));
}



function getCurrentRecordPaths() {
	var paths = [];
	var records = getCurrentRecords();
	for (var i = records.length - 1; i >= 0; i--) {
		paths.push(records[i].find(".version-path").attr("href"));
	}
	return paths;
}



function compareLabsByCourse(a, b) {
	var a = a.find(".courses").text().split(", ")[0];
	var b = b.find(".courses").text().split(", ")[0];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



function compareLabsBySemester(a, b) {
	var a = a.find(".version-semester").text().split(" ")[0];
	var b = b.find(".version-semester").text().split(" ")[0];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



function compareLabsByYear(a, b) {
	var a = a.find(".version-semester").text().split(" ")[1];
	var b = b.find(".version-semester").text().split(" ")[1];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



function compareLabsByName(a, b) {
	var a = a.find(".lab-title").text();
	var b = b.find(".lab-title").text();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}








//*******************************************************************************************
//   SEARCH-RELATED FUNCTIONS (USING SORENSEN-DICE SIMILARITY)
//*******************************************************************************************



function generateSearchResults(query, selector) {
	var minsimilarity = 0.4;
	var querybigrams = makeBigramList(query);
	var lablist = getAllRecords();
	for (var i = lablist.length - 1; i >= 0; i--) {
		lablist[i].css("display", "-webkit-flex");
		lablist[i].css("display", "flex");
		var similarity = compareQueryWithLabRecord(querybigrams, lablist[i], selector);
		if (similarity < minsimilarity) {
			lablist[i].css("display", "none");
		}
	}
}



function compareQueryWithLabRecord(querybigrams, lab, selector) {
	var courses = lab.find(".courses").text().split(", ");
	var disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");
	var topics = lab.find(".lab-data-topics").text().slice(8,).split(", ");
	var equipment = lab.find(".lab-data-equipment").text().slice(11,).split(", ");
	courses = courses.map(function(d) {
		return makeBigramList(d.slice(4,));
	});
	disciplines = disciplines.map(function(d) {
		return makeBigramList(d);
	});
	topics = topics.map(function(d) {
		return makeBigramList(d);
	});
	equipment = equipment.map(function(d) {
		return makeBigramList(d);
	});
	var semester = [makeBigramList(lab.find(".version-semester").text().split(" ")[0])];
	var year = [makeBigramList(lab.find(".version-semester").text().split(" ")[1].slice(2,))];
	var labtitle = [makeBigramList(lab.find(".lab-title").text())];
	switch (selector) {
		case "all":
			var totest = disciplines.concat(courses, semester, year, labtitle, topics, equipment);
			break;
		case "course":
			var totest = courses;
			break;
		case "lab":
			var totest = labtitle;
			break;
		case "year":
			var totest = year;
			break;
		case "semester":
			var totest = semester;
			break;
		case "topic":
			var totest = topics;
			break;
		case "discipline":
			var totest = disciplines;
			break;
		case "equipment":
			var totest = equipment;
			break;
	}
	
	var max = 0.0;
	for (var i = totest.length - 1; i >= 0; i--) {
		var result = sorensenDiceCoef(querybigrams, totest[i]);
		if (result > max) {
			max = result
		}
	}
	return max;
}



function sorensenDiceCoef(bigrams1, bigrams2) {
	var count = 0;
	$.each(bigrams1, function(i, d) {
		if (bigrams2.includes(d)) {
			count++;
		}
	});
	return 2*count / (bigrams1.length + bigrams2.length);
}



function searchQueryHandler() {
	var query = $("#search-bar").val();
	var split = query.split(":");
	var selector = split[0];
	var searchphrase = split.slice(1,).join(" ");
	switch (selector) {
		case "Course":
			courseSearchHandler(searchphrase);
			break;
		case "Lab":
			labSearchHandler(searchphrase);
			break;
		case "Year":
			yearSearchHandler(searchphrase);
			break;
		case "Semester":
			semesterSearchHandler(searchphrase);
			break;
		case "Topic":
			topicSearchHandler(searchphrase);
			break;
		case "Discipline":
			disciplineSearchHandler(searchphrase);
			break;
		case "Equipment":
			equipmentSearchHandler(searchphrase);
			break;
		default:
			defaultSearchHandler(query);
	}
}



function defaultSearchHandler(searchphrase) {
	if(isEmptyString(searchphrase)) {
		return;
	}
	switch(searchphrase) {
		case "silly walk":
			mayISeeYourSillyWalk();
			break;
		case "I came here for an argument":
			iCameHereForAnArgument();
			break;
		case "show me something funny":
			window.open("https://xkcd.com", '_blank');
			break;
		default:
			$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "all");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
	}
}



function courseSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "course");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function labSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "lab");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");	
}



function yearSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "year");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function semesterSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "semester");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function topicSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "topic");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function disciplineSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "discipline");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function equipmentSearchHandler(searchphrase) {
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "equipment");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}












//*******************************************************************************************
//   ZIP-RELATED FUNCTIONS
//*******************************************************************************************



function makePromisesBeginZip() {
	var zip = new JSZip();
	var files = ["/data/testfiles/1.txt","/data/testfiles/2.dat","/data/testfiles/3.js","/data/testfiles/4.jpg"];//getCurrentRecordPaths();
	var promises = []
	for (var i = files.length - 1; i >= 0; i--) {
		var downloadingfile = fileDownloadPromise();
		downloadingfile.done(function(filename, blob) {
			zip.file(filename, blob);
		});
		promises.push(downloadingfile);
		beginDownload(files[i], downloadingfile);
	}
	$.when.apply(this, promises).done(function() {
		zip.generateAsync({type:"blob"}).then(function (blob) {
		saveAs(blob, zipoutputfilename);
	}, function (err) {
          console.log(err); //this should never be thrown as I checked for browser compat. already in canZip()
          					//but for completeness' sake we could write a modal dialog to throw up here.
      });
	return false;
	});
}


function fileDownloadPromise() {
	return new $.Deferred();
}


function beginDownload(filepath, promise) {
	var xhttp = new XMLHttpRequest();
	xhttp.responseType = "blob";
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
            blob = this.response;
            var filename = filepath.split("/");
            filename = filename[filename.length-1];
            promise.resolve(filename, blob);
            console.log("File " + filename + " successfully loaded");
    	} else {
    		console.log("Error on XHTTP Request - Error Code: " + String(this.status));
    	}
  	};
  	xhttp.open("GET", siteroot + filepath, true);
  	xhttp.send();
}



function canZip() {
	var bool = false;
	if (countNumRecords() > 0 && JSZip.support.blob) {
		bool = true
	}
	return bool;
}







//*******************************************************************************************
//   DOM ELEMENT CREATION FUNCTIONS
//*******************************************************************************************



function populateRecordList(docXML) {
	var labs = docXML.getElementsByTagName("lab");
	for (var i = labs.length - 1; i >= 0; i--) {
		createRecordSnapshots(labs[i]);
	}
	displayNumResults(countNumRecords());
}



function populateFilters(docXML) {
	var types = ["course", "year", "semester", "discipline"];
	for (var i = types.length - 1; i >= 0; i--) {
		var validlist = getValidFilterOptions(docXML, types[i]);
		for (var j = validlist.length - 1; j >= 0; j--) {
			d3.select("#" + types[i] + "-select")
			  .append("option")
			  .attr("value", validlist[j])
			  .html(validlist[j]);
		}
	}
}



function createRecordSnapshots(lab) {
	var versionlist = getVersionList(lab);
	for (var i = versionlist.length - 1; i >= 0; i--) {
		var detailsbox = d3.select("#lab-list-box").append("div").classed("lab-record-flex", true);

		var snapshot = detailsbox.append("div").classed("snapshot-flex", true);
		var download = snapshot.append("a").classed("version-path", true).html("Download").attr("href", versionlist[i].path);
		var courses = snapshot.append("p").classed("courses", true).html(getCourseList(lab).join(", "));
		var date = snapshot.append("p").classed("version-semester", true).html(versionlist[i].semester + " " + versionlist[i].year);
		var labtitle = snapshot.append("p").classed("lab-title", true).html(lab.getElementsByTagName("name")[0].childNodes[0].nodeValue);
		var dropiconflex = snapshot.append("div").classed("lab-details-drop-icon-flex", true);
		var dropicon = dropiconflex.append("img").classed("lab-details-drop-icon", true).attr("src", "./img/dropdown-arrow.png");

		var extendedlabdata = detailsbox.append("div").classed("extended-lab-data-flex", true).attr("style", "display: none");
		var labid = extendedlabdata.append("p").classed("lab-data-id", true).html("<span>Lab ID:</span> " + getLabId(lab));
		var labtopics = extendedlabdata.append("p").classed("lab-data-topics", true).html("<span>Topics:</span> " + getLabTopicsList(lab).join(", "));
		var labdisciplines = extendedlabdata.append("p").classed("lab-data-disciplines", true).html("<span>Disciplines:</span> " + getLabDisciplinesList(lab).join(", "));
		var labequipment = extendedlabdata.append("p").classed("lab-data-equipment", true).html("<span>Equipment:</span> " + getLabEquipmentList(lab).join(", "));
		
		var labdoclist = getExtraLabDocs(lab);
		var labdocs = extendedlabdata.append("div").classed("extra-docs", true);
		labdocs.append("p").html("<span>Additional Documents:</span> ");
		for (var j = labdoclist.length - 1; j >= 0; j--) {
			labdocs.append("a").classed("extra-doc", true).attr("href", labdoclist[j].url).html(labdoclist[j].name);
		}
	}
}









//*******************************************************************************************
//   EVENT LISTENERS
//*******************************************************************************************



$(document).on("click", ".lab-details-drop-icon-flex", function(e) {
	var extendeddataflex = $(e.target).parent().siblings(".extended-lab-data-flex");
	extendeddataflex.slideToggle("fast");
	// extendeddataflex.toggleClass("extended-lab-data-visible");
});



$(document).on("click", "#clear-filters-button", function(e) {
	var selects = $("select");
	for (var i = selects.length - 1; i >= 0; i--) {
		$(selects[i]).val([]);
	}
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
});



$(document).on("click", "select", function(e) {
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
});



$(document).on("mousedown", "option", function(e) {
    e.preventDefault();
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});



$(document).on("click", ".search-icon", function(e) {
	searchQueryHandler();
});



$(document).on("keypress", "#search-bar", function(e) {
	var key = e.which;
	if (key == 13) {
	 	$(".search-icon").click();
	 	return false;
	}
});



$(document).on("click", "#search-help-btn", function(e) {
	$(".search-container").toggleClass("search-help-opened");
	$(e.target).next().slideToggle(300);
});



$(document).on("click", "#zip-icon", function(e) {
	makePromisesBeginZip();
});



$(document).on("click", "#sort-name", function(e) {
	sortRecords("name");
});



$(document).on("click", "#sort-year", function(e) {
	sortRecords("year");
});



$(document).on("click", "#sort-semester", function(e) {
	sortRecords("semester");
});



$(document).on("click", "#sort-course", function(e) {
	sortRecords("course");
});









//*******************************************************************************************
//   CONVENIENCE FUNCTIONS
//*******************************************************************************************



function doArraysOverlap(array1, array2) {
	return array1.some(x => array2.includes(x));
}



function makeBigramList(string) {
	list = [];
	var string = string.toLowerCase();
	for (var i = 0; i <= string.length - 2; i++) {
		list.push(string[i] + string[i+1]);
	}
	return Array.from(new Set(list));
}



function arithmeticMean(list) {
	return list.reduce((a, b) => a + b, 0) / list.length;
}



function isEmptyString(string) {
	return !string.replace(/\s/g, '').length;
}







//*******************************************************************************************
//   DOM MODIFIER FUNCTIONS
//*******************************************************************************************



function filterResults(filter) {
	var lablist = $(".lab-record-flex");
	var numrecords = lablist.length;
	for (var i = lablist.length - 1; i >= 0; i--) {
		var lab = $(lablist[i]);
		var courses = lab.find(".courses").text().split(", ");
		var disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");

		if (filter["year-filter"].includes(lab.find(".version-semester").text().slice(-4))       || filter["year-filter"].length == 0) {
			lab.css("display", "-webkit-flex");
			lab.css("display", "flex");
		} else {
			lab.css("display", "none");
			numrecords--;
			continue;
		}
		if (doArraysOverlap(courses, filter["course-filter"])                                    || filter["course-filter"].length == 0) {
			lab.css("display", "-webkit-flex");
			lab.css("display", "flex");
		} else {
			lab.css("display", "none");
			numrecords--;
			continue;
		}
		if (filter["semester-filter"].includes(lab.find(".version-semester").text().slice(0,-5)) || filter["semester-filter"].length == 0) {
			lab.css("display", "-webkit-flex");
			lab.css("display", "flex");
		} else {
			lab.css("display", "none");
			numrecords--;
			continue;
		}
		if (doArraysOverlap(disciplines, filter["discipline-filter"])                            || filter["discipline-filter"].length == 0) {
			lab.css("display", "-webkit-flex");
			lab.css("display", "flex");
		} else {
			lab.css("display", "none");
			numrecords--;
			continue;
		}
	}
}


 
function displayNumResults(numresults) {
	$("#num-results").text(numresults);
	updateZipStatus();
}



function updateZipStatus() {
	var canzip = canZip()
	if (canzip) {
		$("#zip-icon").css("display", "inline-block");
	} else {
		$("#zip-icon").css("display", "none");
	}
}



function sortRecords(by) {
	var records = getCurrentRecords();
	var sorted = [];
	for (var i = records.length - 1; i >= 0; i--) {
		records[i].detach();
	}
	switch (by) {
		case "course":
			if ($("#sort-course").attr("sorted") == "true") {
				records.reverse();
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-course")]);
				falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name")]);
			} else {
				records.sort(compareLabsByCourse);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-course")]);
				falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name")]);
			}
			break;
		case "semester":
			if ($("#sort-semester").attr("sorted") == "true") {
				records.reverse();
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-semester")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-name")]);
			} else {
				records.sort(compareLabsBySemester);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-semester")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-name")]);
			}
			break;
		case "year":
			if ($("#sort-year").attr("sorted") == "true") {
				records.reverse();
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-year")]);
				falsifySort([$("#sort-semester"), $("#sort-course"), $("#sort-name")]);
			} else {
				records.sort(compareLabsByYear);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-year")]);
				falsifySort([$("#sort-semester"), $("#sort-course"), $("#sort-name")]);
			}
			break;
		case "name":
			if ($("#sort-name").attr("sorted") == "true") {
				records.reverse();
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-name")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester")]);
			} else {
				records.sort(compareLabsByName);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-name")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester")]);
			}
			break;
	}
}



function falsifySort(headers) {
	for (var i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "false")
	}
}



function truifySort(headers) {
	for (var i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "true")
	}
}