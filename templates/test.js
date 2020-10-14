var isDown = false;
var startX;
var startY;
var endX;
var endY;
var width;
var height;
var cList = [];
let num = 10;

function getImageCoords(event,img)
{
	//get the image coordinates
	var posX = event.offsetX ? (event.offsetX) : event.pageX - img.offsetLeft;
	var posY = event.offsetY ? (event.offsetY) : event.pageY - img.offsetTop;

	//psuhing the coordinates to the list
	cList.push([posX,posY]);

	if (cList.length > 4)
	{
		cList = [];

	}

	imgPnts = ("[" + "["+cList[0]+"]" + "," + "["+cList[1]+"]" + "," + "["+cList[2]+"]" +","+ "["+cList[3]+"]" +"]")

	//set the value of imgPntsTransform to this
	document.getElementById("imgPntsTransform").value = imgPnts;
	console.log(imgPntsTransform.value)
		

	document.getElementById("pnt1Transform").value = "["+cList[0]+"]"
	document.getElementById("pnt2Transform").value = "["+cList[1]+"]"
	document.getElementById("pnt3Transform").value = "["+cList[2]+"]"
	document.getElementById("pnt4Transform").value = "["+cList[3]+"]"
			
			
	document.getElementById("countNum").value = "(int("+num+"*rawimagescale)"
	
	//testing variable
	console.log(imgPnts)
	console.log(cList)
			
}

function handleMouseDown(e) 
{
	//instantiate variables
	var $canvas = $("#my_canvas");
	var canvasOffset = $canvas.offset();
	var offsetX = canvasOffset.left;
	var offsetY = canvasOffset.top;
	var scrollX = $canvas.scrollLeft();
	var scrollY = $canvas.scrollTop();

	e.preventDefault();
	e.stopPropagation();

	// save the starting x/y of the rectangle
	startX = parseInt(e.clientX - offsetX);
	startY = parseInt(e.clientY - offsetY);
					
				  
	console.log(endX)
	console.log(endY)
	// set a flag indicating the drag has begun
	isDown = true;
}

function handleMouseUp(e) 
{
	//instantiate variables
	var $canvas = $("#my_canvas");
	var canvasOffset = $canvas.offset();
	var offsetX = canvasOffset.left;
	var offsetY = canvasOffset.top;
	var scrollX = $canvas.scrollLeft();
	var scrollY = $canvas.scrollTop();

	e.preventDefault();
	e.stopPropagation();

	endX = parseInt(e.clientX - offsetX);
	endY = parseInt(e.clientY - offsetY);
	console.log(endX)
	console.log(endY)

	// the drag is over, clear the dragging flag
	isDown = false;
}

function handleMouseOut(e) 
{
	//instantiate variables
	var $canvas = $("#my_canvas");
	var canvasOffset = $canvas.offset();
	var offsetX = canvasOffset.left;
	var offsetY = canvasOffset.top;
	var scrollX = $canvas.scrollLeft();
	var scrollY = $canvas.scrollTop();

	e.preventDefault();
	e.stopPropagation();
		  
	if (isDown) 
	{
		endX = parseInt(e.clientX - offsetX);
		endY = parseInt(e.clientY - offsetY);
		console.log(endX)
		console.log(endY)
	}


	// the drag is over, clear the dragging flag
	isDown = false;
}

			

function handleMouseMove(e) {
	//instantiate variables
	var $canvas = $("#my_canvas");
	var canvasOffset = $canvas.offset();
	var offsetX = canvasOffset.left;
	var offsetY = canvasOffset.top;
	var scrollX = $canvas.scrollLeft();
	var scrollY = $canvas.scrollTop();
	var ctx = document.getElementById("my_canvas").getContext("2d");
	var img = document.getElementById("canvas_image")
	//ctx.drawImage(img,0,0)
		


	e.preventDefault();
	e.stopPropagation();
	  
	endX = parseInt(e.clientX - offsetX);
	endY = parseInt(e.clientY - offsetY);

	// if we're not dragging, just return
	if (!isDown) 
	{
		return;
	}

	// get the current mouse position
	mouseX = parseInt(e.clientX - offsetX);
	mouseY = parseInt(e.clientY - offsetY);

	// Put your mousemove stuff here

	// clear the canvas
	ctx.clearRect(0, 0, my_canvas.width, my_canvas.height);
	ctx.drawImage(img,0,0,my_canvas.width, my_canvas.height)
	// calculate the rectangle width/height based
	// on starting vs current mouse position
	var width = mouseX - startX;
	var height = mouseY - startY;
				
	console.log("start(X)" + startX + "\tstart(Y)"+startY)
	// draw a new rect from the start position 
	// to the current mouse position
	ctx.strokeRect(startX, startY, width, height);
				
	if (isDown)
	{
		// console.log("mouseX" + mouseX + "\tmouseY" + mouseY)
		// console.log("width" + width + "\theight" + height)
		testCoords = ("("+startX.toString()+ "," + (startY.toString())+ "," + (width.toString()) + "," + (height.toString())+")")
		// console.log(testCoords)
		document.getElementById("imgRotRoi_window").value = testCoords
			
		document.getElementById("startX_Coord").value = startX
		document.getElementById("startY_Coord").value = startY
		document.getElementById("width_Coord").value = width
		document.getElementById("height_Coord").value = height
	}
				
}