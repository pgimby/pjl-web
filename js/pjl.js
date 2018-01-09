

//*******************************************************************************************
//   GLOBALS
//*******************************************************************************************

var labdatabasepath = "/data/labDB.xml";
var equipmentdatabasepath = "/data/equipmentDB.xml";
var siteroot = "";
var recordmasklength = 20;
var selectedrecords = 0;

// Do __NOT__ change classes or ids without checking jQuery and D3 selectors in the JS code







//*******************************************************************************************
//   MODAL CLASS DEFINITIONS (need to stay at top because JS classes aren't hoisted)
//*******************************************************************************************




// this class defines a modal dialog for viewing (not modifying) the details of an equipment item
//it is instantiated whenever an equipment item is clicked in the inventory list
class EquipmentDisplay {

	constructor(id) {
		var self = this;
		self.id = id;
		self.modalmask = d3.select("body").append("div").classed("modal-screen", true).style("display", "block");

		//retrieve the equipment xml and build the display
		self._loadEquipDB = function() {
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
		    	if (xhttp.readyState == 4 && xhttp.status == 200) {
		            let docXML = xhttp.responseXML;
		            let data = self._getItemData(docXML, self.id);
		            self._buildDisplay(data);
		    	}
		  	};
		  	xhttp.open("GET", siteroot + equipmentdatabasepath, true);
		  	xhttp.send();
		}

		//given the entire xml document, retreive just the item matching 'id'
		self._getItemData = function(xml, id) {
			let nodes = xml.getElementsByTagName("Item");
			for (let i = nodes.length - 1; i >= 0; i--) {
				if (nodes[i].getAttribute("id") == id) {
					return nodes[i];
				}
			}
		}

		//build the display on top of the modal mask and populate with the equipment details contained in 'data'
		self._buildDisplay = function(data) {
			let id = data.getAttribute("id");
			let name = (data.getElementsByTagName("InventoryName")[0].childNodes[0] ? data.getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue : "none");
			let make = (data.getElementsByTagName("Manufacturer")[0].childNodes[0] ? data.getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "none");
			let model = (data.getElementsByTagName("Model")[0].childNodes[0] ? data.getElementsByTagName("Model")[0].childNodes[0].nodeValue : "none");
			let locations = [];
			let locationnodes = data.getElementsByTagName("Locations")[0].getElementsByTagName("Location");
			for (let i = locationnodes.length - 1; i >= 0; i--) {
				let room = locationnodes[i].getElementsByTagName("Room")[0].childNodes[0].nodeValue;
				let storage = locationnodes[i].getElementsByTagName("Storage")[0].childNodes[0].nodeValue;
				locations.push({"room": room, "storage": storage})
			}
			let total = (data.getElementsByTagName("Total")[0].childNodes[0] ? data.getElementsByTagName("Total")[0].childNodes[0].nodeValue : "N/A")
			let service = (data.getElementsByTagName("InService")[0].childNodes[0] ? data.getElementsByTagName("InService")[0].childNodes[0].nodeValue : "N/A")
			let repair = (data.getElementsByTagName("UnderRepair")[0].childNodes[0] ? data.getElementsByTagName("UnderRepair")[0].childNodes[0].nodeValue : "N/A")
			let docs = [];
			let docnodes = data.getElementsByTagName("Document");
			for (let i = docnodes.length - 1; i >= 0; i--) {
				let name = docnodes[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
				let path = docnodes[i].getElementsByTagName("Location")[0].childNodes[0].nodeValue;
				docs.push({"name": name, "path": path})
			}

			let modal = self.modalmask.append("div").classed("eq-modal", true);
			let header = modal.append("div").classed("eq-modal-header", true);
			header.append("h1").classed("eq-modal-title", true).html("Inventory" + "<span>  (" + id +")</span>");
			header.append("i").classed("fa fa-times fa-2x modal-close-button", true).attr("aria-hidden", "true");

			let content = modal.append("div").classed("eq-modal-content", true);
			let img = content.append("div").classed("eq-modal-img", true);
			img.append("img").attr("src", "/img/img-placeholder.png");
			let ident = content.append("div").classed("eq-modal-id", true);
			ident.append("h3").classed("eq-modal-name", true).html(name);
			let mm = ident.append("div").classed("eq-make-model", true);
			mm.append("p").classed("eq-make", true).html(make);
			mm.append("p").classed("eq-model", true).html(model);
			let locs = content.append("div").classed("eq-modal-locations", true);
			locs.append("h1").classed("modal-header", true).html("Locations");
			for (let i = locations.length - 1; i >= 0; i--) {
				locs.append("p").classed("eq-modal-location", true).html(locations[i].room + " " + locations[i].storage);
			}

			let amts = content.append("div").classed("eq-modal-amounts", true);
			amts.append("h1").classed("modal-header", true).html("Amounts");
			let amt1 = amts.append("div").classed("eq-modal-amount total", true);
			amt1.append("h2").html(total);
			amt1.append("h3").html("Total");
			let amt2 = amts.append("div").classed("eq-modal-amount service", true);
			amt2.append("h2").html(service);
			amt2.append("h3").html("In Service");
			let amt3 = amts.append("div").classed("eq-modal-amount repair", true);
			amt3.append("h2").html(repair);
			amt3.append("h3").html("Under Repair");

			let dcs = content.append("div").classed("eq-modal-docs", true);
			dcs.append("h1").classed("modal-header", true).html("Documents");
			for (let i = docs.length - 1; i >= 0; i--) {
				let dc = dcs.append("div").classed("eq-modal-doc", true);
				dc.append("i").classed("fa fa-file-o", true).attr("aria-hidden", "true");
				dc.append("a").attr("href", docs[i].path).attr("target", "_blank").html(docs[i].name);
			}
		}

		//set event listeners to handle closing and to prevent click events from bubbling up from the dialog to the modal mask
		self._setEventListeners = function() {
			$(document).on("click", ".modal-screen", self.removeForm);

			$(document).on("click", ".eq-modal", function(e) {
				e.stopPropagation();
			});

			$(document).on("click", ".modal-close-button", self.removeForm);
		}

		//disconnect event listeners and remove the modal mask from the DOM. Removal of modal mask also removes its children, i.e., the entire dialog
		self.removeForm = function() {
			self.modalmask.remove();
			$("main").removeClass("blurred-page");
			$(document).off("click", ".modal-screen");
			$(document).off("click", ".eq-modal");
			$(document).off("click", ".modal-close-button");
		}

		//everything above this is a definition. This is where it's all called.
		self._loadEquipDB();
		self._setEventListeners();
		$("main").addClass("blurred-page");
	}
}



//this class defines a modal dialog for initializing the downloading of documents from the lab repo.
//it is instantiated whenever the zip button is clicked on the repo page.
class DownloadModalWindow {

	constructor(id) {
		var self = this;
		self.id = id;
		self.modalmask = d3.select("body").append("div").classed("modal-screen", true).style("display", "block");

		//build the dialog on top of the modal mask
		self._buildWindow = function() {
			let modal = self.modalmask.append("div").classed("dl-modal", true);

			let header = modal.append("div").classed("dl-modal-header", true);
			header.append("h1").classed("dl-modal-title", true).html("Download Options<br><span id='dl-modal-number'></span>");
			header.append("i").classed("fa fa-times fa-2x modal-close-button", true).attr("aria-hidden", "true");

			let content = modal.append("div").classed("dl-modal-content", true);
			let msg = content.append("p").html("Select which types of files you want to download or download everything.");
			let chk1 = content.append("div").classed("dl-modal-check", true).attr("id", "PDF");
			chk1.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div1 = chk1.append("dl-modal-item-content", true);
			div1.append("h3").html("PDF");
			div1.append("p").html("PDF of the final lab document (.pdf)");

			let chk2 = content.append("div").classed("dl-modal-check", true).attr("id", "TEX");
			chk2.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div2 = chk2.append("dl-modal-item-content", true);
			div2.append("h3").html("TEX");
			div2.append("p").html("LaTeX source documents for the lab (.tex)");

			let chk3 = content.append("div").classed("dl-modal-check", true).attr("id", "MEDIA");
			chk3.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div3 = chk3.append("dl-modal-item-content", true);
			div3.append("h3").html("Media");
			div3.append("p").html("Images and video files (.tiff, .png, .jpeg, .gif, .mp4, .avi, .dv)");

			let chk4 = content.append("div").classed("dl-modal-check", true).attr("id", "TEMPLATES");
			chk4.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div4 = chk4.append("dl-modal-item-content", true);
			div4.append("h3").html("Templates");
			div4.append("p").html("Data templates used in the experiment (.cmbl, .xlxs, .dat, .csv, .tsv, .txt)");

			let chk5 = content.append("div").classed("dl-modal-check", true).attr("id", "EXTRA");
			chk5.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div5 = chk5.append("dl-modal-item-content", true);
			div5.append("h3").html("Support Documents");
			div5.append("p").html("Supporting documents for the lab and its development (various)");

			let chk6 = content.append("div").classed("dl-modal-check checked", true).attr("id", "ALL");
			chk6.append("i").classed("fa fa-file-o fa-2x", true).attr("aria-hidden", "true");
			let div6 = chk6.append("dl-modal-item-content", true);
			div6.append("h3").html("Everything");
			div6.append("p").html("All files associated with the lab (various)");


			let footer = modal.append("div").classed("dl-modal-footer", true);
			footer.append("h3").classed("dl-modal-confirm", true).html("Download");
		}

		//set event listeners for closing and to prevent click events from bubbling up from the dialog to the modal mask
		//set event listener for initializing the download and toggling the selections
		self._setEventListeners = function() {
			$(document).on("click", ".modal-screen", self.removeWindow);

			$(document).on("click", ".dl-modal", function(e) {
				e.stopPropagation();
			});

			$(document).on("click", ".modal-close-button", self.removeWindow);

			$(document).on("click", ".dl-modal-footer", function(e) {
				var all = $("#ALL").hasClass("checked");
				var pdf = $("#PDF").hasClass("checked");
				var tex = $("#TEX").hasClass("checked");
				var tmp = $("#TEMPLATES").hasClass("checked");
				var med = $("#MEDIA").hasClass("checked");
				var extradocs = $("#EXTRA").hasClass("checked");
				self.removeWindow();
				$("#zip-progress-bar").slideDown(200, function() {
					collectFiles2Zip(all, pdf, tex, tmp, med, extradocs);
				});
			});

			$(document).on("click", ".dl-modal-check", function(e) {
				let checkitem = $(e.target);
				if (checkitem.attr("id") == "ALL" && checkitem.hasClass("checked")) {
					return;
				} else if (checkitem.attr("id") == "ALL" && !checkitem.hasClass("checked")) {
					checkitem.toggleClass("checked");
					checkitem.siblings().removeClass("checked");
				} else if (checkitem.attr("id") != "ALL" && $(".dl-modal-check#ALL").hasClass("checked")) {
					checkitem.toggleClass("checked");
					$(".dl-modal-check#ALL").removeClass("checked");
				} else if (checkitem.attr("id") != "ALL" && !$(".dl-modal-check#ALL").hasClass("checked")) {
					checkitem.toggleClass("checked");
				}
				if (!$(".dl-modal-check").hasClass("checked")) {
					$(".dl-modal-check#ALL").addClass("checked");
				}
			});
		}

		self.removeWindow = function() {
			self.modalmask.remove();
			$("main").removeClass("blurred-page");
			$(document).off("click", ".modal-screen");
			$(document).off("click", ".modal-close-button");
			$(document).off("click", ".dl-modal");
			$(document).off("click", ".dl-modal-footer");
			$(document).off("click", ".dl-modal-check");
		}

		$("main").addClass("blurred-page");
		self._buildWindow();
		self._setEventListeners();
	}
}








//*******************************************************************************************
//   PAGE INITIALIZATION
//*******************************************************************************************



//Initialize the repository page.
function initRepoPage() {
	loadXML();
	$("#search-bar").val("");
}



//Nothing needs to be initialized on the landing page... yet.
function initLandingPage() {

}


//Initialize the equipment inventory page.
function initEquipmentPage() {
	equipmentPageQueryString();
	//see the comment on this function
	loadEquipmentXML(enableEquipmentSearchAutoComplete, populateEquipmentFilters, createEquipRecordSnapshots);
}




















//*******************************************************************************************
//   EVENT LISTENERS
//*******************************************************************************************



$(document).on("click touch", ".lab-details-drop-icon-flex", function(e) {
	var extendeddataflex = $(e.target).parent().siblings(".lab-record-detailed-flex");
	extendeddataflex.stop().slideToggle("fast");
});



$(document).on("click touch", "#clear-filters-button", function(e) {
	var selects = $("select");
	for (let i = selects.length - 1; i >= 0; i--) {
		$(selects[i]).val([]);
	}
	filterResults(getCurrentFilter(), fullset=true);
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("click touch", "#show-recent-button", function(e) {
	showMostRecent();
});



$(document).on("click touch", "select", function(e) {
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("change", "select", function(e) {
	filterResults(getCurrentFilter());
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("mousedown", "option", function(e) {
    e.preventDefault();
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});



$(document).on("click touch", ".search-icon", function(e) {
	searchQueryHandler();
	applyRecordsMask(true)
});



$(document).on("keypress", "#search-bar", function(e) {
	let key = e.which;
	if (key == 13) {
	 	$(".search-icon").click();
	 	return false;
	}
});



$(document).on("click touch", "#search-help-button", function(e) {
	console.log($(e.target), $(e.target).next())
	$(".search-container").toggleClass("search-help-opened");
	$(e.target).next().stop().slideToggle(300);
});



$(document).on("click touch", "#zip-icon", function(e) {
	new DownloadModalWindow();
	if ($("#zip-icon").hasClass("active")) {
		$("#dl-modal-number").text("(" + String($(".fa-circle.selected").length) + " records selected)");
	} else {
		$("#dl-modal-number").text("(" + String(countNumRecords()) + " records selected)");
	}
});



$(document).on("click touch", "#sort-name", function(e) {
	sortRecords("name");
});



$(document).on("click touch", "#sort-year", function(e) {
	sortRecords("year");
});



$(document).on("click touch", "#sort-semester", function(e) {
	sortRecords("semester");
});



$(document).on("click touch", "#sort-course", function(e) {
	sortRecords("course");
});



$(document).on("click touch", "#sort-eq-id", function(e) {
	sortRecords("eq-id");
});



$(document).on("click touch", "#sort-eq-make", function(e) {
	sortRecords("eq-make");
});



$(document).on("click touch", "#sort-eq-model", function(e) {
	sortRecords("eq-model");
});



$(document).on("click touch", "#sort-eq-name", function(e) {
	sortRecords("eq-name");
});



$(document).on("click touch", ".download-icon", function(e) {
	window.open(siteroot + $(e.target).parent().parent().find(".version-path").attr("href"), "_blank");
});



$(document).on("click touch", "#expand-all-button", function(e) {
	flash($("#records-header"));
	let expanded = $(e.target).attr("expanded");
	if (expanded == "true") {
		toggleRecordExpansion(false);
	} else {
		toggleRecordExpansion(true);
	}
});



$(document).on("click touch", "#show-all-button", function(e) {
	$(e.target).css("visibility", "hidden");
	applyRecordsMask(false);
	falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester"), $("#sort-name")]);
});



$(document).on("click touch", "#staff-name-ernst", function(e) {
	window.open("http://phas.ucalgary.ca/phas_info/profiles/wesley-ernst");
});



$(document).on("click touch", "#staff-name-gimby", function(e) {
	window.open("http://phas.ucalgary.ca/phas_info/profiles/peter-gimby");
});



$(document).on("click touch", "#staff-name-ahmed", function(e) {
	window.open("http://phas.ucalgary.ca/phas_info/profiles/zain-ahmed");
});



$(document).on("mouseenter", ".resource-button", function(e) {
	$(e.target).children(".resource-dropdown").slideDown("fast");
});



$(document).on("mouseleave", ".resource-button", function(e) {
	$(e.target).children(".resource-dropdown").hide();
});



$(document).on("mouseleave", ".resource-dropdown", function(e) {
	if($(e.target).is("p")) {
		$(e.target).parent().parent().hide();
	} else if($(e.target).hasClass(".resource-dropdown-content")) {
		$(e.target).parent().hide();
	} else {
		$(e.target).hide();
	}
});



$(document).on("click touch", ".resource-dropdown-content, .mobile-resource-dropdown-content", function(e) {
	let links = {"pjl-regress": "/",
				 "pjl-lab-schedule": "/data/schedules/schedule-current.pdf",
				 "pjl-rooms-schedule": "/data/schedules/rooms-current.pdf",
				 "pjl-geiger": "/",
				 "pjl-repository": "/repository",
				 "pjl-linearization": "/",
				 "pjl-compare-two": "/",
				 "pjl-uncertainty": "/",
				 "pjl-graphing": "/",
				 "pjl-scint": "/",
				 "pjl-latex-template": "/data/landingpage/templates.zip",
				 "pjl-tikz-examples": "/data/landingpage/tikz-examples.zip",
				 "pjl-inventory":"/staffresources/equipment",
				 "pjl-github":"https://github.com/pgimby/pjl-web",
				 "pjl-lab-rules":"/data/safety/lab-rules/Lab-Rules.pdf",
				 "pjl-rad-safety":"/data/safety/training/Radiation-Safety/Radiation-Safety.pdf",
				 "pjl-orientation":"/data/safety/training/Orientation.pdf",
				 "pjl-hacf-pjl":"/data/safety/HACFs/HACF-PJL.pdf",
				 "pjl-hacf-adv":"/data/safety/HACFs/HACF-TA-ADV.pdf",
				 "pjl-hacf-std":"/data/safety/HACFs/HACF-TA-STD.pdf",
				 "pjl-581":"/data/landingpage/physics581.zip",
				 "pjl-481":"/data/landingpage/physics481.zip",
				 "pjl-381":"/data/landingpage/physics381.zip"};
	let buttonid = $(e.target).attr("id");
	window.location = links[buttonid];
});



$(document).on("click touch", ".video-desc #video-see-more", function() {
	window.location = "http://www.phas.ucalgary.ca/teaching_learning/demonstrations";
});



$(document).on("click touch", ".need-help", function(e) {
	window.location.href = "mailto:pgimby@phas.ucalgary.ca?Subject=PJLWeb%20Bug%20Report";
	e.stopPropagation();
});



$(document).on("click touch", "body", function(e) {
	hideMobileNav();
	e.stopPropagation();
});



$(document).on("click touch", "#mobile-nav-button", function(e) {
	showMobileNav();
	e.stopPropagation();
});



$(document).on("click touch", ".equip-item-primary, .equip-item-alt", function(e) {
	let item = $(e.target);
	let id = item.attr("data-eqid");
	let href = "/staffresources/equipment?id=" + id;
	window.open(href, "_blank");
});



$(document).on("click touch", ".eq-record-flex", function(e) {
	new EquipmentDisplay($(e.target).children(".eq-record-id").text());
});



$(document).on("click touch", "#edit-mode-button", function(e) {
	window.location = "./edit/";
});



$(document).on("click", ".record-click-mask", function(e) {
	if ($(e.target).parent().children(".fa-circle").hasClass("selected")) {
		$(e.target).parent().children(".fa-circle").removeClass("selected");
		selectedRecords(-1);
	} else {
		$(e.target).parent().children(".fa-circle").addClass("selected");
		selectedRecords(1);
	}
})
















//*******************************************************************************************
//   DOM ELEMENT CREATION FUNCTIONS
//*******************************************************************************************



//read XML and append all lab records to DOM; update displayed records counter - not type safe
function populateRecordList(docXML) {
	let labs = docXML.getElementsByTagName("Lab");
	for (let i = labs.length - 1; i >= 0; i--) {
		createRecordSnapshots(labs[i]);
	}
	displayNumResults(countNumRecords());
}



//read XML and populate the HTML select boxes with available filter options - not type safe
function populateFilters(docXML) {
	let types = ["Course", "Year", "Semester", "Discipline", "Topic"];
	for (let i = types.length - 1; i >= 0; i--) {
		let validlist = getValidFilterOptions(docXML, types[i]);
		for (let j = validlist.length - 1; j >= 0; j--) {
			d3.select("#" + types[i].toLowerCase() + "-select")
			  .append("option")
			  .attr("value", validlist[j])
			  .html(validlist[j]);
		}
	}
}



//create and append to DOM an appropriate number of records given an XML "lab" node - not type safe
function createRecordSnapshots(lab) {
	let versionlist = getVersionList(lab);
	for (let i = versionlist.length - 1; i >= 0; i--) {
		let detailsbox = d3.select("#record-list-box").append("div").classed("lab-record-flex", true).classed("record-rendered", true);

		let snapshot = detailsbox.append("div").classed("lab-record-simple-flex", true);
		snapshot.append("i").classed("fa fa-circle", true).attr("aria-hidden", "true");
		let download = snapshot.append("a").classed("version-path", true).html("See PDF").attr("href", siteroot + versionlist[i].path).attr("target", "_blank");
		snapshot.append("img").classed("download-icon", true).html("Download").attr("src", siteroot + "/img/download-icon.svg");  //alternate for mobile display
		let clickmask = snapshot.append("div").classed("record-click-mask", true);
		let course = clickmask.append("p").classed("courses", true).html(versionlist[i].course);
		let date = clickmask.append("p").classed("version-semester", true).html(versionlist[i].semester + " " + versionlist[i].year);
		let labtitle = clickmask.append("p").classed("lab-title", true).html(lab.getElementsByTagName("Name")[0].childNodes[0].nodeValue);
		let dropiconflex = snapshot.append("div").classed("lab-details-drop-icon-flex", true);
		let dropicon = dropiconflex.append("img").classed("lab-details-drop-icon", true).attr("src", siteroot + "/img/dropdown-arrow.png");

		let extendedlabdata = detailsbox.append("div").classed("lab-record-detailed-flex", true).attr("style", "display: none");
		let labid = extendedlabdata.append("p").classed("lab-data-id", true).html("<span>Lab ID:</span> " + getLabId(lab));
		let labtopics = extendedlabdata.append("p").classed("lab-data-topics", true).html("<span>Topics:</span> " + getLabTopicsList(lab).join(", "));
		let labdisciplines = extendedlabdata.append("p").classed("lab-data-disciplines", true).html("<span>Disciplines:</span> " + getLabDisciplinesList(lab).join(", "));
		let labequipment = extendedlabdata.append("div").classed("lab-data-equipment", true);
		getLabEquipmentList(lab, labequipment);

		let software = extendedlabdata.append("p").classed("lab-data-software", true).html("<span>Software:</span> " + getLabSoftwareList(lab).join(", "));
		let directory = extendedlabdata.append("p").classed("version-directory", true).html(versionlist[i].directory).style("display", "none");

		let labdoclist = getExtraLabDocs(lab);
		let labdocs = extendedlabdata.append("div").classed("extra-docs", true);
		labdocs.append("p").html("<span>Additional Documents:</span> ");
		for (let j = labdoclist.length - 1; j >= 0; j--) {
			labdocs.append("a").classed("extra-doc", true).attr("href", labdoclist[j].url).html(labdoclist[j].name).attr("target", "_blank");
		}
	}
}



//appends equipment to the lab equipment div given an XML "lab" node and d3 selection to append to
function getLabEquipmentList(lab, selection) {
	let equipnode = lab.getElementsByTagName("Equipment")[0];
	let items = equipnode.getElementsByTagName("Item");
	selection.append("p").classed("equipment-label", true).html("<span>Equipment: </span>");
	for (let i = items.length - 1; i >= 0; i--) {
		let alt = (Boolean(items[i].getElementsByTagName("Alt")[0]) ? {name: items[i].getElementsByTagName("Alt")[0].childNodes[0].nodeValue, id: items[i].getAttribute("id")} : null);
		let item = {};
		item.name = items[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
		item.id = items[i].getAttribute("id");
		item.amount = items[i].getElementsByTagName("Amount")[0].childNodes[0].nodeValue;
		item.alt = alt;

		let eqitem = selection.append("div").classed("equip-item", true);
		eqitem.append("p").classed("equip-item-primary", true).attr("data-eqid", item.id).html(item.name);
		eqitem.append("p").classed("equip-item-amount", true).html("(" + String(item.amount) + ")");
		if (Boolean(item.alt)) {
			eqitem.append("p").classed("equip-item-alt", true).attr("data-eqid", item.alt.id).html("[" + item.alt.name + "]");
		}
	}
}



//create and append to DOM an appropriate number of records given an XML "lab" node - not type safe
function createEquipRecordSnapshots(xml) {
	let equiplist = xml.getElementsByTagName("Item");
	for (let i = equiplist.length - 1; i >= 0; i--) {
		let eqid = equiplist[i].getAttribute("id");
		let eqname = (equiplist[i].getElementsByTagName("InventoryName")[0].childNodes[0] ? equiplist[i].getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue : "—");
		let eqmake = (equiplist[i].getElementsByTagName("Manufacturer")[0].childNodes[0] ? equiplist[i].getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "—");
		let eqmodel = (equiplist[i].getElementsByTagName("Model")[0].childNodes[0] ? equiplist[i].getElementsByTagName("Model")[0].childNodes[0].nodeValue : "—");

		let snapshot = d3.select("#record-list-box").append("div").classed("eq-record-flex", true).classed("record-rendered", true);
		let id = snapshot.append("p").classed("eq-record-id", true).html(eqid);
		let make = snapshot.append("p").classed("eq-record-make", true).html(eqmake);
		let model = snapshot.append("p").classed("eq-record-model", true).html(eqmodel);
		let name = snapshot.append("p").classed("eq-record-name", true).html(eqname);
		let roomnodes = equiplist[i].getElementsByTagName("Room");
		let rooms = [];
		for (let r = roomnodes.length - 1; r >= 0; r--) {
			rooms.push(roomnodes[r].childNodes[0].nodeValue);
		}
		snapshot.attr("data-rooms", rooms.join());
		let repair = (equiplist[i].getElementsByTagName("UnderRepair")[0].childNodes[0] ? equiplist[i].getElementsByTagName("UnderRepair")[0].childNodes[0].nodeValue : "—");
		snapshot.attr("data-repair", repair);
	}
	applyRecordsMask(true);
	displayNumResults(countNumRecords());
}














//*******************************************************************************************
//   DOM MODIFIER FUNCTIONS
//*******************************************************************************************



//given a filter object, filter displayed records and update DOM appropriately
function filterResults(filter, fullset=true) {
	if (isEquipmentDatabase()) {
		if(fullset) {
			var recordlist = $(".eq-record-flex");
		} else {
			var recordlist = getCurrentRecords();
		}
		let numrecords = recordlist.length;
		for (let i = recordlist.length - 1; i >= 0; i--) {
			let item = $(recordlist[i]);
			let id = item.find(".eq-record-id").text();
			let make = item.find(".eq-record-make").text();
			let rooms = item.attr("data-rooms").split(",");
			let repair = (item.attr("data-repair") == "—" ? -1 : parseFloat(item.attr("data-repair")));

			if (filter["manufacturer-filter"].includes(make) || filter["manufacturer-filter"].length == 0) {
				item.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				item.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}

			if (doArraysOverlap(rooms, filter["room-filter"]) || filter["room-filter"].length == 0) {
				item.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				item.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}

			let repairrange = interpretRepairFilter(filter["repair-filter"]);
			if ((repair >= repairrange[0] && repair < repairrange[1]) || filter["repair-filter"].length == 0) {
				item.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				item.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
		}
	} else {
		if(fullset) {
			var recordlist = $(".lab-record-flex");
		} else {
			var recordlist = getCurrentRecords();
		}
		let numrecords = recordlist.length;
		for (let i = recordlist.length - 1; i >= 0; i--) {
			let lab = $(recordlist[i]);
			let courses = lab.find(".courses").text().split(", ");
			let disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");
			let topics = lab.find(".lab-data-topics").text().slice(8,).split(", ");

			if (filter["year-filter"].includes(lab.find(".version-semester").text().slice(-4)) || filter["year-filter"].length == 0) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			}
			else if (lab.find(".version-semester").text().endsWith("—") && filter["year-filter"].includes("—")) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				lab.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
			if (doArraysOverlap(courses, filter["course-filter"]) || filter["course-filter"].length == 0) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				lab.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
			if (filter["semester-filter"].includes(lab.find(".version-semester").text().slice(0,-5)) || filter["semester-filter"].length == 0) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else if(lab.find(".version-semester").text().startsWith("—") && filter["semester-filter"].includes("—")) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				lab.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
			if (doArraysOverlap(disciplines, filter["discipline-filter"]) || filter["discipline-filter"].length == 0) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				lab.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
			if (doArraysOverlap(topics, filter["topic-filter"]) || filter["topic-filter"].length == 0) {
				lab.removeClass("record-not-rendered masked").addClass("record-rendered");
			} else {
				lab.removeClass("record-rendered masked").addClass("record-not-rendered");
				continue;
			}
		}
		falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name"), $("#sort-course")]);
		$("#record-list-box").removeClass("records-unmasked");
	}
}



//update number of displayed records and zip status
function displayNumResults(numresults) {
	$("#num-results").text(numresults);
	updateZipStatus();
}



//confirm that zipping is available and update the zip icon accordingly
function updateZipStatus() {
	let canzip = canZip()
	if (canzip) {
		$("#zip-icon").css("display", "inline-block");
	} else {
		$("#zip-icon").css("display", "none");
	}
}



//take column header identifier string and sort accordingly - not type safe
function sortRecords(by) {
	let records = getCurrentRecords();
	let recordlistbox = $("#record-list-box");
	for (let i = records.length - 1; i >= 0; i--) {
		records[i].detach();
	}
	switch (by) {
		case "course":
			if ($("#sort-course").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareLabsByCourse);
			}
			truifySort([$("#sort-course")]);
			falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name")]);
			break;
		case "semester":
			if ($("#sort-semester").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareLabsBySemester);
			}
			truifySort([$("#sort-semester")]);
			falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-name")]);
			break;
		case "year":
			if ($("#sort-year").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareLabsByYear);
			}
			truifySort([$("#sort-year")]);
			falsifySort([$("#sort-semester"), $("#sort-course"), $("#sort-name")]);
			break;
		case "name":
			if ($("#sort-name").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareLabsByName);
			}
			truifySort([$("#sort-name")]);
			falsifySort([$("#sort-year"), $("#sort-course"), $("#sort-semester")]);
			break;
		case "eq-id":
			if ($("#sort-eq-id").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareEquipById);
			}
			truifySort([$("#sort-eq-id")]);
			falsifySort([$("#sort-eq-make"), $("#sort-eq-model"), $("#sort-eq-name")]);
			break;
		case "eq-make":
			if ($("#sort-eq-make").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareEquipByMake);
			}
			truifySort([$("#sort-eq-make")]);
			falsifySort([$("#sort-eq-id"), $("#sort-eq-model"), $("#sort-eq-name")]);
			break;
		case "eq-model":
			if ($("#sort-eq-model").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareEquipByModel);
			}
			truifySort([$("#sort-eq-model")]);
			falsifySort([$("#sort-eq-make"), $("#sort-eq-id"), $("#sort-eq-name")]);
			break;
		case "eq-name":
			if ($("#sort-eq-name").attr("sorted") == "true") {
				records.reverse();
			} else {
				records.sort(compareEquipByName);
			}
			truifySort([$("#sort-eq-name")]);
			falsifySort([$("#sort-eq-make"), $("#sort-eq-model"), $("#sort-eq-id")]);
			break;
	}
	for (let i = records.length - 1; i >= 0; i--) {
		if (!recordlistbox.hasClass("records-unmasked")) {
			if (i >= records.length - recordmasklength) {
				records[i].removeClass("masked");
			} else {
				records[i].addClass("masked");
			}
		}
		recordlistbox.append(records[i]);
	}
}



//set these headers' (jQuery selections) attribute "sorted=false" - not type safe
function falsifySort(headers) {
	for (let i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "false")
	}
}



//set these headers' (jQuery selections) attribute "sorted=true" - not type safe
function truifySort(headers) {
	for (let i = headers.length - 1; i >= 0; i--) {
		headers[i].attr("sorted", "true")
	}
}



//expands display if truthy, contracts if falsy - type-safe
function toggleRecordExpansion(truthy) {
	let button = $("#expand-all-button");
	if (Boolean(truthy)) {
		let extendeddatarecords = $(".lab-record-detailed-flex");
		for (let i = extendeddatarecords.length - 1; i >= 0; i--) {
			let record = $(extendeddatarecords[i]).parent();
			if (record.hasClass("record-rendered") && record.filter(".record-rendered").length < 100) {
				$(extendeddatarecords[i]).stop().slideDown()
			} else {
				$(extendeddatarecords[i]).css("display", "flex");
			}
		}
		setExpandedButtonTruth(true)
	} else {
		let extendeddatarecords = $(".lab-record-detailed-flex");
		for (let i = extendeddatarecords.length - 1; i >= 0; i--) {
			let record = $(extendeddatarecords[i]).parent();
			if (record.hasClass("record-rendered") && record.filter(".record-rendered").length < 100) {
				$(extendeddatarecords[i]).stop().slideUp()
			} else {
				$(extendeddatarecords[i]).css("display", "none");
			}
		}
		setExpandedButtonTruth(false)
	}
}



//sets "expand-all-button" expanded=truthy - type safe
function setExpandedButtonTruth(truthy) {
	let button = $("#expand-all-button");
	button.attr("expanded", String(Boolean(truthy)));
	if (Boolean(truthy)) {
		button.html("collapse all");
	} else {
		button.html("expand all");
	}
}



//Apply the records mask if 'truthy' is true, remove the mask if false
function applyRecordsMask(truthy) {
	let records = getCurrentRecords();
	unmaskAll(records);
	if (records.length > recordmasklength && Boolean(truthy)) {
		for (let i = records.length - 1; i >= recordmasklength; i--) {
			records[i].addClass("masked");
		}
		$("#num-unmasked-results").text(String(recordmasklength));
		$("#show-all-button").css("visibility", "visible");
	} else {
		for (let i = records.length - 1; i >= 0; i--) {
			records[i].removeClass("masked");
		}
		$("#num-unmasked-results").text(String(records.length));
		$("#show-all-button").css("visibility", "hidden");
	}
	//Reset all the record headers to their unsorted state
	falsifySort([$("#sort-year"), $("#sort-semester"), $("#sort-name"), $("#sort-course")]);
	$("#record-list-box").addClass("records-unmasked");
	if (Boolean(truthy)) {
		$("#record-list-box").removeClass("records-unmasked");
	}
	selectedRecords(0);
}



//Unmask all the records.
function unmaskAll(records) {
	$("#record-list-box").addClass("records-unmasked");
	for (let i = records.length - 1; i >= 0; i--) {
		records[i].removeClass("masked");
	}
	$("#show-all-button").css("visibility", "hidden");
}



//Counts the number of unmasked records and updates the 'Showing X of XXX total records' string on the page
function setNumberRecordsUnmasked() {
	let records = getCurrentRecords();
	let num = records.length;
	for (let i = records.length - 1; i >= 0; i--) {
		if (records[i].hasClass("masked")) {
			num--;
		}
	}
	$("#num-unmasked-results").html(String(num));
}



//filter the records by showing only those from the most recent semester and year.
function showMostRecent() {
	let uniquelabs = [];
	let records = getCurrentRecords();
	unmaskAll(records);
	setNumberRecordsUnmasked();

	//build a set ('set', meaning list without duplicate entries) of lab IDs.
	//Since we're here, we'll un-render all the records as well
	for (let i = records.length - 1; i >= 0; i--) {
		let labid = records[i].find(".lab-data-id").text().slice(-4,);
		if(!uniquelabs.includes(labid)) {
			uniquelabs.push(labid);
		}
		records[i].removeClass("record-rendered").addClass("record-not-rendered");
	}

	//go through the labs by ID and render their most recent version along with recent versions of the same lab from different courses
	for (let i = uniquelabs.length - 1; i >= 0; i--) {
		let year = 0;
		let mostrecent = null;
		let sameyeardifcourse = [];
		for (let j = records.length - 1; j >= 0; j--) {
			if (records[j].find(".lab-data-id").text().slice(-4,) == uniquelabs[i]) {
				let recordsemester = records[j].find(".version-semester").text();
				let date = parseFloat(recordsemester.split(" ")[1]) + parseFloat(semesterDecimal[recordsemester.split(" ")[0]]);
				if (date > year) {
					mostrecent = records[j];
					year = date;
					sameyeardifcourse = [];
				} else if(date == year) {
					sameyeardifcourse.push(records[j])
					year = date;
				}
				if(!mostrecent && recordsemester.split(" ")[1] == "—") {
					mostrecent = records[j];
				}
			}
		}
		if(mostrecent) {
			mostrecent.removeClass("record-not-rendered").addClass("record-rendered");
			for (let j = sameyeardifcourse.length - 1; j >= 0; j--) {
				sameyeardifcourse[j].removeClass("record-not-rendered").addClass("record-rendered");
			}
		}
	}
	sortRecords("year");
	displayNumResults(countNumRecords());
	setNumberRecordsUnmasked();
	selectedRecords(0);
}



//Populate the filters with appropriate values found in equipment XML
function populateEquipmentFilters(xml) {
	let manufacturers = new Set(["—"]);
	let rooms = new Set([]);
	let mannodes = xml.getElementsByTagName("Manufacturer");
	let roomnodes = xml.getElementsByTagName("Room");

	for (let i = mannodes.length - 1; i >= 0; i--) {
		manufacturers.add((mannodes[i].childNodes[0] ? mannodes[i].childNodes[0].nodeValue : "—"));
	}

	for (let i = roomnodes.length - 1; i >= 0; i--) {
		rooms.add((roomnodes[i].childNodes[0] ? roomnodes[i].childNodes[0].nodeValue : "—"));
	}

	manufacturers = Array.from(manufacturers);
	rooms = Array.from(rooms);
	let manlist = d3.select("#manufacturer-select");
	let roomlist = d3.select("#room-select");

	for (let i = manufacturers.length - 1; i >= 0; i--) {
		manlist.append("option").attr("value", manufacturers[i]).html(manufacturers[i]);
	}

	for (let i = rooms.length - 1; i >= 0; i--) {
		roomlist.append("option").attr("value", rooms[i]).html(rooms[i]);
	}
}



//Show the mobile Nav if not already displayed
function showMobileNav() {
	if($(".mobile-landing-nav").css("display") == "none") {
		$(".mobile-landing-nav").show("slide", {direction: "left"}, 300);
	}
}



//Hide the mobile nav if it is currently displayed
function hideMobileNav() {
	if($(".mobile-landing-nav").css("display") == "block") {
		$(".mobile-landing-nav").hide("slide", {direction: "left"}, 300);
	}
}


















//*******************************************************************************************
//   SEARCH-RELATED FUNCTIONS (USING SORENSEN-DICE SIMILARITY)
//*******************************************************************************************



//take query and search-selector and make yes/no decisions on what records to include; display accordingly
function generateSearchResults(query, selector) {
	let minsimilarity = 0.4;
	let querybigrams = makeBigramList(query);
	let recordlist = getAllRecords();
	let skipsim = ("id" == selector ? true : false);

	if (isEquipmentDatabase()) {
		for (let i = recordlist.length - 1; i >= 0; i--) {
			recordlist[i].removeClass("record-not-rendered masked").addClass("record-rendered");
			let similarity = compareQueryWithEquipRecord(querybigrams, recordlist[i]);
			if (similarity < .9) {
				recordlist[i].removeClass("record-rendered").addClass("record-not-rendered");
			}
		}
	} else {
		for (let i = recordlist.length - 1; i >= 0; i--) {
			recordlist[i].removeClass("record-not-rendered masked").addClass("record-rendered");
			let similarity = (skipsim ? 0.0 : compareQueryWithLabRecord(querybigrams, recordlist[i], selector));
			if (similarity < minsimilarity && !queryLiteralInLabRecord(query, recordlist[i], selector)) {
				recordlist[i].removeClass("record-rendered").addClass("record-not-rendered");
			}
		}
	}
}



//Given a selector, return true if the search query can be found exactly in a record
function queryLiteralInLabRecord(query, lab, selector) {
	let courses = lab.find(".courses").text().toLowerCase();
	let disciplines = lab.find(".lab-data-disciplines").text().slice(13,).toLowerCase();
	let topics = lab.find(".lab-data-topics").text().slice(8,).toLowerCase();
	let equipment = lab.find(".lab-data-equipment").text().slice(11,).toLowerCase();
	let semester = lab.find(".version-semester").text().split(" ")[0].toLowerCase();
	let year = lab.find(".version-semester").text().split(" ")[1].toLowerCase();
	let labtitle = lab.find(".lab-title").text().toLowerCase();
	let id = lab.find(".lab-data-id").text().slice(-4,).toLowerCase();
	switch (selector) {
		case "all":
			return courses.includes(query) || disciplines.includes(query) || topics.includes(query) || equipment.includes(query) || semester.includes(query) || year.includes(query) || labtitle.includes(query);
			break;
		case "course":
			return courses.includes(query);
			break;
		case "lab":
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
		case "id":
			return id == query;
			break;
	}
}



//make bigram sets for appropriate meta data of record and perform SDC comparison with search query; return best score - super not type safe
function compareQueryWithLabRecord(querybigrams, lab, selector) {
	let courses = lab.find(".courses").text().split(", ");
	let disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");
	let topics = lab.find(".lab-data-topics").text().slice(8,).split(", ");
	let equipment = lab.find(".lab-data-equipment").text().slice(11,).split(", ");
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
	let semester = [makeBigramList(lab.find(".version-semester").text().split(" ")[0])];
	let year = [makeBigramList(lab.find(".version-semester").text().split(" ")[1].slice(2,))];
	let labtitle = [makeBigramList(lab.find(".lab-title").text())];
	let totest = [""];
	switch (selector) {
		case "all":
			totest = disciplines.concat(courses, semester, year, labtitle, topics, equipment);
			break;
		case "course":
			totest = courses;
			break;
		case "lab":
			totest = labtitle;
			break;
		case "year":
			totest = year;
			break;
		case "semester":
			totest = semester;
			break;
		case "topic":
			totest = topics;
			break;
		case "discipline":
			totest = disciplines;
			break;
		case "equipment":
			totest = equipment;
			break;
	}

	let max = 0.0;
	for (let i = totest.length - 1; i >= 0; i--) {
		let result = sorensenDiceCoef(querybigrams, totest[i]);
		if (result > max) {
			max = result
		}
	}
	return max;
}


//Returns Sorensen-Dice coefficient comparing equipment name with a search query
function compareQueryWithEquipRecord(querybigrams, eqitem) {
	let name = eqitem.find(".eq-record-name").html();
	let recordbigrams = makeBigramList(name);
	return sorensenDiceCoef(recordbigrams, querybigrams);
}



//calculate Sorensen-Dice Coefficient for two sets (arrays) of bigrams - not type safe
function sorensenDiceCoef(bigrams1, bigrams2) {
	let count = 0;
	$.each(bigrams1, function(i, d) {
		if (bigrams2.includes(d)) {
			count++;
		}
	});
	return 2*count / (bigrams1.length + bigrams2.length);
}



//This is the top of the search stream, pulling raw query right from the search bar.
//Handle search request by checking for search selectors and pass along the appropriate branch.
function searchQueryHandler() {
	let query = $("#search-bar").val();
	let split = query.split(":");
	let selector = split[0].trim();
	let searchphrase = split.slice(1,).join(" ").trim();
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
		case "id":
			idSearchHandler(searchphrase);
			break;
		default:
			defaultSearchHandler(query);
	}
}



//handle a non-selected search request - not type safe
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
			// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
			generateSearchResults(searchphrase, "all");
			displayNumResults(countNumRecords());
	 		//$("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
	}
}



//handle the search request for course search selector - not type safe
function courseSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "course");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for lab name search selector - not type safe
function labSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "lab");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for year search selector - not type safe
function yearSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "year");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for semester search selector - not type safe
function semesterSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "semester");
	displayNumResults(countNumRecords());
	 // $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for topic search selector - not type safe
function topicSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "topic");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for discipline search selector - not type safe
function disciplineSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "discipline");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for equipment search selector - not type safe
function equipmentSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "equipment");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



//handle the search request for id search selector - not type safe
function idSearchHandler(searchphrase) {
	// $('html, body').animate({scrollTop: ($('#record-list-box').offset().top)}, 500);  //UNCOMMENT TO SCROLL DOWN TO SEARCH RESULTS AFTER SEARCH
	generateSearchResults(searchphrase, "id");
	displayNumResults(countNumRecords());
	// $("#search-bar").val("");  //UNCOMMENT TO CLEAR SEARCH BAR AFTER SEARCH
}



















//*******************************************************************************************
//   ZIP-RELATED FUNCTIONS
//*******************************************************************************************


//Given a list of file paths, download them, zip them, and serve them to the user.
function makePromisesBeginZip(filelist) {
	let zip = new JSZip();
	let files = filelist;
	let promises = [];
	let xhrs = [];


	//this callback runs whenever a file is successfully retreived. It updates the progress bar.
	function increaseProgress() {
		return function() {
			let currentval = parseFloat($("#zip-progress-bar progress").attr("value"));
			let newval = currentval + (1/files.length);
			$("#zip-progress-bar progress").attr("value", newval.toFixed(3));
		}
	}

	//Start the file download and make associated promises.
	//Also save the list of XHRs
	for (let i = files.length - 1; i >= 0; i--) {
		let downloadingfile = new $.Deferred();
		downloadingfile.done(function(filename, blob) {
			zip.file(filename, blob);
		}, increaseProgress());
		let xhr = beginDownload(files[i], downloadingfile);
		promises.push(downloadingfile);
		xhrs.push(xhr);
	}

	deferredzip = $.when.apply($, promises);

	//if the file download succeeds, serve the zipped file to the user
	deferredzip.done(function() {
		let today = new Date();
		let zipoutputfilename = "PJL_"+ String(today.getHours()%12).padStart(2, '0') + "-" + String(today.getMinutes()).padStart(2, '0') + ".zip";
		zip.generateAsync({type:"blob"}).then(function (blob) {
			//'saveAs' is a FileSaver.js function
			saveAs(blob, zipoutputfilename);
			$("#zip-progress-bar progress").attr("value", "0");
			$("#zip-progress-bar").stop().slideUp(500);
		});
		return false;
	});

	//if the file download fails, close the zip progress bar and continue on
	deferredzip.fail(function() {
		setTimeout(function() {
			$("#file-prep").text("Download failed.");
			setTimeout(function() {
				console.log("zip failed or cancelled");
				$("#zip-progress-bar progress").attr("value", "0");
				$("#zip-progress-bar").stop().slideUp(500, function() {
				$("#file-prep").text("Preparing files...");
				});
			}, 2000);
		}, 700);
	});

	//if the close is clicked on the docnload progress bar, abort XHRs and reject associate promises.
	//The promise fail callbacks will take care of the rest..
	$(document).on("click", "#cancel-download", function(e) {
		for (let i = xhrs.length - 1; i >= 0; i--) {
			xhrs[i].abort();
			promises[i].reject();
		}
		$("#zip-progress-bar progress").attr("value", "0");
		$("#zip-progress-bar").stop().slideUp(500);
		$(document).off("click", "#cancel-download");
		return;
	});
}



//start downloading and resolve associated promise upon completion (or failure) - not type safe
//return XML HTTP request object
function beginDownload(filepath, promise) {
	var xhttp = new XMLHttpRequest();
	xhttp.responseType = "blob";
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
            blob = this.response;
            //get the filename from the path
            var filename = filepath.split("/");
            filename = filename[filename.length-1];
            // promise.notify(); //this line might be dead code - TOTEST
            //'filename' and 'blob' are passed as arguments to the resolved callback (see 'downloadingfile' promise in 'makePromisesBeginZip')
            promise.resolve(filename, blob);
    	} else if(this.status == 404) {
    		promise.reject();
    	} else if (this.status == 403) {
    		promise.reject();
    	}
  	};
  	xhttp.open("GET", siteroot + filepath, true);
  	xhttp.send();
  	return xhttp;
}



//The top of the zipping process. Get all lab directories and collect their file contents to be passed to JSZip for zipping and serving to user.
function collectFiles2Zip(doALL, doPDF, doTEX, doTMP, doMED, doEXTRA) {
	let dirlist = [];
	let filelist = [];
	let promises = [];
	let extradocs = [];
	let records = getCurrentRecords();

	//callback to be run when PHP returns a list of contents for a given directory (when its promise is resolved)
	function fileCallback(promise) {
		return function(d) {
			console.log(d)
			filelist = filelist.concat(d.split(","));
			promise.resolve();
		}
	}

	//Compile directory lists to be sniffed. Concurrently compile a list of extra documents from the corresponding lab record.
	//First checks for a user sub selection of records. If no sub selection then it collects all rendered records.
	if ($("#zip-icon").hasClass("active")) {
		for (let i = records.length - 1; i >= 0; i--) {
			if (records[i].children(".lab-record-simple-flex").children(".fa-circle").hasClass("selected")) {
				dirlist.push(records[i].find(".version-directory").text());
				extradocs.concat(getExtraDocsFromRecord(records[i]));
			}
		}
	} else {
		for (let i = records.length - 1; i >= 0; i--) {
			dirlist.push(records[i].find(".version-directory").text());
			extradocs.concat(getExtraDocsFromRecord(records[i]));
		}
	}


	//Create a promise for each directory to be resolved when PHP successfully returns a file list representing the contents of the directory
	for (let i = dirlist.length - 1; i >= 0; i--) {
		let promise = $.Deferred();
		promises.push(promise);
		$.post(siteroot + "/php/getFileListRecursive.php", "dirpath=" + dirlist[i], fileCallback(promise));
	}

	//create a new promise to be resolved when all other promises are resolved
	let deferredFileList = $.when.apply($, promises);

	//when PHP has finished sniffing all the files inside the directories and returned the file lists 'deferredFileList' is resolved
	deferredFileList.done(function() {
		filteredlist = filterFileList(doALL, doPDF, doTEX, doTMP, doMED, filelist);
		if(doEXTRA || doALL) {
			filteredlist.concat(extradocs);
		}
		makePromisesBeginZip(filteredlist);
		console.log("An elegant syntax for ease of use,\neasy reading. Not abstruse.\n\nHaving this would sure be swell.\nPHP can rot in hell.")
	});

	//There is no graceful way to bail from this from a website functionality perspective.
	//If this promise fails the website should be considered broken so a simple console log is printed.
	deferredFileList.fail(function() {console.log("File collection failed: Unable to locate files for selection.")});
}


//Take an array of file paths and filter it according to boolean arguments. Return filtered list
function filterFileList(doALL, doPDF, doTEX, doTMP, doMED, filelist) {
	//if 'Everything' options selected then return the whole, unfiltered list.
	if (doALL) {
		return filelist;
	}
	let filteredfiles = [];
	for (let i = filelist.length - 1; i >= 0; i--) {
		if(!filelist[i].startsWith("/data/")) {
			continue;
		}
		if (filelist[i].endsWith(".pdf") && doPDF) {
			filteredfiles.push(filelist[i]);
			continue;
		}
		if (filelist[i].endsWith(".tex") && doTEX) {
			filteredfiles.push(filelist[i]);
			continue;
		}
		if ((filelist[i].endsWith(".txt") || filelist[i].endsWith(".dat") || filelist[i].endsWith(".xml") || filelist[i].endsWith(".xlsx") || filelist[i].endsWith(".ods") || filelist[i].endsWith(".csv") || filelist[i].endsWith(".tsv") || filelist[i].endsWith(".cmbl")) && doTMP) {
			filteredfiles.push(filelist[i]);
			continue;
		}
		if ((filelist[i].endsWith(".png") || filelist[i].endsWith(".jpg") || filelist[i].endsWith(".jpeg") || filelist[i].endsWith(".gif") || filelist[i].endsWith(".tiff") || filelist[i].endsWith(".mp4") || filelist[i].endsWith(".avi") || filelist[i].endsWith(".dv")) && doMED) {
			filteredfiles.push(filelist[i]);
			continue;
		}
	}
	return filteredfiles;
}



//record is an HTML DOM element. Returns a list of dictionaries holding information about a lab's extra documents
function getExtraDocsFromRecord(record) {
	let docs = $(record).children(".extra-docs").children(".extra-doc");
	list = [];
	for (let i = docs.length - 1; i >= 0; i--) {
		let docname = docs[i].text();
		let docpath = docs[i].attr("href");
		list.push({name: docname, url: docpath});
	}
	return list;
}



//adds a class 'active' to the #zip-icon so it knows to download only the user-selected subset of records
function zipSome(truthy) {
	if (Boolean(truthy)) {
		$("#zip-icon").addClass("active");
	} else {
		$("#zip-icon").removeClass("active");
	}
}













//*******************************************************************************************
//   GENERAL FUNCTIONS
//*******************************************************************************************



//load the XML document holding all the lab records and pass it along to callbacks
function loadXML() {
	let xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            populateRecordList(docXML);
            populateFilters(docXML);
            applyRecordsMask(true);
    	}
  	};
  	xhttp.open("GET", siteroot + labdatabasepath, true);
  	xhttp.send();
}



//the repair backlog filter has strings indicating ranges of backlog.
//This function maps them to a numerical range in the form of an array.
function interpretRepairFilter(value) {
	switch (value) {
		case "0":
			return [0,0.1];
		case "1-2":
			return [1,2];
		case "3-5":
			return [3,5];
		case ">5":
			return [5,9999];
		default:
			return [0,9999];
	}
}



//return boolean for ability to zip currently displayed records
function canZip() {
	let bool = false;
	if (countNumRecords() > 0 && JSZip.support.blob) {
		bool = true
	}
	return bool;
}



//returns currently displayed lab records as array of jQuery objects
//Finds rendered records even if they're masked. Masked records are records that are unmasked by the 'show all' button.
//Records classed with 'record-not-rendered' remain in the DOM but are not rendered because they have been excluded by a user search or filter.
function getCurrentRecords() {
	let list = [];
	if (isEquipmentDatabase()) {
		let eqlist = $(".eq-record-flex");
		for (let i = eqlist.length - 1; i >= 0; i--) {
			if($(eqlist[i]).hasClass("record-rendered")) {
				list.push($(eqlist[i]));
			}
		}
	} else {
		let lablist = $(".lab-record-flex");
		for (let i = lablist.length - 1; i >= 0; i--) {
			if ($(lablist[i]).hasClass("record-rendered")) {
				list.push($(lablist[i]));
			}
		}
	}
	return list;
}



//returns all lab records as array of jQuery objects
//This function is reusable for both equipment inventory page and lab repo page
function getAllRecords() {
	var list = [];
	if (isEquipmentDatabase()) {
		let eqlist = $(".eq-record-flex");
		for (let i = eqlist.length - 1; i >= 0; i--) {
			list.push($(eqlist[i]));
		}
	} else {
		let lablist = $(".lab-record-flex");
		for (let i = lablist.length - 1; i >= 0; i--) {
			list.push($(lablist[i]));
		}
	}
	return list;
}



//return the number of currently displayed records
function countNumRecords() {
	let currentrecords = getCurrentRecords();
	return currentrecords.length;
}



//return a filter object of currently activated filters
function getCurrentFilter() {
	let selects = $("select");
	let filter = {};
	for (let i = selects.length - 1; i >= 0; i--) {
		if (selects[i].value) {
			filter[$(selects[i]).parent().attr("id")] = $(selects[i]).val();
		} else {
			filter[$(selects[i]).parent().attr("id")] = [];
		}
	}
	return filter;
}



//return lab ID as a string for an XML "lab" node - not type safe
function getLabId(lab) {
	return lab.getAttribute("labId");
}



function mayISeeYourSillyWalk() {  //I'd like to apply for a government grant to develop my silly walk
	let itsnotparticularlysillyisit = "The right leg isn't silly at all and the left leg merely does a forward aerial half turn every alternate step.";
	$(".search-icon").attr("src","/img/silly-walk.png");
	$(".search-icon").css({height: "45px", width: "35px", top: "-49px", right: "-35px"})
	$("#search-bar").attr("placeholder", itsnotparticularlysillyisit);
	$("#search-bar").css("font-size", "11px");
	$("#search-bar").val("");
	setTimeout(function() {
		$(".search-icon").attr("src","/img/search-icon.png");
		$(".search-icon").css({height: "40px", width: "40px", top: "-45px", right: "-35px"})
		$("#search-bar").attr("placeholder", "Keyword, topic, course...");
		$("#search-bar").css("font-size", "1rem");
		$("#search-bar").val("");
	}, 6000);

}



//return an array of topics (strings) for an XML "lab" node - not type safe
function getLabTopicsList(lab) {
	let list = [];
	let topics = lab.getElementsByTagName("Topic");
	for (let i = topics.length - 1; i >= 0; i--) {
		list.push(topics[i].childNodes[0].nodeValue);
	}
	return list;
}



//return an array of disciplines (strings) for an XML "lab" node - not type safe
function getLabDisciplinesList(lab) {
	let list = [];
	let disciplines = lab.getElementsByTagName("Discipline");
	for (let i = disciplines.length - 1; i >= 0; i--) {
		list.push(disciplines[i].childNodes[0].nodeValue);
	}
	return list;
}



//return an array of software (strings) for an XML "lab" node - not type safe
function getLabSoftwareList(lab) {
	let list = [];
	let software = lab.getElementsByTagName("Software")[0];
	let names = software.getElementsByTagName("Name");
	for (let i = names.length - 1; i >= 0; i--) {
		list.push(names[i].childNodes[0].nodeValue);
	}
	return list;
}



//return an array of extra doc objects for an XML "lab" node - not type safe
function getExtraLabDocs(lab) {
	let list = [];
	let docs = lab.getElementsByTagName("Doc");
	for (let i = docs.length - 1; i >= 0; i--) {
		let docname = docs[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
		let docpath = docs[i].getElementsByTagName("Path")[0].childNodes[0].nodeValue;
		list.push({name: docname, url: docpath});
	}
	return list;
}



function iCameHereForAnArgument() {  //Oh, I'm sorry, this is abuse...
	let i = 0;
	$(".search-icon").attr("src","/img/silly-walk.png");
	$(".search-icon").css({height: "45px", width: "35px", top: "-49px", right: "-35px"});
	$("#search-bar").val("");
	let id = setInterval(function() {
		if (i == montyargument.length - 1) {
			clearInterval(id);
			$(".search-icon").attr("src","/img/search-icon.png");
			$(".search-icon").css({height: "40px", width: "40px", top: "-45px", right: "-35px"});
			$("#search-bar").val("");
			$("#search-bar").attr("placeholder", "Keyword, topic, course...");
			return;
		}
		$("#search-bar").attr("placeholder", montyargument[i]);
		i++;
	}, 1000);
}



//return an array of version objects for a given XML "lab" node
function getVersionList(lab) {
	let versionlist = [];
	let versions = lab.getElementsByTagName("Version");
	for (let i = versions.length - 1; i >= 0; i--) {
		let p = versions[i].getElementsByTagName("Path")[0];
		let y = versions[i].getElementsByTagName("Year")[0];
		let s = versions[i].getElementsByTagName("Semester")[0];
		let c = versions[i].getElementsByTagName("Course")[0];
		let d = versions[i].getElementsByTagName("Directory")[0];
		versionlist.push({path: (Boolean(p.childNodes[0]) ? p.childNodes[0].nodeValue : "—"),
						  semester: (Boolean(s.childNodes[0]) ? s.childNodes[0].nodeValue : "—"),
						  year: (Boolean(y.childNodes[0]) ? y.childNodes[0].nodeValue : "—"),
						  course: (Boolean(c.childNodes[0]) ? c.childNodes[0].nodeValue : "—"),
						  directory: (Boolean(d.childNodes[0]) ? d.childNodes[0].nodeValue : null)});
	}
	return versionlist;
}



//PETER WROTE THIS ONE
//return the set of values available for filtering on a given filter type as an array - not type safe
function getValidFilterOptions(docXML, type) {
	let nodes = docXML.getElementsByTagName(type);
    let valueslist = [];
    for (let i = nodes.length - 1; i >= 0; i--) {
	    valueslist.push(nodes[i].childNodes[0] ? nodes[i].childNodes[0].nodeValue : "—");
    }
    return Array.from(new Set(valueslist)).sort();
}



//return currently displayed lab document paths as a list of strings
function getCurrentRecordPaths() {
	let paths = [];
	let records = getCurrentRecords();
	for (let i = records.length - 1; i >= 0; i--) {
		paths.push(records[i].find(".version-path").attr("href"));
	}
	return paths;
}



//comparison function for Array.prototype.sort on lab course of jQuery ".lab-record-flex" selection - not type safe
function compareLabsByCourse(a, b) {
	a = a.find(".courses").text().split(", ")[0];
	b = b.find(".courses").text().split(", ")[0];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//comparison function for Array.prototype.sort on lab semester of jQuery ".lab-record-flex" selection - not type safe
function compareLabsBySemester(a, b) {
	a = a.find(".version-semester").text().split(" ")[0];
	b = b.find(".version-semester").text().split(" ")[0];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//comparison function for Array.prototype.sort on lab year of jQuery ".lab-record-flex" selection - not type safe
function compareLabsByYear(a, b) {
	a = a.find(".version-semester").text().split(" ")[1];
	b = b.find(".version-semester").text().split(" ")[1];
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//comparison function for Array.prototype.sort on lab name of jQuery ".lab-record-flex" selection - not type safe
function compareLabsByName(a, b) {
	a = a.find(".lab-title").text().toLowerCase();
	b = b.find(".lab-title").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//sorting comparison function that takes two '.eq-record-flex' selections and compares them by id number
function compareEquipById(a, b) {
	a = a.find(".eq-record-id").text().toLowerCase();
	b = b.find(".eq-record-id").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//sorting comparison function that takes two '.eq-record-flex' selections and compares them by manufacturer
function compareEquipByMake(a, b) {
	a = a.find(".eq-record-make").text().toLowerCase();
	b = b.find(".eq-record-make").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//sorting comparison function that takes two '.eq-record-flex' selections and compares them by model
function compareEquipByModel(a, b) {
	a = a.find(".eq-record-model").text().toLowerCase();
	b = b.find(".eq-record-model").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}



//sorting comparison function that takes two '.eq-record-flex' selections and compares them by name
function compareEquipByName(a, b) {
	a = a.find(".eq-record-name").text().toLowerCase();
	b = b.find(".eq-record-name").text().toLowerCase();
	if (a < b) {
		return -1;
	}
	if (b < a) {
		return 1;
	}
	return 0;
}


//given a jQuery selection, this function will animate a flash effect on it for major style points.
function flash(jqitem) {
	jqitem.css("opacity", ".8");
	jqitem.stop().animate({opacity: 1}, 600);
}



//Takes the equipment xml and populates the data-list associated with the search bar so that autocomplete has a list of equipment names to match against
function enableEquipmentSearchAutoComplete(xml) {
	let namenodes = xml.getElementsByTagName("InventoryName");
	let datalist = d3.select("#equipment-datalist");
	let names = [];
	for (let i = namenodes.length - 1; i >= 0; i--) {
		datalist.append("option").attr("value", (namenodes[i].childNodes[0] ? namenodes[i].childNodes[0].nodeValue : "—"));
	}
}



//whenever the equipment inventory page is loaded this function checks the URL for a query string holding an ID number.
//For example, http://www.pjl.ucalgary.ca/staffresources/equipment/?id=0003
//If an ID is found it will load the page with an equipment display for that item.
function equipmentPageQueryString() {
	let url = window.location.href.split("?");
	let queryobj = {};
	if (url.length > 1) {
		let query = url[1].split("&");
		for (let i = query.length - 1; i >= 0 ; i--) {
			let param = query[i].split("=");
			queryobj[param[0]] = param[1];
		}
		if (queryobj.id) {
			new EquipmentDisplay(queryobj.id);
		}
	}
}



//this is a great pattern for re-using a 'loadXML'-type function.
//Any number of arguments may be passed as long as they are functions (not function calls) which take an xmlDoc as an argument.
//When the document successfully loads, each function is called and passed 'docXML' as an argument.
function loadEquipmentXML() {
	let args = arguments;
	let xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            for (let i = args.length - 1; i >= 0; i--) {
            	args[i](docXML);
            }
    	}
  	};
  	xhttp.open("GET", siteroot + "/data/equipmentDB.xml", true);
  	xhttp.send();
}



//increments (1), decrements (-1), or resets (0) the selectedrecords variable to keep track of the number of user-selected records.
function selectedRecords(amount) {
	if (amount == -1) {
		selectedrecords = selectedrecords + amount;
	} else if (amount == 1) {
		selectedrecords = selectedrecords + amount;
	} else if (amount == 0) {
		selectedrecords = 0;
		$(".lab-record-simple-flex .fa-circle").removeClass("selected");
	}
	if (selectedrecords == 0) {
		zipSome(false);
	} else {
		zipSome(true);
	}
}












//*******************************************************************************************
//   CONVENIENCE FUNCTIONS
//*******************************************************************************************



//determines if two arrays share any entries - not type safe
function doArraysOverlap(array1, array2) {
	return array1.some(x => array2.includes(x));
}


//Uses the HTML 'title' tag to determine if the current page is the lab repo or the equipment inventory.
//Allows for reusability of some functions
function isEquipmentDatabase() {
	return (document.title == "Physics Junior Laboratory - Equipment Database" ? true : false);
}



//Map a plain English semester string to a year decimal for comparison of most recent lab versions
var semesterDecimal = {"Fall": 0.75, "Winter": 0.0, "Spring": 0.25, "Summer": 0.50};



//takes a string and returns an array of bigrams - not type safe
function makeBigramList(string) {
	let list = [];
	string = string.toLowerCase();
	for (let i = 0; i < string.length - 1; i++) {
		list.push(string[i] + string[i+1]);
	}
	return Array.from(new Set(list));
}



//calculates arithmetic mean of and array of numbers - not type safe
function arithmeticMean(list) {
	return list.reduce((a, b) => a + b, 0) / list.length;
}



//checks if string is empty - not type safe
function isEmptyString(string) {
	return !string.replace(/\s/g, '').length;
}



//Gets the most recent semester as a decimal date
//For example, December returns 1.0 and April returns 0.25
function mostRecentDecimalSemester() {
	let date = new Date();
	return Math.round(date.getMonth() / 3) / 4;
}

