var editor = CodeMirror.fromTextArea(codeAr, {
    lineNumbers: true
});

window.setInterval(updateCode, 2500);

function updateCode(){
    $.get("/get_buffered", function(data, status){
        console.log(data);
    });
}

/*
//check for browser support
if(typeof(EventSource)!=="undefined") {
//create an object, passing it the name and location of the server side script
	var eSource = new EventSource("codeCreation.py");
	//detect message receipt
	eSource.onmessage = function(event) {
		//write the received data to the page
		document.getElementById("changeMe").innerHTML = event.data;
	};
} else {
	document.getElementById("changeMe").innerHTML="Whoops! Your browser doesn't receive server-sent events.";
}
*/