#!/usr/bin/env python3
import sys
import os,json
from modula import *
   
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
            tabla=read_table("symbols.json")
            datos=read_file(sys.argv[1])
            tok=Tokenizer(datos,tabla)
            while tok.hasNextToken():
                token=tok.nextToken()
                print(token)
            with open("scaneado.c",mode="w") as f:
                f.write(tok.ncad)
            print("Archivo 'scaneado.c' traducido correctamente en {0}".format(os.getcwd()))
    except Exception as e:
       print(e)
       print("consulte la documentacion 'https://es.cppreference.com/w/' y mejore su sintaxis")
            
