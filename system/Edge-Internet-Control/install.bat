@echo off
chcp 65001 >nul
echo ===================================================
echo     上网助手 (msedge_helper) 一键部署安装脚本
echo ===================================================
echo.

:: 1. 定义安装路径（放在用户本地 AppData 下，隐蔽且无需管理员权限）
set "INSTALL_DIR=%LocalAppData%\Microsoft\EdgeHelper"
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: 2. 检查当前目录下是否存在必要文件
if not exist "dist\msedge_helper.exe" (
    if not exist "msedge_helper.exe" (
        echo [错误] 未找到 msedge_helper.exe，请先运行 build.bat 打包程序！
        pause
        exit /b
    ) else (
        set "EXE_SRC=msedge_helper.exe"
    )
) else (
    set "EXE_SRC=dist\msedge_helper.exe"
)

if not exist "图标.ico" (
    echo [错误] 未找到 图标.ico 文件，请确保图标文件在当前目录下！
    pause
    exit /b
)

:: 3. 复制文件到隐蔽安装目录
echo 正在复制程序文件到安装目录...
copy /Y "%EXE_SRC%" "%INSTALL_DIR%\msedge_helper.exe" >nul
copy /Y "图标.ico" "%INSTALL_DIR%\图标.ico" >nul

:: 4. 定义快捷方式路径
set "DESKTOP_LNK=%USERPROFILE%\Desktop\上网助手.lnk"
set "STARTUP_LNK=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\msedge_helper.lnk"

:: 5. 使用 PowerShell 自动化创建桌面快捷方式（自动绑定您提供的“图标.ico”）
echo 正在创建桌面解锁快捷方式 (已自动绑定 上网助手 图标)...
powershell -ExecutionPolicy Bypass -Command "^
$WshShell = New-Object -ComObject WScript.Shell;^
$Shortcut = $WshShell.CreateShortcut('%DESKTOP_LNK%');^
$Shortcut.TargetPath = '%INSTALL_DIR%\msedge_helper.exe';^
$Shortcut.WorkingDirectory = '%INSTALL_DIR%';^
$Shortcut.IconLocation = '%INSTALL_DIR%\图标.ico';^
$Shortcut.Save();"

:: 6. 使用 PowerShell 自动化创建自启动快捷方式（带 --startup 参数，使用 exe 伪装图标）
echo 正在创建开机自启动项 (使用 Edge 伪装图标)...
powershell -ExecutionPolicy Bypass -Command "^
$WshShell = New-Object -ComObject WScript.Shell;^
$Shortcut = $WshShell.CreateShortcut('%STARTUP_LNK%');^
$Shortcut.TargetPath = '%INSTALL_DIR%\msedge_helper.exe';^
$Shortcut.Arguments = '--startup';^
$Shortcut.WorkingDirectory = '%INSTALL_DIR%';^
$Shortcut.Save();"

echo ===================================================
echo.
echo 部署安装成功！
echo.
echo 已为您自动完成以下配置：
echo 1. 程序主文件已复制到隐蔽目录: %INSTALL_DIR%
echo 2. 桌面生成快捷方式【上网助手】（显示的也是您的 图标.ico）
echo 3. 启动文件夹生成快捷方式【msedge_helper】（开机默默断网，且在任务管理器里伪装为 Edge 图标）
echo.
echo ===================================================
pause
