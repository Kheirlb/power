"""Pass signal samples around."""

import json    

class Signal:
    def __init__(self, key, units=None, display_name=None, value=None) -> None:
        self.display_name = display_name
        self.key = key
        self.units = units
        self.value = value

    def __str__(self) -> str:
        return f"{self.display_name}\n{self.key}\n{self.units}"

    def to_dict(self):
        return {
            "display_name": self.display_name,
            "key": self.key,
            "units": self.units,
            "value": self.value
        }

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

spec = Signal("test", "Celsius", "Test")
print(spec)
print(spec.to_json())