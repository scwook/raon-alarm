
const SVG_ALARM_STAT = '<svg width="40" height="35"><path style="fill:#d4145a" d="M17.44,1.5L.41,31c-1.15,2,.29,4.5,2.6,4.5h34.06c2.31,0,3.75-2.5,2.6-4.5L22.63,1.5c-1.15-2-4.04-2-5.2,0Z" /><circle style="fill:#eee" cx="20.04" cy="27.82" r="2.54" /><path style="fill:#eee" d="M20.04,9.18c-1.4,0-2.54,1.14-2.54,2.54l1.02,12.19h3.05l1.02-12.19c0-1.4-1.14-2.54-2.54-2.54Z" /></svg>';
const SVG_NORMAL_STAT = '<svg width="40" height="40"><circle style="fill:#22b573" cx="20" cy="20" r="20" /><path style="fill:#eee" d="M19.11,29.82h0c-1.06,0-2.04-.54-2.62-1.41l-5.71-7.26c-.68-.87-.53-2.12.33-2.81.87-.68,2.13-.53,2.81.33l5.03,6.39,6.91-13.79c.49-.99,1.7-1.39,2.68-.89.99.49,1.39,1.7.89,2.68l-7.61,15.19c-.56.97-1.6,1.57-2.71,1.57Z" /></svg>';
const SVG_PHONE = '<svg width="30" height="30"><path style="fill:#eee" d="M1.05,27.4l4.01,2.32c1,.58,2.28.23,2.85-.76l2.09-3.62c.58-1,.23-2.28-.76-2.85l-.9-.52c-1-.58-1.34-1.85-.76-2.85l5.22-9.04c.58-1,1.85-1.34,2.85-.76l.9.52c1,.58,2.28.23,2.85-.76l2.09-3.62c.58-1,.23-2.28-.76-2.85l-1.81-1.04-2.2-1.27c-.83-.48-1.89-.34-2.55.35C7.52,7.64,2.83,15.77.08,25.02c-.27.92.14,1.91.97,2.38Z"/></svg>';
const SVG_EDIT = '<svg width="30" height="30"><path style="fill:#eee" d="M14.65.07h0c1.66,0,3,1.34,3,3v2h-6v-2C11.65,1.41,12.99.07,14.65.07Z" transform="translate(3.25 -6.98) rotate(30)"/><path style="fill:#eee" d="M9.8,4.96l-1,1.73L.13,21.71c-.11.19-.15.41-.13.62l.4,3.3c.08.66.77,1.07,1.39.8l3.06-1.31c.2-.09.37-.23.47-.42l8.67-15.01,1-1.73-5.2-3Z"/></svg>';
const SVG_DELETE = '<svg width="30" height="30"><path style="fill:#eee" d="M20,2h-7c0-1.1-.9-2-2-2s-2,.9-2,2H2C.9,2,0,2.9,0,4h22c0-1.1-.9-2-2-2Z"/><path style="fill:#eee" d="M.98,6l2.39,22.62c.02.77.65,1.38,1.42,1.38h12.44c.77,0,1.4-.61,1.42-1.38l2.39-22.62H.98ZM8,22.19c0,.55-.45,1-1,1s-1-.45-1-1v-10c0-.55.45-1,1-1s1,.45,1,1v10ZM12,22.19c0,.55-.45,1-1,1s-1-.45-1-1v-10c0-.55.45-1,1-1s1,.45,1,1v10ZM16,22.19c0,.55-.45,1-1,1s-1-.45-1-1v-10c0-.55.45-1,1-1s1,.45,1,1v10Z"/></svg>';
const SVG_CLEAR = '<svg width="30" height="30"><path style="fill:#eee" d="M23.11,12.58l-2.86-1.65,4.62-8c.54-.93.22-2.13-.71-2.67-.94-.54-2.13-.22-2.67.71l-4.62,8-2.85-1.65c-2.33-1.35-5.32-.55-6.67,1.79l-.09.16,17.54,10.13.09-.16c1.35-2.33.55-5.32-1.79-6.67Z"/><path style="fill:#eee" d="M22.21,20.23L7.7,11.85c-.84-.48-1.9-.31-2.54.42L.25,17.85c-.42.48-.3,1.23.25,1.55l4.93,2.84,4.57-5.09-2.12,6.5,10.76,6.21c.52.3,1.18.09,1.43-.46l2.97-6.58c.43-.95.07-2.07-.84-2.59Z"/></svg>';

const SVG_PHONE_DELETE = '<svg width="25" height="25"><circle cx="12.5" cy="12.5" r="12.5" style="fill:#d4145a"/><rect x="5" y="10.5" width="15" height="4" style="fill:#eee" /></svg>';
const SVG_PHONE_ACTIVATION = '<svg width="20" height="20"><path class="cls-12" d="M9.44,15.9c-.59,0-1.12-.29-1.44-.78l-3.59-4.56c-.34-.43-.27-1.06.17-1.4.43-.34,1.06-.27,1.4.17l3.4,4.32,4.51-9c.25-.49.85-.69,1.34-.45.49.25.69.85.45,1.34l-4.74,9.45c-.34.59-.89.91-1.51.91Z" style="fill: #eee;"/></svg>';


function createAlarmInfo(data) {
    let alarmListContainer = document.getElementById('alarm-list-container');

    const alarmItemContainer = document.createElement('div');
    alarmItemContainer.classList.add('alarmItem');

    // Alarm Infomation
    const alarmInfoContainer = document.createElement('div');
    alarmInfoContainer.classList.add('alarmInfo');

    const activationElem = document.createElement('div');
    activationElem.classList.add('alarmActivation');

    const activationContainerElem = document.createElement('label');
    activationContainerElem.classList.add('activationContainer');

    const activationInput = document.createElement('input');
    activationInput.classList.add('activationCheckBox');
    activationInput.checked = data['activation'];
    activationInput.setAttribute('type', 'checkbox');
    activationInput.addEventListener('change', () => {
        setAlarmActivation(activationInput, data);
    });

    const activationToggle = document.createElement('span');
    activationToggle.classList.add('activationToggelButton');

    activationContainerElem.appendChild(activationInput);
    activationContainerElem.appendChild(activationToggle);
    activationElem.appendChild(activationContainerElem);

    const pvnameElem = document.createElement('div');
    pvnameElem.classList.add('alarmPVName');
    pvnameElem.innerText = data['pvname'];

    const valueElem = document.createElement('div');
    valueElem.classList.add('alarmValue')
    valueElem.innerText = data['value'];

    const conditionElem = document.createElement('div');
    conditionElem.classList.add('alarmCondition');
    conditionElem.innerHTML = convertContition(data['operator'])

    const statusElem = document.createElement('div');
    statusElem.classList.add('alarmStatus');
    statusElem.innerHTML = alarmStateCheck(data['state']);

    const delayElem = document.createElement('div');
    delayElem.classList.add('alarmDelay');
    delayElem.innerText = data['delay'] + 's';

    const repetationElem = document.createElement('div');
    repetationElem.classList.add('alarmRepetation');
    repetationElem.innerText = String(data['repetation'] / 60) + 'm';

    const phoneElem = document.createElement('div');
    phoneElem.classList.add('alarmPhone');
    phoneElem.innerHTML = SVG_PHONE;
    phoneElem.addEventListener('click', () => {
        displaySMSList(alarmItemContainer);
    });

    const editElem = document.createElement('div');
    editElem.classList.add('alarmEdit');
    editElem.innerHTML = SVG_EDIT;
    editElem.addEventListener('click', () => {
        showAlarmConfigurationDialog('update', data);
    });

    const clearElem = document.createElement('div');
    clearElem.classList.add('alarmClear');
    clearElem.innerHTML = SVG_CLEAR;
    clearElem.addEventListener('click', () => {
        clearAlarmItem(data['pvname']);
    });

    const deleteElem = document.createElement('div');
    deleteElem.classList.add('alarmDelete');
    deleteElem.innerHTML = SVG_DELETE;
    deleteElem.addEventListener('click', () => {
        deleteAlarmItem(alarmListContainer, alarmItemContainer, data['pvname']);
    });

    alarmInfoContainer.appendChild(activationElem);
    alarmInfoContainer.appendChild(pvnameElem);
    alarmInfoContainer.appendChild(valueElem);
    alarmInfoContainer.appendChild(conditionElem);
    alarmInfoContainer.appendChild(statusElem);
    alarmInfoContainer.appendChild(delayElem);
    alarmInfoContainer.appendChild(repetationElem);
    alarmInfoContainer.appendChild(phoneElem);
    alarmInfoContainer.appendChild(editElem);
    alarmInfoContainer.appendChild(clearElem);
    alarmInfoContainer.appendChild(deleteElem);

    alarmItemContainer.appendChild(alarmInfoContainer);

    // SMS Information
    // console.log(data);
    for (let sms of data['sms']) {
        const smsInfoContainer = document.createElement('div');
        smsInfoContainer.classList.add('smsInfo');
        smsInfoContainer.style.display = 'none';

        const smsActivationElem = document.createElement('div');
        smsActivationElem.classList.add('smsActivation');

        const smsActivationContainerElem = document.createElement('label');
        smsActivationContainerElem.classList.add('smsActivationContainer');

        const smsActivationInput = document.createElement('input');
        smsActivationInput.classList.add('smsActivationCheckBox');
        smsActivationInput.checked = sms['activation'];

        smsActivationInput.setAttribute('type', 'checkbox');
        smsActivationInput.addEventListener('change', () => {
            setSMSActivation(smsActivationInput, sms);
        });

        const smsActivationCheck = document.createElement('span');
        smsActivationCheck.classList.add('smsActivationCheckButton');
        smsActivationCheck.innerHTML = SVG_PHONE_ACTIVATION;


        smsActivationContainerElem.appendChild(smsActivationInput);
        smsActivationContainerElem.appendChild(smsActivationCheck);
        smsActivationElem.appendChild(smsActivationContainerElem);


        const smsPhoneNumberElem = document.createElement('div');
        smsPhoneNumberElem.classList.add('smsPhoneNumber');

        smsPhoneNumberElem.innerText = sms['phone']

        const smsDeleteElem = document.createElement('div');
        smsDeleteElem.classList.add('smsDelete');
        smsDeleteElem.innerHTML = SVG_PHONE_DELETE;
        smsDeleteElem.addEventListener('click', () => {
            // smsInfoContainer.remove();

            const oldFlexItemsInfo = getFlexItemsInfo(alarmListContainer);
            removeFlexItem(alarmItemContainer, smsInfoContainer);
            const newFlexItemsInfo = getFlexItemsInfo(alarmListContainer);
            aminateFlexItems(oldFlexItemsInfo, newFlexItemsInfo);

            deleteSMSInfo(sms['phone'], data['pvname']);

        });

        smsInfoContainer.appendChild(smsActivationElem);
        smsInfoContainer.appendChild(smsPhoneNumberElem);
        smsInfoContainer.appendChild(smsDeleteElem);

        alarmItemContainer.appendChild(smsInfoContainer);
    }

    alarmListContainer.appendChild(alarmItemContainer);
}

function makeAlarmList() {
    if (simulation) {
        sim_getAlarmListAll();
    }
    else {
        getAlarmListAll();
    }
}

function searchKeyDown(event) {
    if (event.key == "Enter") {

        if (simulation) {

        }
        else {
            event.preventDefault();
            searchAlarmData();
        }
    }
}

function searchAlarmData() {
    const searchData = document.getElementById('search-input').value;

    if (simulation) {

    }
    else {
        getAlarmListFromPVName(searchData);
    }

}


function addAlarmItem() {

}

function deleteAlarmItem(container, item, pvname) {
    removeFlexItem(container, item);

    if (simulation) {

    }
    else {
        deleteAlarmInfo(pvname)
        // elem.remove();
    }

}

function clearAlarmItem(pvname) {
    if (simulation) {

    }
    else {
        updateAlarmField(pvname, 'state', 'normal');
    }

}

function setAlarmActivation(elem, data) {
    let isChecked = elem.checked;
    let pvname = data['pvname'];

    updateAlarmField(pvname, 'activation', Number(isChecked));
}

function setSMSActivation(elem, data) {
    let isChecked = elem.checked;
    let phone = data['phone'];
    let pvname = data['pvname'];

    if (simulation) {

    }
    else {
        updateSMSInfo(phone, pvname, 'activation', Number(isChecked));
    }
}

function displaySMSList(container) {
    const smsNodes = container.getElementsByClassName('smsInfo');

    for (let i = 0; i < smsNodes.length; i++) {
        let id = smsNodes[i];
        if (id.style.display == 'none') {
            id.style.display = "flex";
        }
        else {
            id.style.display = "none";
        }
    }
}

function convertContition(operator) {
    switch (operator) {
        case 0:
            return '&#61';

        case 1:
            return '&#60';

        case 2:
            return '&#62';

        case 3:
            return '&#8800';

        case 4:
            return '&#8804';

        case 5:
            return '&#8805';

        default:
            return 'Error';
    }
}

function alarmStateCheck(state) {
    switch (state) {
        case 'alarm':
            return SVG_ALARM_STAT;
        case 'normal':
            return SVG_NORMAL_STAT;
        case 'disconnect':
            return 'Disconnect'
        default:
            return 'Error';
    }
}

function createMessageUser() {
    const messageList = document.getElementById('config-message-user-list');

    const messageListItemElem = document.createElement('div');
    messageListItemElem.classList.add('configMessageUserListContainer');

    const phoneIconElem = document.createElement('div');
    phoneIconElem.classList.add('configMessagePhoneIcon');
    phoneIconElem.innerHTML = SVG_PHONE;

    const phoneInputElem = document.createElement('input');
    phoneInputElem.classList.add('configMessageInputPhone');
    phoneInputElem.setAttribute('name', 'phone');
    phoneInputElem.setAttribute('type', 'tel');
    phoneInputElem.setAttribute('pattern', '[0-9]{10,}');
    phoneInputElem.setAttribute('placeholder', '01046821357');
    phoneInputElem.addEventListener('focusout', () => {
        let value = phoneInputElem.value;
        // console.log(Number.isInteger(value));
        if (!value) {
            removeFlexItem(messageList, messageListItemElem);
            // messageListItemElem.remove();
        }
    });
    // phoneInputElem.addEventListener('keypress', (event) => {
    //     if(event.key == "Enter") {
    //         event.preventDefault();
    //         phoneInputElem.dispatchEvent(new Event('focusout'));
    //         console.log(event.key);
    //     }
    // });

    const phoneDeleteElem = document.createElement('div');
    phoneDeleteElem.classList.add('configMessagePhoneDelete');

    messageListItemElem.appendChild(phoneIconElem);
    messageListItemElem.appendChild(phoneInputElem);
    messageListItemElem.appendChild(phoneDeleteElem);

    messageList.insertBefore(messageListItemElem, messageList.firstChild);
}

function addMessageUser(data) {
    const messageList = document.getElementById('config-message-user-list');

    const messageListItemElem = document.createElement('div');
    messageListItemElem.classList.add('configMessageUserListContainer');

    const phoneIconElem = document.createElement('div');
    phoneIconElem.classList.add('configMessagePhoneIcon');
    phoneIconElem.innerHTML = SVG_PHONE;

    const phoneInputElem = document.createElement('input');
    phoneInputElem.classList.add('configMessageInputPhone');
    phoneInputElem.value = data;
    phoneInputElem.setAttribute('name', 'phone');
    phoneInputElem.setAttribute('type', 'tel');
    phoneInputElem.setAttribute('pattern', '[0-9]{10,}');
    phoneInputElem.setAttribute('placeholder', '01046821357');
    phoneInputElem.addEventListener('focusout', () => {
        let value = phoneInputElem.value;
        if (!value) {
            removeFlexItem(messageList, messageListItemElem);
            // messageListItemElem.remove();
        }
    });

    const phoneDeleteElem = document.createElement('div');
    phoneDeleteElem.classList.add('configMessagePhoneDelete');
    phoneDeleteElem.innerHTML = SVG_PHONE_DELETE;
    phoneDeleteElem.addEventListener('click', () => {
        removeFlexItem(messageList, messageListItemElem);
        // messageListItemElem.remove();
    });

    messageListItemElem.appendChild(phoneIconElem);
    messageListItemElem.appendChild(phoneInputElem);
    messageListItemElem.appendChild(phoneDeleteElem);

    messageList.insertBefore(messageListItemElem, messageList.firstChild);
}

function showAlarmConfigurationDialog(target, data) {

    switch (target) {
        case 'create':
            var searchInputId = document.getElementById('search-input');
            document.getElementById('config-pvname').value = searchInputId.value;
            document.getElementById('config-value').value = "";
            document.getElementById('config-description').value = "";
            document.getElementById('config-condition').selectedIndex = 0;
            document.getElementById('config-delay').value = "5";
            document.getElementById('config-repetation').value = "0";

            // Remove all child nodes which are message list 
            var messageList = document.getElementById('config-message-user-list');
            messageList.textContent = '';

            var createButtonID = document.getElementById('config-set-button');
            createButtonID.innerText = 'Create';
            createButtonID.addEventListener('click', createAlarm);
            break;

        case 'update':
            document.getElementById('config-pvname').value = data['pvname'];
            document.getElementById('config-description').value = data['description'];
            document.getElementById('config-value').value = data['value'];
            document.getElementById('config-condition').selectedIndex = data['operator'];
            document.getElementById('config-delay').value = String(data['delay']);
            document.getElementById('config-repetation').value = String(data['repetation'] / 60);

            // Remove all child nodes which are message list 
            var messageList = document.getElementById('config-message-user-list');
            messageList.textContent = '';

            for (let x of data['sms']) {
                addMessageUser(x['phone']);
            }

            var createButtonID = document.getElementById('config-set-button');
            createButtonID.innerText = 'Update';
            createButtonID.addEventListener('click', updateAlarm);
            break;

    }

    let configContainerId = document.getElementById('config-dialog-body');
    configContainerId.style.display = 'flex';

    let configFormId = document.getElementById('config-form-container');
    configFormId.animate([
        {
            transform: "translateY(50px)",
            opacity: 0
        },
        {
            transform: "translate(0px)",
            opacity: 1
        }
    ], {
        duration: 300,
        easing: "ease-out",
        fill: "forwards"
    });
}

function createAlarm() {
    let formData = new FormData(document.getElementById('config-form-container'));
    let formDataCheck = checkFromData(formData);

    if (formDataCheck == "OK") {

        const dictData = convertToDictionary(formData);

        insertAlarmInfo(dictData);
        // document.getElementById('config-dialog-body').style.display = 'none';
        closeAlarmConfigurationDialog();
    }
    else if (formDataCheck == "EMPTY") {
        alert('The Process Variable or Value is required')
    }
    else if (formDataCheck == "VALUE") {
        alert('The input value must be a number')
    }
    else {
        alert('Check Input Data');
    }
}

function updateAlarm() {
    let formData = new FormData(document.getElementById('config-form-container'));
    let formDataCheck = checkFromData(formData);

    if (formDataCheck == "OK") {

        const dictData = convertToDictionary(formData);

        updateAlarmInfo(dictData);
        // document.getElementById('config-dialog-body').style.display = 'none';
        closeAlarmConfigurationDialog();
    }
    else if (formDataCheck == "EMPTY") {
        alert('The Process Variable or Value is required')
    }
    else if (formDataCheck == "VALUE") {
        alert('The input value must be a number')
    }
    else {
        alert('Check Input Data');
    }
}

function closeAlarmConfigurationDialog() {
    let configContainerId = document.getElementById('config-dialog-body');
    let configFormId = document.getElementById('config-form-container');
    let createButtonId = document.getElementById('config-set-button');
    createButtonId.removeEventListener('click', createAlarm);
    createButtonId.removeEventListener('click', updateAlarm);

    setTimeout(() => {
        configContainerId.style.display = 'none';
    }, 300);

    configFormId.animate([
        {
            transform: "translateY(0px)",
            opacity: 1
        },
        {
            transform: "translateY(50px)",
            opacity: 0
        }
    ], {
        duration: 300,
        easing: "ease-out",
        fill: "forwards"
    });
}

function checkFromData(formData) {
    for (let [key, value] of formData.entries()) {
        switch (key) {
            case 'pvname':
                if (!value) {
                    return 'EMPTY';
                }
                break;

            case 'value':
                if (!value) {
                    return 'EMPTY';
                }
                else {
                    if (!(parseFloat(value))) {
                        return 'VALUE';
                    }
                }
                break;
        }
    }

    return 'OK';

}

function convertToDictionary(formData) {
    const dictData = {};
    const phoneArray = [];

    for (let [key, value] of formData.entries()) {
        if (key == 'phone') {
            phoneArray.push(value);
        }
        else {
            dictData[key] = value;
        }
        // console.log(`${key}: ${value}`);
    }

    dictData['phone'] = phoneArray;

    return dictData;
}

function monitoringAlarmState() {
    if (simulation) {
        sim_getAlarmStateAll();
    }
    else {
        getAlarmStateAll();
    }
}

function monitoringConnectionState() {
    if (simulation) {

    }
    else {
        getConnectionStateAll();
    }
}

function applyAlarmState(data) {
    const alarmListContainer = document.getElementById('alarm-list-container');
    const alarmItem = alarmListContainer.getElementsByClassName('alarmItem');
    let alarmCount = 0;
    let normalCount = 0;

    for (let x of alarmItem) {
        const alarmInfo = x.querySelector('.alarmInfo');
        const pvname = alarmInfo.querySelector('.alarmPVName').textContent;
        const state = findAlarmState(data, pvname);

        if (state == 'alarm') {
            alarmCount += 1;
        }
        else if (state == 'normal') {
            normalCount += 1;
        }

        alarmInfo.querySelector('.alarmStatus').innerHTML = alarmStateCheck(state);
        document.getElementById('summary-alarm-text').innerText = alarmCount;
        document.getElementById('summary-normal-text').innerText = normalCount;
    }
}

function findAlarmState(data, pvname) {
    for (let x of data) {
        if (x['pvname'] == pvname) {
            return x['state'];
        }
    }

    return null
}

function applyConnectionState(data) {
    const alarmListContainer = document.getElementById('alarm-list-container');
    const alarmItem = alarmListContainer.getElementsByClassName('alarmItem');

    for (let x of alarmItem) {
        const alarmInfo = x.querySelector('.alarmInfo');
        const pvname = alarmInfo.querySelector('.alarmPVName').textContent;
        const state = findConnectionState(data, pvname);
        let textColor = '#123456';
        if (state) {
            textColor = '#eeeeee'
        }
        else {
            textColor = '#aaaaaa'
        }

        alarmInfo.querySelector('.alarmPVName').style.color = textColor;

    }
}

function findConnectionState(data, pvname) {
    for (let x of data) {
        if (x['pvname'] == pvname) {
            return x['state'];
        }
    }

    return null
}

function removeFlexItem(container, item) {
    const oldFlexItemsInfo = getFlexItemsInfo(container);
    container.removeChild(item);
    const newFlexItemsInfo = getFlexItemsInfo(container);
    aminateFlexItems(oldFlexItemsInfo, newFlexItemsInfo);
}
function getFlexItemsInfo(container) {
    return Array.from(container.children).map((item) => {
        const rect = item.getBoundingClientRect();
        return {
            element: item,
            x: rect.left,
            y: rect.top,
            width: rect.right - rect.left,
            height: rect.bottom - rect.top
        };
    });
}

function aminateFlexItems(oldFlexItemsInfo, newFlexItemsInfo) {
    for (const newFlexItemInfo of newFlexItemsInfo) {
        const oldFlexItemInfo = oldFlexItemsInfo.find((itemInfo) => itemInfo.element === newFlexItemInfo.element);
        // const translateX = oldFlexItemInfo.x - newFlexItemInfo.x;
        const translateY = oldFlexItemInfo.y - newFlexItemInfo.y;
        // const scaleX = oldFlexItemInfo.width / newFlexItemInfo.width;
        // const scaleY = oldFlexItemInfo.height / newFlexItemInfo.height;
        newFlexItemInfo.element.animate([
            {
                transform: `translateY(${translateY}px`
            },
            { transform: "none" }
        ], {
            duration: 250,
            easing: "ease-out"
        });
    }
}