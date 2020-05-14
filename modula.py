#! /usr/bin/env python3
"""Modulo de python encargado de brindar soporte interno a el procesamiento de Tokens"""

class Token():
    def __init__(self):
        self.type=str()
        self.value=str()

    def __str__(self):
        return "{0:<9} -> {1}".format(self.type,self.value)
    
class Tokenizer(object):
    def __init__(self,cadena,table):
        self.table=table
        self.currentIndex=0
        self.currentLine=0
        self.cadena=cadena

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
                        raise Exception("Error linea {0}: No se reconoce '{1}' como directiva de Preprocesador".format(self.currentLine,token.value))
                else:
                        raise Exception("Error Lexico linea {0}: Simbolo no reconocido, mejore su sintaxis: {1}".format(self.currentLine,character))

            else:
                raise Exception("Error Lexico linea {0}: Simbolo no reconocido : '{1}' ".format(self.currentLine,character))
        return token

    def searchToken(self,value=str(),type=str()):
        for subtype in self.table[type]:
            if value in self.table[type][subtype]:
                return subtype
        return None #si retorna None entonces elemento no existe,pero si lo es, devuelve una tupla con el type,subtype
    def ignore(self):
        #agregaremos un control de excepciones para evitar el final de la cadena y cause un error grave
        try:
        #primero ignoramos los espacios
            while self.cadena[self.currentIndex]==" " or self.cadena[self.currentIndex]=="\n":
                if self.cadena[self.currentIndex]=="\n":
                    self.currentLine+=1
                self.currentIndex+=1
                #ignoramos los comentarios de 2 lineas '//'
                if self.cadena[self.currentIndex]=="/" and self.cadena[self.currentIndex+1]=="/": 
                    self.currentIndex+=2
                    while self.cadena[self.currentIndex] !="\n":
                        self.currentIndex+=1
                    self.currentIndex+=1
                    self.currentLine+=1
                #ignoramos los comentarios de extension /* */
                if self.cadena[self.currentIndex]=="/" and self.cadena[self.currentIndex+1]=="*":
                    self.currentIndex+=2
                   
                    while self.cadena[self.currentIndex]!="*" and self.cadena[self.currentIndex+1]!="/":
                        self.currentIndex+=1
                        if self.cadena[self.currentIndex] =="\n":
                            self.currentLine+=1
                        
                    self.currentIndex+=2
            #si hay mas implementaciones que ignorar, las vamos especificando poco a poco
        except IndexError as e: 
            #si se lanzo la excepcion el index sobrepaso la longitud  de la cadena
            #lo que significa que se termino de analizar la cadena
            return False #retornamos False indicando el fin del analisis
        
        return True #si la limpieza se ejecuta correctamente, proseguimos con el analisis
    
    def hasNextToken(self):
        return  self.ignore() #si la limpieza fue exitosa significa quee hay mas token
        #en caso contraio el analisi ha terminado

