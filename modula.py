#! /usr/bin/env python3
"""Modulo de python encargado de brindar soporte interno a el procesamiento de Tokens"""
class Util(object):
    variables=dict()
    macros=dict()
    """ Funcion para guardar las variables por su Tipo (aplicable para todas)"""
    @staticmethod
    def saveVariable(type=str(),value=str()):
        if type not in Util.variables.keys():
            Util.variables[type]=list()
        if value not in Util.variables[type]:
            Util.variables[type].append(value)
    
    """Funcion para obtener el nombre normalizado de una variable. ejemp(a -> f001)"""
    @staticmethod   
    def getNameVariable(value=str()):
        name=str()
        for key in Util.variables.keys():
            if value in Util.variables[key]:
                name=key[0]+str(Util.variables[key].index(value)+1).zfill(3)
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
        self.table=table #la tabla de simbolos completa
        self.currentIndex=0 #el indice actual
        self.currentLine=0 #nos devuelve la linea actual del scanner
        self.cadena=cadena  #contiene la cadena a Analizar
        self.ncad=str() #es la nueva cadena ya Normalizada
        self.hasVariable=False # para saber si hay uno o mas variables luego de una PR de tipo
        self.hasMacro=False #para saber si hay macros
        self.lastType="" #sirve para identificar cual es la ultima PR de tipo registrada
        self.lastMacro=""
    def nextToken(self):
        token=Token()
        character=self.cadena[self.currentIndex]
        if character.isalpha() : #verifica si es un ID o PR
            while character.isalnum() or character=="_": #esto es imporartente ya que una varaible en C puede tener guion bajo
                token.value+=character
                self.currentIndex+=1
                if len(self.cadena)> self.currentIndex: 
                    character=self.cadena[self.currentIndex] 
                else :break
            subtype=self.searchToken(token.value,"PR") #verificamos si es una palabra reservada PR
            if subtype:
                token.type=subtype
            else:   #en caso contrario es un ID
                token.type="ID"
                
        elif character in ["\"","'"]: #verifica si se trata de una cadena
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
        elif character.isdigit(): #verifica si se trata de un numero
            while character.isdigit():
                token.value+=character
                self.currentIndex+=1
                if len(self.cadena)> self.currentIndex: 
                    character=self.cadena[self.currentIndex] 
                else :break
            token.type="NUM"
        else:
            subtype= self.searchToken(character,"OP") #si se trata de un Operador
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
            #especial en C/C++
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
        
        self.normalize(token)
        
        return token

    def searchToken(self,value=str(),type=str()):
        for subtype in self.table[type]:
            if value in self.table[type][subtype]:
                return subtype
        return None #si retorna None entonces elemento no existe,pero si lo es, devuelve una tupla con el type,subtype
    def normalize(self,token):
        #para la normalizacion de Variables
        """
        if self.hasMacro:
            if token.type=="ID":
                Util.macros[token.value]=Util.macros.get(token.value,"")
                self.lastMacro=token.value
            else:
                Util.macros[self.lastMacro]+=token.value
            self.ncad+=token.value
            """
        if token.type=="ID": #si es identificador
            if self.hasVariable: #y se ha declarado como variable
                Util.saveVariable(self.lastType,token.value) #guardamos dicha variable
            name=Util.getNameVariable(token.value) #obtenemos el nombre del ID normalizado
            self.ncad+=name
        else:
            if token.type=="PR_MACRO":
                self.hasMacro=True
            if token.type=="PR_TYPE":
                self.hasVariable=True
                self.lastType=token.value
            elif token.type not in ("CAD","NUM") and token.value not in ",=" and self.hasVariable:
                self.hasVariable=False   
            self.ncad+=token.value
            
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

