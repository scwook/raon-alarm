const simulation = true;

let simData = [
    {
        'activation': 1,
        'pvname':'SYS-SUBSYS:scwook-ai1:test',
        'description':'sim test',
        'value':'6.19e-9',
        'operator': 0,
        'state': 'normal',
        'delay': 5,
        'repetation': 0,
        'sms': [
            {'activation': 1, 'phone':'04212345678'},
            {'activation': 1, 'phone':'04212345679'},
            {'activation': 1, 'phone':'04212345671'}
        ]
    },
    {
        'activation': 1,
        'pvname':'SYS-SUBSYS:scwook-ai2:test',
        'description':'sim test',
        'value':'6.19e-9',
        'operator': 1,
        'state': 'alarm',
        'delay': 5,
        'repetation': 0,
        'sms': [
            {'activation': 1, 'phone':'04212345678'},
            {'activation': 1, 'phone':'04212345679'},
            {'activation': 1, 'phone':'04212345671'}
        ]
    },
    {
        'activation': 1,
        'pvname':'SYS-SUBSYS:scwook-ai3:test',
        'description':'sim test',
        'value':'6.19e-9',
        'operator': 2,
        'state': 'normal',
        'delay': 5,
        'repetation': 0,
        'sms': [
            {'activation': 1, 'phone':'04212345678'},
            {'activation': 1, 'phone':'04212345679'},
            {'activation': 1, 'phone':'04212345671'}
        ]
    }
];

function sim_getAlarmListAll() {
    for( let x in simData) {
        createAlarmInfo(simData[x]);
    }
}

function sim_getAlarmStateAll() {
    applyAlarmState(simData);
}


