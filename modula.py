#! /usr/bin/env python3
"""Modulo de python encargado de brindar soporte interno a el procesamiento de Tokens"""

class Token():
    def __init__(self):
        self.type=str()
        self.value=str()

class Tokenizer(object):
    def __init__(self,table):
        self.table=table

    def set_cadena(self,number,cadena):
        self.cadena=cadena.strip()
        self.currentIndex=0
        self.number=number
    def nextToken(self):
        token=Token()

        character=self.cadena[self.currentIndex]
        if character.isalpha() :
            while character.isalnum() or character=="_":
                token.value+=character
                self.currentIndex+=1
                if len(self.cadena)> self.currentIndex: 
                    character=self.cadena[self.currentIndex] 
                else :break
            subtype=self.searchToken(token.value,"PR")
            token.type= subtype if subtype else "ID"

        elif character in ["\"","'"]:
            token.value+=character
            self.currentIndex+=1
            character=self.cadena[self.currentIndex]
            while character not in ["\"","'"]:
                token.value+=character
                self.currentIndex+=1
                character=self.cadena[self.currentIndex]
            token.value+=character
            self.currentIndex+=1
            token.type="CAD"
        elif character.isdigit():
            while character.isdigit():
                token.value+=character
                self.currentIndex+=1
                if len(self.cadena)> self.currentIndex: 
                    character=self.cadena[self.currentIndex] 
                else :break
            token.type="NUM"
        else:
            subtype= self.searchToken(character,"OP")
            if subtype:
                token.type=subtype
                token.value+=character
                self.currentIndex+=1
                nextChar= self.cadena[self.currentIndex] if len(self.cadena)> self.currentIndex else "0"
                doubleOperator=character+nextChar
                subtype= self.searchToken(doubleOperator,"OP")
                if subtype :
                    token.value+=nextChar
                    self.currentIndex+=1 
                    token.type=subtype
            
            elif character=="#": #si bien las anteriores combinaciones eran validas
                #ahora reconocemos si se trata de una directiva de procesador(exclusivo de C/C++) como ultima oportunidad
                token.value+=character
                self.currentIndex+=1
                while self.cadena[self.currentIndex]==" ": self.currentIndex+=1
                if self.cadena[self.currentIndex].isalpha() or self.cadena[self.currentIndex]=="_":
                    while self.cadena[self.currentIndex].isalpha() or self.cadena[self.currentIndex]=="_":
                        character=self.cadena[self.currentIndex]
                        token.value+=character
                        self.currentIndex+=1
                        if len(self.cadena)> self.currentIndex: 
                            character=self.cadena[self.currentIndex] 
                        else :break
                    if token.value.lower() in self.table["PR"]["PR_MACRO"]:
                        token.value=token.value.lower()
                        token.type="PR_MACRO"
                    else:
                        raise Exception("Error linea {0}: No se reconoce '{1}' como directiva de Preprocesador".format(self.number,token.value))
                else:
                        raise Exception("Error Lexico linea {0}: Simbolo no reconocido, mejore su sintaxis: {1}".format(self.number,character))

            else:
                raise Exception("Error Lexico linea {0}: Simbolo no reconocido : '{1}' ".format(self.number,character))
        return token

    def searchToken(self,value=str(),type=str()):
        for subtype in self.table[type]:
            if value in self.table[type][subtype]:
                return subtype
        return None #si retorna None entonces elemento no existe,pero si lo es, devuelve una tupla con el type,subtype


    def hasNextToken(self):
        if len(self.cadena)>self.currentIndex:
            while self.cadena[self.currentIndex]==" ":
                self.currentIndex+=1
            if not (self.cadena[self.currentIndex]=="/" and self.cadena[self.currentIndex+1]=="/"):
                return True  
        return False

