from dataclasses import dataclass, field
from typing import List

@dataclass
class BuiltinType:
    name: str

    def __str__(self):
        return self.name

@dataclass
class Array:
    type: BuiltinType # TODO: any type
    count: int

    def __str__(self):
        return f'({self.type!s} [{self.count}])'

@dataclass
class Literal:
    type: BuiltinType
    value: int

    def __str__(self):
        return f'({self.type!s}){self.value}'

@dataclass
class AggregateInit:
    type: any # TODO
    values: any # TODO

    def __str__(self):
        values = ', '.join(str(v) for v in self.values)
        return f'{self.type!s} {{{values}}}'

@dataclass
class Function:
    name: any # TODO
    return_type: any # TODO
    argument_types: any # TODO

    def __str__(self):
        args = ', '.join(str(a) for a in self.argument_types)
        signature = f'{self.name}({args})'

        if self.return_type is not None:
            signature = f'{self.return_type!s} {signature})'

        return signature

@dataclass
class Name:
    name: str
    parent: any = None # TODO
    template_args: any = None # TODO

    def __str__(self):
        s = self.name

        if self.parent is not None:
            s = f'{self.parent!s}::{s}'

        if self.template_args is not None:
            args = ', '.join(str(a) for a in self.template_args)
            s = f'{s}<{args}>'

        return s
