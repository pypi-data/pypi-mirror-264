# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scfile',
 'scfile.exceptions',
 'scfile.file',
 'scfile.file.dds',
 'scfile.file.mcsa',
 'scfile.file.mic',
 'scfile.file.obj',
 'scfile.file.ol',
 'scfile.file.ol.converter',
 'scfile.file.png',
 'scfile.io',
 'scfile.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'lz4>=4.3.2,<5.0.0',
 'numpy>=1.26.3,<2.0.0',
 'quicktex>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['build = build:build']}

setup_kwargs = {
    'name': 'sc-file',
    'version': '3.0.1',
    'description': 'Utility & Library for decoding stalcraft assets',
    'long_description': '# SC FILE\n\nUtility and Library for decoding and converting stalcraft assets files, such as models and textures into well-known formats.\n\nYou can use executable from [Releases](https://github.com/onejeuu/sc-file/releases) page.\n\n> [!WARNING]\n> Do not use game assets directly.\n> You can get banned for any changes in game client.\n\n# 📁 Formats\n\n| Type    | Source format | Output format |\n| ------- | ------------- | ------------- |\n| Model   | .mcsa         | .obj          |\n| Texture | .ol           | .dds          |\n| Image   | .mic          | .png          |\n\nModel versions supported: 7.0, 8.0, 10.0\n\nTexture formats supported: DXT1, DXT3, DXT5, RGBA8, BGRA8, RGBA32F, DXN_XY\n\nTexture formats unsupported: Cubemaps (hdri, sky)\n\n# 💻 CLI Utility\n\n## Usage\n\nYou can drag and drop one or multiple files to `scfile.exe`.\n\nFrom bash:\n\n```bash\nscfile [OPTIONS] [FILES]...\n```\n\n## Arguments\n\n- `FILES`: **List of file paths to be converted**. Multiple files should be separated by **spaces**. Accepts both full and relative paths. **Does not accept directory**.\n\n## Options\n\n- `-O`, `--output`: **One path to output file or directory**. Can be specified multiple times for different output files or directories. If not specified, file will be saved in the same directory with a new suffix. You can specify multiple `FILES` and a single `--output` directory.\n\n## Examples\n\n1. Convert a single file:\n\n   ```bash\n   scfile file.mcsa\n   ```\n\n   _Will be saved in the same directory with a new suffix._\n\n1. Convert a single file with a specified path or name:\n\n   ```bash\n   scfile file.mcsa --output path/to/file.obj\n   ```\n\n1. Convert multiple files to a specified directory:\n\n   ```bash\n   scfile file1.mcsa file2.mcsa --output path/to/dir\n   ```\n\n1. Convert multiple files with explicitly specified output files:\n\n   ```bash\n   scfile file1.mcsa file2.mcsa -O 1.obj -O 2.obj\n   ```\n\n   _If the count of `FILES` and `-O` is different, as many files as possible will be converted._\n\n1. Convert all `.mcsa` files in the current directory:\n\n   ```bash\n   scfile *.mcsa\n   ```\n\n   _In this case, `-O` accepts only a directory. Subdirectories are not included._\n\n1. Convert all `.mcsa` files with subdirectories to a specified directory:\n\n   ```bash\n   scfile **/*.mcsa -O path/to/dir\n   ```\n\n   _In this case, `-O` accepts only a directory. With `-O` specified, directory structure is not duplicated._\n\n# 📚 Library\n\n## Install\n\n### Pip\n\n```bash\npip install sc-file -U\n```\n\n### Manual\n\n```bash\ngit clone git@github.com:onejeuu/sc-file.git\n```\n\n```bash\ncd sc-file\n```\n\n```bash\npoetry install\n```\n\n## Usage\n\n### Simple\n\n```python\nfrom scfile import convert\n\n# Output path is optional.\n# Defaults to source path with new suffix.\nconvert.mcsa_to_obj("path/to/model.mcsa", "path/to/model.obj")\nconvert.ol_to_dds("path/to/texture.ol", "path/to/texture.dds")\nconvert.mic_to_png("path/to/image.mic", "path/to/image.png")\n\n# Or determinate it automatically\nconvert.auto("path/to/model.mcsa")\n```\n\n### Advanced\n\nDefault\n\n```python\nfrom scfile.file.data import ModelData\nfrom scfile.file.mcsa.decoder import McsaDecoder\nfrom scfile.file.obj.encoder import ObjEncoder\n\nmcsa = McsaDecoder("model.mcsa")\ndata: ModelData = mcsa.decode()\nmcsa.close() # ? Necessary to close\n\nobj = ObjEncoder(data)\nobj.encode().save("model.obj") # ? Encoder closes after saving\n```\n\nUse encoding content bytes\n\n```python\nobj = ObjEncoder(data)\nobj.encode()\n\nwith open("model.obj", "wb") as fp:\n    fp.write(obj.content)\n\nobj.close() # ? Necessary to close\n```\n\nUse convert methods\n\n```python\nmcsa = McsaDecoder("model.mcsa")\nmcsa.convert_to(ObjEncoder).save("model.obj")\nmcsa.close() # ? Necessary to close\n```\n\n```python\nmcsa = McsaDecoder("model.mcsa")\nmcsa.to_obj().save("model.obj")\nmcsa.close() # ? Necessary to close\n```\n\nSave multiple copies\n\n```python\nmcsa = McsaDecoder(".test/extractor.mcsa")\nobj = mcsa.to_obj()\nobj.save_as("model_1.obj")\nobj.save_as("model_2.obj")\nmcsa.close() # ? Necessary to close\nobj.close() # ? Necessary to close\n```\n\nUse context manager\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    data: ModelData = mcsa.decode()\n\nwith ObjEncoder(data) as obj:\n    obj.encode().save("model.obj")\n```\n\nUse context manager + convert methods\n\n```python\nwith McsaDecoder("model.mcsa") as mcsa:\n    mcsa.to_obj().save("model.obj")\n```\n\n# 🛠️ Build\n\n> [!IMPORTANT]\n> You will need [poetry](https://python-poetry.org) to do compilation.\n\n> [!TIP]\n> Before proceeding, it\'s recommended to create virtual environment\n>\n> ```bash\n> poetry shell\n> ```\n\nThen install dependencies:\n\n```bash\npoetry install\n```\n\nAnd run script to compile:\n\n```bash\npoetry run build\n```\n\nExecutable file will be created in `/dist` directory.\n',
    'author': 'onejeuu',
    'author_email': 'bloodtrail@beber1k.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
