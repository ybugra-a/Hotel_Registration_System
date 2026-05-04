[Setup]
AppId={{F4A2B1C3-9E5D-4F8A-B2C7-3D6E9A1F0B4C}
AppName=Otel Kayit Sistemi
AppVersion=1.0
AppPublisher=Otel Yonetimi
DefaultDirName=C:\OtelKayit
DefaultGroupName=Otel Kayit Sistemi
DisableProgramGroupPage=yes
OutputDir=dist\installer
OutputBaseFilename=OtelKayitKurulum
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
CreateUninstallRegKey=yes
UninstallDisplayName=Otel Kayit Sistemi
UninstallDisplayIcon={app}\app\OtelKayit.exe
SetupIconFile=otel.ico

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaustu kisayolu olustur"

[Dirs]
Name: "{app}\app"
Name: "{app}\data"
Name: "{app}\config"

[Files]
Source: "dist\OtelKayit\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userdesktop}\Otel Kayit Sistemi"; Filename: "{app}\app\OtelKayit.exe"; Tasks: desktopicon; IconFilename: "{app}\app\OtelKayit.exe"
Name: "{group}\Otel Kayit Sistemi"; Filename: "{app}\app\OtelKayit.exe"
Name: "{group}\Kaldir"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\app\OtelKayit.exe"; Description: "Uygulamayi simdi baslat"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\app"
