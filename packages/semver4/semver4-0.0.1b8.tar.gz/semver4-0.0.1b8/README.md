## Overview
A python module to deal with modified semantic versioning.

### Motivation
There are three numbers as main part of a version in semantic version ([semver.org](https://semver.org)). Third number, patch, is defined as:
> PATCH version when you make backward compatible bug fixes

However, sometimes we need to distinguish two types of a bugfix.
1. bugfix which is released in a standard way
1. bugfix which has to be release immidiately as hotfix

The first type is released in a standard release process and at the end the patch of a version is increased.

The second one is the case when we identified a bug which has to be fixed and released immidiately. In this case the version increased patch can potentially already exists as any sort of pre-release version.
<br>Let's assume there is version *0.4.2* deployed in production. Versions *0.4.3-rc* and *0.4.4-rc* already exist in our non prod environment but they are not ready to be released. So, what should be the version of the hotfix? If we want to increase patch we would have to jump to *0.4.5* which may (and will) brings confusion in the versioning.

### Fix version part
To solve to the scenario described above, we introduce 4th number to main version part. Let's call it fix version and define it as:
> FIX version when you make hot fixes released immidiately

So the new version in the described scenario would be *0.4.2.1*

At the end, the modification is only the one number.

## Usage
Few samples how to use the module. There are tow classes:
- *Version4*: this class parses a version which includes the fix part as described above
- *SemVersion*: classis semver2.0 version parser

```python
from semver4 import Version


version = Version4('2.4.4.0-alpha+123')
print(version)
# '2.4.4-alpha+123'

version = Version4(major=2, minor=4, patch=4, prerelease='beta', build='12346')
print(version)
# '2.4.4-beta+12346'
print(version.minor, version.fix)
# 4 0
print(version.core)
# '2.4.4'

print(version > Version('0.4.2.4'))
# True
print(version == '2.4.4-beta+12346')
# True
print(version == 'blabla')
# raises NotComparableError

version.inc_fix()
print(version)
# '2.4.4.1'
print(version.fix)
# 1

version.prerelease = 'rc'
version.metadata = '987'
print(version)
# '2.4.4.1-rc+987'
print(version.core)
# '2.4.4.1'

version.inc_minor().inc_major().inc_patch()
print(version)
# '3.0.1'

# classic semver2.0 parser
v = SemVersion('1.2.3-alpha+007')
print(v)
# '1.2.3-alpha+007'
```

Both, Version4 and SemVersion objects now support json serialization and yaml serialization.

```python
import json
import yaml
from semver4 import Version
from semver4.yaml import get_version4_dumper, get_version4_loader


data = {
    'version': Version('1.2.3.4-beta')
}
dumped = json.dumps(data, default=Version.json_enc)
print(dumped)
# '{"version": "1.2.3.4-beta"}'
print(json.loads(dumped, object_hook=Version.json_dec))
# {"version": 1.2.3.4-beta}

dumped = yaml.dump(data, Dumper=get_version4_dumper())
print(dumped)
# version: 1.2.3.4-beta
print(yaml.load(dumped, Loader=get_version4_loader()))
# {'version': 1.2.3.4-beta}
```
The [PyYAML module](https://pypi.org/project/PyYAML) is not installed with the package because it is required by only one specific feature of the semver4 package which makes it redundant in most of use cases. This also the reason the dumper and the loader are placed in dedicated module.

Installation of PyYAML:
```bash
python3 -m pip install PyYAML
# or python or py or whatever alias you have set
# add --user for installation to the user dir
```