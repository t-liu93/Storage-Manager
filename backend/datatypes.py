#!/usr/bin/python3

from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class PostBodyBase(BaseModel):
    type: str
    body: Dict

class CategoryBase(BaseModel):
    name: str
    description: str

class ExpireDateBase(BaseModel):
    date: str
    amount: int

class ItemBase(BaseModel):
    uuid: str
    name: str
    amount: int
    category: List[str]
    expireDate: List[ExpireDateBase]
    lastModifiedDate: str

class ServerResults(Enum):
    OK = 0,
    DB_DUPLICATE_ENTRY = 1,
    RESULTS_UNKNOWN = 255,

class Category():
    def __init__(self):
        self._name: str = ''
        self._description: str = ''

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

