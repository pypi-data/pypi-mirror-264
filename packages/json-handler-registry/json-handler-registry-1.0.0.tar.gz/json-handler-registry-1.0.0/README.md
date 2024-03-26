# JSON Handler Registry
---
Standardized way of registering custom JSON serializers/deserializers.

Package `json` lacks standard approach to registering custom JSON handlers.

Project `json-handler-registry` has been created to solve that issue.

## Usage:

Registering your own handlers:

```python
from typing import Optional
from json_handler_registry import JsonHandlerRegistry, IJsonEncoder, IJsonDecoder
from json_handler_registry.encoder import EncodingResult

# Enable registry:
JsonHandlerRegistry.enable()


# Implement your custom class encoder:
class MyJsonEncoder(IJsonEncoder):
    def encodeObject(self, obj: object) -> Optional[EncodingResult]:
        """Convert object to a JSON serializable data.
        Or return ``None`` instead.
        """
        pass  # TODO: Actual implementation goes here!


# Implement your custom class decoder:
class MyJsonDecoder(IJsonDecoder):
    def decodeDict(self, dct: dict) -> Optional[object]:
        """Convert dictionary to your type instance.
        Or return ``None`` instead.
        """
        pass  # TODO: Actual implementation goes here!

    def decodeStr(self, valueStr: str) -> Optional[object]:
        """Convert string value to your type instance.
        Or return ``None`` instead.
        """
        pass  # TODO: Actual implementation goes here!


# Register your serializer and deserializer:
JsonHandlerRegistry.registerEncoder(MyJsonEncoder())
JsonHandlerRegistry.registerDecoder(MyJsonDecoder())
```

Serialization & deserialization:
```python
# Using `tunit` package as an example:
import json
from tunit import TUnitConfig, Seconds

TUnitConfig.registerJsonHandler() # Enables registry and registers handlers.

# JSON serialization:
messageDto = {"delay": Seconds(10)}
messageJson = json.dumps(messageDto)
print(messageJson) # Prints: '{"delay": "10s"}'

# JSON deserialization:
messageJson = '{"delay": "10s"}'
messageDto = json.loads(messageJson)
print(messageDto) # Prints: {'delay': Seconds(10)}
```

## License
MIT
