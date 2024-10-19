import os
import site

# Set paths
project_directory = os.getcwd()  # The base directory of the project, containing the AIMemeGenerator.py file

def get_package_path(package_to_find):
    site_packages_paths = site.getsitepackages()
    for path in site_packages_paths:
        potential_package_path = os.path.join(path, package_to_find)
        if os.path.exists(potential_package_path):
            return potential_package_path
    return None

# Get necessary package paths
stability_sdk_path = get_package_path('stability_sdk')

# Check if icon file exists
icon_path = os.path.join(project_directory, 'icon.ico') if os.path.exists(os.path.join(project_directory, 'icon.ico')) else None

# Check if version file exists
version_info_file_path = os.path.join(project_directory, 'VersionInfo.txt') if os.path.exists(os.path.join(project_directory, 'VersionInfo.txt')) else None

# ----------------------------------- PYINSTALLER CORE SPEC FILE CONTENTS -----------------------------------
block_cipher = None
a = Analysis(['AIMemeGenerator.py'],
            pathex=[project_directory,
                    os.path.join(stability_sdk_path, "interfaces/src/tensorizer/tensors"),
                    os.path.join(stability_sdk_path, "interfaces/gooseai/generation"),
                    ],
            binaries=[],
            datas=[(stability_sdk_path, 'stability_sdk')],
            hiddenimports=[
                'stability_sdk', 
                'stability_sdk.client', 
                'stability_sdk.interfaces.gooseai.generation.generation_pb2', 
                'stability_sdk.interfaces.src.tensorizer.tensors.tensors_pb2'
            ],
            hookspath=[],
            hooksconfig={},
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)

# Check for additional data files before adding
if os.path.exists('assets/api_keys_empty.ini'):
    a.datas += [('api_keys_empty.ini', '.\\assets\\api_keys_empty.ini', 'DATA')]
if os.path.exists('assets/settings_default.ini'):
    a.datas += [('settings_default.ini', '.\\assets\\settings_default.ini', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='AIMemeGenerator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        icon=icon_path,  # Use the icon path here
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        version=version_info_file_path)
