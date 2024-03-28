import argparse
import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


Id = str
ServiceId = Id
ApplicationId = Id

Service = dict
Application = dict

SLA = dict
DbObject = dict


# Custom type for nicer type hints
Subparsers = argparse._SubParsersAction
