// Don't use window.onLoad like this in production, because it can only listen to one function.
$(function () {
    function httpGet(theUrl) {
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        } else {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                $("#graph").append(xmlhttp.responseText);
                $("svg").css("max-width", "100%");
            }
        }
        xmlhttp.open("GET", theUrl + "&preventCache=" + new Date(), false);
        xmlhttp.send();
    }
    httpGet($("#graph").attr("data-graph-url"));

    svgPanZoom('svg', {
        zoomEnabled: true,
        controlIconsEnabled: true
    });
});
