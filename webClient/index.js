let triggerAll = document.getElementById("all")

function sendData(data) {    

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://192.168.1.240');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        console.log(xhr.responseText);
        // Do something with the response data        
    }
    };
    xhr.send(JSON.stringify(data));

}

var ceilingSlider = document.getElementById("ceiling-slider")
var shopSlider = document.getElementById("shop-slider")
var sliderSteps = 5

function slider(id, val) {
    if (val % sliderSteps === 0) {
        let temp = {}
        temp[id + "-brightness"] = parseInt(val)
        console.log(temp)

        sendData(temp)
        
    }
}
