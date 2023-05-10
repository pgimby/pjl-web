/*---------------------------------------------------------------------
 Video Analysis Tool for University of Calgary Physics Labs
 Created by Christopher Cully
 2020 May 07

 version 1.5
 last revision 2020 May 07
 
 Copyright 2020, Christopher Cully
 This file is licensed under Creative Commons Attribution 4.0.
 If you find this software useful, please let me know:
 cmcully@ucalgary.ca
---------------------------------------------------------------------*/

'use strict';

// ----------------------------- Controls Functions ----------------------------------
var controlState={playLeft:50, skipLeft:100, sliderLeft: 150, sliderWidth:250, state:"paused", active:true};
function controlsDrawPlayButtons(){
  var ctx = controlsCanvas.getContext("2d");
  var h = controlsCanvas.offsetHeight;
  var left=0;
    
  // Skip button (-1 frame)
  left=0;
  ctx.beginPath();
  ctx.moveTo(left+h*7/8,h*7/8);
  ctx.lineTo(left+h*2/8,h*0.5);
  ctx.lineTo(left+h*7/8,h*1/8);
  ctx.rect(left+h*1/8,h*1/8,h*1/8,h*6/8);
  if (controlState.state=="paused") ctx.fillStyle="white";
	else ctx.fillStyle="grey";
  ctx.fill();

  // Play/pause button
  controlState.playLeft = 1*h;
  left=controlState.playLeft;
  ctx.beginPath();
  ctx.rect(left,0,h,h);
  ctx.fillStyle="#303030";
  ctx.fill();
  if (controlState.state=="paused") {
	// draw play button
    ctx.beginPath();
    ctx.moveTo(left+h*0.25,h*7/8);
    ctx.lineTo(left+h*7/8,h*0.5);
    ctx.lineTo(left+h*0.25,h*1/8);
    ctx.fillStyle="white";
    ctx.fill();
  } else {
	// draw pause button
    ctx.beginPath();
    ctx.rect(left+h*1/8,h*1/8,h*1/4,h*3/4);
    ctx.rect(left+h*5/8,h*1/8,h*1/4,h*3/4);
    ctx.fillStyle="white";
    ctx.fill();
  }  

  // Skip button (+1 frame)
  controlState.skipLeft = 2*h;
  left=controlState.skipLeft;
  ctx.beginPath();
  ctx.moveTo(left+h*1/8,h*7/8);
  ctx.lineTo(left+h*6/8,h*0.5);
  ctx.lineTo(left+h*1/8,h*1/8);
  ctx.rect(left+h*6/8,h*1/8,h*1/8,h*6/8);
  if (controlState.state=="paused") ctx.fillStyle="white";
	else ctx.fillStyle="grey";
  ctx.fill();

}

function controlsDrawSlider(){
  var ctx = controlsCanvas.getContext("2d");
  var h = controlsCanvas.offsetHeight;
  var w = controlsCanvas.offsetWidth;

  // Layout
  if (w > 4.5*h){
    controlState.sliderLeft = 3.25*h;
    controlState.sliderWidth = w-3.5*h;
  } else {
    controlState.sliderLeft = -1;
    controlState.sliderWidth = 0;
	return;
  }
  
  // Draw the slider background
  ctx.beginPath();
  ctx.rect(controlState.sliderLeft,h/8,controlState.sliderWidth,h*3/4);
  ctx.fillStyle="#A0A0A0";
  ctx.fill();
  
  // Draw the slider
  var pos = myVideo.currentTime/myVideo.duration;
  if (isFinite(pos)) {
    ctx.beginPath();
    ctx.rect(controlState.sliderLeft,h*3/16,controlState.sliderWidth*pos,h*5/8);
    ctx.fillStyle="white";
    ctx.fill();
	
	if (controlState.active) ctx.fillStyle = "black";
	else ctx.fillStyle = "grey";
    ctx.font = "20px Arial";
    var txt = myVideo.currentTime.toFixed(3) + ' s ';
    ctx.fillText(txt, controlState.sliderLeft+10, h*0.75);
  }
}

function controlsSetup(){
  // Make the actual control canvas size equal to the DOM size
  controlsCanvas.width=controlsCanvas.offsetWidth;
  controlsCanvas.height=controlsCanvas.offsetHeight;
  
  // Draw background
  var ctx = controlsCanvas.getContext("2d");
  ctx.beginPath();
  ctx.rect(0,0,controlsCanvas.offsetWidth,controlsCanvas.offsetHeight);
  ctx.fillStyle="#303030";
  ctx.fill();

  // Draw everything else  
  controlsDrawPlayButtons();
  controlsDrawSlider();
  
  // Add the event listeners
  controlsCanvas.addEventListener("click",controlsClicked,false);
}

function controlsClicked(event){
  var h = controlsCanvas.offsetHeight;

  if (controlState.active==false) {
    return;
  }

  if (event.offsetX < h){
	// Skip backward button pressed
    videoSkipBack();
	return;
  }

	  
  if ((event.offsetX >  controlState.playLeft) && 
      (event.offsetX < (controlState.playLeft + h))) {
	// Play/pause button pressed
	if (controlState.state=="paused"){
		controlState.state="playing";
		videoPlay();
	} else{
		controlState.state="paused";
		videoPause();
	}
	controlsDrawPlayButtons();
	return;
  }

  if ((event.offsetX >  controlState.skipLeft) && 
      (event.offsetX < (controlState.skipLeft + h))) {
	// Skip button pressed
    videoSkipForward();
	return;
  }
  
  if ((event.offsetX >  controlState.sliderLeft) &&
      (event.offsetX < (controlState.sliderLeft + controlState.sliderWidth))) {
	// Slider pressed
	var pos = (event.offsetX - controlState.sliderLeft)/controlState.sliderWidth;
	videoSeekTo(pos*myVideo.duration);
  }

}



// ----------------------------- Video Functions ----------------------------------
var buffCanvas, buffContext, currentFrame, prevFrame,videoDt,videoT0;
var videoSetup = false;
function videoPlay(){
  myVideo.play();
}

function videoPause(){
  myVideo.pause();
  videoSyncFrame();
}

function videoEnded(){
  myVideo.pause();
  controlState.state="paused";
  videoTimeUpdateCallback();
  controlsDrawPlayButtons();
}

function videoSeekTo(seekTime){
  myVideo.currentTime=seekTime;
  if (myVideo.paused) videoSyncFrame();
}

function videoSkipBack(){
  if (myVideo.currentTime > (videoDt+0.01))
    myVideo.currentTime-= videoDt;
}

function videoSkipForward(){
  if (myVideo.currentTime < (myVideo.duration - videoDt - 0.01))
    myVideo.currentTime+= videoDt;	
}

function videoSyncFrame(){
// Synchronizes time to middle of current frame
  var currFrame = Math.round((myVideo.currentTime-videoT0)/videoDt);
  myVideo.currentTime = videoT0+videoDt*currFrame;
  videoTimeUpdateCallback();
}

function videoTimeUpdateCallback(){
  if (videoSetup){
    controlsDrawSlider();
    updateCanvas();
  }
}

function videoIsNewFrame(){
  buffContext.drawImage(myVideo, 0, 0, myVideo.videoWidth,myVideo.videoHeight);
  currentFrame=buffContext.getImageData(0,0,myVideo.videoWidth,myVideo.videoHeight);
  for (var i=0;i<(currentFrame.data.length-1);i+=Math.round(currentFrame.data.length/1000)){
	if(currentFrame.data[i] != prevFrame.data[i]){
 	  return true;
	}
  }
  return false;
}

var videoNextFrameState={state:"init",trange:[0,0],dt:0,resolve: function(){},reject: function(){},
                         timestamps:[], calledAsPromise: false};
function videoNextFrame(argin){

  // Default: seek forward. But, if passed a number as arg, use that direction.
  var dir = 1.0;
  if (!isNaN(argin)) dir = argin;
	  
  switch(videoNextFrameState.state){
    case "init":
      // Don't do anything if already playing or almost finished
      if(!myVideo.paused) return;
      if (myVideo.currentTime > (myVideo.duration - 1/30)) return;
	  
      // turn off the time updates while playing forward in slow motion
      myVideo.removeEventListener("timeupdate",videoTimeUpdateCallback);
      controlState.active=false;  

      // Capture the current frame and set up the initial guess at the timerange.
      prevFrame = buffContext.getImageData(0,0,myVideo.videoWidth,myVideo.videoHeight);
	  videoNextFrameState.dt=1/60*dir;
	  videoNextFrameState.trange=[myVideo.currentTime,myVideo.currentTime+videoNextFrameState.dt];	  
	  myVideo.addEventListener("seeked",videoNextFrame);

     // Skip forward by dt to check the end of the current interval
	  myVideo.currentTime+=videoNextFrameState.dt;
	  videoNextFrameState.state="refine";
	  return;  // "seeked" callback is  active
	  break;
	case "refine":
	  // Seek is done. Check if it's a new frame. If not, try the next interval
	  if ((videoNextFrameState.trange[0] > 0) && (videoNextFrameState.trange[1] < myVideo.duration) &&!videoIsNewFrame()){
		  videoNextFrameState.trange[0]+=videoNextFrameState.dt;
		  videoNextFrameState.trange[1]+=videoNextFrameState.dt;
		  myVideo.currentTime+=videoNextFrameState.dt;
		  return;  // "seeked" callback is still active
	  } else {
		  // New frame. Draw on canvas to cover the back-and-forth
		  videoTimeUpdateCallback();
		  
		  // New frame. Try stepping with a smaller increment.
		  videoNextFrameState.dt/=2;
		  if (videoNextFrameState.dt < 0.0001){
			// Done. Time has been found. Cancel the callback and finish up.
			controlState.active=true;
            videoTimeUpdateCallback();
			myVideo.removeEventListener("seeked",videoNextFrame); 
  	        myVideo.addEventListener("timeupdate",videoTimeUpdateCallback);
		  	videoNextFrameState.state="init";
			
			// Function is called as a promise when building up the initial timing model.
			if (videoNextFrameState.calledAsPromise){
			  videoNextFrameState.calledAsPromise = false;
              videoNextFrameState.timestamps.push(videoNextFrameState.trange[0]+videoNextFrameState.dt/2);		  
			  videoNextFrameState.resolve();
			}
	        return;
          }
		  myVideo.currentTime-=videoNextFrameState.dt;
		  videoNextFrameState.trange[1]=myVideo.currentTime;
		  return;  // "seeked" callback still active
	  }
	  break;
  } 
}

function videoNextFramePromise(){
  return new Promise(function(resolve, reject) {
    videoNextFrameState.resolve=resolve;
    videoNextFrameState.reject=reject;
	videoNextFrameState.calledAsPromise=true;
    videoNextFrame(resolve, reject);
  });
}

function videoLoaded(){  
  // Wait for the video to be ready and paused
  if(myVideo.seeking || (myVideo.readystate < 2)){
	setTimeout(videoLoaded,5);
	return;
  }
  console.log("Checking timing.");
  myVideo.pause();
  
  // Reduce the playback speed
  try {myVideo.playbackRate=0.25;}
  catch(err){ console.log("Cannot reduce playback rate."); }

  // Set up the buffer canvas
  buffCanvas = document.createElement('canvas');
  buffCanvas.width = myVideo.videoWidth;
  buffCanvas.height = myVideo.videoHeight;
  buffContext = buffCanvas.getContext('2d');
  
  // Blank canvas to hide video
  myCanvas.width = myCanvas.offsetWidth;
  myCanvas.height = myCanvas.offsetHeight;
  var ctx = myCanvas.getContext("2d");
  ctx.beginPath();
  ctx.rect(0,0,myCanvas.width,myCanvas.height);
  ctx.fillStyle="#A0A0A0";
  ctx.fill();

  // Initialize the timing model.
  var fps=prompt("Please enter your video frame rate (fps), or have the browser try to auto-detect it by entering 'auto' or hitting 'cancel'.","30.0")  
  var manualFramerateMode=true;
  if (fps == null) fps="auto";
  if (fps.search("uto")>0) manualFramerateMode=false;
  framerateText.style.display = "block";
  
  if (manualFramerateMode) {
	console.log("Manual framerate mode.");
	fps = parseFloat(fps);
	if (isNaN(fps)) fps=30.0;
    videoDt = 1/fps;
    videoT0=videoDt/2;
    videoSetup = true;
 	framerateText.innerHTML = "Manually-set video frame rate is "+(1/videoDt).toFixed(2)+" fps.";
    controlsSetup();
    initCanvas();
  } else {
	console.log("Auto-detecting framerate.");
    ctx.fillStyle = "black";
    ctx.font = "20px Arial";
    ctx.fillText("Checking your video's timing.", 50, myCanvas.height/2);
    ctx.fillText("  Please wait.", 50, myCanvas.height/2+30);
	
    videoNextFramePromise()
    .then(fn => videoNextFramePromise())
    .then(fn => {
        ctx.fillText("    10% done.", 50, myCanvas.height/2+60);
	    return new Promise(function(resolve, reject) {resolve()});
	})
    .then(fn => videoNextFramePromise())
    .then(fn => videoNextFramePromise())
    .then(fn => {
		// Calculate frames per second based on the above transitions, then skip forward by 1 second
		var dt = (videoNextFrameState.timestamps[3]-videoNextFrameState.timestamps[2]);
	    console.log("fps (frame 2-3): "+ 1/dt);	
        ctx.fillText("    50% done.", 50, myCanvas.height/2+90);
        myVideo.currentTime+=dt*(Math.round(1/dt)-0.5);
		// Proceed once the video is done seeking
	    return new Promise(function(resolve, reject) {
			myVideo.addEventListener("seeked",resolve());
		});
	})
    .then(fn => videoNextFramePromise())
    .then(fn => videoNextFramePromise())
    .then(fn => videoNextFramePromise())
    .then(fn => {
		// Calculate the frame rate
	    console.log("Time stamps: "+ videoNextFrameState.timestamps);
		var dt1 = (videoNextFrameState.timestamps[3]-videoNextFrameState.timestamps[2]);
		var dt2 = (videoNextFrameState.timestamps[6]-videoNextFrameState.timestamps[2]);
		var nframes = Math.round(dt2/dt1);
		console.log("fps (frames 1-"+(nframes+1)+"): ",nframes/dt2);
		videoDt=dt2/nframes;
        videoT0=videoNextFrameState.timestamps[2]+videoDt/2;
		// Set the video in the exact middle of one of the frames
		myVideo.currentTime=videoT0;
		// Proceed once the video is done seeking
	    return new Promise(function(resolve, reject) {
			myVideo.addEventListener("seeked",resolve());
		});
	})
    .then(fn =>{				
        // Set up the controls
	    console.log("Video setup done.");
 		framerateText.innerHTML = "Auto-detected video frame rate is "+(1/videoDt).toFixed(2)+" fps.";
		videoSetup = true;
        controlsSetup();
        initCanvas();
	    console.log("Setup done.");
	});
  }
}



// ----------------------------- Canvas Functions ----------------------------------
var canvasState={zoomed:false,zoomX:0,zoomY:0,letterboxCorner:[0,0], letterboxSize:[0,0], forceRotate: false};
var canvasBuffer;

function initCanvas() {
  // Make the actual control canvas size equal to the DOM size
  myCanvas.width = myCanvas.offsetWidth;
  myCanvas.height = myCanvas.offsetHeight;
    
  // Initialize canvas state and callback
  myCanvas.addEventListener("click",imageClicked,false);
  myCanvas.addEventListener("mousemove",imageHover,false);
  myCanvas.addEventListener("mouseout",imageMouseout,false);
  canvasState.zoomed=false;
  
  // If the video isn't loaded yet, return.
  if (myVideo.readyState<2) return;
  
  // Calculate letterboxed video boundaries
  var videoAspect = myVideo.videoHeight/myVideo.videoWidth;
  var canvasAspect = myCanvas.height/myCanvas.width;  
  if (videoAspect > canvasAspect){
    // Letterboxing on the sides
	var videoWidth=myCanvas.height/videoAspect;
	canvasState.letterboxCorner=[(myCanvas.width-videoWidth)/2,0];
	canvasState.letterboxSize=[videoWidth,myCanvas.height];
  } else {
    // Letterboxing top/bottom
	var videoHeight=myCanvas.width*videoAspect;
	canvasState.letterboxCorner=[0,(myCanvas.height-videoHeight)/2];
	canvasState.letterboxSize=[myCanvas.width,videoHeight];
  }
  
  // Check for special case of Firefox with portrait orientation video:
  // Note: Opera on Mac may have the same problem.
  if(navigator.userAgent.search("irefox") > 0){
	console.log("WARNING: Firefox browser detected. Known browser issues with portrait-orientation videos.");
	if (myVideo.videoWidth < myVideo.videoHeight){
      console.log("  Video is portrait orientation. Will try to compensate for browser bug 1423850.");
  	  canvasState.forceRotate = true;
	  // allocate buffer for off-screen rotation
      canvasBuffer = document.createElement('canvas');
      canvasBuffer.width = myCanvas.offsetHeight;
      canvasBuffer.height = myCanvas.offsetWidth;
      var buffCtx = canvasBuffer.getContext('2d');
	  buffCtx.translate(myCanvas.offsetHeight,0);  // set rotation pivot point
	  buffCtx.rotate(Math.PI/2);                   // set canvas rotation
	} else console.log("  Video is landscape orientation.");
  }
  
  // Update the canvas
  updateCanvas();
}


function updateCanvas(){  
  var ctx = myCanvas.getContext("2d");
  
  // Set the cursor type
  if (!myVideo.paused) myCanvas.style.cursor="default";
    else if (canvasState.zoomed) myCanvas.style.cursor="crosshair";
	else myCanvas.style.cursor="zoom-in";
	
  // Clear anything else on the canvas
  ctx.clearRect(0, 0, myCanvas.width, myCanvas.height);


  // Render zoomed-in from video to canvas
  if (canvasState.forceRotate){
    // Rotation metadata not properly supported (Firefox):
    // Known bug in Firefox: https://bugzilla.mozilla.org/show_bug.cgi?id=1423850
    // May be present in Mac versions of Opera, too: https://blog.addpipe.com/mp4-rotation-metadata-in-mobile-video-files/
	
    var buffCtx = canvasBuffer.getContext('2d');  // (rotated buffer)
    //context.drawImage(img,sx,sy,
	//                  swidth,sheight,
    //                  x,y,width,height);
    if (canvasState.zoomed){
      // Blank canvas
      var ctx = myCanvas.getContext("2d");
      ctx.beginPath();
      ctx.rect(0,0,myCanvas.width,myCanvas.height);
      ctx.fillStyle="white";
      ctx.fill();
	  // render image
   	  buffCtx.drawImage(myVideo,canvasState.zoomY,myVideo.videoWidth-canvasState.zoomX-myCanvas.width,
	                        myCanvas.height,myCanvas.width,
	                        0,0,myCanvas.offsetWidth,myCanvas.offsetHeight);
  	  ctx.drawImage(canvasBuffer,0,0,
	                myCanvas.offsetHeight,myCanvas.offsetWidth,
	                0,0,myCanvas.offsetWidth,myCanvas.offsetHeight);
	} else{
  	  buffCtx.drawImage(myVideo,0,0,myVideo.videoHeight,myVideo.videoWidth,
	                        0,0,myCanvas.offsetWidth,myCanvas.offsetHeight);
  	  ctx.drawImage(canvasBuffer,0,0,
	                myCanvas.offsetHeight,myCanvas.offsetWidth,
	                canvasState.letterboxCorner[0],canvasState.letterboxCorner[1],
	                canvasState.letterboxSize[0],canvasState.letterboxSize[1]);
	}
  } else {
    // Rotation metadata fully supported (Chrome/Edge/Opera/Safari):
    if (canvasState.zoomed){
      // Blank canvas
      var ctx = myCanvas.getContext("2d");
      ctx.beginPath();
      ctx.rect(0,0,myCanvas.width,myCanvas.height);
      ctx.fillStyle="white";
      ctx.fill();
	  // render image
	  // Cafeful with out-of-bounds (e.g. negative) pixels on the video. Safari does not like them.
	  var w=Math.min(myCanvas.width,myVideo.videoWidth);
	  var h=Math.min(myCanvas.height,myVideo.videoHeight);
	  ctx.drawImage(myVideo,Math.max(canvasState.zoomX,0),Math.max(canvasState.zoomY,0),w,h,
	                  Math.max(-canvasState.zoomX,0),Math.max(-canvasState.zoomY,0),w,h); 
	} else
		ctx.drawImage(myVideo,0,0,myVideo.videoWidth,myVideo.videoHeight,
	                  canvasState.letterboxCorner[0],canvasState.letterboxCorner[1],
	                  canvasState.letterboxSize[0],canvasState.letterboxSize[1]);
		
  }
  
  // Draw zoom out icon
  if (canvasState.zoomed){
    ctx.beginPath();
    ctx.rect(myCanvas.width-60, myCanvas.height-60,51,51);
    ctx.fillStyle="rgba(255,255,255,0.5)";
    ctx.fill();
    ctx.beginPath();
    ctx.arc(myCanvas.width-40, myCanvas.height-40, 15, 0, 2 * Math.PI);
    ctx.strokeStyle = "black";
    ctx.lineWidth=3;
    ctx.stroke();
    ctx.moveTo(myCanvas.width-50, myCanvas.height-40);
    ctx.lineTo(myCanvas.width-30, myCanvas.height-40);
    ctx.stroke();
    ctx.moveTo(myCanvas.width-40+15/Math.sqrt(2), myCanvas.height-40+15/Math.sqrt(2));
    ctx.lineTo(myCanvas.width-40+25, myCanvas.height-40+25);
    ctx.stroke();
  }
 }

function imageClicked(event){	
  if(!myVideo.paused) return;
	
  if(canvasState.zoomed){
	if (event.offsetX > (myCanvas.width-60))
	  if (event.offsetY > (myCanvas.height-60)){
	    // User selected zoom out tool
		canvasState.zoomed=false;
		tooltip.style.display="none";
		updateCanvas();
		return;
	  }

    // Add time/x/y data to table
    var row = resultsTable.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    cell1.innerHTML = myVideo.currentTime.toFixed(3);
    cell2.innerHTML = (event.offsetX + canvasState.zoomX).toFixed(0);
    cell3.innerHTML = (myVideo.videoHeight - (event.offsetY + canvasState.zoomY)).toFixed(0);
	
	// Blank canvas
	var ctx = myCanvas.getContext("2d");
	ctx.beginPath();
    ctx.rect(0,0,myCanvas.width,myCanvas.height);
    ctx.fillStyle="white";
    ctx.fill();

    // Zoom out and move to next frame
    videoSkipForward();
  } else {
	// Calculate corner of zoom region
	
    if (myVideo.videoWidth < myCanvas.width){
	  canvasState.zoomX = (myVideo.videoWidth - myCanvas.width)/2;
	} else {
	  canvasState.zoomX = (event.offsetX-canvasState.letterboxCorner[0])/canvasState.letterboxSize[0]*myVideo.videoWidth;
	  canvasState.zoomX-=myCanvas.width/2;
	  if (canvasState.zoomX < 0) canvasState.zoomX=0;
	  if (canvasState.zoomX > (myVideo.videoWidth-myCanvas.width)) canvasState.zoomX=(myVideo.videoWidth-myCanvas.width);
	}
    if (myVideo.videoHeight < myCanvas.height){
	  canvasState.zoomY = (myVideo.videoHeight - myCanvas.height)/2;
	} else {
      canvasState.zoomY = (event.offsetY-canvasState.letterboxCorner[1])/canvasState.letterboxSize[1]*myVideo.videoHeight;
      canvasState.zoomY-=myCanvas.height/2;
      if (canvasState.zoomY < 0) canvasState.zoomY=0;
      if (canvasState.zoomY > (myVideo.videoHeight-myCanvas.height)) canvasState.zoomY=(myVideo.videoHeight-myCanvas.height);
    }

	// Zoom in
	canvasState.zoomed=true;
	updateCanvas();
  }
}

function imageHover(e){
  if (canvasState.zoomed){
	var x,y;
    // Activate and position tooltip canvas
    tooltip.style.display="block";
	y=e.y+15;
	if (y < 30) y=30;
	if (y > myCanvas.height) y = myCanvas.height;
    tooltip.style.top=y+"px";
	if(e.x < myCanvas.width - 150)
      tooltip.style.left=(e.x+65)+"px";
    else
	  tooltip.style.left=(e.x-80)+"px";
	
	// Update text for present position (in the image)
	x = (event.offsetX + canvasState.zoomX).toFixed(0);
    y = (myVideo.videoHeight - (event.offsetY + canvasState.zoomY)).toFixed(0);
    tooltiptext.innerHTML="("+x+", "+y+")";
  }
}

function imageMouseout(){
  tooltip.style.display="none";
}

// ----------------------------- Top-level Functions ----------------------------------
function setupPage(){  
  // Hide the file selector. Show the video and table.
  uploadBtnWrapper.style.display = "none";
  outsideWrapper.style.display = "block";
  resultsDiv.style.display = "block";
  resultsActionsDiv.style.display = "block";
  controlsWrapper.style.display = "block";
  tooltip.style.display="none";

  // Initialize the video
  console.log("Loading video.");
  myVideo.src = URL.createObjectURL(fileSelector.files[0]);
  myVideo.addEventListener("loadeddata", videoLoaded);
  myVideo.addEventListener("resize", initCanvas);
  myVideo.addEventListener("timeupdate",videoTimeUpdateCallback);
  myVideo.addEventListener("ended",videoEnded);
  myVideo.addEventListener("error", function() {
    var msg = "ERROR loading/playing video. Check the developer console for details.";
    if(navigator.userAgent.search("irefox") > 0){
      msg += " Firefox has several known bugs with HTML5 and cellphone video;";
      msg += " another browser (e.g. Google Chrome) may work better.";
    }
    alert(msg);
  });
  myVideo.muted=true;
  myVideo.pause();

 }

function removeRow(){
  if (resultsTable.rows.length > 1)
    resultsTable.deleteRow(-1);
}

function exportCSV(){
  if (resultsTable.rows.length > 1){
	// Create CSV string
    var csv = [];
    for (var i = 0; i < resultsTable.rows.length; i++) {
        var row = [];
		var cols = resultsTable.rows[i].querySelectorAll("td, th");
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        csv.push(row.join(","));        
    }
	csv=csv.join("\n");
    
    // Create CSV file, attach to (hidden) download link and click it
	var csvFile, downloadLink;
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement("a");
    downloadLink.download = "position_vs_time.csv";
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
  }
}

function winResize(){
  controlsSetup();
  initCanvas();
}

framerateText.style.display = "none";
document.querySelector('#fileSelector').addEventListener('change', setupPage, false);
window.addEventListener('resize',winResize,false);
