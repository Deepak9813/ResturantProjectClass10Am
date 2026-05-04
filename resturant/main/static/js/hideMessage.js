// Wait 3 seconds (3000ms), then hide the element
setTimeout(function () {
    var element = document.getElementById("hideMessage");
    if (element) {
        element.style.display = "none";
    }
}, 3000);
