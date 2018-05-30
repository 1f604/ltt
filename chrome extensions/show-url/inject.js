

function doit() {
    var start = " |url:";

    if (document.title.indexOf(start) == -1) {
        document.title += start + location.href;
    }
}

doit();

window.onload = function () {
    doit();
}