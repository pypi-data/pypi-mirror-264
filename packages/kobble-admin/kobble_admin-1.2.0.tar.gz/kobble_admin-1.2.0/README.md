# Kobble Admin SDK

## Requirements

- python >= 3.11

## Usage

Initialize a `Kobble` instance from a secret previously generated from your [Kobble dashboard](https://app.kobble.io/p/sdk/secrets).

```py
from kobble_admin import Kobble

kobble = Kobble("<secret>")
whoami = kobble.whoami()

print(whoami)
```

Exported functions are extensively documented, and more documentation can be found on our [official docs](https://docs.kobble.io).
