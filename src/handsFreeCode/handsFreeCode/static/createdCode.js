/*var editor = CodeMirror.fromTextArea(codeAr, {
    lineNumbers: true
});*/

window.setInterval(updateCode, 50);

function updateCode(){
    $.getJSON("/get_new_cont", function(content){
        if (!content.hasChanged){
            return null;
        }
        console.log(content);
        codeAr = document.getElementById("codeArForNow");

        //append lines
        for (var i = 0; i<content.appendLines.length; i++) {
            console.log(content.appendLines[i]);
            var line = document.createElement("span");
            line.id = "line"+codeAr.childNodes;
            line.innerHTML = content.appendLines[i];
            codeAr.appendChild(line);
        }

    });
}