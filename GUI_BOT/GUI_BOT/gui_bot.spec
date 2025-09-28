# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gui_bot.py'],
    pathex=[],
    binaries=[],
    datas=[],  # Убираем background.jpg для экономии места
    hiddenimports=[
        'selenium',
        'undetected_chromedriver',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'cv2',  # Исключаем OpenCV
        'numpy',  # Исключаем numpy
        'webview',  # Исключаем webview
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'tkinter.test',
        'test',
        'unittest',
        'doctest',
        'pdb',
        'pydoc',
        'difflib',
        # 'ast',  # Убираем из исключений - нужен для PyInstaller
        'code',
        'codeop',
        'py_compile',
        'compileall',
        # 'dis',  # Убираем из исключений - нужен для PyInstaller
        'pickletools'
    ],
    noarchive=False,
    optimize=2,  # Максимальная оптимизация Python кода
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YouTubeVideoFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Убираем отладочную информацию
    upx=True,  # Сжатие исполняемого файла
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Убираем иконку для экономии места
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,  # Убираем отладочную информацию
    upx=True,  # Сжатие всех файлов
    upx_exclude=[],
    name='YouTubeVideoFinder',
)
app = BUNDLE(
    coll,
    name='YouTubeVideoFinder.app',
    icon=None,  # Убираем иконку для экономии места
    bundle_identifier='com.youtubevideofinder.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [],
        'LSMinimumSystemVersion': '10.13.0',  # Минимальная версия macOS
        'NSHighResolutionCapable': True,
    },
)
