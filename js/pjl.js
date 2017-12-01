

//*******************************************************************************************
//   GLOBALS
//*******************************************************************************************

var mainxmlpath = "/data/labDB.xml";
var equipmentdatabasepath = "/data/equipmentDB.xml";
var zipoutputfilename = "PJL-lab-docs.zip";
var siteroot = "";
// var docXML;

// Do __NOT__ change classes or ids without checking jQuery and D3 selectors in the JS code

//I wouldn't mind adding a "show more" or "show all" button at the bottom of the record list
//or maybe have a scroll box of a specific size. When we load all the labs from the final XML
//the initial length will be huge and you'll have to scroll forever to get to the footer. - Donesies

//Also would like to have the zip, expand all, maybe search bar pinned to the top while scrolling
//down through the list along with a "back to top" button.


//Somehow need to deal with file errors in the zip call. Think about how to bail gracefully.
//The top-level promise is waiting for all the files to load, what happens if one doesn't?
//---set a deferred.fail() callback on the top-level promise. easy peasy. - Donesies







//*******************************************************************************************
//   PAGE INITIALIZATION
//*******************************************************************************************



function initRepoPage() {  //initialize the repository page
	loadXML();
	$("#search-bar").val("");
	// $(".dl-modal").slimScroll({
	//     position: 'left',
	//     height: 'auto',
	//     railVisible: true,
	//     alwaysVisible: false
	// });
}



function initLandingPage() {
	console.log("landing page initalized")
}


function initEquipmentModPage() {
	loadEquipmentXML(populateEquipDisplay);
}

function initEquipmentPage() {
	equipmentPageQueryString();
	loadEquipmentXML(enableEquipmentSearchAutoComplete, populateEquipmentFilters, createEquipRecordSnapshots);
}


function enableEquipmentSearchAutoComplete(xml) {
	let namenodes = xml.getElementsByTagName("InventoryName");
	let datalist = d3.select("#equipment-datalist");
	let names = [];
	for (let i = 0; i < namenodes.length; i++) {
		datalist.append("option").attr("value", (namenodes[i].childNodes[0] ? namenodes[i].childNodes[0].nodeValue : "—"));
	}
}


function populateEquipmentFilters(xml) {
	let manufacturers = new Set(["—"]);
	let rooms = new Set(["—"]);
	let mannodes = xml.getElementsByTagName("Manufacturer");
	let roomnodes = xml.getElementsByTagName("Room");
	for (let i = 0; i < mannodes.length; i++) {
		manufacturers.add((mannodes[i].childNodes[0] ? mannodes[i].childNodes[0].nodeValue : "—"));
	}
	for (let i = 0; i < roomnodes.length; i++) {
		rooms.add((roomnodes[i].childNodes[0] ? roomnodes[i].childNodes[0].nodeValue : "—"));
	}

	let manlist = d3.select("#manufacturer-select");
	let roomlist = d3.select("#room-select");
	for (let item of manufacturers) {
		manlist.append("option").attr("value", item).html(item);
	}
	for (let item of rooms) {
		roomlist.append("option").attr("value", item).html(item);
	}
}


function equipmentPageQueryString() {
	let url = window.location.href.split("?");
	let queryobj = {};
	if (url.length > 1) {
		var query = url[1].split("&");
		for (let i = 0; i < query.length; i++) {
			let param = query[i].split("=");
			queryobj[param[0]] = param[1];
		}
		if (queryobj.id) {
			new EquipmentDisplay(queryobj.id);
		}
	}
}



function loadEquipmentXML() {
	let args = arguments;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            for (let i = 0; i < args.length; i++) {
            	args[i](docXML);
            }
    	}
  	};
  	xhttp.open("GET", siteroot + "/data/equipmentDB.xml", true);
  	xhttp.send();
}

function populateEquipDisplay(xml) {
	container = d3.select("main");
	items = xml.getElementsByTagName("Item");
	for (let i = 0; i < items.length; i++) {
		item = container.append("div").classed("eq-item-display", true);
		item.append("h2").classed("eq-item-text", true).html(items[i].getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue);
		item.append("a").classed("eq-item-pdf", true).html("PDF").attr("data", items[i].getAttribute("id"));
	}
	sortEquipList();
	linkPDFs();
}






function createEquipRecordSnapshots(xml) {  //create and append to DOM an appropriate number of records given an XML "lab" node - not type safe
	var equiplist = xml.getElementsByTagName("Item");
	for (let i = 0; i < equiplist.length; i++) {
		// console.log(equiplist[i])
		let eqid = equiplist[i].getAttribute("id");
		let eqname = (equiplist[i].getElementsByTagName("InventoryName")[0].childNodes[0] ? equiplist[i].getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue : "—");
		let eqmake = (equiplist[i].getElementsByTagName("Manufacturer")[0].childNodes[0] ? equiplist[i].getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "—");
		let eqmodel = (equiplist[i].getElementsByTagName("Model")[0].childNodes[0] ? equiplist[i].getElementsByTagName("Model")[0].childNodes[0].nodeValue : "—");

		let snapshot = d3.select("#eq-list-box").append("div").classed("eq-record-flex", true).classed("record-rendered", true);
		let id = snapshot.append("p").classed("eq-record-id", true).html(eqid);
		let make = snapshot.append("p").classed("eq-record-make", true).html(eqmake);
		let model = snapshot.append("p").classed("eq-record-model", true).html(eqmodel);
		let name = snapshot.append("p").classed("eq-record-name", true).html(eqname);
	}
}

$(document).on("click", ".eq-record-flex", function(e) {
	console.log($(e.target).children(".eq-record-id").text())
	new EquipmentDisplay($(e.target).children(".eq-record-id").text());
});








// TEMPORARY FUNCTIONS FOR TEMPORARY EQUIPMENT MOD PAGE -----------------------

function sortEquipList() {
	items = $(".eq-item-display");
	items.sort(compareEquipNames);
	items.each(function() {
		$("main").append(this);
	});
}

function compareEquipNames(a,b) {
	return ($(a).find(".eq-item-text").text() < $(b).find(".eq-item-text").text()) ? 1 : ($(a).find(".eq-item-text").text() > $(b).find(".eq-item-text").text()) ? -1 : 0;
}

function linkPDFs() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            let labs = docXML.getElementsByTagName("Lab");
            let items = $(".eq-item-pdf");
            eqloop: for (let i = 0; i < items.length; i++) {
            	let id = $(items[i]).attr("data");
            	labloop: for (let j = 0; j < labs.length; j++) {
            		let equipment = labs[j].getElementsByTagName("Item");
            		eqtwoloop: for (let k = 0; k < equipment.length; k++) {
            			if (equipment[k].getAttribute("id") == id) {
            				$(items[i]).attr("target", "_blank").attr("href", "http://www.pjl.ucalgary.ca"+labs[j].getElementsByTagName("Path")[0].childNodes[0].nodeValue);
            				break labloop;
	            		}
            		}
            	}
            }
    	}
  	};
  	xhttp.open("GET", siteroot + "/dev/labDB.xml", true);
  	xhttp.send();
}

//-----------------------------------------------------------------------------------


class EquipmentDisplay {

	constructor(id) {
		var self = this;
		self.id = id;
		self.modalmask = d3.select("body").append("div").classed("modal-screen", true).style("display", "block");


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

		self._getItemData = function(xml, id) {
			let nodes = xml.getElementsByTagName("Item");
			for (let i = 0; i < nodes.length; i++) {
				if (nodes[i].getAttribute("id") == id) {
					return nodes[i];
				}
			}
		}

		self._buildDisplay = function(data) {
			let name = (data.getElementsByTagName("InventoryName")[0].childNodes[0] ? data.getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue : "none");
			let make = (data.getElementsByTagName("Manufacturer")[0].childNodes[0] ? data.getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "none");
			let model = (data.getElementsByTagName("Model")[0].childNodes[0] ? data.getElementsByTagName("Model")[0].childNodes[0].nodeValue : "none");
			let locations = [];
			let locationnodes = data.getElementsByTagName("Locations")[0].getElementsByTagName("Location");
			for (let i = 0; i < locationnodes.length; i++) {
				let room = locationnodes[i].getElementsByTagName("Room")[0].childNodes[0].nodeValue;
				let storage = locationnodes[i].getElementsByTagName("Storage")[0].childNodes[0].nodeValue;
				locations.push({"room": room, "storage": storage})
			}
			let total = (data.getElementsByTagName("Total")[0].childNodes[0] ? data.getElementsByTagName("Total")[0].childNodes[0].nodeValue : "N/A")
			let service = (data.getElementsByTagName("InService")[0].childNodes[0] ? data.getElementsByTagName("InService")[0].childNodes[0].nodeValue : "N/A")
			let repair = (data.getElementsByTagName("UnderRepair")[0].childNodes[0] ? data.getElementsByTagName("UnderRepair")[0].childNodes[0].nodeValue : "N/A")
			let docs = [];
			let docnodes = data.getElementsByTagName("Document");
			for (let i = 0; i < docnodes.length; i++) {
				let name = docnodes[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
				let path = docnodes[i].getElementsByTagName("Location")[0].childNodes[0].nodeValue;
				docs.push({"name": name, "path": path})
			}

			let modal = self.modalmask.append("div").classed("eq-modal", true);
			let header = modal.append("div").classed("eq-modal-header", true);
			header.append("h1").classed("eq-modal-title", true).html("Inventory");
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
			for (let i = 0; i < locations.length; i++) {
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
			for (let i = 0; i < docs.length; i++) {
				let dc = dcs.append("div").classed("eq-modal-doc", true);
				dc.append("i").classed("fa fa-file-o", true).attr("aria-hidden", "true");
				dc.append("a").attr("href", docs[i].path).attr("target", "_blank").html(docs[i].name);
			}
		}

		self._setEventListeners = function() {
			$(document).on("click", ".modal-screen", self.removeForm);

			$(document).on("click", ".eq-modal", function(e) {
				e.stopPropagation();
			});
		}

		self.removeForm = function() {
			$(".eq-modal").slideUp("fast", function() {
				self.modalmask.remove();
			});
			$(".modal-screen").remove();
			$("main").removeClass("blurred-page");
			$(document).off("click", ".modal-screen");
			$(document).off("click", ".eq-modal");
		}

		self._loadEquipDB();
		$("main").addClass("blurred-page");
	}
}


class DownloadModalWindow {

	constructor(id) {
		var self = this;
		self.id = id;
		self.modalmask = d3.select("body").append("div").classed("modal-screen", true).style("display", "block");

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
		}

		self.removeWindow = function() {
			self.modalmask.remove();
			$("main").removeClass("blurred-page");
			$(document).off("click", ".modal-screen");
			$(document).off("click", ".modal-close-button");
			$(document).off("click", ".dl-modal");
			$(document).off("click", ".dl-modal-footer");
		}

		$("main").addClass("blurred-page");
		self._buildWindow();
		self._setEventListeners();
	}
}



class EquipmentModForm {

	constructor(id) {
		var self = this;
		self.id = id;
		self.form = d3.select("body").append("form").classed("equip-mod-form", true);


		self._buildForm = function() {
			let formheader = self.form.append("div").classed("header", true);
			let headerid = formheader.append("h3").classed("id", true).html("Equipment Item #" + String(self.id));

			let formbody = self.form.append("div").classed("buttons", true);
			let idbutton = formbody.append("h3").classed("button id-button", true).html("Identification");
			let idcontent = formbody.append("div").classed("id-content", true);
			idcontent.append("label").html("Name");
			idcontent.append("input").classed("eq-name", true)
						.attr("name", "eq-name")
						.attr("type", "text")
						.attr("autocomplete", "off");
			idcontent.append("label").html("Manufacturer");
			idcontent.append("input").classed("eq-make", true)
						.attr("name", "eq-make")
						.attr("type", "text")
						.attr("autocomplete", "off");
			idcontent.append("label").html("Model");
			idcontent.append("input").classed("eq-model", true)
						.attr("name", "eq-model")
						.attr("type", "text")
						.attr("autocomplete", "off");


			let locbutton = formbody.append("h3").classed("button loc-button", true).html("Add/Change Locations");
			let loccontent = formbody.append("div").classed("loc-content", true);
			let addloc = loccontent.append("i").classed("fa fa-plus fa-lg", true)
										.attr("id", "add-location")
										.attr("aria-hidden", "true");



			let amountbutton = formbody.append("h3").classed("button amount-button", true).html("Change Service Amounts");
			let amountcontent = formbody.append("div").classed("amount-content", true);
			let amountrow = amountcontent.append("div").classed("amount-row", true);
			amountrow.append("label").html("Total");
			amountrow.append("input").classed("eq-total", true)
						.attr("name", "eq-total")
						.attr("type", "text")
						.attr("autocomplete", "off");

			amountrow = amountcontent.append("div").classed("amount-row", true);
			amountrow.append("label").html("In Service");
			amountrow.append("input").classed("eq-service", true)
						.attr("name", "eq-service")
						.attr("type", "text")
						.attr("autocomplete", "off");
			amountrow = amountcontent.append("div").classed("amount-row", true);
			amountrow.append("label").html("Under Repair");
			amountrow.append("input").classed("eq-repair", true)
						.attr("name", "eq-repair")
						.attr("type", "text")
						.attr("autocomplete", "off");


			let formfooter = self.form.append("div").classed("footer", true);
			let submit = formfooter.append("input")
							.classed("submit", true)
							.attr("name", "submit")
							.attr("type", "submit")
							.attr("value", "Submit");
		}


		self._populateForm = function() {
			self._loadEquipDB()
		}

		self._loadEquipDB = function() {
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
		    	if (xhttp.readyState == 4 && xhttp.status == 200) {
		            let docXML = xhttp.responseXML;
		            self._populateFields(docXML);
		    	}
		  	};
		  	xhttp.open("GET", siteroot + equipmentdatabasepath, true);
		  	xhttp.send();
		}

		self._populateFields = function(xml) {
			let items = xml.getElementsByTagName("Item");
			for (let i = 0; i < items.length; i++) {
				if (items[i].getAttribute("id") == self.id) {
					let name = items[i].getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue;
					let make = (items[i].getElementsByTagName("Manufacturer")[0].hasChildNodes() ? items[i].getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "");
					let model = (items[i].getElementsByTagName("Model")[0].hasChildNodes() ? items[i].getElementsByTagName("Model")[0].childNodes[0].nodeValue : "");
					let amount = (items[i].getElementsByTagName("Total")[0].hasChildNodes() ? items[i].getElementsByTagName("Total")[0].childNodes[0].nodeValue : "");
					let service = (items[i].getElementsByTagName("InService")[0].hasChildNodes() ? items[i].getElementsByTagName("InService")[0].childNodes[0].nodeValue : "");
					let repair = (items[i].getElementsByTagName("UnderRepair")[0].hasChildNodes() ? items[i].getElementsByTagName("UnderRepair")[0].childNodes[0].nodeValue : "");
					let locations = items[i].getElementsByTagName("Locations")[0].getElementsByTagName("Location");
					let form = self.form.select(".loc-content");

					for (let j = 0; j < locations.length; j++) {
						form.insert("label", "#add-location").html("Room");
						form.insert("input", "#add-location")
								.attr("id","eq-room")
								.attr("name","eq-room[]")
								.attr("type","text")
								.attr("value", locations[j].getElementsByTagName("Room")[0].childNodes[0].nodeValue)
								.attr("autocomplete", "off");
						form.insert("label", "#add-location").html("Storage");
						form.insert("input", "#add-location")
								.attr("id","eq-storage")
								.attr("name","eq-storage[]")
								.attr("type","text")
								.attr("value", locations[j].getElementsByTagName("Storage")[0].childNodes[0].nodeValue)
								.attr("autocomplete", "off");
					}
					$(".eq-name").attr("value", name)
					$(".eq-make").attr("value", make)
					$(".eq-model").attr("value", model)
					$(".eq-total").attr("value", amount)
					$(".eq-service").attr("value", service)
					$(".eq-repair").attr("value", repair)
					break;
				}
			}
		}

		self._setEventListeners = function() {

			$(document).on("submit", ".equip-mod-form", function(e) {
				e.preventDefault();
				let dat = $(e.target).serialize();
				$.post(siteroot + "/php/modifyEquipDB.php", dat + "&eq-id=" + self.id, function(data) {
					self.removeForm();
				});
			});

			$(document).on("click", ".equip-mod-form", function(e) {
				e.stopPropagation();
			});



			$(document).on("click", "#add-location", function(e) {
				let form = self.form.select(".loc-content");
				let row = form.insert("div", "#add-location").classed("loc-row", true);
				row.insert("label", "#add-location").html("Room");
				row.insert("input", "#add-location").attr("id","eq-room").attr("name","eq-room[]").attr("type","text");
				row = form.insert("div", "#add-location").classed("loc-row", true);
				row.insert("label", "#add-location").html("Storage");
				row.insert("input", "#add-location").attr("id","eq-storage").attr("name","eq-storage[]").attr("type","text");
				form.insert("div", "#add-location").classed("sep", true);
			});

			$(window).on("swipeleft", self.removeForm);
		}

		self._unsetEventListeners = function() {
			$(document).off("submit", ".equip-mod-form");
			$(document).off("click", ".equip-mod-form");
			$(document).off("click", "#add-location");
			$(window).off("swipeleft", self.removeForm);
		}

		self.removeForm = function() {
			self._unsetEventListeners();
			$(".equip-mod-form").slideUp("fast", function() {
				self.form.remove();
			});
			$("main").removeClass("blurred-page");
		}

		$("main").addClass("blurred-page")
		self._buildForm();
		self._populateForm();
		self._setEventListeners();
	}

}








//*******************************************************************************************
//   EVENT LISTENERS
//*******************************************************************************************



$(document).on("click", ".lab-details-drop-icon-flex", function(e) {
	var extendeddataflex = $(e.target).parent().siblings(".lab-record-detailed-flex");
	extendeddataflex.stop().slideToggle("fast");
});



$(document).on("click", "#clear-filters-button", function(e) {
	var selects = $("select");
	for (var i = selects.length - 1; i >= 0; i--) {
		$(selects[i]).val([]);
	}
	filterResults(getCurrentFilter(), fullset=true);
	displayNumResults(countNumRecords());
	applyRecordsMask(true)
});



$(document).on("click", "#show-recent-button", function(e) {
	showMostRecent();
});



$(document).on("click", "select", function(e) {
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



$(document).on("click", ".search-icon", function(e) {
	searchQueryHandler();
	applyRecordsMask(true)
});



$(document).on("keypress", "#search-bar", function(e) {
	var key = e.which;
	if (key == 13) {
		console.log("enter")
	 	$(".search-icon").click();
	 	return false;
	}
});



$(document).on("click", "#search-help-button", function(e) {
	$(".search-container").toggleClass("search-help-opened");
	$(e.target).next().stop().slideToggle(300);
});



$(document).on("click", "#zip-icon", function(e) {
	new DownloadModalWindow();
	$("#dl-modal-number").text("(" + String(countNumRecords()) + " records selected)");
	// $("main").addClass("blurred-page");
	// $(".modal-screen").css("display", "block");
	// $(".dl-modal").stop().fadeIn(200);
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





// $(document).on("click", ".dl-modal, .eq-modal", function(e) {
// 	e.stopPropagation();
// });


// $(document).on("click", ".modal-close-button", function(e) {
// 	$("main").removeClass("blurred-page");
// 	$(".modal-screen").css({display: 'none'});
// 	$("#zip-options").css({display: 'none'});
// });



// $(document).on("click", ".modal-screen", function(e) {
// 	$("main").removeClass("blurred-page");
// 	$(".modal-screen").css({display: 'none'});
// 	$("#zip-options").css({display: 'none'});
// 	console.log("line 647 listener")
// });



// $(document).on("click", ".modal-content", function(e) {
// 	e.stopPropagation();
// });






// $(document).on("change", ".download-checkbox", function(e) {
// 	var checkboxes = $(".dc-right");
// 	if($(e.target).prop("id") == "ALL") {
// 		checkboxes.each(function() {
// 			$(this).prop("checked", false)
// 		});
// 	} else {
// 		var somethingchecked = false;
// 		checkboxes.each(function() {
// 			if ($(this).prop("checked")) {
// 				somethingchecked = true;
// 			}
// 		});
// 		if (somethingchecked) {
// 			$("#ALL").prop("checked", false);
// 		}
// 	}

// });



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
	window.open(siteroot + $(e.target).parent().parent().find(".version-path").attr("href"), "_blank");
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



$(document).on("click", "#staff-name-ernst", function(e) {
	window.open("http://phas.ucalgary.ca/phas_info/profiles/wesley-ernst");
});



$(document).on("click", "#staff-name-gimby", function(e) {
	window.open("http://phas.ucalgary.ca/phas_info/profiles/peter-gimby");
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




$(document).on("click", ".resource-dropdown-content, .mobile-resource-dropdown-content", function(e) {
	var links = {"pjl-regress": "/",
				 "pjl-lab-schedule": "/data/schedules/schedule-current.pdf",
				 "pjl-rooms-schedule": "/data/schedules/rooms-current.pdf",
				 "pjl-geiger": "/",
				 "pjl-repository": "/repository",
				 "pjl-linearization": "/",
				 "pjl-compare-two": "/",
				 "pjl-uncertainty": "/",
				 "pjl-graphing": "/",
				 "pjl-scint": "/",
				 "pjl-latex-template": "/",
				 "pjl-inventory":"/",
				 "pjl-github":"https://github.com/pgimby/pjl-web",
				 "pjl-lab-rules":"/data/safety/lab-rules/Lab-Rules.pdf",
				 "pjl-rad-safety":"/data/safety/training/Radiation-Safety/Radiation-Safety.pdf",
				 "pjl-orientation":"/data/safety/training/Orientation.pdf",
				 "pjl-hacf-pjl":"/data/safety/HACFs/HACF-PJL.pdf",
				 "pjl-hacf-adv":"/data/safety/HACFs/HACF-TA-ADV.pdf",
				 "pjl-hacf-std":"/data/safety/HACFs/HACF-TA-STD.pdf",
				 "pjl-equipment-page":"/staffresources/equipdb"}
	var buttonid = $(e.target).attr("id");
	window.open(links[buttonid], '_blank');
});



$(document).on("click touch", ".need-help", function(e) {
	window.location.href = "mailto:pgimby@phas.ucalgary.ca?Subject=PJLWeb%20Bug%20Report";
	e.stopPropagation();
});




$(document).on("click touch", "body", function(e) {
	// hideContactForm();
	hideMobileNav();
	e.stopPropagation();
});



$(document).on("click touch", "#mobile-nav-button", function(e) {
	showMobileNav();
	e.stopPropagation();
});



$(window).on("swipeleft", hideMobileNav);
$(window).on("swiperight", showMobileNav);


$(document).on("click", ".eq-item-text", function(e) {
	$("main").addClass("blurred-page");
	let id = $(e.target).next().attr("data");
	let form = new EquipmentModForm(id);
	e.stopPropagation();
})




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
		var download = snapshot.append("a").classed("version-path", true).html("Download").attr("href", siteroot + versionlist[i].path).attr("target", "_blank");
		snapshot.append("img").classed("download-icon", true).html("Download").attr("src", siteroot + "/img/download-icon.svg");  //alternate for mobile display
		var course = snapshot.append("p").classed("courses", true).html(versionlist[i].course);
		var date = snapshot.append("p").classed("version-semester", true).html(versionlist[i].semester + " " + versionlist[i].year);
		var labtitle = snapshot.append("p").classed("lab-title", true).html(lab.getElementsByTagName("Name")[0].childNodes[0].nodeValue);
		var dropiconflex = snapshot.append("div").classed("lab-details-drop-icon-flex", true);
		var dropicon = dropiconflex.append("img").classed("lab-details-drop-icon", true).attr("src", siteroot + "/img/dropdown-arrow.png");

		var extendedlabdata = detailsbox.append("div").classed("lab-record-detailed-flex", true).attr("style", "display: none");
		var labid = extendedlabdata.append("p").classed("lab-data-id", true).html("<span>Lab ID:</span> " + getLabId(lab));
		var labtopics = extendedlabdata.append("p").classed("lab-data-topics", true).html("<span>Topics:</span> " + getLabTopicsList(lab).join(", "));
		var labdisciplines = extendedlabdata.append("p").classed("lab-data-disciplines", true).html("<span>Disciplines:</span> " + getLabDisciplinesList(lab).join(", "));
		var labequipment = extendedlabdata.append("div").classed("lab-data-equipment", true);
		getLabEquipmentList(lab, labequipment);
		//.html("<span>Equipment:</span> " + spanTheList(getLabEquipmentList(lab), "equip-item").join(", "));

		var software = extendedlabdata.append("p").classed("lab-data-software", true).html("<span>Software:</span> " + getLabSoftwareList(lab).join(", "));
		var directory = extendedlabdata.append("p").classed("version-directory", true).html(versionlist[i].directory).style("display", "none");

		var labdoclist = getExtraLabDocs(lab);
		var labdocs = extendedlabdata.append("div").classed("extra-docs", true);
		labdocs.append("p").html("<span>Additional Documents:</span> ");
		for (var j = labdoclist.length - 1; j >= 0; j--) {
			labdocs.append("a").classed("extra-doc", true).attr("href", labdoclist[j].url).html(labdoclist[j].name).attr("target", "_blank");
		}
	}
}



function getLabEquipmentList(lab, selection) {  //appends equipment to the lab equipment div given an XML "lab" node and d3 selection to append to
	let equipnode = lab.getElementsByTagName("Equipment")[0];
	let items = equipnode.getElementsByTagName("Item");
	selection.append("p").classed("equipment-label", true).html("<span>Equipment: </span>");
	for (let i = 0; i < items.length; i++) {
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

$(document).on("click", ".equip-item-primary, .equip-item-alt", function(e) {
	let item = $(e.target);
	let id = item.attr("data-eqid");
	let href = "/staffresources/equipment?id=" + id
	window.open(href, "_blank");
});






//*******************************************************************************************
//   DOM MODIFIER FUNCTIONS
//*******************************************************************************************



function filterResults(filter, fullset=true) {  //given a filter object, filter displayed records and update DOM appropriately
	if(fullset) {
		var lablist = $(".lab-record-flex");
	} else {
		var lablist = getCurrentRecords();
	}
	var numrecords = lablist.length;
	for (var i = lablist.length - 1; i >= 0; i--) {
		var lab = $(lablist[i]);
		var courses = lab.find(".courses").text().split(", ");
		var disciplines = lab.find(".lab-data-disciplines").text().slice(13,).split(", ");
		var topics = lab.find(".lab-data-topics").text().slice(8,).split(", ");

		if (filter["year-filter"].includes(lab.find(".version-semester").text().slice(-4)) || filter["year-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		}
		else if (lab.find(".version-semester").text().endsWith("—") && filter["year-filter"].includes("—")) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			continue;
		}
		if (doArraysOverlap(courses, filter["course-filter"])                                    || filter["course-filter"].length == 0) {
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
		if (doArraysOverlap(disciplines, filter["discipline-filter"])                            || filter["discipline-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
			continue;
		}
		if (doArraysOverlap(topics, filter["topic-filter"])                            || filter["topic-filter"].length == 0) {
			lab.removeClass("record-not-rendered masked").addClass("record-rendered");
		} else {
			lab.removeClass("record-rendered masked").addClass("record-not-rendered");
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
	let canzip = canZip()
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
			var record = $(extendeddatarecords[i]).parent();
			if (record.hasClass("record-rendered") && record.filter(".record-rendered").length < 100) {
				$(extendeddatarecords[i]).stop().slideDown()
			} else {
				$(extendeddatarecords[i]).css("display", "flex");
			}
		}
		setExpandedButtonTruth(true)
	} else {
		var extendeddatarecords = $(".lab-record-detailed-flex");
		for (var i = extendeddatarecords.length - 1; i >= 0; i--) {
			var record = $(extendeddatarecords[i]).parent();
			if (record.hasClass("record-rendered") && record.filter(".record-rendered").length < 100) {
				$(extendeddatarecords[i]).stop().slideUp()
			} else {
				$(extendeddatarecords[i]).css("display", "none");
			}
		}
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
	$("#lab-list-box").addClass("records-unmasked");
	if (Boolean(truthy)) {
		$("#lab-list-box").removeClass("records-unmasked");
	}
}



function unmaskAll(records) {
	$("#lab-list-box").addClass("records-unmasked");
	for (var i = records.length - 1; i >= 0; i--) {
		records[i].removeClass("masked");
	}
	$("#show-all-button").css("visibility", "hidden");
}



function setNumberRecordsUnmasked() {
	var records = getCurrentRecords();
	var num = records.length;
	for (var i = records.length - 1; i >= 0; i--) {
		if (records[i].hasClass("masked")) {
			num--;
		}
	}
	$("#num-unmasked-results").html(String(num));
}




function showMostRecent() {
	var uniquelabs = [];
	var records = getCurrentRecords();
	unmaskAll(records);
	setNumberRecordsUnmasked();

	for (var i = records.length - 1; i >= 0; i--) {
		var labid = records[i].find(".lab-data-id").text().slice(-4,);
		if(!uniquelabs.includes(labid)) {
			uniquelabs.push(labid);
		}
		records[i].removeClass("record-rendered").addClass("record-not-rendered");
	}

	for (var i = uniquelabs.length - 1; i >= 0; i--) {
		var year = 0;
		var mostrecent = null;
		var sameyeardifcourse = [];
		for (var j = records.length - 1; j >= 0; j--) {
			if (records[j].find(".lab-data-id").text().slice(-4,) == uniquelabs[i]) {
				var recordsemester = records[j].find(".version-semester").text();
				var date = parseFloat(recordsemester.split(" ")[1]) + parseFloat(semesterDecimal[recordsemester.split(" ")[0]]);
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
			for (var j = sameyeardifcourse.length - 1; j >= 0; j--) {
				sameyeardifcourse[j].removeClass("record-not-rendered").addClass("record-rendered");
			}
		}
	}
	sortRecords("year");
	sortRecords("year");
	displayNumResults(countNumRecords());
	setNumberRecordsUnmasked();
}


function showMobileNav() {
	if($(".mobile-landing-nav").css("display") == "none") {
		$(".mobile-landing-nav").show("slide", {direction: "left"}, 300);
	}
}


function hideMobileNav() {
	if($(".mobile-landing-nav").css("display") == "block") {
		$(".mobile-landing-nav").hide("slide", {direction: "left"}, 300);
	}
}




var semesterDecimal = {"Fall": 0.75, "Winter": 0.0, "Spring": 0.25, "Summer": 0.50}











//*******************************************************************************************
//   SEARCH-RELATED FUNCTIONS (USING SORENSEN-DICE SIMILARITY)
//*******************************************************************************************



function generateSearchResults(query, selector) {  //take query and search-selector and make yes/no decisions on what records to include; display accordingly
	var minsimilarity = 0.4;
	var querybigrams = makeBigramList(query);
	var lablist = getAllRecords();
	var skipsim = ("id" == selector ? true : false)
	for (var i = lablist.length - 1; i >= 0; i--) {
		lablist[i].removeClass("record-not-rendered masked").addClass("record-rendered");
		var similarity = (skipsim ? 0.0 : compareQueryWithLabRecord(querybigrams, lablist[i], selector));
		if (similarity < minsimilarity && !queryLiteralInLabRecord(query, lablist[i], selector)) {
			lablist[i].removeClass("record-rendered").addClass("record-not-rendered");
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
	var id = lab.find(".lab-data-id").text().slice(-4,).toLowerCase();
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
	var totest = [""];
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
		case "id":
			idSearchHandler(searchphrase);
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



function idSearchHandler(searchphrase) {  //handle the search request for id search selector - not type safe
	$('html, body').animate({scrollTop: ($('#lab-list-box').offset().top)}, 500);
			generateSearchResults(searchphrase, "id");
			displayNumResults(countNumRecords());
	 		$("#search-bar").val("");
}












//*******************************************************************************************
//   ZIP-RELATED FUNCTIONS
//*******************************************************************************************



function makePromisesBeginZip(filelist) {
	var zip = new JSZip();
	var files = filelist;
	var promises = [];
	var xhrs = [];

	function increaseProgress(j) {
		return function() {
			console.log((j/files.length).toFixed(1))
			$("#zip-progress-bar progress").attr("value", (j/files.length).toFixed(1));
		}
	}

	for (let i = 0; i < files.length; i++) {
		let downloadingfile = new $.Deferred();
		downloadingfile.done(function(filename, blob) {
			zip.file(filename, blob);
		}, increaseProgress(i));
		let xhr = beginDownload(files[i], downloadingfile);
		promises.push(downloadingfile);
		xhrs.push(xhr);
	}


	deferredzip = $.when.apply($, promises);


	deferredzip.done(function() {
		zip.generateAsync({type:"blob"}).then(function (blob) {
			saveAs(blob, zipoutputfilename);
			console.log("zip done")
			$("#zip-progress-bar progress").attr("value", "0");
			$("#zip-progress-bar").stop().slideUp(500);
		});
		return false;
	});

	deferredzip.fail(function() {
		setTimeout(function() {
			$("#file-prep").text("Download failed.");
			setTimeout(function() {
				$("#zip-progress-bar progress").attr("value", "0");
				$("#zip-progress-bar").stop().slideUp(500, function() {
				$("#file-prep").text("Preparing files...");
				});
			}, 2000);
		}, 700);
	});


	$(document).on("click", "#cancel-download", function(e) {
		for (var i = xhrs.length - 1; i >= 0; i--) {
			xhrs[i].abort();
			promises[i].reject();
		}
		$("#zip-progress-bar progress").attr("value", "0");
		$("#zip-progress-bar").stop().slideUp(500);
		return;
	});

}


function fileDownloadPromise() {  //return a jQuery promise
	return new $.Deferred();
}


function beginDownload(filepath, promise) {
//start downloading and resolve associated promise upon completion (or failure) - not type safe
//return XML HTTP request object
	var xhttp = new XMLHttpRequest();
	xhttp.responseType = "blob";
	xhttp.onreadystatechange = function() {
    	if (this.readyState == 4 && this.status == 200) {
            blob = this.response;
            var filename = filepath.split("/");
            filename = filename[filename.length-1];
            promise.notify();
            promise.resolve(filename, blob);
    	} else if(this.status == 404) {
    		promise.reject();
    	} else if (this.status == 403) {
    		promise.reject();
    	} else {
    		$("#zip-progress-bar progress").attr("value", "0");
			$("#zip-progress-bar").stop().slideUp(500);
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


// var promises = []
function collectFiles2Zip(doALL, doPDF, doTEX, doTMP, doMED, doEXTRA) {
	var dirlist = [];
	var filelist = [];
	var promises = [];
	var extradocs = [];
	var records = getCurrentRecords();
	function fileCallback(promise) {
		return function(d) {
			filelist = filelist.concat(d.split(","));
			promise.resolve();
		}
	}
	for (var i = records.length - 1; i >= 0; i--) {
		dirlist.push(records[i].find(".version-directory").text());
		extradocs.concat(getExtraDocsFromRecord(records[i]));
	}

	for (var i = dirlist.length - 1; i >= 0; i--) {
		let promise = $.Deferred();
		promises.push(promise)
		$.post(siteroot + "/php/getFileListRecursive.php", "dirpath=" + dirlist[i], fileCallback(promise));
	}

	var deferredFileList = $.when.apply($, promises);

	deferredFileList.done(function() {
		filteredlist = filterFileList(doALL, doPDF, doTEX, doTMP, doMED, filelist);
		if(doEXTRA || doALL) {
			filteredlist.concat(extradocs);
		}
		makePromisesBeginZip(filteredlist);
		console.log("An elegant syntax for ease of use,\neasy reading. Not abstruse.\n\nHaving this would sure be swell.\nPHP can rot in hell.")
	});
	deferredFileList.fail(function() {console.log("File collection failed: Unable to locate files for selection.")});
}


function filterFileList(doALL, doPDF, doTEX, doTMP, doMED, filelist) {
	if (doALL) {
		return filelist;
	}
	var filteredfiles = [];
	for (var i = filelist.length - 1; i >= 0; i--) {
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



function getExtraDocsFromRecord(record) { //record is an HTML DOM element
	var docs = $(record).children(".extra-docs").children(".extra-doc");
	list = [];
	for (var i = docs.length - 1; i >= 0; i--) {
		let docname = docs[i].text();
		let docpath = docs[i].attr("href");
		list.push({name: docname, url: docpath});
	}
	return list;
}






//*******************************************************************************************
//   GENERAL FUNCTIONS
//*******************************************************************************************



function loadXML() {  //load the XML document holding all the lab records (see global var for XML URL)
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    	if (xhttp.readyState == 4 && xhttp.status == 200) {
            let docXML = xhttp.responseXML;
            populateRecordList(docXML);
            populateFilters(docXML);
            applyRecordsMask(true);
    	}
  	};
  	xhttp.open("GET", siteroot + mainxmlpath, true);
  	xhttp.send();
}



function sendEquipXMLModification(data) { //data is a dictionary
	//data = {itemid:"0001", make: "Pasco", model: "8010A", amount: "10", service: "10", repair: "0"}
	$.ajax({
	  method: "POST",
	  url: "/php/modifyEquipDB.php",
	  data: data
	})
	  .done(function( msg ) {
	    alert( "Data saved: " + msg );
	  });
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
	return lab.getAttribute("labId");
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



// function getLabEquipmentList(lab) {  //return an array of equipment (strings) for an XML "lab" node - not type safe
// 	let list = [];
// 	let ids = [];
// 	var equipment = lab.getElementsByTagName("Item");
// 	for (var i = equipment.length - 1; i >= 0; i--) {
// 		list.push(equipment[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue + " (" + equipment[i].getElementsByTagName("Amount")[0].childNodes[0].nodeValue + ")");
// 		ids.push()
// 	}
// 	return {"equip": list, "ids": ids};
// }



function getLabSoftwareList(lab) {  //return an array of software (strings) for an XML "lab" node - not type safe
	var list = [];
	var software = lab.getElementsByTagName("Software")[0];
	var names = software.getElementsByTagName("Name");
	for (var i = names.length - 1; i >= 0; i--) {
		list.push(names[i].childNodes[0].nodeValue);
	}
	return list;
}



function getExtraLabDocs(lab) {  //return an array of extra doc objects for an XML "lab" node - not type safe
	var list = [];
	var docs = lab.getElementsByTagName("Doc");
	for (var i = docs.length - 1; i >= 0; i--) {
		var docname = docs[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
		var docpath = docs[i].getElementsByTagName("Path")[0].childNodes[0].nodeValue;
		list.push({name: docname, url: docpath});
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
		var p = list[i].getElementsByTagName("Path")[0];
		var y = list[i].getElementsByTagName("Year")[0];
		var s = list[i].getElementsByTagName("Semester")[0];
		var c = list[i].getElementsByTagName("Course")[0];
		var d = list[i].getElementsByTagName("Directory")[0];
		versionlist.push({path: (Boolean(p.childNodes[0]) ? p.childNodes[0].nodeValue : "—"),
						  semester: (Boolean(s.childNodes[0]) ? s.childNodes[0].nodeValue : "—"),
						  year: (Boolean(y.childNodes[0]) ? y.childNodes[0].nodeValue : "—"),
						  course: (Boolean(c.childNodes[0]) ? c.childNodes[0].nodeValue : "—"),
						  directory: (Boolean(d.childNodes[0]) ? d.childNodes[0].nodeValue : null)});
	}
	return versionlist;
}


//PETER WROTE THIS ONE
function getValidFilterOptions(docXML, type) {  //return the set of values available for filtering on a given filter type as an array - not type safe
	var nodelist = docXML.getElementsByTagName(type);
    var valueslist = [];
    for (var i = 0; i < nodelist.length; i ++) {
	    var value = nodelist[i].childNodes[0];
	    valueslist.push((Boolean(value) ? value.nodeValue : "—"));
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
	jQueryDOMSelection.stop().animate({opacity: 1}, 600);
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



function mostRecentDecimalSemester() {
	var date = new Date();
	return Math.round(date.getMonth() / 3) / 4;
}


function spanTheList(list, classname, ids) {
	for (let i = list.length - 1; i >= 0; i--) {
		list[i] = "<span class='" + classname + "' data-eqid=" + ids[i] + ">" + String(list[i]).split("(")[0].trim() + "</span>" + " (" + String(list[i]).split("(")[1];
	}
	return list;
}
