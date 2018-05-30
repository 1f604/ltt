

function doit() {
    var start = " |url:";

    if (document.title.indexOf(start) == -1) {
        document.title += start + location.href;
    }
}

doit();
document.addEventListener('DOMContentLoaded', function() {
    doit();
 }, false);
window.onload = function () {
    doit();
}
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