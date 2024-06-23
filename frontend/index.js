function sendToBackend () {
    var req = new XMLHttpRequest();
    req.open("GET", "test/test?message=hello", false);
    req.send(null);
    console.log(req.responseText);
}