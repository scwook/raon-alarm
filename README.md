# COntrol Message Alarm system(COMA)
- EPICS value 기반으로 알람 상태를 문자로 전송하는 시스템
- 알람 상태를 모니터링 하는 서버(COMA)와 메시지를 전송하는 서버(MCS)로 구성
- 2개의 서버는 시리얼 포트로 연결(망분리 상황을 가정)
- COMA 서버는 mariaDB에 상태 정보를 저장
- 메시지 전송이 필요 없는경우 MCS 서버는 구축안해도 됨

### COMA
- coma.py: flask기반COMA Web interface 및 serial send
- epics.py: EPICS monitoring, Alarm check
- sql.py: DB interface
- clue.py: Error or warning message print

### MCS
- mcs.py: SMS 메시지 전송 서버
- serialReceive.py: serial receive
- clue.py: Error or warning message print

### Web interface
