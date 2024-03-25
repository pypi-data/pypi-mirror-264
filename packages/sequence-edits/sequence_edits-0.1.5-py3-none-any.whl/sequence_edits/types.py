from typing import Literal, TypeVar, Generic
from dataclasses import dataclass

A = TypeVar('A')

@dataclass
class Skip:
    idx: int       
    type: Literal['skip'] = 'skip'

@dataclass
class Insert(Generic[A]):
    idx: int
    value: A = None
    type: Literal['insert'] = 'insert'
    
Edit = Insert | Skip
    
@dataclass
class Inserted(Generic[A]):
    value: A