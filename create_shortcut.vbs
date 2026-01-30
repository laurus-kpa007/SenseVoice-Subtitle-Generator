Set objShell = CreateObject("WScript.Shell")
Set objShortcut = objShell.CreateShortcut(objShell.SpecialFolders("Desktop") & "\SenseVoice 자막 생성기.lnk")
objShortcut.TargetPath = "C:\Users\lauru\miniconda3\pythonw.exe"
objShortcut.Arguments = "D:\Python\SenseVoice\main.py"
objShortcut.WorkingDirectory = "D:\Python\SenseVoice"
objShortcut.IconLocation = "C:\Windows\System32\shell32.dll,165"
objShortcut.Description = "SenseVoice 자막 생성기 (CMD 창 없음)"
objShortcut.WindowStyle = 1
objShortcut.Save

WScript.Echo "바탕화면에 바로가기가 생성되었습니다!"
