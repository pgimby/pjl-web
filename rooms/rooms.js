
function roomMouseOver(d) {
	if (d != "none" && !d.endsWith("Stairs")) {
		switch (d) {
			case "042":
				$("#room-name").html("Development Room");
				break;
			case "042A":
				$("#room-name").html("Server Room");
				break;
			case "046":
				$("#room-name").html("SOAR Workspace");
				break;
			case "09":
				$("#room-name").html("Rutherford Scattering Experiment");
				break;
			case "09A":
				$("#room-name").html("Nuclear Decay Experiment");
				break;
			case "09B":
				$("#room-name").html("Photoelectric Effect Experiment");
				break;
			case "026":
				$("#room-name").html("Hugo Graumann Memorial Computational Physics Lab");
				break;
			case "025":
				$("#room-name").html("Study Room");
				break;
			case "025A":
				$("#room-name").html("Storage Room");
				break;
			case "029":
				$("#room-name").html("Radiation Lab");
				break;
			case "039":
				$("#room-name").html("Workshop");
				break;
			case "050":
				$("#room-name").html("Vacuum Lab");
				break;
			default:
				$("#room-name").html("");
		}
		$("#room-number").html("Room " + d);
	} else if (d.endsWith("Stairs")) {
		$("#room-number").html(d);
		$("#room-name").html("...they're stairs. I don't know what else to tell you.");
	} else {
		$("#room-number").html("");
		$("#room-name").html("");
	}

}


function mouseLeftRoom() {
	$("#room-number").html("");
	$("#room-name").html("");
}


function roomClick(e) {
	$("#click").html("CLICK")
	setTimeout(function(){
		$("#click").html("")
	}, 100);
	var room = e.target.getAttribute("id").slice(1,)
	window.open("http://ucmapspro.ucalgary.ca/RoomFinder/?Building=ST&Room=" + room, "target=_blank");
}