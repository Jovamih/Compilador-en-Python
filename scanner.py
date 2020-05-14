#!/usr/bin/env python3
import sys
import os,json
from modula import Tokenizer

def read_file(path=str()):
    with open(path,mode="r") as f:
        data=f.read()
    return data

def read_table(path=str()):
    with open(path,mode="r") as f:
        table=json.load(f)
    return table

if __name__=="__main__":

    if len(sys.argv)<2:
        print("Ingrese un archivo C como parametro para el analizador Lexico")
        exit(0)
    try:
        table_symbols=read_table("symbols.json")
        data_file=read_file(sys.argv[1])
        tok=Tokenizer(table_symbols)
        for line in data_file.split("\n"):
            tok.set_cadena(line)
            while tok.hasNextToken():
                token=tok.nextToken()
                print("{0: <9} ->{1}".format(token.type,token.value))
    except Exception as e:
        print(e)
            
