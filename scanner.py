#!/usr/bin/env python3
import sys
import os,json
from modula import Tokenizer,Token

def clean_file(content=str()):
    cleanText=list()
    index=0
    for line in content.split("\n"):
        index=line.find("//")
        if index!=-1:
            line=line[:index]
        cleanText.append(line+"\n")
    return "".join(cleanText)

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
        data_file=clean_file(data_file)
        tok=Tokenizer(table_symbols)
        previousToken=Token()
        newText= data_file
        variables=dict()
        for line in data_file.split("\n"):
            tok.set_cadena(line)
            while tok.hasNextToken(): #mientras hayan token disponibles en esta linea
                currentToken=tok.nextToken() #obtenenmos el token actual
                typeAct=currentToken.type #obtenemos el tipo de token actual
                #si el token anterior es un ReservedWord de tipo y el actual es un identificador
                #entonces el token actual es una variable y debemos asginarle un nombre especial al valor que ya tenia

                if previousToken.type in ["PR_TYPE","PR_MACRO"] and typeAct == "ID":
                    #agregar las variables a un diccionario con KEYS igual al tipo de variable
                    #y VALUES igual a las variables declaradas con ese tipo
                    name=str() #inicializamos el nombre del token
                    if previousToken.value not in variables.keys():
                        variables[previousToken.value]=list()
                    #proceso de asignarle un nombre nuevo en funcion de las variables que ya fueron
                    #declaradas con este tipo. Buscamos si esta variable ya se declaro
                    if currentToken.value in variables[previousToken.value]:
                        #pues es un error ya que no se pude declarar 2 veces una variable
                        pass
                    else:
                        variables[previousToken.value].append(currentToken.value)
                        #creamos el nombre en funcion del numero de variables ya declaradas
                        name=previousToken.value[0]+str(len(variables[previousToken.value])).zfill(3)
                    #ya con el nombre obtenido y el valor del token procedemos areemplzarlos en el texto original
                    newText=newText.replace(currentToken.value,name)
                                            
                print("{0: <9} ->{1}".format(currentToken.type,currentToken.value))
                previousToken=currentToken
        #guardamos el texto ya procesado
        nameFile=sys.argv[1][sys.argv[1].rfind("\\")+1:] #un poco de codigo para obtener el nombre del archivo obtenido como prametro
        with open(nameFile,"w") as f:
            f.write(newText)
        print("Archivo Normalizado guardado correctamente")
    except Exception as e:
        print(e)
            
