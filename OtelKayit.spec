# -*- mode: python ; coding: utf-8 -*-
# OtelKayit.spec - PyInstaller yapilandirma dosyasi

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# PyQt5 eklentileri
hiddenimports = collect_submodules('PyQt5')
hiddenimports += [
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.styles',
    'openpyxl.utils',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.writer',
    'openpyxl.reader',
    'pkg_resources.py2_warn',
]

datas = []
datas += collect_data_files('openpyxl')

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OtelKayit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # Konsol penceresi acilmasin
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,              # Icon eklemek isterseniz: icon='otel.ico'
    version_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OtelKayit',
)
