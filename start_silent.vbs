' SenseVoice 자막 생성기 - 무음 실행 (콘솔 창 없음)
' pythonw 대신 python 사용하여 stdout 문제 해결
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 현재 스크립트 위치
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 임시 배치 파일 생성
strTempBat = objFSO.BuildPath(objFSO.GetSpecialFolder(2), "sensevoice_start.bat")
Set objFile = objFSO.CreateTextFile(strTempBat, True)
objFile.WriteLine "@echo off"
objFile.WriteLine "cd /d """ & strScriptPath & """"
objFile.WriteLine "call C:\Users\lauru\miniconda3\Scripts\activate.bat C:\Users\lauru\miniconda3\envs\sensevoice"
objFile.WriteLine "start """" /MIN python main.py"
objFile.Close

' 배치 파일 실행 (창 숨김)
objShell.Run """" & strTempBat & """", 0, False

' 정리 (3초 후 임시 파일 삭제)
WScript.Sleep 3000
On Error Resume Next
objFSO.DeleteFile strTempBat
On Error Goto 0
