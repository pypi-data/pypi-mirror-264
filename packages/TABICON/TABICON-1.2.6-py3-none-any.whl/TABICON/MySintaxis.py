#! usr/bin/env python 3
# coding=utf-8

import re
from TABICON.MyListArgs import *
from TABICON.ManejoER import *

__autor = 'Ulises García Calderón'

class MySintaxis():
    '''
    Esta clase permite revisar el nivel léxico y sintactico de gramaticas del
    tipo TABICON. en el nivel léxico se revisa si las etquetas escritas por el usuario
    están de manera correcta, por ultimo se revisa si estan escritas de acuerdo con
    la gramatica para la aplicación
    '''
    param = MyListArgs
    tokens = []
    subtok = []
    reOrder = ''
    newPath = ''
    er = ManejoER('(-\\w+)(:[\\p{Graph}]+)*')
    er1 = ManejoER('-\\w+:([\\p{Graph}]+)')


    def __init__(self,sintaxis, parametros):
        '''
        Constructor donde se hace practicamente todo el trabajo, la estrategia seguida es:
        1.- En la sintaxis se separan los elementos de asociación y el operador de disyunción, por espacios en blanco
        2.- De acuerdo a los elementos léxicos de la sintaxis se revisan cuales utiliza el usuario y su formato
          Desde aqui es posible que ocurran errores
        3.- Cada etiqueta de los elementos utilizados por el usuario son escritos en una nueva cadena
        4.- En la sintaxis original se cambian [ por ( y ] por )?

        :param sintaxis: La gramatica tipo tabicon utilizada para la aplicación
        :param parametros: Objeto con el mapa de los parámetros y sus valores leeidos previamente
        '''
        self.error = ''
        self.param = parametros
        self.sintaxis = re.sub('(\\(|\\)|\\[|\\]|\\|)',' \\1 ',sintaxis)
        self.sintaxis = re.sub('\\s+', ' ', self.sintaxis)
        self.tokens = self.sintaxis.strip().split(' ')
        self.newPath = re.sub('\\]',')?',re.sub('\\[','(',self.sintaxis.strip()))
        self.newPath = self.newPath.replace(' ','\\s*')

        for token in self.tokens:
            if re.compile('(\\(|\\)|\\[|\\]|\\|)').match(token):
                continue
            elif self.er.existER(token): #self.er.existER(token):
                if self.param.exist(self.er.grupo(1)):
                    self.reOrder = self.reOrder + ' ' + token.strip()
                    if self.er.grupo(2) != None:
                        self.error = self.revisarTipoDato(self.er.grupo(1),self.er.grupo(2))
                        if not self.error == '':
                            print('error')
            else:
                print('Se desconoce el elemento: [',token,']')

        self.reOrder = self.reOrder.strip()

        try:
            if not re.compile(self.newPath).match(self.reOrder):
                print('OldPath [',self.sintaxis,']\n','NewPath [',self.newPath,']\nBuscar en ['+self.reOrder+']')
                print('Error en los parametros')
                exit(0)
        except IOError:
            print('Error de sintaxis: el sistema reporta: ',IOError.strerror)
            exit(0)


    def revisarTipoDato(self,token,tipo):
        '''
        Revisa si se especificó un tipo de dato para el parámetro y si el del usuario cumple con dicho formato. También
        es posible definir un conjunto de valor que solo pueden ocurrir, esto sucede cuando hay dos o más tipos expresa-
        dos para esa etiqueta.

        :param token (string): Etiqueta correspondiente al tipo de dato
        :param tipo (string): Tipo de dato o conjunto de datos posibles separados por :
        :return: '' si no se detectó ningún error, de contrario el error encontrado
        '''
        while tipo.startswith(':'):
            tipo = re.sub("^:","",tipo,1) # Eliminar todos los : iniciales

        self.subtok = tipo.strip().split(':') # Dividirlo en cadenas separadas por :

        if len(self.subtok) > 1:
            tipo = self.param.args.get(token)

            for tok in self.subtok:
                if tipo.__eq__(tok):
                    return ''

            return 'Para la etiqueta [',token,'] se encontró el valor [',tipo,'] y no concuerda ninguno de los tipos predefinidos ',tipo

        else:
            tipo = self.subtok[0]


        if tipo.startswith("") and tipo.endswith("") and len(tipo) > 3:
            # Para evaluar expresiones regulares
            tipo = re.sub("<","[",tipo)
            tipo = re.sub(">","]",tipo)
            tipo = re.sub("\\{","(",tipo)
            tipo = re.sub("}",")",tipo)
            tipo = tipo[1:]
            if re.compile(tipo).match(self.param.args.get(token)):
                return 'Se esperaba una cadena con el formato de expresion regular [',tipo,'] para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('str'):
            # Para evaluar cadenas
            if self.param.args.get(token).__eq__(''):
                return 'Se esparaba una cadena para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('int'):
            # Para evaluar enteros
            if not re.compile('-?\\d+').match(self.param.args.get(token).lower()):
                return 'Se esperaba un entero para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('float') or tipo.lower().__eq__('double'):
            # Para evaluar flotantes o dobles
            if self.param.valueArgsAsFloat(token,float('nan')) == float('nan'):
                return 'Se esperaba un flotante o doble para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('bool'):
            # Para evaluar valores booleanos
            if not re.compile('(true|false)').match(self.param.args.get(token).lower()):
                return 'Se esperaba un booleano para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('date'):
            # Para evaluar fechas
            if not re.compile('(\\d{2,4})/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/([01]?[0-9]|[2][0-3])/([0-5]?[0-9])').match(self.param.args.get(token).lower()):
                return 'Se esperaba una fecha para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('char'):
            # Para evaluar un caracter
            if len(self.param.args.get(token)) != 1:
                return 'Se esperaba un caracter para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('hex'):
            # Para evaluar hexadecimales
            if not re.compile('[0-9a-f]+').match(self.param.args.get(token)):
                return 'Se esperaba un hexadecimal para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        elif tipo.lower().__eq__('byte'):
            # Para evaluar datos tipo byte
            if not re.compile('([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5])').match(self.param.args.get(token)):
                return 'Se esperaba un byte para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        else:
            # En caso de encontrar tipos de datos desconocidos
            return 'Tipo de dato desconocido: ',tipo

        return ''
