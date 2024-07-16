import numpy as np
import pandas as pd
import re

from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('bolsafamilia/chromedriver.exe')

df_numeros = pd.DataFrame()
df = pd.read_csv('bolsafamilia/lista_cpf_bosafamilia.csv', sep=';')

for ndx,i in df.iterrows():
    cpf = df['cpf'][ndx]
    url = f'https://www.beneficiossociais.caixa.gov.br/consulta/beneficio/04.01.06-01_12.asp?intNuCpf={cpf}&Origem=1'
    driver.get(url)

    r = driver.page_source

    nis = re.search('txtNISRespLegal.value = \'(\d*)\'',r)
    
    if nis is None:
        nis = ''
    else:
        nis = nis[1]
        
    #df_numeros = df_numeros.append({
    #    'nis': nis
    #}, ignore_index=True)

    #print(f'[{ndx}] nis: {nis}')
    if nis != '':
        print("UPDATE EDA SET bolsafamilia_nis='" + str(nis) + "' WHERE cpf_normalizado = right('00000000000'+'" + str(cpf) + "', 11) ")
