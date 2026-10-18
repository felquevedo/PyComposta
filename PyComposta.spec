# -*- mode: python ; coding: utf-8 -*-
"""Empacotamento Windows do PyComposta (executar na raiz do projeto)."""
from pathlib import Path

raiz = Path(SPECPATH).resolve()
datas = []
pasta_figuras = raiz / 'figuras'
if not pasta_figuras.is_dir():
    raise FileNotFoundError('Pasta figuras/ não encontrada ao lado do arquivo .spec')
datas.append((str(pasta_figuras), 'figuras'))
logo = raiz / 'logo_ufrgs.png'
if logo.is_file():
    datas.append((str(logo), '.'))

icone = raiz / 'pycomposta.ico'
exe_icon = str(icone) if icone.is_file() else None

a = Analysis(
    [str(raiz / 'interface_pycomposta.py')],
    pathex=[str(raiz)],
    binaries=[],
    datas=datas,
    hiddenimports=[
    "shapely",
    "shapely.geometry",
    "shapely.ops",],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name='PyComposta', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=False, console=False, icon=exe_icon,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='PyComposta')
