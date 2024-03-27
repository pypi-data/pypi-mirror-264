# backstage-catalog-client

[![Release](https://img.shields.io/github/v/release/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/v/release/mspiegel31/backstage-catalog-client)
[![Build status](https://img.shields.io/github/actions/workflow/status/mspiegel31/backstage-catalog-client/main.yml?branch=main)](https://github.com/mspiegel31/backstage-catalog-client/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mspiegel31/backstage-catalog-client/branch/main/graph/badge.svg)](https://codecov.io/gh/mspiegel31/backstage-catalog-client)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/commit-activity/m/mspiegel31/backstage-catalog-client)
[![License](https://img.shields.io/github/license/mspiegel31/backstage-catalog-client)](https://img.shields.io/github/license/mspiegel31/backstage-catalog-client)

A python client for the Backstage catalog API. Only uses native python datatypes.

- **Github repository**: <https://github.com/mspiegel31/backstage-catalog-client/>
- **Documentation** <https://mspiegel31.github.io/backstage-catalog-client/>

# Installation

backstage_catalog_client is available [on PyPi](https://pypi.org/project/backstage_catalog_client/). Requires python 3.8+

```
python3 -m pip install backstage_catalog_client
```

# Usage

to use a ready-made client, import it and make requests

```python
import asyncio
import json
from backstage_catalog_client import HttpxClient


async def main():
    catalog = HttpxClient("https://demo.backstage.io/")
    data = await catalog.get_entities()
    for entity in data.items[:1]:
        print(json.dumps(entity, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

# Documentation

project documentation is available at the [main documentation site](https://mspiegel31.github.io/backstage-catalog-client/)

# Prior Art

1. JS Catalog Client: [backstage-catalog-client](https://www.npmjs.com/package/@backstage/catalog-client)
1. Go Catalog Client: [go-backstage](https://github.com/tdabasinskas/go-backstage)

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
