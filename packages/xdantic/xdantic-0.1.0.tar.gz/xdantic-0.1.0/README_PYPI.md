# xdantic
Lightweight configuration library on top of Pydantic

## Getting started

This notebook shows some example usages of xdantic.

It explains how to provide values to the configuration object, how to
access values and how nested configurations work.

The configuration management is simple, including the config object
itself with all the fields that you implement

```python
from typing import Literal
from pydantic import HttpUrl, Field

from xdantic import XConfig

class DemoConfig(XConfig):
    """
    The object `DemoConfig` is the central config object that
    will hold your values and can be extended to your needs with new values.
    Here, you can leverage the power of Pydantic and Python typehints to create a configuration
    that is safe, documented and easy to use.
    
    Check https://pydantic-docs.helpmanual.io/usage/types/ to learn more about field types in Pydantic.
    """
    DB_HOST: HttpUrl  # will be validate to be a httpUrl 
    DB_PORT: int = Field(default=3333, le=64000, ge=1024)  # will be validated to be in the given range
    DB_TYPE: Literal["postgres", "mysql"] = "mysql"  # can only take on values present in the `Literal` definition
```

#### Create a config

To create a config object with parsed values you can simply call the
initializer method and XConfig will automatically create the object
using values from e.g. environment variables.

Now that we have the `DemoConfig` we are ready to use our config in the
code. The next cell provides an example of parsing values to the config
from environment variables and accessing them:

```python
import os 

os.environ['DB_PORT'] = '8888'  # note, how this value will take presedence over the default
os.environ['DB_HOST'] = 'https://postgres-develop.cluster.svc.local'
os.environ['DB_TYPE'] = 'postgres'

print(DemoConfig())
```

#### Nested configuration

Sometime, it is desired to nest configurations to have a structure like
`config.db.usernamne`. This can be easily achieved by creating a
separate class that inherits from `pydantic.BaseModel` and add it as an
attribute to the config object (`DemoConfig`). In the cell below, we
overwrite the definitions from above to create the nested config object:

```python
from pydantic import BaseModel, PositiveFloat, HttpUrl


# for objects that will be nested into the root config object, inherit from `BaseModel`
class ModelConfig(BaseModel):
    lr: PositiveFloat = 1e-3
        

# overwrite the `XConfig` definition from above to include the sub-config object.
class DemoConfig(XConfig):
    MODEL_CFG: ModelConfig = ModelConfig()
    
    DB_HOST: HttpUrl  # will be validate to be a httpUrl 
    DB_PORT: int = Field(default=3333, le=64000, ge=1024)  # will be validated to be in the given range
    DB_TYPE: Literal["postgres", "mysql"] = "mysql"  # can only take on values present in the `Literal` definition
```

```python
os.environ['MODEL_CFG__LR'] = '0.1'

print(DemoConfig())
```

#### Reading from .env file {#reading-from-env-file}

In the notebooks folder there is a file called \'.env\' containing some
config values. XConfig objects will also parse .env files automatically
if they exist.

```python
os.environ.pop('MODEL_CFG__LR', None)
print(ModelConfig())
```

