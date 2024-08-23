const serverAddr = "http://192.168.131.161";
const serverPort = "8000";

function getAlarmListAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            for (let x in jsonValue) {
                createAlarmInfo(jsonValue[x]);
            }
        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmListAll";
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}

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

function getAlarmListFromPVName(search) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);

            // Clear alarm list
            let alarmListContainer = document.getElementById('alarm-list-container');
            alarmListContainer.textContent = "";

            if (jsonValue.length != 0) {
                // Create new alarm list
                for (let x in jsonValue) {
                    createAlarmInfo(jsonValue[x]);
                }
            }
            else {
                getAlarmListFromPhone(search);
            }

        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmListFromPV/" + search;
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}

function getAlarmListFromPhone(search) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            if (jsonValue.length != 0) {
                // Create new alarm list
                for (let x in jsonValue) {
                    createAlarmInfo(jsonValue[x]);
                }
            }
            else {

            }

        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmListFromPhone/" + search;
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}

function updateAlarmInfo(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            console.log(this.responseText);
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };


    const endPoint = serverAddr + ":" + serverPort + "/updateAlarmInfo";
    xhttp.open("POST", endPoint, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data));
}


function updateAlarmField(pvname, field, value) {
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

    const endPoint = serverAddr + ":" + serverPort + "/updateAlarmField";
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

function insertAlarmInfo(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            console.log(this.responseText);
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };


    const endPoint = serverAddr + ":" + serverPort + "/insertAlarmInfo";
    xhttp.open("POST", endPoint, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data));
}

function deleteAlarmInfo(pvname) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // var jsonValue = JSON.parse(this.responseText);
            // console.log(jsonValue);
        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/deleteAlarmInfo/" + pvname;
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}

function monitoringAlarmStatus() {
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

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmStatusAll";
    xhttp.open("GET", endPoint, false);
    xhttp.send();
}