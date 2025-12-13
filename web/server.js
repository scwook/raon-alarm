const wasAddr = "http://192.168.131.194";
// const wasAddr = "http://192.168.150.219";
const wasPort = "9009";
const webSocketAddr = "ws://192.168.131.194";
const webSocketPort = "9010";

const wasEndPoint = wasAddr + ":" + wasPort;
const webSocketURL = webSocketAddr + ":" + webSocketPort;

const ws = new WebSocket(webSocketURL);
ws.onopen = () => {
    console.log('server open');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);

    let field = data['field'];
    switch(field) {
        case 'activation':
            applyActivationState(data);
            break;

        case 'delete':
            applyDeleteAlarmInfo(data);
            break;

        case 'create':
            applyCreateAlarmInfo(data);
            break;

        case 'update':
            applyUpdateAlarmInfo(data);
            break;
            
        default:
            console.log('unknown');
    }
    
};

ws.onclose = () => {
    console.log('server closed');
};

ws.onerror = (err) => {
    console.log('server error');
};

function getAlarmListAll() {
    url = wasEndPoint + '/getAlarmListAll';
    fetch(url)
        .then(res => res.json())
        .then(data => {
            // Clear alarm list
            let alarmListContainer = document.getElementById('alarm-list-container');
            alarmListContainer.textContent = "";

            for (let x in data) {
                createAlarmInfo(data[x]);
            }
        })
        .catch(err => console.log("Fetch error: " + err));
}

function getAlarmListFromPVName(search) {
    url = wasEndPoint + '/getAlarmListFromPV/' + search;
    fetch(url)
        .then(res => res.json())
        .then(data => {
            // Clear alarm list
            let alarmListContainer = document.getElementById('alarm-list-container');
            alarmListContainer.textContent = "";

            if (data.length != 0) {
                // Create new alarm list
                for (let x in data) {
                    createAlarmInfo(data[x]);
                }
            }
            else {
                getAlarmListFromPhone(search);
            }
        })
        .catch(err => console.log("Fetch error: " + err));
}

function getAlarmListFromPhone(search) {
    url = wasEndPoint + '/getAlarmListFromPhone/' + search;
    fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.length != 0) {
                // Create new alarm list
                for (let x in data) {
                    createAlarmInfo(data[x]);
                }
            }
            else {

            }
        })
        .catch(err => console.log("Fetch error: " + err));
}

function updateAlarmInfo(sendData) {
    url = wasEndPoint + '/updateAlarmInfo';
    fetch(url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sendData)
        })
        .then(res => res.text())
        .then(data => {} )
        .catch(err => console.log("Fetch error: " + err));
}

function updateAlarmField(pvname, field, value) {
    url = wasEndPoint + '/updateAlarmField';
    sendData = { 'pvname': pvname, 'field': field, 'value': value };
    fetch(url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sendData)
        })
        .then(res => res.text())
        .then(data => { })
        .catch(err => console.log("Fetch error: " + err));
}

function deleteSMSInfo(phone, pvname) {
    url = wasEndPoint + '/deleteSMSInfo';
    sendData = { 'phone':phone, 'pvname': pvname};
    fetch(url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sendData)
        })
        .then(res => res.text())
        .then(data => { })
        .catch(err => console.log("Fetch error: " + err));
}

function updateSMSInfo(phone, pvname, field, value) {
    url = wasEndPoint + '/smsInfoUpdate';
    sendData = { 'phone': phone, 'pvname': pvname, 'field': field, 'value': value };
    fetch(url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sendData)
        })
        .then(res => res.text())
        .then(data => { })
        .catch(err => console.log("Fetch error: " + err));
}

function insertAlarmInfo(sendData) {
    url = wasEndPoint + '/insertAlarmInfo';
    fetch(url,
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sendData)
        })
        .then(res => res.text())
        .then(data => {
            if (data == 'Invalid PV') {
                alert('PV already exists');
            }

            if (data == 'Invalid Value') {
                alert('Invalid Value: Check value or phone number');
            }
        })
        .catch(err => console.log("Fetch error: " + err));
}

function deleteAlarmInfo(pvname) {
    url = wasEndPoint + '/deleteAlarmInfo/' + pvname;
    fetch(url)
        .then(res => res.text())
        .then(data => { })
        .catch(err => console.log("Fetch error: " + err));
}

function getAlarmStateAll() {
    url = wasEndPoint + '/getAlarmStateAll';
    fetch(url)
        .then(res => res.json())
        .then(data => {
            applyAlarmState(data);

            document.getElementById('coma-logo-up').style = "fill:#F2F2F2";
            document.getElementById('coma-logo-down').style = "fill:#F2F2F2";
        })
        .catch(err => {
            document.getElementById('coma-logo-up').style = "fill:#D4145A";
            document.getElementById('coma-logo-down').style = "fill:#D4145A";
            console.log("Fetch error: " + err);
        });
}

function getConnectionStateAll() {
    url = wasEndPoint + '/getConnectionStateAll';
    fetch(url)
        .then(res => res.json())
        .then(data => {
            applyConnectionState(data)
        })
        .catch(err => console.log("Fetch error: " + err));
}

