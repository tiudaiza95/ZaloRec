#define AppVersion "3.0.0"
[Setup]
AppId={{20AA6AF9-727D-445F-BB49-852A942694B1}
AppName=ZaloRec
AppVersion={#AppVersion}
AppVerName=ZaloRec {#AppVersion}
DefaultDirName={localappdata}\Programs\ZaloRec
DefaultGroupName=ZaloRec
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
WizardStyle=modern
SetupIconFile=..\assets\companion.ico
UninstallDisplayIcon={app}\ZaloRec.exe
OutputDir=..\release\ZaloRec-3.0.0
OutputBaseFilename=ZaloRec-3.0.0-Setup
Compression=lzma2
SolidCompression=yes
AppMutex=Local\ZaloRec.Instance
CloseApplications=no
RestartApplications=no
DisableProgramGroupPage=yes
UsePreviousAppDir=no
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: checkedonce
[Files]
Source: "..\release\payload\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{userprograms}\ZaloRec"; Filename: "{app}\ZaloRec.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\ZaloRec"; Filename: "{app}\ZaloRec.exe"; WorkingDir: "{app}"; Tasks: desktopicon
[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueName: "ZaloRec"; Flags: uninsdeletevalue
[Run]
Filename: "{app}\ZaloRec.exe"; Description: "Open ZaloRec"; Flags: nowait postinstall skipifsilent unchecked
[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var Existing: String;
begin
  if CurStep = ssPostInstall then
    if RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Run', 'ZaloRec', Existing) then
      RegWriteStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Run', 'ZaloRec', '"' + ExpandConstant('{app}\ZaloRec.exe') + '"');
end;
