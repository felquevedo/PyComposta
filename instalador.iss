#define AppName "PyComposta"
#define AppVersion "1.0.0"
#define AppExeName "PyComposta.exe"

[Setup]
AppId={{6C1ACBA9-95A6-4C8F-BE8E-4C4BA93808E2}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Felipe Pinto da Motta Quevedo
DefaultDirName={localappdata}\Programs\{#AppName}
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=dist_instalador
OutputBaseFilename=PyComposta_Setup_{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked

; Usa a compilacao validada fora do OneDrive.
; Mantenha esta pasta e o arquivo .bat na mesma configuracao.
[Files]
Source: "C:\PyCompostaBuild\dist\PyComposta\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Executar {#AppName}"; Flags: nowait postinstall skipifsilent
