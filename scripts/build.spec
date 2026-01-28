# build_final.spec
import os
import sys

# Anaconda 环境路径
conda_env = r'C:\Users\localpc\anaconda3\envs\cat'

block_cipher = None

# Define datas list first
datas_list = [
    # Only include bongo_cat.ico if it exists - we no longer use the image in the GUI
    ('bongo_cat.ico', '.') if os.path.exists('bongo_cat.ico') else None,
    # Tcl/Tk 数据文件
    (os.path.join(conda_env, 'Library', 'lib', 'tcl8.6'), 'tcl'),
    (os.path.join(conda_env, 'Library', 'lib', 'tk8.6'), 'tk'),
]

# Filter out None values if bongo_cat.ico doesn't exist
filtered_datas = [item for item in datas_list if item is not None]

a = Analysis(
    ['auto_click_gui.py'],
    pathex=[],
    binaries=[
        # Tkinter DLLs
        (os.path.join(conda_env, 'Library', 'bin', 'tcl86t.dll'), '.'),
        (os.path.join(conda_env, 'Library', 'bin', 'tk86t.dll'), '.'),
        (os.path.join(conda_env, 'DLLs', '_tkinter.pyd'), '.'),
    ],
    datas=filtered_datas,
    # 关键：隐藏导入 pynput 后端模块
    hiddenimports=[
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'pynput._util.win32',
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
    name='BongoCat_AutoTyper',  # Updated name to reflect the typing functionality
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bongo_cat.ico'] if os.path.exists('bongo_cat.ico') else None,
)