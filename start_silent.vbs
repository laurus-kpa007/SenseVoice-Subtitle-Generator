' SenseVoice 자막 생성기 - 무음 실행 (콘솔 창 없음)
Set objShell = CreateObject("WScript.Shell")

' Conda 환경 활성화 후 pythonw로 실행
' /B: 새 창을 만들지 않음, 0: 창 숨김
objShell.Run "cmd /c ""call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice && start /B pythonw main.py""", 0, False

' 사용자에게 시작 알림 (선택사항 - 주석 처리하면 완전 무음)
' WScript.Sleep 500
' MsgBox "SenseVoice가 백그라운드에서 시작되었습니다.", 64, "SenseVoice"
