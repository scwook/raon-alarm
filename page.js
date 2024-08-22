
const SVG_ALARM_STAT = '<svg width="40" height="35"><path class="icon-alarm" d="M17.44,1.5L.41,31c-1.15,2,.29,4.5,2.6,4.5h34.06c2.31,0,3.75-2.5,2.6-4.5L22.63,1.5c-1.15-2-4.04-2-5.2,0Z" /><circle class="icon-fill" cx="20.04" cy="27.82" r="2.54" /><path class="icon-fill" d="M20.04,9.18c-1.4,0-2.54,1.14-2.54,2.54l1.02,12.19h3.05l1.02-12.19c0-1.4-1.14-2.54-2.54-2.54Z" /></svg>';
const SVG_NORMAL_STAT = '<svg width="40" height="40"><circle class="icon-normal" cx="20" cy="20" r="20" /><path class="icon-fill" d="M19.11,29.82h0c-1.06,0-2.04-.54-2.62-1.41l-5.71-7.26c-.68-.87-.53-2.12.33-2.81.87-.68,2.13-.53,2.81.33l5.03,6.39,6.91-13.79c.49-.99,1.7-1.39,2.68-.89.99.49,1.39,1.7.89,2.68l-7.61,15.19c-.56.97-1.6,1.57-2.71,1.57Z" /></svg>';
const SVG_PHONE = '<svg width="22" height="30"><path class="icon-fill" d="M7.66,22.73h0c-1.5-.91-2.01-2.84-1.13-4.36l4.88-8.46c.88-1.52,2.81-2.05,4.34-1.2h0s.52.3.52.3c.96.55,2.19.23,2.74-.73l1.86-3.22c.55-.96.23-2.19-.73-2.74L16.31.1c-1.54-.89-6.33,4.53-10.7,12.1C1.24,19.77-1.06,26.63.48,27.52l3.83,2.21c.96.55,2.19.23,2.74-.73l1.86-3.22c.55-.96.23-2.19-.73-2.74l-.52-.3Z" /></svg>';
const SVG_EDIT = '<svg width="19" height="30"><path class="icon-fill" d="M0,25.01v4.42c0,.44.48.72.86.5l3.83-2.21c.17-.1.32-.24.42-.42L16.39,7.75l-4.95-2.86L.15,24.44c-.1.17-.15.37-.15.57Z" /><path class="icon-fill" d="M17.34.38c-1.37-.79-3.12-.32-3.9,1.05l-1.43,2.48,4.95,2.86,1.43-2.48c.79-1.37.32-3.12-1.05-3.9Z" /></svg>';
const SVG_DELETE = '<svg width="22" height="30"><path class="icon-fill" d="M.62,5.96l2.39,22.66c.02.77.65,1.38,1.42,1.38h12.44c.77,0,1.4-.61,1.42-1.38l2.39-22.66H.62ZM7.27,22.39c0,.44-.36.8-.8.8h-.12c-.44,0-.8-.36-.8-.8v-10.58c0-.44.36-.8.8-.8h.12c.44,0,.8.36.8.8v10.58ZM11.5,22.39c0,.44-.36.8-.8.8h-.12c-.44,0-.8-.36-.8-.8v-10.58c0-.44.36-.8.8-.8h.12c.44,0,.8.36.8.8v10.58ZM15.74,22.39c0,.44-.36.8-.8.8h-.12c-.44,0-.8-.36-.8-.8v-10.58c0-.44.36-.8.8-.8h.12c.44,0,.8.36.8.8v10.58Z" /><path class="icon-fill" d="M19.29,1.7h-6.95c0-.94-.76-1.7-1.7-1.7s-1.7.76-1.7,1.7H2C.9,1.7,0,2.6,0,3.7v.84h21.29v-.84c0-1.1-.9-2-2-2Z" /></svg>';
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

    const deleteElem = document.createElement('div');
    deleteElem.classList.add('alarmDelete');
    deleteElem.innerHTML = SVG_DELETE;
    deleteElem.addEventListener('click', () => {
        deleteAlarmItem(alarmItemContainer, data['pvname']);
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

        smsInfoContainer.appendChild(smsActivationElem);
        smsInfoContainer.appendChild(smsPhoneNumberElem);
        smsInfoContainer.appendChild(smsDeleteElem);

        alarmItemContainer.appendChild(smsInfoContainer);
    }

    alarmListContainer.appendChild(alarmItemContainer);

}

function searchKeyDown(event) {
    if (event.key == "Enter") {
        event.preventDefault();
        searchAlarmData()
    }
}

function searchAlarmData() {
    const searchData = document.getElementById('search-input').value;

    getAlarmListFromPVName(searchData);
}


function addAlarmItem() {

}

function deleteAlarmItem(elem, pvname) {
    deleteAlarmInfo(pvname)
    elem.remove();
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

    updateSMSInfo(phone, pvname, 'activation', Number(isChecked));
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
            messageListItemElem.remove();
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
            messageListItemElem.remove();
        }
    });

    const phoneDeleteElem = document.createElement('div');
    phoneDeleteElem.classList.add('configMessagePhoneDelete');
    phoneDeleteElem.innerHTML = SVG_PHONE_DELETE;
    phoneDeleteElem.addEventListener('click', () => {
        messageListItemElem.remove();
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
            document.getElementById('config-condition').selectedIndex = 0;
            document.getElementById('config-delay').value = "5";
            document.getElementById('config-repetation').value = "0";

            // Remove all child nodes which are message list 
            var messageList = document.getElementById('config-message-user-list');
            messageList.textContent = '';

            var createButtonID = document.getElementById('config-set-button');
            createButtonID.innerText = 'Create';
            createButtonID.addEventListener('click', () => {
                let formData = new FormData(document.getElementById('config-form-container'));
                const dictData = convertToDictionary(formData);

                insertAlarmInfo(dictData);
            });
            break;

        case 'update':
            document.getElementById('config-pvname').value = data['pvname'];
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
            createButtonID.addEventListener('click', () => {
                let formData = new FormData(document.getElementById('config-form-container'));
                const dictData = convertToDictionary(formData);

                updateAlarmInfo(dictData);
            });

            break;

    }

    let id = document.getElementById('config-dialog-body');
    id.style.display = 'flex';
}

function closeAlarmConfigurationDialog() {
    let id = document.getElementById('config-dialog-body');
    id.style.display = 'none';
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