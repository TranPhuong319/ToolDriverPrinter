echo off
Title Installing Vietnamese Driver
setlocal ENABLEEXTENSIONS 
cls

Echo ======================================================
Echo    Installing language Vietnamese for drievr Canon.
Echo ======================================================
echo.

timeout 1 >nul

net session >NUL 2>&1
if %errorlevel% neq 0 (
    color 4f
    echo. ^>^> Administrator privileges required! Please re-run as Administrator
    timeout 3 >nul
    exit /b
)

pushd %~dp0

echo Stopping task:
taskkill /F /IM CNABBSWK.EXE > NUL 2>&1
taskkill /F /IM CNAP2LAK.EXE > NUL 2>&1
taskkill /F /IM CNAP2RPK.EXE > NUL 2>&1
echo.


Echo Backing up files:

rd /s /q .\backup > NUL 2>&1
mkdir .\backup

xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\PCL5ERES.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNABBUND.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNABBSTD.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNABBM.DLL"   .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNAP2NSD.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNABBPMK.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNABB809.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CPC10SAK.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CPC10EAK.DLL" .\backup\  >nul 2>&1
xcopy /Y "C:\Windows\System32\spool\drivers\x64\3\CNXPCP32.DLL" .\backup\  >nul 2>&1

echo. 
echo Successfully backup !
echo. 
echo Deleting file old dll:
del /s /q "C:\Windows\System32\spool\drivers\x64\3\PCL5ERES.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNABBUND.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNABBSTD.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNABBM.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNAP2NSD.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNABBPMK.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNABB809.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CPC10SAK.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CPC10EAK.DLL"  >nul 2>&1
del /s /q "C:\Windows\System32\spool\drivers\x64\3\CNXPCP32.DLL"  >nul 2>&1
echo.
echo Successfully delete old dll !
echo.
echo Copying file dll Vietnamese:
cd ..
xcopy /Y ".\DLL_Vietnam\PCL5ERES.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNABBUND.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNABBSTD.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNABBM.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNAP2NSD.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNABBPMK.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNABB809.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CPC10SAK.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CPC10EAK.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
xcopy /Y ".\DLL_Vietnam\CNXPCP32.DLL" "C:\Windows\System32\spool\drivers\x64\3\" 
 
echo.
echo Successfully !
echo.
