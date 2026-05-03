; =====================================================
; Inno Setup Script - Otel Kayit ve Oda Yonetim Sistemi
; =====================================================

#define AppName "Otel Kayit Sistemi"
#define AppVersion "1.0"
#define AppPublisher "Otel Yonetimi"
#define AppExeName "OtelKayit.exe"
#define AppDir "C:\OtelKayit"

[Setup]
AppId={{F4A2B1C3-9E5D-4F8A-B2C7-3D6E9A1F0B4C}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={#AppDir}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=dist\installer
OutputBaseFilename=OtelKayitKurulum
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
CreateUninstallRegKey=yes
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\app\{#AppExeName}
; Windows 7 ve uzeri desteklenir
MinVersion=6.1

; Kurulum wizard gorsel ayarlari
WizardSmallImageFile=
WizardImageFile=
SetupIconFile=

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaustu kisayolu olustur"; GroupDescription: "Ek gorevler:"; Flags: checked

[Dirs]
; Klasor yapisi olustur
Name: "{app}\app"
Name: "{app}\data"
Name: "{app}\config"

[Files]
; PyInstaller ciktisindaki tum dosyalari kopyala
Source: "dist\OtelKayit\*"; DestDir: "{app}\app"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Masaustu kisayolu
Name: "{userdesktop}\Otel Kayit Sistemi"; Filename: "{app}\app\{#AppExeName}"; Tasks: desktopicon; Comment: "Otel Kayit ve Oda Yonetim Sistemi"
; Baslat menusu
Name: "{group}\Otel Kayit Sistemi"; Filename: "{app}\app\{#AppExeName}"; Comment: "Otel Kayit ve Oda Yonetim Sistemi"
Name: "{group}\Kaldir"; Filename: "{uninstallexe}"

[Run]
; Kurulum bittikten sonra uygulamayi baslat
Filename: "{app}\app\{#AppExeName}"; Description: "Uygulamayi simdi baslat"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Kaldirma sirasinda olusturulan dosyalari temizle (data ve config klasoru KALSIN)
Type: filesandordirs; Name: "{app}\app"

[Code]
// Kurulum oncesi data klasoru varsa mevcut Excel dosyasini koru
procedure CurStepChanged(CurStep: TSetupStep);
var
  DataDir, ConfigDir: String;
begin
  if CurStep = ssPostInstall then
  begin
    DataDir := ExpandConstant('{app}\data');
    ConfigDir := ExpandConstant('{app}\config');
    
    // data ve config klasorleri zaten varsa bilgilendirme
    if not DirExists(DataDir) then
      CreateDir(DataDir);
    if not DirExists(ConfigDir) then
      CreateDir(ConfigDir);
  end;
end;

// Kaldirma sirasinda data klasorunu koru
function InitializeUninstall(): Boolean;
var
  DataPath: String;
  Response: Integer;
begin
  DataPath := ExpandConstant('{app}\data\kayitlar.xlsx');
  if FileExists(DataPath) then
  begin
    Response := MsgBox(
      'Kayit verileri (kayitlar.xlsx) silinsin mi?' + #13#10 +
      #13#10 +
      'HAYIR secerseniz verileriniz korunur.' + #13#10 +
      'EVET secerseniz tum kayitlar kalici olarak silinir.',
      mbConfirmation, MB_YESNO or MB_DEFBUTTON2
    );
    if Response = IDNO then
    begin
      // Veri dosyasini masaustune yedekle
      FileCopy(DataPath, ExpandConstant('{userdesktop}\kayitlar_yedek.xlsx'), False);
      MsgBox('Verileriniz masaustune yedeklendi: kayitlar_yedek.xlsx', mbInformation, MB_OK);
    end;
  end;
  Result := True;
end;
