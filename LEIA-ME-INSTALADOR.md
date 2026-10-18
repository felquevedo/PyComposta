# Instalador do PyComposta para Windows

## Pré-requisitos (somente para quem compila)

- Windows 10/11, 64 bits.
- Python 3.10 ou superior, 64 bits, com `py` disponível.
- [Inno Setup 6](https://jrsoftware.org/isinfo.php).

## Estrutura esperada

Copie `PyComposta.spec`, `instalador.iss` e `gerar_instalador.bat` para a **raiz** do projeto, ao lado de `interface_pycomposta.py`, `requirements.txt`, `geometria/` e `figuras/`. O arquivo `logo_ufrgs.png` é incluído quando existir. Opcionalmente, inclua `pycomposta.ico` para definir o ícone do executável.

## Compilar

No Prompt de Comando do Windows, execute:

```bat
gerar_instalador.bat
```

O script cria/usa `.venv`, instala as dependências, executa PyInstaller e compila o instalador com Inno Setup 6, se encontrado.

- Aplicativo: `dist\PyComposta\PyComposta.exe`
- Instalador: `dist_instalador\PyComposta_Setup_1.0.0.exe`

É possível compilar manualmente:

```powershell
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean PyComposta.spec
```

Depois, abra `instalador.iss` no Inno Setup 6 e clique em **Compile**.

## Verificações antes de publicar

1. Execute `dist\PyComposta\PyComposta.exe` e verifique inclusão de figuras, esquemas, círculo de Mohr e arquivos JSON.
2. Instale em outro Windows **sem Python** e repita os testes.
3. Confirme que as imagens estão em `dist\PyComposta\_internal\figuras\` e que o logo, quando presente, foi incluído.
4. Atualize `AppVersion` em `instalador.iss` a cada versão publicada.
5. Distribua o instalador preferencialmente por uma página oficial de releases e considere assinatura digital para reduzir alertas do Windows SmartScreen.

**Nota:** não foi realizada compilação Windows neste ambiente. O instalador precisa ser gerado e testado no Windows. Antes de redistribuir o logotipo institucional, confirme a autorização de uso.
