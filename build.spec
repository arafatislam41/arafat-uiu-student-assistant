# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
customtkinter_datas = collect_data_files('customtkinter')

added_files = [
    ('data', 'data'),
    *customtkinter_datas
]

a = Analysis(
    ['src/gui.py'],
    pathex=['src'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'customtkinter', 'tkinter', 'json', 'pathlib',
        'sqlite3', 'database', 'analytics', 'config', 'schedule', 'exporter', 'webbrowser', 'examcon'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UIU-Student-Assistant-V2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)



