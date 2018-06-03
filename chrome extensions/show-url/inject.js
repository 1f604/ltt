
function doit() {
    var start = " |url:";

    if (document.title.indexOf(start) == -1) {
        document.title += start + location.href;
    }
}
//script from here: https://stackoverflow.com/questions/18214826/prevent-other-scripts-from-setting-window-title
function titleModified() {
    //window.alert("Title modifed");
        doit();
}
window.onload = function() {
    var titleEl = document.getElementsByTagName("title")[0];
    var docEl = document.documentElement;

    if (docEl && docEl.addEventListener) {
        docEl.addEventListener("DOMSubtreeModified", function(evt) {
            var t = evt.target;
            if (t === titleEl || (t.parentNode && t.parentNode === titleEl)) {
                titleModified();
            }
        }, false);
    } else {
        document.onpropertychange = function() {
            if (window.event.propertyName == "title") {
                titleModified();
            }
        };
    }
};
doit();


document.addEventListener('DOMContentLoaded', function() {
    doit();
 }, false);
//window.onload = function () {//   doit();}
setTimeout(function(){
    doit();
   }, 1000);
setTimeout(function(){
    doit();
   }, 2000);
setTimeout(function(){
    doit();
   }, 3000);
setTimeout(function(){
    doit();
    }, 4000);
setTimeout(function(){
    doit();
    }, 5000);
