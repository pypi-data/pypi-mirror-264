# Find JCMWAVE v1.0.2
A minimal package that finds the third party support library of jcmwave by looking at the `JCMROOT` environment variable. 
Install by:

```bash
pip install find-jcmwave
```

```python
import find_jcmwave as jcmwave
```

and never worry about linking your jcmwave python library anymore.

## Advanced usage
This package also provides a cli to tightly integrate jcmwave with your python environment. This helps with syntax highlighting, code traversal etc.:
### TLDR;
```bash
find-jcm -li
```

### Third party support package
To link the `jcmwave` package into your environment use:
```bash
find-jcm -l
```

### Packages -> JCM
Make environment packages available from jcm spawned python:
```bash
find-jcm -i
```
To use packages in the templating/callbacks make sure to update the site-packages before importing packages from your env:
```python
import site
site.main()

...

import jax
```