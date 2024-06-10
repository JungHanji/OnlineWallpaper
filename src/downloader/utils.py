from json import load
from requests import request, get

def smartindex(str: str, fnd: str, strt: int = 0): 
    return str.index(fnd, strt) + len(fnd)