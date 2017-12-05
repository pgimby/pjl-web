


$(document).off("click", ".eq-record-flex");

$(document).on("click", ".eq-record-flex", function(e) {
	new EquipmentEditDisplay($(e.target).children(".eq-record-id").text());
});

$(document).off("click", "#edit-mode-button");

$(document).on("click", "#edit-mode-button", function(e) {
	window.location = "../";
});




class EquipmentEditDisplay {

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
			let name = (data.getElementsByTagName("InventoryName")[0].childNodes[0] ? data.getElementsByTagName("InventoryName")[0].childNodes[0].nodeValue : "");
			let make = (data.getElementsByTagName("Manufacturer")[0].childNodes[0] ? data.getElementsByTagName("Manufacturer")[0].childNodes[0].nodeValue : "");
			let model = (data.getElementsByTagName("Model")[0].childNodes[0] ? data.getElementsByTagName("Model")[0].childNodes[0].nodeValue : "");
			let locations = [];
			let locationnodes = data.getElementsByTagName("Locations")[0].getElementsByTagName("Location");
			for (let i = 0; i < locationnodes.length; i++) {
				let room = locationnodes[i].getElementsByTagName("Room")[0].childNodes[0].nodeValue;
				let storage = locationnodes[i].getElementsByTagName("Storage")[0].childNodes[0].nodeValue;
				locations.push({"room": room, "storage": storage})
			}
			let total = (data.getElementsByTagName("Total")[0].childNodes[0] ? data.getElementsByTagName("Total")[0].childNodes[0].nodeValue : "")
			let service = (data.getElementsByTagName("InService")[0].childNodes[0] ? data.getElementsByTagName("InService")[0].childNodes[0].nodeValue : "")
			let repair = (data.getElementsByTagName("UnderRepair")[0].childNodes[0] ? data.getElementsByTagName("UnderRepair")[0].childNodes[0].nodeValue : "")
			let docs = [];
			let docnodes = data.getElementsByTagName("Document");
			for (let i = 0; i < docnodes.length; i++) {
				let name = docnodes[i].getElementsByTagName("Name")[0].childNodes[0].nodeValue;
				let path = docnodes[i].getElementsByTagName("Location")[0].childNodes[0].nodeValue;
				docs.push({"name": name, "path": path})
			}

			self.form = self.modalmask.append("form").classed("eq-modal-edit-form", true);

			let modal = self.form.append("div").classed("eq-modal", true);
			let header = modal.append("div").classed("eq-modal-header", true);
			header.append("h1").classed("eq-modal-title", true).html("Inventory");
			header.append("i").classed("fa fa-times fa-2x modal-close-button", true).attr("aria-hidden", "true");

			let content = modal.append("div").classed("eq-modal-content", true);
			let img = content.append("div").classed("eq-modal-img", true);
			img.append("img").attr("src", "/img/img-placeholder.png");
			let ident = content.append("div").classed("eq-modal-id", true);
			ident.append("input").classed("eq-modal-name", true)
						.attr("name", "eq-name")
						.attr("value", name)
						.attr("type", "text")
						.attr("placeholder", "Name...")
						.attr("autocomplete", "off");
			let mm = ident.append("div").classed("eq-make-model", true);
			mm.append("input").classed("eq-make", true)
						.attr("name", "eq-make")
						.attr("value", make)
						.attr("type", "text")
						.attr("placeholder", "Manufacturer...")
						.attr("autocomplete", "off");
			mm.append("input").classed("eq-model", true)
						.attr("name", "eq-model")
						.attr("value", model)
						.attr("type", "text")
						.attr("placeholder", "Model...")
						.attr("autocomplete", "off");
			self.locs = content.append("div").classed("eq-modal-locations", true);
			self.locs.append("h1").classed("modal-header", true).html("Locations");
			for (let i = 0; i < locations.length; i++) {
				let loc = self.locs.append("div").classed("eq-modal-location", true);
				loc.append("input").classed("eq-modal-room", true)
						.attr("name", "eq-room[]")
						.attr("value", locations[i].room)
						.attr("type", "text")
						.attr("placeholder", "Room")
						.attr("autocomplete", "off");
				loc.append("input").classed("eq-modal-storage", true)
						.attr("name", "eq-storage[]")
						.attr("value", locations[i].storage)
						.attr("type", "text")
						.attr("placeholder", "Storage...")
						.attr("autocomplete", "off");
			}
			self.locs.append("i").classed("fa fa-plus fa-lg", true)
										.attr("id", "add-location")
										.attr("aria-hidden", "true");

			let amts = content.append("div").classed("eq-modal-amounts", true);
			amts.append("h1").classed("modal-header", true).html("Amounts");
			let amt1 = amts.append("div").classed("eq-modal-amount total", true);
			amt1.append("input").classed("eq-modal-total", true)
						.attr("name", "eq-total")
						.attr("value", total)
						.attr("type", "text")
						.attr("autocomplete", "off");
			amt1.append("h3").html("Total");
			let amt2 = amts.append("div").classed("eq-modal-amount service", true);
			amt2.append("input").classed("eq-modal-service", true)
						.attr("name", "eq-service")
						.attr("value", service)
						.attr("type", "text")
						.attr("autocomplete", "off");
			amt2.append("h3").html("In Service");
			let amt3 = amts.append("div").classed("eq-modal-amount repair", true);
			amt3.append("input").classed("eq-modal-repair", true)
						.attr("name", "eq-repair")
						.attr("value", repair)
						.attr("type", "text")
						.attr("autocomplete", "off");
			amt3.append("h3").html("Under Repair");

			let dcs = content.append("div").classed("eq-modal-docs", true);
			dcs.append("h1").classed("modal-header", true).html("Documents");
			for (let i = 0; i < docs.length; i++) {
				let dc = dcs.append("div").classed("eq-modal-doc", true);
				dc.append("i").classed("fa fa-file-o", true).attr("aria-hidden", "true");
				dc.append("a").attr("href", docs[i].path).attr("target", "_blank").html(docs[i].name);
			}

			let footer = modal.append("div").classed("eq-modal-footer", true);
			footer.append("h3").classed("eq-modal-confirm", true).html("Submit");
		}

		self._setEventListeners = function() {
			$(document).on("click", ".modal-screen", self.removeForm);

			$(document).on("click", ".eq-modal", function(e) {
				e.stopPropagation();
			});

			$(document).on("click", ".modal-close-button", self.removeForm);

			$(document).on("click", "#add-location", function(e) {
				let loc = self.locs.insert("div", "#add-location").classed("eq-modal-location", true);
				loc.append("input").classed("eq-modal-room", true)
						.attr("name", "eq-room[]")
						.attr("value", "")
						.attr("type", "text")
						.attr("placeholder", "Room...")
						.attr("autocomplete", "off");
				loc.append("input").classed("eq-modal-storage", true)
						.attr("name", "eq-storage[]")
						.attr("value", "")
						.attr("type", "text")
						.attr("placeholder", "Storage...")
						.attr("autocomplete", "off");
			});

			$(document).on("click", ".eq-modal-footer", function(e) {
				e.preventDefault();
				let dat = $(e.target).serialize();
				console.log(dat)
				$.post(siteroot + "/php/modifyEquipDB.php", dat + "&eq-id=" + self.id, function(data) {
					self.removeForm();
				});
			});
		}

		self.removeForm = function() {
			self.modalmask.remove();
			$("main").removeClass("blurred-page");
			$(document).off("click", ".modal-screen");
			$(document).off("click", ".eq-modal");
			$(document).off("click", ".modal-close-button");
			$(document).off("click", "#add-location");
			$(document).off("click", ".eq-modal-footer");
		}

		self._loadEquipDB();
		self._setEventListeners();
		$("main").addClass("blurred-page");
	}
}