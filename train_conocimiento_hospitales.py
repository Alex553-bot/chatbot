import json 
import numpy as np

import spacy
from unidecode import unidecode


nlp = spacy.load("es_core_news_sm")

with open('./conocimiento/hospitales.json') as file: 
    data = json.load(file)
departamentos = [(item['departamento']).upper() for item in data['datos']]
municipios = [(municipio['municipio']).upper() for departamento in data['datos'] for municipio in departamento['municipios']]
hospitales = [hospital['nombre'].upper() for departamento in data['datos'] for municipio in departamento['municipios'] for hospital in municipio['hospitales']]
especialidades = {especialidad.upper() for departamento in data['datos'] for municipio in departamento['municipios'] for hospital in municipio['hospitales'] for especialidad in hospital['especialidades']}

class RobotLocalizacion(object):
    """docstring for RobotLocalizacion"""
    def __init__(self):
        super(RobotLocalizacion, self).__init__()
    def isMunicipio(self, texto): 
        texto = texto.upper()
        lista = []
        for elemento in municipios: 
            text = (elemento)
            text = unidecode(text)
            lista.append(text)

        if texto in lista: 
            return 1
        else: 
            return 0
        
    def isEspecialidad(self, texto):
        lista = []
        for elemento in especialidades: 
            text = (elemento.upper())
            text = unidecode(text)
            lista.append(text)

        texto = texto.upper()
        if texto in especialidades: 
            return 1
        else:
            return 0
    def obtainHospital(self, muni, especial): 
        res = []
        muni = unidecode((muni.upper()))
        especial = [unidecode((especiales.upper())) for especiales in especial]
        hospitales = [hospital for departamento in data['datos'] for municipio in departamento['municipios'] if muni==unidecode((municipio['municipio'].upper())) for hospital in municipio['hospitales'] ]
        print(hospitales)
        for hospital in hospitales:
            r = 0 
            for especialidad in hospital['especialidades']: 
                if unidecode((especialidad.upper())) in especial: 
                    r+=1
            n = len(especial)
            if n==0: n = r = 1
            MIN_PERCENT = 37.000001
            if MIN_PERCENT<(r/n*100):
                res.append([100-r/n*100, str(hospital)])
        res = sorted(res)
        print(res)
        return [hospital for _, hospital in res]
