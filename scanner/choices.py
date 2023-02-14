from enum import Enum


class FormEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class ScanTypes(FormEnum):
    FULL = 'Full Scan'
    REFLECTED = 'Reflected Scan'
    STORED = 'Stored Scan'
    DOM_BASED = 'DOM-Based Scan'
