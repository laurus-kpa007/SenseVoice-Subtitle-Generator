' 바탕화면에 SenseVoice 바로가기 생성 (콘솔 창 없음)
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 현재 스크립트 위치 확인
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strVBSPath = objFSO.BuildPath(strScriptPath, "start_silent.vbs")

' 바탕화면 경로
strDesktop = objShell.SpecialFolders("Desktop")
strShortcutPath = objFSO.BuildPath(strDesktop, "SenseVoice 자막생성기.lnk")

' 바로가기 생성
Set objShortcut = objShell.CreateShortcut(strShortcutPath)
objShortcut.TargetPath = "wscript.exe"
objShortcut.Arguments = """" & strVBSPath & """"
objShortcut.WorkingDirectory = strScriptPath
objShortcut.Description = "SenseVoice 자막 생성기"
objShortcut.WindowStyle = 1
objShortcut.Save

MsgBox "바탕화면에 바로가기가 생성되었습니다!" & vbCrLf & vbCrLf & _
       "바로가기를 더블클릭하면 콘솔 창 없이 실행됩니다.", _
       64, "바로가기 생성 완료"
