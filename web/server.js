const serverAddr = "http://192.168.131.161";
// const serverAddr = "http://192.168.150.219";
const serverPort = "8000";

function getAlarmListAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);

            // Clear alarm list
            let alarmListContainer = document.getElementById('alarm-list-container');
            alarmListContainer.textContent = "";
            
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

// function getSMSListFromPV(pvname) {
//     var xhttp = new XMLHttpRequest();
//     xhttp.onreadystatechange = function () {
//         if (this.readyState == 4 && this.status == 200) {
//             var jsonValue = JSON.parse(this.responseText);
//             // console.log(jsonValue);
//             for (let x in jsonValue) {
//             }
//         }
//         // else {
//         // 	alert('Status Error : ' + this.status);
//         // }

//     };

//     var serverAddr = "http://192.168.131.161:8000/get";
//     xhttp.open("GET", serverAddr, true);
//     xhttp.send();
// }

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

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmListFromPV/" + search;
    xhttp.open("GET", endPoint, true);
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

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmListFromPhone/" + search;
    xhttp.open("GET", endPoint, true);
    xhttp.send();
}

function updateAlarmInfo(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // var jsonValue = JSON.parse(this.responseText);
            getAlarmListAll()

            if(this.responseText == 'Invalid Value') {
                alert('Invalid Value: Check value or phone number')
            }
            // console.log(this.responseText);
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

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

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

    var data = { 'pvname': pvname, 'field': field, 'value': value };

    const endPoint = serverAddr + ":" + serverPort + "/updateAlarmField";
    xhttp.open("POST", endPoint, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data));
}

function deleteSMSInfo(phone, pvname) {
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

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

    var data = { 'phone': phone, 'pvname': pvname };

    const endPoint = serverAddr + ":" + serverPort + "/deleteSMSInfo";
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


    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

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
            getAlarmListAll();
            if(this.responseText == 'Invalid PV') {
                alert('PV already exists');
            }
            // var jsonValue = JSON.parse(this.responseText);
            // console.log(this.responseText);
            if(this.responseText == 'Invalid Value') {
                alert('Invalid Value: Check value or phone number')
            }
        }

        // else {
        // 	alert('Status Error : ' + this.status);
        // }
    };

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

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

    xhttp.onerror = function () {
        alert('Server Connection Error');
    }

    const endPoint = serverAddr + ":" + serverPort + "/deleteAlarmInfo/" + pvname;
    xhttp.open("GET", endPoint, true);
    xhttp.send();
}

function getAlarmStateAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            applyAlarmState(jsonValue);

            document.getElementById('coma-logo-up').style="fill:#F2F2F2";
            document.getElementById('coma-logo-down').style="fill:#F2F2F2";

        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    xhttp.onerror = function () {
        document.getElementById('coma-logo-up').style="fill:#D4145A";
        document.getElementById('coma-logo-down').style="fill:#D4145A";
    }

    const endPoint = serverAddr + ":" + serverPort + "/getAlarmStateAll";
    xhttp.open("GET", endPoint, true);
    xhttp.send();
}

function getConnectionStateAll() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var jsonValue = JSON.parse(this.responseText);
            applyConnectionState(jsonValue);
            // console.log(jsonValue)

        }
        // else {
        // 	alert('Status Error : ' + this.status);
        // }

    };

    const endPoint = serverAddr + ":" + serverPort + "/getConnectionStateAll";
    xhttp.open("GET", endPoint, true);
    xhttp.send();
}