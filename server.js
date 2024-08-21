const serverAddr = "http://192.168.131.161";
const serverPort = "8000";

function getSMSListFromPV(pvname) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            // console.log(jsonValue);
            for (let x in jsonValue) {
            }
        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    var serverAddr = "http://192.168.131.161:8000/get";
    xhttp.open("GET", serverAddr, false);
    xhttp.send();
}

function getAlarmDataAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            for (let x in jsonValue) {
                createAlarmData(jsonValue[x]);
            }
        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    var serverAddr = "http://192.168.131.161:8000/getAlarmDataAll";
    xhttp.open("GET", serverAddr, false);
    xhttp.send();
}

function getAlarmDataFromPVName(pvname) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            console.log(jsonValue);
        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmInfoFromPV/" + pvname;
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}


function updateAlarmInfo(pvname, field, value) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // var jsonValue = JSON.parse(this.responseText);
            console.log(this.responseText);
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };

    var data = { 'pvname': pvname, 'field': field, 'value': value };

    const endPoint = serverAddr + ":" + serverPort + "/alarmInfoUpdate";
    xhttp.open("POST", endPoint, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data));
}

function updateSMSInfo(phone, pvname, field, value) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // var jsonValue = JSON.parse(this.responseText);
            console.log(this.responseText);
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };

    var data = { 'phone': phone, 'pvname': pvname, 'field': field, 'value': value };

    const endPoint = serverAddr + ":" + serverPort + "/smsInfoUpdate";
    xhttp.open("POST", endPoint, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data));
}