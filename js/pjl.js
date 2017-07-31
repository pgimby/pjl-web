

//*******************************************************************************************
//   GLOBALS
//*******************************************************************************************

var mainxmlpath = "/data/labDB.xml";
var zipoutputfilename = "PJL-lab-docs.zip";
var siteroot = "";//"/pjl-web";


// Do __NOT__ change classes or ids without checking jQuery and D3 selectors in the JS code
//I wouldn't mind adding a "show more" or "show all" button at the bottom of the record list
//or maybe have a scroll box of a specific size. When we load all the labs from the final XML
//the initial length will be huge and you'll have to scroll forever to get to the footer. - Donesies

//Also would like to have the zip, expand all, maybe search bar pinned to the top while scrolling
//down through the list alond with a "back to top" button.

//Footer isn't bold enough. Feels too light compared with rest of page. Maybe have dark
//frame around staff details.

//Somehow need to deal with file errors in the zip call. Think about how to bail gracefully.
//The top-level promis is waiting for all the files to load, what happens if one doesn't?
//---set a deferred.fail() callback on the top-level promise. easy peasy.







//*******************************************************************************************
//   PAGE INITIALIZATION
//*******************************************************************************************



function initPage() {  //initialize the page
	loadXML();
	$("#search-bar").val("");
}








//*******************************************************************************************
//   EVENT LISTENERS
//*******************************************************************************************



$(document).on("click", ".lab-details-drop-icon-flex", function(e) {
	var extendeddataflex = $(e.target).parent().siblings(".lab-record-detailed-flex");
	extendeddataflex.slideToggle("fast");
});



$(document).on("click", "#clear-filters-button", function(e) {
	var selects = $("select");
	for (var i = selects.length - 1; i >= 0; i--) {
		$(selects[i]).val([]);
	}
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("click", "select option", function(e) {
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("mousedown", "option", function(e) {
    e.preventDefault();
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});



$(document).on("click", ".search-icon", function(e) {
	searchQueryHandler();
	applyRecordsMask(true)
});



$(document).on("keypress", "#search-bar", function(e) {
	var key = e.which;
	if (key == 13) {
	 	$(".search-icon").click();
	 	return false;
	}
});



$(document).on("click", "#search-help-button", function(e) {
	$(".search-container").toggleClass("search-help-opened");
	$(e.target).next().slideToggle(300);
});



$(document).on("click", "#zip-icon", function(e) {
	$("#zip-progress-bar").slideDown(100);
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



$(document).on("click", ".download-icon", function(e) {
	window.open($(e.target).parent().parent().find(".version-path").attr("href"), "_blank");
});



$(document).on("click", "#expand-all-button", function(e) {
	flash($("#records-header"));
	var expanded = $(e.target).attr("expanded");
	if (expanded == "true") {
		toggleRecordExpansion(false);
	} else {
		toggleRecordExpansion(true);
	}
});



$(document).on("click", "#show-all-button", function(e) {
	$(e.target).css("visibility", "hidden");
	applyRecordsMask(false);
	falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester"), $("#sort-name")]);
});






//*******************************************************************************************
//   DOM ELEMENT CREATION FUNCTIONS
//*******************************************************************************************



function populateRecordList(docXML) {  //read XML and append all lab records to DOM; update displayed records counter - not type safe
	var labs = docXML.getElementsByTagName("Lab");
	for (var i = labs.length - 1; i >= 0; i--) {
		createRecordSnapshots(labs[i]);
	}
	displayNumResults(countNumRecords());
}



function populateFilters(docXML) {  //read XML and populate the HTML select boxes with available filter options - not type safe
	var types = ["Course", "Year", "Semester", "Discipline", "Topic"];
	for (var i = types.length - 1; i >= 0; i--) {
		var validlist = getValidFilterOptions(docXML, types[i]);
		for (var j = validlist.length - 1; j >= 0; j--) {
			d3.select("#" + types[i].toLowerCase() + "-select")
			  .append("option")
			  .attr("value", validlist[j])
			  .html(validlist[j]);
		}
	}
}



function createRecordSnapshots(lab) {  //create and append to DOM an appropriate number of records given an XML "lab" node - not type safe
	var versionlist = getVersionList(lab);
	for (var i = versionlist.length - 1; i >= 0; i--) {
		var detailsbox = d3.select("#lab-list-box").append("div").classed("lab-record-flex", true).classed("record-rendered", true);

		var snapshot = detailsbox.append("div").classed("lab-record-simple-flex", true);
		var download = snapshot.append("a").classed("version-path", true).html("Download").attr("href", versionlist[i].path).attr("target", "_blank");
		snapshot.append("img").classed("download-icon", true).html("Download").attr("src", "./img/download-icon.svg");  //alternate for mobile display
		var courses = snapshot.append("p").classed("courses", true).html(getCourseList(lab).join(", "));
		var date = snapshot.append("p").classed("version-semester", true).html(versionlist[i].semester + " " + versionlist[i].year);
		var labtitle = snapshot.append("p").classed("lab-title", true).html(lab.getElementsByTagName("Name")[0].childNodes[0].nodeValue);
		var dropiconflex = snapshot.append("div").classed("lab-details-drop-icon-flex", true);
		var dropicon = dropiconflex.append("img").classed("lab-details-drop-icon", true).attr("src", "./img/dropdown-arrow.png");

		var extendedlabdata = detailsbox.append("div").classed("lab-record-detailed-flex", true).attr("style", "display: none");
		var labid = extendedlabdata.append("p").classed("lab-data-id", true).html("<span>Lab ID:</span> " + getLabId(lab));
		var labtopics = extendedlabdata.append("p").classed("lab-data-topics", true).html("<span>Topics:</span> " + getLabTopicsList(lab).join(", "));
		var labdisciplines = extendedlabdata.append("p").classed("lab-data-disciplines", true).html("<span>Disciplines:</span> " + getLabDisciplinesList(lab).join(", "));
		var labequipment = extendedlabdata.append("p").classed("lab-data-equipment", true).html("<span>Equipment:</span> " + getLabEquipmentList(lab).join(", "));

		var labdoclist = getExtraLabDocs(lab);
		var labdocs = extendedlabdata.append("div").classed("extra-docs", true);
		labdocs.append("p").html("<span>Additional Documents:</span> ");
		for (var j = labdoclist.length - 1; j >= 0; j--) {
			labdocs.append("a").classed("extra-doc", true).attr("href", labdoclist[j].url).html(labdoclist[j].name).attr("target", "_blank");
		}
	}
}









//*******************************************************************************************
//   DOM MODIFIER FUNCTIONS
//*******************************************************************************************



function filterResults(filter) {  //given a filter object, filter displayed records and update DOM appropriately
	var lablist = $(".lab-record-flex");
	var numrecords = lablist.length;
	for (var i = lablist.length - 1; i >= 0; i--) {
		var lab = $(lablist[i]);
		var courses = lab.find(".courses").text().split(", ");
		var disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");
		var topics = lab.find(".lab-data-topics").text().slice(8,).split(", ");

		if (filter["year-filter"].includes(lab.find(".version-semester").text().slice(-4))       || filter["year-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			numrecords--;
			continue;
		}
		if (doArraysOverlap(courses, filter["course-filter"])                                    || filter["course-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			numrecords--;
			continue;
		}
		if (filter["semester-filter"].includes(lab.find(".version-semester").text().slice(0,-5)) || filter["semester-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			numrecords--;
			continue;
		}
		if (doArraysOverlap(disciplines, filter["discipline-filter"])                            || filter["discipline-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			numrecords--;
			continue;
		}
		if (doArraysOverlap(topics, filter["topic-filter"])                            || filter["topic-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			numrecords--;
			continue;
		}
	}
	falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name"), $("#sort-course")]);
	$("#lab-list-box").removeClass("records-unmasked");
}



function displayNumResults(numresults) {  //update number of displayed records and zip status
	$("#num-results").text(numresults);
	updateZipStatus();
}



function updateZipStatus() {  //confirm that zipping is available and update the zip icon accordingly
	var canzip = canZip()
	if (canzip) {
		$("#zip-icon").css("display", "inline-block");
	} else {
		$("#zip-icon").css("display", "none");
	}
}



function sortRecords(by) {  //take column header identifier string and sort accordingly - not type safe
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
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-course")]);
				falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name")]);
			} else {
				records.sort(compareLabsByCourse);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
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
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-semester")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-name")]);
			} else {
				records.sort(compareLabsBySemester);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
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
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-year")]);
				falsifySort([$("#sort-semester"), $("#sort-course"), $("#sort-name")]);
			} else {
				records.sort(compareLabsByYear);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
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
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-name")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester")]);
			} else {
				records.sort(compareLabsByName);
				var lablistbox = $("#lab-list-box");
				for (var i = records.length - 1; i >= 0; i--) {
					if (!$("#lab-list-box").hasClass("records-unmasked")) {
						if (i > records.length - 21) {
							records[i].removeClass("masked");
						} else {
							records[i].addClass("masked");
						}
					}
					lablistbox.append(records[i]);
				}
				truifySort([$("#sort-name")]);
				falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester")]);
			}
			break;
	}
}



function falsifySort(headers) {  //set these headers' (jQuery selections) attribute "sorted=false" - not type safe
	for (var i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "false")
	}
}



function truifySort(headers) {  //set these headers' (jQuery selections) attribute "sorted=true" - not type safe
	for (var i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "true")
	}
}



function toggleRecordExpansion(truthy) {  //expands display if truthy, contracts if falsy - type-safe
	var button = $("#expand-all-button");
	if (Boolean(truthy)) {
		var extendeddatarecords = $(".lab-record-detailed-flex");
		for (var i = extendeddatarecords.length - 1; i >= 0; i--) {
			if ($(extendeddatarecords[i]).parent().hasClass("record-rendered")) {
				$(extendeddatarecords[i]).slideDown()
			}
		}
		// extendeddatarecords.slideDown();
		setExpandedButtonTruth(true)
	} else {
		var extendeddatarecords = $(".lab-record-detailed-flex");
		for (var i = extendeddatarecords.length - 1; i >= 0; i--) {
			if ($(extendeddatarecords[i]).parent().hasClass("record-rendered")) {
				$(extendeddatarecords[i]).slideUp()
			}
		}
		// var extendeddatarecords = $(".lab-record-detailed-flex");
		// extendeddatarecords.slideUp();
		setExpandedButtonTruth(false)
	}
}



function setExpandedButtonTruth(truthy) {  //sets "expand-all-button" expanded=truthy - type safe
	var button = $("#expand-all-button");
	button.attr("expanded", String(Boolean(truthy)));
	if (Boolean(truthy)) {
		button.html("collapse all");
	} else {
		button.html("expand all");
	}
}



function applyRecordsMask(truthy) {
	var masksize = 20;
	var records = getCurrentRecords();
	unmaskAll(records);
	if (records.length > masksize && Boolean(truthy)) {
		for (var i = records.length - 1; i >= masksize; i--) {
			records[i].addClass("masked");
		}
		$("#num-unmasked-results").text(String(masksize));
		$("#show-all-button").css("visibility", "visible");
	} else {
		for (var i = records.length - 1; i >= 0; i--) {
			records[i].removeClass("masked");
		}
		$("#num-unmasked-results").text(String(records.length));
		$("#show-all-button").css("visibility", "hidden");
	}
	falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name"), $("#sort-course")]);
	$("#lab-list-box").removeClass("records-unmasked");
}



function unmaskAll(records) {
	$("#lab-list-box").addClass("records-unmasked");
	for (var i = records.length - 1; i >= 0; i--) {
		records[i].removeClass("masked");
	}
}



function getNumberRecordsUnmasked() {
	var records = getCurrentRecords();
	var num = records.length;
	for (var i = records.length - 1; i >= 0; i--) {
		if (records[i].hasClass("masked")) {
			num--;
		}
	}
	$("#num-unmasked-results").html(String(num));
}










//*******************************************************************************************
//   SEARCH-RELATED FUNCTIONS (USING SORENSEN-DICE SIMILARITY)
//*******************************************************************************************



function generateSearchResults(query, selector) {  //take query and search-selector and make yes/no decisions on what records to include; display accordingly
	var minsimilarity = 0.4;
	var querybigrams = makeBigramList(query);
	var lablist = getAllRecords();
	for (var i = lablist.length - 1; i >= 0; i--) {
		lablist[i].removeClass("record-not-rendered masked").addClass("record-rendered");
		// lablist[i].css("display", "-webkit-flex");
		// lablist[i].css("display", "flex");
		var similarity = compareQueryWithLabRecord(querybigrams, lablist[i], selector);
		if (similarity < minsimilarity && !queryLiteralInLabRecord(query, lablist[i], selector)) {
			lablist[i].removeClass("record-rendered").addClass("record-not-rendered");
			// lablist[i].css("display", "none");
		}
	}
}



function queryLiteralInLabRecord(query, lab, selector) {
	var courses = lab.find(".courses").text().toLowerCase();
	var disciplines = lab.find(".lab-data-disciplines").text().slice(13,).toLowerCase();
	var topics = lab.find(".lab-data-topics").text().slice(8,).toLowerCase();
	var equipment = lab.find(".lab-data-equipment").text().slice(11,).toLowerCase();
	var semester = lab.find(".version-semester").text().split(" ")[0].toLowerCase();
	var year = lab.find(".version-semester").text().split(" ")[1].toLowerCase();
	var labtitle = lab.find(".lab-title").text().toLowerCase();
	switch (selector) {
		case "all":
		console.log(courses.includes(query) || disciplines.includes(query) || topics.includes(query) || equipment.includes(query) || semester.includes(query) || year.includes(query) || labtitle.includes(query))
			return courses.includes(query) || disciplines.includes(query) || topics.includes(query) || equipment.includes(query) || semester.includes(query) || year.includes(query) || labtitle.includes(query);
			break;
		case "course":
			return courses.includes(query);
			break;
		case "lab":
			console.log(labtitle.includes(query));
			return labtitle.includes(query);
			break;
		case "year":
			return year.includes(query)
			break;
		case "semester":
			return semester.includes(query)
			break;
		case "topic":
			return topics.includes(query)
			break;
		case "discipline":
			return disciplines.includes(query)
			break;
		case "equipment":
			return equipment.includes(query)
			break;
	}


}



//make bigram sets for appropriate meta data of record and perform SDC comparison with search query; return best score - super not type safe
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



function sorensenDiceCoef(bigrams1, bigrams2) {  //calculate Sorensen-Dice Coefficient for two sets (arrays) of bigrams - not type safe
	var count = 0;
	$.each(bigrams1, function(i, d) {
		if (bigrams2.includes(d)) {
			count++;
		}
	});
	return 2*count / (bigrams1.length + bigrams2.length);
}



//this is the top of the search stream, pulling raw query right from the search bar
function searchQueryHandler() {  //handle search request by checking for search selectors and pass along the appropriate branch
	var query = $("#search-bar").val();
	var split = query.split(":");
	var selector = split[0];
	var searchphrase = split.slice(1,).join(" ");
	switch (selector.toLowerCase()) {
		case "course":
			courseSearchHandler(searchphrase);
			break;
		case "lab":
			labSearchHandler(searchphrase);
			break;
		case "year":
			yearSearchHandler(searchphrase);
			break;
		case "semester":
			semesterSearchHandler(searchphrase);
			break;
		case "topic":
			topicSearchHandler(searchphrase);
			break;
		case "discipline":
			disciplineSearchHandler(searchphrase);
			break;
		case "equipment":
			equipmentSearchHandler(searchphrase);
			break;
		default:
			defaultSearchHandler(query);
	}
}



function defaultSearchHandler(searchphrase) {  //handle a non-selected search request - not type safe
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



function courseSearchHandler(searchphrase) {  //handle the search request for course search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "course");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function labSearchHandler(searchphrase) {  //handle the search request for lab name search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "lab");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function yearSearchHandler(searchphrase) {  //handle the search request for year search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "year");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function semesterSearchHandler(searchphrase) {  //handle the search request for semester search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "semester");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function topicSearchHandler(searchphrase) {  //handle the search request for topic search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "topic");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function disciplineSearchHandler(searchphrase) {  //handle the search request for discipline search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "discipline");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}



function equipmentSearchHandler(searchphrase) {  //handle the search request for equipment search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "equipment");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}












//*******************************************************************************************
//   ZIP-RELATED FUNCTIONS
//*******************************************************************************************



function makePromisesBeginZip() {  //take URLs for currently displayed records, create promises, and zip for download upon resolution of all promises
	var zip = new JSZip();
	var files = ["/data/testfiles/3.pdf","/data/testfiles/1.txt","/data/testfiles/4.pdf",
	"/data/testfiles/3.txt","/data/testfiles/5.pdf","/data/testfiles/3.txt","/data/testfiles/6.pdf",
	"/data/testfiles/2.txt","/data/testfiles/4.pdf","/data/testfiles/4.txt","/data/testfiles/4.pdf",
	"/data/testfiles/8.txt","/data/testfiles/9.txt","/data/testfiles/10.txt","/data/testfiles/11.txt",
	"/data/testfiles/12.txt","/data/testfiles/13.txt","/data/testfiles/14.txt","/data/testfiles/15.txt",
	"/data/testfiles/1.pdf"];//getCurrentRecordPaths();
	var promises = [];
	var xhrs = [];
	var progresscount = 0;
	var progress = function(i) {return i/files.length};
	for (var i = files.length - 1; i >= 0; i--) {
		var downloadingfile = fileDownloadPromise();
		downloadingfile.done(function(filename, blob) {
			zip.file(filename, blob);
		});
		promises.push(downloadingfile);
		xhrs.push(beginDownload(files[i], downloadingfile));
	}
	$(document).on("click", "#cancel-download", function(e) {
		for (var i = xhrs.length - 1; i >= 0; i--) {
			xhrs[i].abort();
		}
		console.log("cancelled")
		$("#zip-progress-bar").slideUp(500);
		return;
	});
	var deferredzip = $.when.apply(this, promises);
	deferredzip.progress(function() {
		progresscount++;
		$("#zip-progress-bar progress").attr("value", String(progress(progresscount)));
	});
	deferredzip.done(function() {
		zip.generateAsync({type:"blob"}).then(function (blob) {
		saveAs(blob, zipoutputfilename);
		$("#zip-progress-bar").slideUp(500);
	}, function (err) {
          console.log(err); //this should never be thrown as I checked for browser compat. already in canZip()
          					//but for completeness' sake we could write a modal dialog to throw up here.
      });
	return false;
	});
}


function fileDownloadPromise() {  //return a jQuery promise
	return new $.Deferred();
}


function beginDownload(filepath, promise) {  //start downloading PDF and resolve associated promise upon completion - not type safe
	var xhttp = new XMLHttpRequest();
	xhttp.responseType = "blob";
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
            blob = this.response;
            var filename = filepath.split("/");
            filename = filename[filename.length-1];
            promise.notify();
            promise.resolve(filename, blob);
            console.log("File " + filename + " successfully loaded");
    	} else {
    		console.log("Error on XHTTP Request - Error Code: " + String(this.status));
    	}
  	};
  	xhttp.open("GET", siteroot + filepath, true);
  	xhttp.send();
  	return xhttp;
}



function canZip() {  //return boolean for ability to zip currently displayed records
	var bool = false;
	if (countNumRecords() > 0 && JSZip.support.blob) {
		bool = true
	}
	return bool;
}












//*******************************************************************************************
//   GENERAL FUNCTIONS
//*******************************************************************************************



function loadXML() {  //load the XML document holding all the lab records (see global var for XML URL)
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            docXML = xhttp.responseXML;
            populateRecordList(docXML);
            populateFilters(docXML);
            applyRecordsMask(true);
    	}
  	};
  	xhttp.open("GET", siteroot + mainxmlpath, true);
  	xhttp.send();
}



function getCurrentRecords() {  //returns currently displayed lab records as array of jQuery objects
	var list = [];
	var lablist = $(".lab-record-flex");
	for (var i = lablist.length - 1; i >= 0; i--) {
		if($(lablist[i]).hasClass("record-rendered")) {
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



function countNumRecords() {  //return the number of currently displayed records
	var currentrecords = getCurrentRecords();
	return currentrecords.length;
}



function getCurrentFilter() {  //return a filter object of currently activated filters
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



function getLabId(lab) {  //return lab ID as a string for an XML "lab" node - not type safe
	return lab.getAttribute("LabId");
}



function mayISeeYourSillyWalk() {  //I'd like to apply for a government grant to develop my silly walk
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



function getLabTopicsList(lab) {  //return an array of topics (strings) for an XML "lab" node - not type safe
	var list = [];
	var topics = lab.getElementsByTagName("Topic");
	for (var i = topics.length - 1; i >= 0; i--) {
		list.push(topics[i].childNodes[0].nodeValue);
	}
	return list;
}



function getLabDisciplinesList(lab) {  //return an array of disciplines (strings) for an XML "lab" node - not type safe
	var list = [];
	var disciplines = lab.getElementsByTagName("Discipline");
	for (var i = disciplines.length - 1; i >= 0; i--) {
		list.push(disciplines[i].childNodes[0].nodeValue);
	}
	return list;
}



function getLabEquipmentList(lab) {  //return an array of equipment (strings) for an XML "lab" node - not type safe
	var list = [];
	var equipment = lab.getElementsByTagName("Item");
	// console.log(equipment)
	for (var i = equipment.length - 1; i >= 0; i--) {
		list.push(equipment[i].childNodes[0].nodeValue);
	}
	return list;
}



function getCourseList(lab) {  //return an array of courses (strings) for an XML "lab" node - not type safe
	var list = [];
	var courses = lab.getElementsByTagName("Course");
	for (var i = courses.length - 1; i >= 0; i--) {
		list.push(courses[i].childNodes[0].nodeValue);
	}
	return list;
}



function getExtraLabDocs(lab) {  //return an array of extra doc objects for an XML "lab" node - not type safe
	var list = [];
	var docs = lab.getElementsByTagName("Doc");
	for (var i = docs.length - 1; i >= 0; i--) {
		list.push({name: docs[i].getAttribute("type"), url: docs[i].childNodes[0].nodeValue});
	}
	return list;
}



function iCameHereForAnArgument() {  //Oh, I'm sorry, this is abuse...
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



function getVersionList(lab) {  //return an array of version objects for a given XML "lab" node
	var versionlist = [];
	var list = lab.getElementsByTagName("Version");
	for (var i = list.length - 1; i >= 0; i--) {
		versionlist.push({path: list[i].getElementsByTagName("Path")[0].childNodes[0].nodeValue,
						  semester: list[i].getElementsByTagName("Semester")[0].childNodes[0].nodeValue,
						  year: list[i].getElementsByTagName("Year")[0].childNodes[0].nodeValue});
	}
	return versionlist;
}


//PETER WROTE THIS ONE
function getValidFilterOptions(docXML, type) {  //return the set of values available for filtering on a given filter type as an array - not type safe
	var nodelist = docXML.getElementsByTagName(type);
    var valueslist = [];
    for (var i = 0; i < nodelist.length; i ++) {
	    var value = nodelist[i].childNodes[0].nodeValue;
	    valueslist.push(value);
    }
    return Array.from(new Set(valueslist)).sort();
}



function getCurrentRecordPaths() {  //return currently displayed lab document paths as a list of strings
	var paths = [];
	var records = getCurrentRecords();
	for (var i = records.length - 1; i >= 0; i--) {
		paths.push(records[i].find(".version-path").attr("href"));
	}
	return paths;
}



function compareLabsByCourse(a, b) {  //comparison function for Array.prototype.sort on lab course of jQuery ".lab-record-flex" selection - not type safe
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



function compareLabsBySemester(a, b) {  //comparison function for Array.prototype.sort on lab semester of jQuery ".lab-record-flex" selection - not type safe
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



function compareLabsByYear(a, b) {  //comparison function for Array.prototype.sort on lab year of jQuery ".lab-record-flex" selection - not type safe
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



function compareLabsByName(a, b) {  //comparison function for Array.prototype.sort on lab name of jQuery ".lab-record-flex" selection - not type safe
	var a = a.find(".lab-title").text().toLowerCase();
	var b = b.find(".lab-title").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



function flash(jQueryDOMSelection) {
	jQueryDOMSelection.css("opacity", ".8");
	jQueryDOMSelection.animate({opacity: 1}, 600);
}









//*******************************************************************************************
//   CONVENIENCE FUNCTIONS
//*******************************************************************************************



function doArraysOverlap(array1, array2) {  //determines if two arrays share any entries - not type safe
	return array1.some(x => array2.includes(x));
}



function makeBigramList(string) {  //takes a string and returns an array of bigrams - not type safe
	list = [];
	var string = string.toLowerCase();
	for (var i = 0; i <= string.length - 2; i++) {
		list.push(string[i] + string[i+1]);
	}
	return Array.from(new Set(list));
}



function arithmeticMean(list) {  //calculates arithmetic mean of and array of numbers - not type safe
	return list.reduce((a, b) => a + b, 0) / list.length;
}



function isEmptyString(string) {  //checks if string is empty - not type safe
	return !string.replace(/\s/g, '').length;
}







