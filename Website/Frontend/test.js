var req = new XMLHttpRequest();
req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        console.log(req.responseText)
        var img = document.createElement("img");
        img.src = req.responseText;
        document.getElementById("test").appendChild(img);
    }
};
req.open("GET", "http://127.0.0.1:8080/get_overhead/01_15_2020", true);
req.send();

var req2 = new XMLHttpRequest();
req2.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var video = document.createElement('video');
        video.type = "video/mp4";
        video.src = req2.responseText;
        video.autoplay = true;
        video.muted = true; // Chrome requires autoplay videos to be muted
        document.getElementById("test").appendChild(video);
    }
};
req2.open("GET", "http://127.0.0.1:8080/get_timelapse/01_16_2020", true);
req2.send();