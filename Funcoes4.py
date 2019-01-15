"""
    Copyright (c) 2017 Guilherme Taborda Ribas.
    Copyright (c) 2012-2013 Matplotlib Development Team; All Rights Reserved.
    Copyright (c) 2017 NumPy developers.
    Copyright (c) 2008-2012, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team All rights reserved.
    Copyright (c) 2016 Riverbank Computing Limited.
    Copyright (c) 2017 The Qt Company.

    This file is part of MoneyMap SCLAB.
    MoneyMap is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or any later version.
    MoneyMap is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    You should have received a copy of the GNU Lesser General Public License
    along with MoneyMap.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import pandas as pd

class Funcoes():

    def __init__(self):
        pass
    ##############
    ##Candlesticks
    ##############
    def doji(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Doji('+str(par)+')'] = df['Fech'] == df['Abert']
        else:
            df['Doji('+str(par)+')'] = df['Fech'].shift(abs(d)) == df['Abert'].shift(abs(d))
            
        return df

    def martelo_alta(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Martelo Alta('+str(par)+')'] = (df['Abert']<df['Fech']) & (df['Fech']==df['Max']) & ((df['Fech']-df['Abert'])<=(df['Abert']-df['Min'])/2)
        else:
            df['Martelo Alta('+str(par)+')'] = (df['Abert'].shift(abs(d))<df['Fech'].shift(abs(d))) & (df['Fech'].shift(abs(d))==df['Max'].shift(abs(d))) & ((df['Fech'].shift(abs(d))-df['Abert'].shift(abs(d)))<=(df['Abert'].shift(abs(d))-df['Min'].shift(abs(d)))/2)

        return df

    def martelo_baixa(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Martelo Baixa('+str(par)+')'] = (df['Abert']>df['Fech']) & (df['Abert']==df['Max']) & ((df['Abert']-df['Fech'])<=(df['Fech']-df['Min'])/2)
        else:
            df['Martelo Baixa('+str(par)+')'] = (df['Abert'].shift(abs(d))>df['Fech'].shift(abs(d))) & (df['Abert'].shift(abs(d))==df['Max'].shift(abs(d))) & ((df['Abert'].shift(abs(d))-df['Fech'].shift(abs(d)))<=(df['Fech'].shift(abs(d))-df['Min'].shift(abs(d)))/2)

        return df

    def martelo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
##        d = int(par.split(',')[0])
        self.martelo_alta(df, parDia)
        self.martelo_baixa(df, parDia)
        
        df['Martelo('+str(par)+')'] = df['Martelo Alta('+str(par)+')'] | df['Martelo Baixa('+str(par)+')']

        return df

    def estrela_cadente_alta(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela Cadente Alta('+str(par)+')'] = (df['Abert']<df['Fech']) & (df['Abert']==df['Max']) & ((df['Fech']-df['Abert'])<=(df['Max']-df['Fech'])/2)
        else:
            df['Estrela Cadente Alta('+str(par)+')'] = (df['Abert'].shift(abs(d))<df['Fech'].shift(abs(d))) & (df['Abert'].shift(abs(d))==df['Max'].shift(abs(d))) & ((df['Fech'].shift(abs(d))-df['Abert'].shift(abs(d)))<=(df['Max'].shift(abs(d))-df['Fech'].shift(abs(d)))/2)

        return df

    def estrela_cadente_baixa(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela Cadente Baixa('+str(par)+')'] = (df['Abert']>df['Fech']) & (df['Fech']==df['Max']) & ((df['Abert']-df['Fech'])<=(df['Max']-df['Abert'])/2)
        else:
            df['Estrela Cadente Baixa('+str(par)+')'] = (df['Abert'].shift(abs(d))>df['Fech'].shift(abs(d))) & (df['Fech'].shift(abs(d))==df['Max'].shift(abs(d))) & ((df['Abert'].shift(abs(d))-df['Fech'].shift(abs(d)))<=(df['Max'].shift(abs(d))-df['Abert'].shift(abs(d)))/2)

        return df

    def estrela_cadente(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        self.estrela_cadente_alta(df, parDia)
        self.estrela_cadente_baixa(df, parDia)
        
        df['Estrela Cadente('+str(par)+')'] = df['Estrela Cadente Alta('+str(par)+')'] | df['Estrela Cadente Baixa('+str(par)+')']

        return df

    def engolfo_de_alta(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Engolfo de Alta('+str(par)+')'] = (df['Abert']<df['Fech']) & (df['Abert'].shift(1)>=df['Fech'].shift(1)) & (df['Abert']<df['Abert'].shift(1)) & (df['Abert'].shift(1)<df['Fech']) & (df['Abert']<df['Fech'].shift(1)) & (df['Fech'].shift(1)<df['Fech'])
        else:
            df['Engolfo de Alta('+str(par)+')'] = (df['Abert'].shift(abs(d))<df['Fech'].shift(abs(d))) & (df['Abert'].shift(1+abs(d))>=df['Fech'].shift(1+abs(d))) & (df['Abert'].shift(abs(d))<df['Abert'].shift(1+abs(d))) & (df['Abert'].shift(1+abs(d))<df['Fech'].shift(abs(d))) & (df['Abert'].shift(abs(d))<df['Fech'].shift(1+abs(d))) & (df['Fech'].shift(1+abs(d))<df['Fech'].shift(abs(d)))
            
        return df

    def engolfo_de_baixa(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Engolfo de Baixa('+str(par)+')'] = (df['Abert']>df['Fech']) & (df['Abert'].shift(1)<=df['Fech'].shift(1)) & (df['Abert']>df['Abert'].shift(1)) & (df['Abert'].shift(1)>df['Fech']) & (df['Abert']>df['Fech'].shift(1)) & (df['Fech'].shift(1)>df['Fech'])
        else:
            df['Engolfo de Baixa('+str(par)+')'] = (df['Abert'].shift(abs(d))>df['Fech'].shift(abs(d))) & (df['Abert'].shift(1+abs(d))<=df['Fech'].shift(1+abs(d))) & (df['Abert'].shift(abs(d))>df['Abert'].shift(1+abs(d))) & (df['Abert'].shift(1+abs(d))>df['Fech'].shift(abs(d))) & (df['Abert'].shift(abs(d))>df['Fech'].shift(1+abs(d))) & (df['Fech'].shift(1+abs(d))>df['Fech'].shift(abs(d)))

        return df
            
    def engolfo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
##        d = int(par.split(',')[0])
        self.engolfo_de_alta(df, parDia)
        self.engolfo_de_baixa(df, parDia)
        
        df['Engolfo('+str(par)+')'] = df['Engolfo de Alta('+str(par)+')'] | df['Engolfo de Baixa('+str(par)+')']

        return df

    def piercing_line(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Piercing Line('+str(par)+')'] = (df['Fech']>df['Abert']) & (df['Fech'].shift(1)<df['Abert'].shift(1)) & (df['Abert']<df['Min'].shift(1)) & (df['Fech']>=(df['Fech'].shift(1)+ df['Abert'].shift(1))/2)
        else:
            df['Piercing Line('+str(par)+')'] = (df['Fech'].shift(abs(d))>df['Abert'].shift(abs(d))) & (df['Abert'].shift(abs(d))<df['Min'].shift(1+abs(d))) & (df['Fech'].shift(abs(d))>=(df['Fech'].shift(1+abs(d))+ df['Abert'].shift(1+abs(d)))/2)

        return df

    ###A partir daqui, nenhuma def de candles foi testada, verificar isso tudo.
    def dark_cloud_cover(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Piercing Line('+str(par)+')'] = (df['Fech']<df['Abert']) & (df['Fech'].shift(1)>df['Abert'].shift(1)) & (df['Abert']>df['Max'].shift(1)) & (df['Fech']<=(df['Fech'].shift(1)+ df['Abert'].shift(1))/2)
        else:
            df['Piercing Line('+str(par)+')'] = (df['Fech'].shift(abs(d))<df['Abert'].shift(abs(d))) & (df['Fech'].shift(1+abs(d))>df['Abert'].shift(1+abs(d))) & (df['Abert'].shift(abs(d))>df['Max'].shift(1+abs(d))) & (df['Fech'].shift(abs(d))<=(df['Fech'].shift(1+abs(d))+ df['Abert'].shift(1+abs(d)))/2)

        return df

    def harami_de_fundo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Harami de Fundo('+str(par)+')'] = (df['Fech']>df['Abert']) & (df['Fech'].shift(1)<df['Abert'].shift(1)) & (df['Abert']>df['Fech'].shift(1)) & (df['Fech']<df['Abert'].shift(1)) & ((df['Fech']-df['Abert'])<=((df['Abert'].shift(1)-df['Fech'].shift(1))/4))
        else:
            df['Harami de Fundo('+str(par)+')'] = (df['Fech'].shift(abs(d))>df['Abert'].shift(abs(d))) & (df['Fech'].shift(1+abs(d))<df['Abert'].shift(1+abs(d))) & (df['Abert'].shift(abs(d))>df['Fech'].shift(1+abs(d))) & (df['Fech'].shift(abs(d))<df['Abert'].shift(1+abs(d))) & ((df['Fech'].shift(abs(d))-df['Abert'].shift(abs(d)))<=((df['Abert'].shift(1+abs(d))-df['Fech'].shift(1+abs(d)))/4))

        return df

    def harami_de_topo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Harami de Topo('+str(par)+')'] = (df['Fech']<df['Abert']) & (df['Fech'].shift(1)>df['Abert'].shift(1)) & (df['Abert']<df['Fech'].shift(1)) & (df['Fech']>df['Abert'].shift(1)) & ((df['Abert']-df['Fech']))<=((df['Fech'].shift(1)-df['Abert'].shift(1))/4)
        else:
            df['Harami de Topo('+str(par)+')'] = (df['Fech'].shift(abs(d))<df['Abert'].shift(abs(d))) & (df['Fech'].shift(1+abs(d))>df['Abert'].shift(1+abs(d))) & (df['Abert'].shift(abs(d))<df['Fech'].shift(1+abs(d))) & (df['Fech'].shift(abs(d))>df['Abert'].shift(1+abs(d))) & ((df['Abert'].shift(abs(d))-df['Fech'].shift(abs(d)))<=((df['Fech'].shift(1+abs(d))-df['Abert'].shift(1+abs(d)))/4))

        return df

    def pinca_de_fundo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Pinça de Fundo('+str(par)+')'] = ((df['Min']==df['Min'].shift(1)) | (df['Min']==df['Min'].shift(2)) | (df['Min']==df['Min'].shift(3))) & (df['Min']<=df['Min'].rolling(window=3).min())
        else:
            df['Pinça de Fundo('+str(par)+')'] = ((df['Min'].shift(abs(d))==df['Min'].shift(1+abs(d))) | (df['Min'].shift(abs(d))==df['Min'].shift(2+abs(d))) | (df['Min'].shift(abs(d))==df['Min'].shift(3+abs(d)))) & (df['Min'].shift(abs(d))<=df['Min'].rolling(window=3).min())

        return df

    def pinca_de_topo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Pinça de Topo('+str(par)+')'] = ((df['Max']==df['Max'].shift(1)) | (df['Max']==df['Max'].shift(2)) | (df['Max']==df['Max'].shift(3))) & (df['Max'] >= (df['Max'].rolling(window=3).max()))
        else:
            df['Pinça de Topo('+str(par)+')'] = ((df['Max'].shift(abs(d))==df['Max'].shift(1+abs(d))) | (df['Max'].shift(abs(d))==df['Max'].shift(2+abs(d))) | (df['Max'].shift(abs(d))==df['Max'].shift(3+abs(d)))) & (df['Max'].shift(abs(d)) >= (df['Max'].rolling(window=3).max()))

        return df

    def estrela_da_manha(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela da Manhã('+str(par)+')'] = (df['Fech']>df['Abert']) & (df['Fech']>df['Fech'].shift(2)) & (df['Fech'].shift(2)<df['Abert'].shift(2)) & (df['Fech','Abert'].max(axis=0).shift(1)<df['Fech'].shift(2)) & (df['Fech','Abert'].max(axis=0).shift(1)<df['Abert']) & ((df['Abert'].shift(1)-df['Fech'].shift(1))<=((df['Abert'].shift(2)-df['Fech'].shift(2))/4))
        else:
            df['Estrela da Manhã('+str(par)+')'] = (df['Fech'].shift(abs(d))>df['Abert'].shift(abs(d))) & (df['Fech'].shift(abs(d))>df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(2+abs(d))<df['Abert'].shift(2+abs(d))) & (df['Fech','Abert'].max(axis=0).shift(1+abs(d))<df['Fech'].shift(2+abs(d))) & (df['Fech','Abert'].max(axis=0).shift(1+abs(d))<df['Abert'].shift(abs(d))) & ((df['Abert'].shift(1+abs(d))-df['Fech'].shift(1+abs(d)))<=((df['Abert'].shift(2+abs(d))-df['Fech'].shift(2+abs(d)))/4))

        return df

    def estrela_da_tarde(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela da Tarde('+str(par)+')'] = (df['Fech']<df['Abert']) & (df['Fech']<df['Fech'].shift(2)) & (df['Fech'].shift(2)>df['Abert'].shift(2)) & (df['Fech','Abert'].min(axis=0).shift(1)>df['Fech'].shift(2)) & (df['Fech','Abert'].min(axis=0).shift(1)>df['Abert']) & ((df['Abert'].shift(1)-df['Fech'].shift(1))<=((df['Abert'].shift(2)-df['Fech'].shift(2))/4))
        else:
            df['Estrela da Tarde('+str(par)+')'] = (df['Fech'].shift(abs(d))<df['Abert'].shift(abs(d))) & (df['Fech'].shift(abs(d))<df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(2+abs(d))>df['Abert'].shift(2+abs(d))) & (df['Fech','Abert'].min(axis=0).shift(1+abs(d))>df['Fech'].shift(2+abs(d))) & (df['Fech','Abert'].min(axis=0).shift(1+abs(d))>df['Abert'].shift(abs(d))) & ((df['Abert'].shift(1+abs(d))-df['Fech'].shift(1+abs(d)))<=((df['Abert'].shift(2+abs(d))-df['Fech'].shift(2+abs(d)))/4))
        return df

    def bebe_abandonado_de_fundo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Bebê Abandonado de Fundo('+str(par)+')'] = (df['Fech']>df['Abert']) & (df['Fech']>df['Fech'].shift(2)) & (df['Fech'].shift(2)<df['Abert'].shift(2)) & (df['Max'].shift(1)<df['Min'].shift(2)) & (df['Max'].shift(1)<df['Min']) & ((df['Abert'].shift(1)-df['Fech'].shift(1))<=((df['Abert'].shift(2)-df['Fech'].shift(2))/4))
        else:
            df['Bebê Abandonado de Fundo('+str(par)+')'] = (df['Fech'].shift(abs(d))>df['Abert'].shift(abs(d))) & (df['Fech'].shift(abs(d))>df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(2+abs(d))<df['Abert'].shift(2+abs(d))) & (df['Max'].shift(1+abs(d))<df['Min'].shift(2+abs(d))) & (df['Max'].shift(1+abs(d))<df['Min'].shift(abs(d))) & ((df['Abert'].shift(1+abs(d))-df['Fech'].shift(1+abs(d)))<=((df['Abert'].shift(2+abs(d))-df['Fech'].shift(2+abs(d)))/4))

        return df

    def bebe_abandonado_de_topo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Bebê Abandonado de Topo('+str(par)+')'] = (df['Fech']<df['Abert']) & (df['Fech']<df['Fech'].shift(2)) & (df['Fech'].shift(2)>df['Abert'].shift(2)) & (df['Min'].shift(1)>df['Max'].shift(2)) & (df['Min'].shift(1)>df['Max']) & ((df['Abert'].shift(1)-df['Fech'].shift(1))<=((df['Abert'].shift(2)-df['Fech'].shift(2))/4))
        else:
            df['Bebê Abandonado de Topo('+str(par)+')'] = (df['Fech'].shift(abs(d))<df['Abert'].shift(abs(d))) & (df['Fech'].shift(abs(d))<df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(2+abs(d))>df['Abert'].shift(2+abs(d))) & (df['Min'].shift(1+abs(d))>df['Max'].shift(2+abs(d))) & (df['Min'].shift(1+abs(d))>df['Max'].shift(abs(d))) & ((df['Abert'].shift(1+abs(d))-df['Fech'].shift(1+abs(d)))<=((df['Abert'].shift(2+abs(d))-df['Fech'].shift(2+abs(d)))/4))
        return df

    def estrela_tripla_de_fundo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela Tripla de Fundo('+str(par)+')'] = (df['Fech']==df['Abert']) & (df['Fech'].shift(2)==df['Abert'].shift(2)) & (df['Fech'].shift(1)==df['Abert'].shift(1)) & (df['Fech'].shift(1)<df['Fech'].shift(2)) & (df['Fech'].shift(1)<df['Fech'])
        else:
            df['Estrela Tripla de Fundo('+str(par)+')'] = (df['Fech'].shift(abs(d))==df['Abert'].shift(abs(d))) & (df['Fech'].shift(2+abs(d))==df['Abert'].shift(2+abs(d))) & (df['Fech'].shift(1+abs(d))==df['Abert'].shift(1+abs(d))) & (df['Fech'].shift(1+abs(d))<df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(1+abs(d))<df['Fech'].shift(abs(d)))

        return df

    def estrela_tripla_de_topo(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['Estrela Tripla de Topo('+str(par)+')'] = (df['Fech']==df['Abert'])& (df['Fech'].shift(2)==df['Abert'].shift(2)) & (df['Fech'].shift(1)==df['Abert'].shift(1)) & (df['Fech'].shift(1)>df['Fech'].shift(2)) & (df['Fech'].shift(1)>df['Fech'])
        else:
            df['Estrela Tripla de Topo('+str(par)+')'] = (df['Fech'].shift(abs(d))==df['Abert'].shift(abs(d))) & (df['Fech'].shift(2+abs(d))==df['Abert'].shift(2+abs(d))) & (df['Fech'].shift(1+abs(d))==df['Abert'].shift(1+abs(d))) & (df['Fech'].shift(1+abs(d))>df['Fech'].shift(2+abs(d))) & (df['Fech'].shift(1+abs(d))>df['Fech'].shift(abs(d)))

        return df
                                                                                                                                                                                                                                                                                                                                                                                         

    #####
    ##Gap
    #####

    def gap_true_alta(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['GAP Verdadeiro de Alta('+str(par)+')'] = df['Max'].shift(1) < df['Min']
        else:
            df['GAP Verdadeiro de Alta('+str(par)+')'] = df['Max'].shift(1+abs(d)) < df['Min'].shift(abs(d))
        return df

    def gap_true_baixa(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['GAP Verdadeiro de Baixa('+str(par)+')'] = df['Min'].shift(1) > df['Max']
        else:
            df['GAP Verdadeiro de Baixa('+str(par)+')'] = df['Min'].shift(1+abs(d)) > df['Max'].shift(abs(d))
        return df

    def gap_fech_abert_alta(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['GAP - fechamento/abertura de Alta('+str(par)+')'] = df['Fech'].shift(1) < df['Abert']
        else:
            df['GAP - fechamento/abertura de Alta('+str(par)+')'] = df['Fech'].shift(1+abs(d)) < df['Abert'].shift(abs(d))
        return df

    def gap_fech_abert_baixa(self, df, parDia):
        par = parDia.replace(')', '').replace('(', '')
        d = int(par.split(',')[0])
        if abs(d) == 0:
            df['GAP - fechamento/abertura de Baixa('+str(par)+')'] = df['Fech'].shift(1) > df['Abert']
        else:
            df['GAP - fechamento/abertura de Baixa('+str(par)+')'] = df['Fech'].shift(1+abs(d)) > df['Abert'].shift(abs(d))
        return df

    ###############
    ##Médias Móveis
    ###############
    def fech_menos_med(self, df, par):                
        par = par.replace(')', '').replace('(', '')
        name = 'F-M('+par+')'

        par = int(par.split(',')[0])

        df[name] = df['Fech'] - df['Fech'].rolling(center=False,window=par).mean()

        return df, name
        
    def fech_cruza_cima_med(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Fechamento cruza para cima a média('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        d = int(par[1])
        
        df[med] = df['Fech'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = ((df['Fech']-df[med])>0.) & ((df['Fech'].shift(1)-df[med].shift(1))<0.)
        else:
            df[name] = ((df['Fech'].shift(abs(d))-df[med].shift(abs(d)))>0.) & ((df['Fech'].shift(1+abs(d))-df[med].shift(1+abs(d)))<0.)

        return df

    def fech_cruza_baixo_med(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Fechamento cruza para baixo a média('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        d = int(par[1])
        
        df[med] = df['Fech'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = ((df['Fech']-df[med])<0.) & ((df['Fech'].shift(1)-df[med].shift(1))>0.)
        else:
            df[name] = ((df['Fech'].shift(abs(d))-df[med].shift(abs(d)))<0.) & ((df['Fech'].shift(1+abs(d))-df[med].shift(1+abs(d)))>0.)

        return df

    def fech_menos_media_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Fechamento menos média >= X('+par+')'
        med = 'MA('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        df[med] = df['Fech'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Fech']-df[med])>=pX
        else:
            df[name] = (df['Fech'].shift(abs(d))-df[med].shift(abs(d)))>=pX

        return df

    def fech_menos_media_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Fechamento menos média <= X('+par+')'
        med = 'MA('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        df[med] = df['Fech'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Fech']-df[med])<=pX
        else:
            df[name] = (df['Fech'].shift(abs(d))-df[med].shift(abs(d)))<=pX

        return df

    def med1_menos_med2(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'M1-M2('+par+')'
        
        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])

        df[name] = df['Fech'].rolling(center=False,window=pMed1).mean() - df['Fech'].rolling(center=False,window=pMed2).mean()

        return df, name
    
    def med1_cruza_cima_med2(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Média_1 cruza para cima a Média_2('+par+')'
        med1 = 'MA_1('+par+')'
        med2 = 'MA_2('+par+')'
         
        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        d = int(par[2])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = ((df[med1]-df[med2])>0.) & ((df[med1].shift(1)-df[med2].shift(1))<0.)
        else:
            df[name] = ((df[med1].shift(abs(d))-df[med2].shift(abs(d)))>0.) & ((df[med1].shift(1+abs(d))-df[med2].shift(1+abs(d)))<0.)

        return df

    def med1_cruza_baixo_med2(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Média_1 cruza para baixo a Média_2('+par+')'
        med1 = 'MA_1('+par+')'
        med2 = 'MA_2('+par+')'
        
        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        d = int(par[2])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = ((df[med1]-df[med2])<0.) & ((df[med1].shift(1)-df[med2].shift(1))>0.)
        else:
            df[name] = ((df[med1].shift(abs(d))-df[med2].shift(abs(d)))<0.) & ((df[med1].shift(1+abs(d))-df[med2].shift(1+abs(d)))>0.)

        return df

    def med1_menos_med2_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Média_1 menos Média_2 >= X('+par+')'
        med1 = 'MA_1('+par+')'
        med2 = 'MA_2('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = (df[med1]-df[med2])>=pX
        else:
            df[name] = (df[med1].shift(abs(d))-df[med2].shift(abs(d)))>=pX

        return df

    def med1_menos_med2_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Média_1 menos Média_2 <= X('+par+')'
        med1 = 'MA_1('+par+')'
        med2 = 'MA_2('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = (df[med1]-df[med2])<=pX
        else:
            df[name] = (df[med1].shift(abs(d))-df[med2].shift(abs(d)))<=pX

        return df

    #################
    ##Bollinger Bands
    #################
    def percentB_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Percent B >= X('+par+')'
        med = 'MA('+par+')'
        std = 'STD('+par+')'
        bs = 'BS('+par+')'
        bi = 'BI('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pFact = float(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med] = df['Fech'].rolling(center=False, window=pMed).mean()
        df[std] = df['Fech'].rolling(center=False, window=pMed).std()
        df[bs] = df[med] + (pFact * df[std])
        df[bi] = df[med] - (pFact * df[std])
        if abs(d) == 0:            
            df[name] = (np.where(df[bs]==df[bi], 50.0, 100*(df['Fech']-df[bi])/(df[bs]-df[bi]))) >= pX
        else:
            df[name] = (np.where(df[bs].shift(abs(d))==df[bi].shift(abs(d)), 50.0, 100*(df['Fech'].shift(abs(d))-df[bi].shift(abs(d)))/(df[bs].shift(abs(d))-df[bi].shift(abs(d))))) >= pX

        return df

    def percentB_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Percent B <= X('+par+')'
        med = 'MA('+par+')'
        std = 'STD('+par+')'
        bs = 'BS('+par+')'
        bi = 'BI('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pFact = float(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med] = df['Fech'].rolling(center=False, window=pMed).mean()
        df[std] = df['Fech'].rolling(center=False, window=pMed).std()
        df[bs] = df[med] + (pFact * df[std])
        df[bi] = df[med] - (pFact * df[std])
        if abs(d) == 0:            
            df[name] = (np.where(df[bs]==df[bi], 50.0, 100*(df['Fech']-df[bi])/(df[bs]-df[bi]))) <= pX
        else:
            df[name] = (np.where(df[bs].shift(abs(d))==df[bi].shift(abs(d)), 50.0, 100*(df['Fech'].shift(abs(d))-df[bi].shift(abs(d)))/(df[bs].shift(abs(d))-df[bi].shift(abs(d))))) <= pX

        return df

    def bwidth_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'BandWidth >= X('+par+')'
        med = 'MA('+par+')'
        std = 'STD('+par+')'
        bs = 'BS('+par+')'
        bi = 'BI('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pFact = float(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med] = df['Fech'].rolling(center=False, window=pMed).mean()
        df[std] = df['Fech'].rolling(center=False, window=pMed).std()
        df[bs] = df[med] + (pFact * df[std])
        df[bi] = df[med] - (pFact * df[std])
        if abs(d) == 0:            
            df[name] = (100*(df[bs]-df[bi])/df[med]) >= pX
        else:
            df[name] = (100*(df[bs].shift(abs(d))-df[bi].shift(abs(d)))/df[med].shift(abs(d))) >= pX

        return df

    def bwidth_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'BandWidth <= X('+par+')'
        med = 'MA('+par+')'
        std = 'STD('+par+')'
        bs = 'BS('+par+')'
        bi = 'BI('+par+')'

        par = par.split(',')
        pMed = int(par[0])
        pFact = float(par[1])
        pX = float(par[2])
        d = int(par[3])

        df[med] = df['Fech'].rolling(center=False, window=pMed).mean()
        df[std] = df['Fech'].rolling(center=False, window=pMed).std()
        df[bs] = df[med] + (pFact * df[std])
        df[bi] = df[med] - (pFact * df[std])
        if abs(d) == 0:            
            df[name] = (100*(df[bs]-df[bi])/df[med]) <= pX
        else:
            df[name] = (100*(df[bs].shift(abs(d))-df[bi].shift(abs(d)))/df[med].shift(abs(d))) <= pX

        return df

    ######
    ##MACD
    ######
    def macd_cruza_sinal_cima(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'MACD cruza SINAL para cima('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pSinal = int(par[2])
        d = int(par[3])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[macd]>df[sinal]) & (df[macd].shift(1)<df[sinal].shift(1))
        else:
            df[name] = (df[macd].shift(abs(d))>df[sinal].shift(abs(d))) & (df[macd].shift(1+abs(d))<df[sinal].shift(1+abs(d)))

        return df

    def macd_cruza_sinal_baixo(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'MACD cruza SINAL para baixo('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pSinal = int(par[2])
        d = int(par[3])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[macd]<df[sinal]) & (df[macd].shift(1)>df[sinal].shift(1))
        else:
            df[name] = (df[macd].shift(abs(d))<df[sinal].shift(abs(d))) & (df[macd].shift(1+abs(d))>df[sinal].shift(1+abs(d)))

        return df

    def macd_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'MACD >= X('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
##        pSinal = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
##        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[macd] >= pX
        else:
            df[name] = df[macd].shift(abs(d)) >= pX

        return df

    def macd_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'MACD <= X('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
##        pSinal = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
##        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[macd] <= pX
        else:
            df[name] = df[macd].shift(abs(d)) <= pX

        return df

    def sinal_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'SINAL >= X('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pSinal = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[sinal] >= pX
        else:
            df[name] = df[sinal].shift(abs(d)) >= pX

        return df

    def sinal_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'SINAL <= X('+par+')'
        macd = 'MACD('+par+')'
        sinal = 'SINAL('+par+')'

        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pSinal = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[macd] =  (df['Fech'].ewm(span=pMed1, adjust=False).mean()) - (df['Fech'].ewm(span=pMed2, adjust=False).mean())
        df[sinal] = df[macd].ewm(span=pSinal, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[sinal] <= pX
        else:
            df[name] = df[sinal].shift(abs(d)) <= pX

        return df

    
    #####
    ##ADX
    #####
    def tr_dm(self, df):        
        dmpList=[]
        dmnList=[]
        trList=[]
        tr=0.0
        dmp=0.0
        dmn=0.0
        for i in range(0, df.index[-1]):
            if i<1:
                tr=0
                dmp=0
                dmn=0
            else:
                tr = max((df.loc[i, 'Max']-df.loc[i, 'Min']),abs(df.loc[i, 'Max']-df.loc[i-1, 'Fech']),abs(df.loc[i, 'Min']-df.loc[i-1, 'Fech']))
                if (df.loc[i, 'Max']-df.loc[i-1, 'Max'])>(df.loc[i-1, 'Min']-df.loc[i, 'Min']):
                    dmp = max((df.loc[i, 'Max']-df.loc[i-1, 'Max']),0)
                else:
                    dmp = 0
                if (df.loc[i-1, 'Min']-df.loc[i, 'Min'])>(df.loc[i, 'Min']-df.loc[i-1, 'Min']):
                    dmn = max((df.loc[i-1, 'Min']-df.loc[i, 'Min']),0)
                else:
                    dmn = 0
            if tr!=0:                
                dmpList.append(100*dmp/tr)
                dmnList.append(100*dmn/tr)
            else:
                dmpList.append(0)
                dmnList.append(0)
        return dmpList, dmnList
    
    def DIP_cruza_cima_DIN(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'DIp cruza DIn para cima('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        d = int(par[1])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[dip]>df[din]) & (df[dip].shift(1)<df[din].shift(1))
        else:
            df[name] = (df[dip].shift(abs(d))>df[din].shift(abs(d))) & (df[dip].shift(1+abs(d))<df[din].shift(1+abs(d)))

        return df

    def DIP_cruza_baixo_DIN(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'DIp cruza DIn para baixo('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        d = int(par[1])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[dip]<df[din]) & (df[dip].shift(1)>df[din].shift(1))
        else:
            df[name] = (df[dip].shift(abs(d))<df[din].shift(abs(d))) & (df[dip].shift(1+abs(d))>df[din].shift(1+abs(d)))

        return df

    def DIP_menos_DIN_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'DIp menos DIn >= X('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[dip]-df[din]) >= pX
        else:
            df[name] = (df[dip].shift(abs(d))-df[din].shift(abs(d))) >= pX

        return df

    def DIP_menos_DIN_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'DIp menos DIn <= X('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = (df[dip]-df[din]) <= pX
        else:
            df[name] = (df[dip].shift(abs(d))-df[din].shift(abs(d))) <= pX

        return df

    def ADX_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'ADX >= X('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'
        adx = 'ADX('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        df[adx] = 100*abs(df[dip]-df[din])/(df[dip]+df[din])
        df[adx] = df[adx].ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[adx] >= pX
        else:
            df[name] = df[adx].shift(abs(d))>= pX

        return df

    def ADX_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'ADX <= X('+par+')'
        dip = 'DIp('+par+')'
        din = 'DIn('+par+')'
        adx = 'ADX('+par+')'

        par = par.split(',')
        pAdx = int(par[0])
        pX = float(par[1])
        d = int(par[2])

        dmpList, dmnList = self.tr_dm(df)

        df[dip] = pd.Series(dmpList).ewm(span=pAdx, adjust=False).mean()
        df[din] = pd.Series(dmnList).ewm(span=pAdx, adjust=False).mean()
        df[adx] = 100*abs(df[dip]-df[din])/(df[dip]+df[din])
        df[adx] = df[adx].ewm(span=pAdx, adjust=False).mean()
        if abs(d) == 0:            
            df[name] = df[adx] <= pX
        else:
            df[name] = df[adx].shift(abs(d))<= pX

        return df
        
    #############
    ##Estocástico
    #############
    def K_cruza_cima_D(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'K cruza D para cima('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        d = int(par[3])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = (df[ks]>df[ds]) & (df[ks].shift(1)<df[ds].shift(1))
        else:
            df[name] = (df[ks].shift(abs(d))>df[ds].shift(abs(d))) & (df[ks].shift(1+abs(d))<df[ds].shift(1+abs(d)))

        return df

    def K_cruza_baixo_D(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'K cruza D para baixo('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        d = int(par[3])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = (df[ks]<df[ds]) & (df[ks].shift(1)>df[ds].shift(1))
        else:
            df[name] = (df[ks].shift(abs(d))<df[ds].shift(abs(d))) & (df[ks].shift(1+abs(d))>df[ds].shift(1+abs(d)))

        return df

    def K_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'K >= X('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
##        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
##        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = df[ks]>=pX
        else:
            df[name] = df[ks].shift(abs(d))>=pX

        return df

    def K_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'K <= X('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
##        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
##        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = df[ks]<=pX
        else:
            df[name] = df[ks].shift(abs(d))<=pX

        return df

    def D_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'D >= X('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = df[ds]>=pX
        else:
            df[name] = df[ds].shift(abs(d))>=pX

        return df

    def D_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'D <= X('+par+')'
        kf = 'Kf('+par+')'
        ks = 'Ks('+par+')'
        ds = 'ds('+par+')'

        par = par.split(',')
        pKF = int(par[0])
        pKS = int(par[1])
        pD = int(par[2])
        pX = float(par[3])
        d = int(par[4])

        df[kf] = 100*(df['Fech']-df['Min'].rolling(center=False,window=pKF).min())/(df['Max'].rolling(center=False,window=pKF).max()-df['Min'].rolling(center=False,window=pKF).min())
        df[kf].replace([np.inf, -np.inf, ''], float(100), inplace=True)
        df[ks] = df[kf].rolling(center=False, window=pKS).mean()
        df[ds] = df[ks].rolling(center=False, window=pD).mean()
        if abs(d) == 0:            
            df[name] = df[ds]<=pX
        else:
            df[name] = df[ds].shift(abs(d))<=pX

        return df

    ########
    ##Volume
    ########
    def vol_cruza_cima_med(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Volume cruza média para cima('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        d = int(par[1])
        
        df[med] = df['Volume'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Volume']>df[med]) & (df['Volume'].shift(1)<df[med].shift(1))
        else:
            df[name] = (df['Volume'].shift(abs(d))>df[med].shift(abs(d))) & (df['Volume'].shift(1+abs(d))<df[med].shift(1+abs(d)))

        return df

    def vol_cruza_baixo_med(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Volume cruza média para baixo('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        d = int(par[1])
        
        df[med] = df['Volume'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Volume']<df[med]) & (df['Volume'].shift(1)>df[med].shift(1))
        else:
            df[name] = (df['Volume'].shift(abs(d))<df[med].shift(abs(d))) & (df['Volume'].shift(1+abs(d))>df[med].shift(1+abs(d)))

        return df

    def vol_menos_med_maior(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Volume menos média >= X('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        pX = float(par[1])
        d = int(par[2])
        
        df[med] = df['Volume'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Volume']-df[med]) >= pX
        else:
            df[name] = (df['Volume'].shift(abs(d))-df[med].shift(abs(d))) >= pX

        return df

    def vol_menos_med_menor(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Volume menos média <= X('+par+')'
        med = 'MA('+par+')'
        
        par = par.split(',')
        pMed = int(par[0])
        pX = float(par[1])
        d = int(par[2])
        
        df[med] = df['Volume'].rolling(center=False,window=pMed).mean()
        if abs(d) == 0:
            df[name] = (df['Volume']-df[med]) <= pX
        else:
            df[name] = (df['Volume'].shift(abs(d))-df[med].shift(abs(d))) <= pX

        return df

    ###############
    ##Aleatoriedade
    ###############
    def aleatoriedade(self, df, par):
        df['Inserir Aleatoriedade'] = pd.Series(np.random.choice([True, False], df.size))
        return df

    ############
    ##Didi Index
    ############
    def didi_agulhada_compra(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Agulhada de Compra('+par+')'
        med1 = 'MA1('+par+')'
        med2 = 'MA2('+par+')'
        
        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pMed3 = int(par[2])
        d = int(par[3])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean() - df['Fech'].rolling(center=False,window=pMed2).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed3).mean() - df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = (df[med1]>0) & (df[med2]<0) & (df[med1].shift(1)<0) & (df[med2].shift(1)>0)
        else:
            df[name] = (df[med1].shift(abs(d))>0) & (df[med2].shift(abs(d))<0) & (df[med1].shift(1+abs(d))<0) & (df[med2].shift(1+abs(d))>0)

        return df

    def didi_agulhada_venda(self, df, par):
        par = par.replace(')', '').replace('(', '')
        name = 'Agulhada de Venda('+par+')'
        med1 = 'MA1('+par+')'
        med2 = 'MA2('+par+')'
        
        par = par.split(',')
        pMed1 = int(par[0])
        pMed2 = int(par[1])
        pMed3 = int(par[2])
        d = int(par[3])

        df[med1] = df['Fech'].rolling(center=False,window=pMed1).mean() - df['Fech'].rolling(center=False,window=pMed2).mean()
        df[med2] = df['Fech'].rolling(center=False,window=pMed3).mean() - df['Fech'].rolling(center=False,window=pMed2).mean()
        if abs(d) == 0:
            df[name] = (df[med1]<0) & (df[med2]>0) & (df[med1].shift(1)>0) & (df[med2].shift(1)<0)
        else:
            df[name] = (df[med1].shift(abs(d))<0) & (df[med2].shift(abs(d))>0) & (df[med1].shift(1+abs(d))>0) & (df[med2].shift(1+abs(d))<0)

        return df
         


    
    
