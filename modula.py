#! /usr/bin/env python3
"""Modulo de python encargado de brindar soporte interno a el procesamiento de Tokens"""
variables=dict()

""" Funcion para guardar las variables por su Tipo (aplicable para todas)"""
def saveVariable(type=str(),value=str()):
    if type not in variables.keys():
        variables[type]=list()
    if value not in variables[type]:
        variables[type].append(value)

"""Funcion para obtener el nombre normalizado de una variable. ejemp(a -> f001)"""
def getNameVariable(value=str()):
    name=str()
    for key in variables.keys():
        if value in variables[key]:
            name=key[0]+str(variables[key].index(value)+1).zfill(3)
            return name
    return value
 
""" Clase Token que maneja el 'tipo' y 'valor' """
class Token():
    def __init__(self):
        self.type=str()
        self.value=str()

    def __str__(self):
        return "{0:<9} -> {1}".format(self.type,self.value)
    
""" La clase madre del modulo que maneja las propiedades
    principales para el manejo de la cadena de Tokens
"""    
class Tokenizer(object):
    def __init__(self,cadena,table):
        self.table=table
        self.currentIndex=0
        self.currentLine=0
        self.cadena=cadena
        self.ncad=""
        self.prevToken=Token()

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
            if subtype:
                token.type=subtype
            else:
                token.type="ID"
                if self.prevToken.type=="PR_TYPE":
                    token.type="ID"
                    saveVariable(self.prevToken.value,token.value)
                
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
        
        if token.type=="ID":
            if token.value=="iostream":
                print("iostream estuvo aqui")
            name=getNameVariable(token.value)
            if name=="iostream":
                print("iostrea, logro pasar")
            self.ncad+= name
        else: self.ncad+=token.value
        self.prevToken=token
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
                self.ncad+=self.cadena[self.currentIndex]
                if self.cadena[self.currentIndex]=="\n":
                    self.currentLine+=1
                self.currentIndex+=1
                #ignoramos los comentarios de 2 lineas '//'
                if self.cadena[self.currentIndex]=="/" and self.cadena[self.currentIndex+1]=="/":
                    self.currentIndex+=2
                    while self.cadena[self.currentIndex] !="\n":
                        self.currentIndex+=1
                    self.ncad+=self.cadena[self.currentIndex]
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

