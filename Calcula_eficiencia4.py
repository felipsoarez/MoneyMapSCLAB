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

class Calcula_eficiencia4():
    def calcula(self, frame, quantidade_ativos, comprado_vendido, dt_normal,
                todas_entradas,preco_entrada,kEntrada,
                preco_fech, kSaida, PtsReais, custos,
                slvar, tpvar, slPP, tpPP,
                beStartvar, beStepvar):

        relColumns = ['DatasEntradas','DatasSaidas', 'EvolSaldoSemCusto', 'EvolSaldo', 'Saldos', 'SaldosRel', 'ValMax', 'ValMin', 'nCandOp']
        colNames = np.append(frame.columns.values, relColumns)
        result = pd.DataFrame(columns=colNames)

        aux_evolucao_saldoSemCustos = 0.
        aux_evolu_saldo = 0.
        
        total = frame.index[0]
        total_aux = frame.index[0]
        i = 0     

        while total < frame.index[-1]:
            total_aux = total

            if (frame.loc[total, "Setup Entrada"]):
                total+=kEntrada

                preco_ref = frame.loc[total, preco_entrada]
                data_entrada = frame.loc[total,'Data']
                
                maior_desvalorizacao = 0.0
                maior_valorizacao = 0.0
                ValMax=0.0
                ValMin=0.0

                ##Determiação de preços de sl e tp##
                preco_maximo = frame.loc[total,'Max']
                preco_minimo = frame.loc[total,'Min']
                stop_loss = ''
                take_profit = ''
                stop_loss_preco = 0.
                take_profit_preco = 0.
                beAtivo = False
                if slvar != 0:
                    if comprado_vendido == 'Operar comprado':
                        stop_loss_preco = preco_ref + slvar
                    else:
                        stop_loss_preco = preco_ref - slvar
                if tpvar != 0:
                    if comprado_vendido == 'Operar comprado':
                        take_profit_preco = preco_ref + tpvar
                    else:
                        take_profit_preco = preco_ref - tpvar
                if (beStepvar != 0) and (beStartvar != 0):
                    if comprado_vendido == 'Operar comprado':
                        break_even_start = preco_ref + beStartvar
                    else:
                        break_even_start = preco_ref - beStartvar
                        
                #############################################

                if kEntrada == 0: #creio que seja para evitar sair no mesmo dia
                    total+=1                    
                while total < frame.index[-1]:
                    ##Para calcular Stops
                    preco_maximo = frame.loc[total,'Max']
                    preco_minimo = frame.loc[total,'Min']
                    if slvar != 0:
                        if self.stopLossPontos(comprado_vendido, stop_loss_preco, preco_maximo, preco_minimo):#eval(sl):
                            stop_loss = 'FlagSL'
                            break
                    if (beStepvar != 0) and (beStartvar != 0) and (not beAtivo):
                        if self.breakevenPontos(comprado_vendido, break_even_start, preco_maximo, preco_minimo):
                            beAtivo=True 
                            if comprado_vendido == 'Operar comprado':
                                stop_loss_preco = preco_ref + beStepvar
                            else:
                                stop_loss_preco = preco_ref - beStepvar
                    if tpvar !=0:
                        if self.takeProfitPontos(comprado_vendido, take_profit_preco, preco_maximo, preco_minimo):#eval(tp):
                            take_profit = 'FlagTP'
                            break
##                    if slvar != 0:
##                        if self.stopLossPontos(comprado_vendido, preco_ref, preco_maximo, preco_minimo, slvar):#eval(sl):
##                            stop_loss = 'FlagSL'
##                            break
##                    if tpvar !=0:
##                        if self.takeProfitPontos(comprado_vendido, preco_ref, preco_maximo, preco_minimo, tpvar):#eval(tp):
##                            take_profit = 'FlagTP'
##                            break
                    if dt_normal == 'DayTrade' and data_entrada.date() != frame.loc[total,'Data'].date():
                        break
                    if (frame.loc[total, "Setup Saida"]):
                        break                    
                    total+=1

                total+=kSaida
                ##Determinação do preço de saida se houver stop. Ver depois
                if stop_loss == 'FlagSL':
                    if slPP == '%':
                        stp_loss_var = preco_ref*slvar/100
                    else:
                        stp_loss_var = slvar
                    if comprado_vendido == 'Operar comprado':
                        preco_saida = stop_loss_preco
                    else:
                        preco_saida = stop_loss_preco
                elif take_profit == 'FlagTP':
                    if tpPP == '%':
                        tk_profit_var = preco_ref*tpvar/100
                    else:
                        tk_profit_var = tpvar
                    if comprado_vendido == 'Operar comprado':
                        preco_saida = take_profit_preco
                    else:
                        preco_saida = take_profit_preco
                else:
                    preco_saida = frame.loc[total, preco_fech]
                
                data_saida = frame.loc[total,'Data']
                ValMax = frame['Max'][total_aux+kEntrada:total+1].max()
                ValMin = frame['Min'][total_aux+kEntrada:total+1].min()

                ##Determinação do Saldo, Maior Valorização e desvalorização
                if quantidade_ativos >= 1:####Add recentemente                    
                    if comprado_vendido == 'Operar comprado':
                        saldo = PtsReais*(-(quantidade_ativos*preco_ref) + (quantidade_ativos*preco_saida))
                        maior_desvalorizacao = PtsReais*(-(quantidade_ativos*preco_ref) + (quantidade_ativos*ValMin))
                        maior_valorizacao = PtsReais*(-(quantidade_ativos*preco_ref) + (quantidade_ativos*ValMax))
                    else:
                        saldo = PtsReais*((quantidade_ativos*preco_ref) - (quantidade_ativos*preco_saida))
                        maior_desvalorizacao = PtsReais*((quantidade_ativos*preco_ref) - (quantidade_ativos*ValMax))
                        maior_valorizacao = PtsReais*((quantidade_ativos*preco_ref) - (quantidade_ativos*ValMin))

                    aux_evolucao_saldoSemCustos += saldo
                    saldo = round((saldo - 2*custos),2)                   
                    saldo_rel = round(100*(saldo/(quantidade_ativos*preco_ref*PtsReais)), 4)
                    aux_evolu_saldo += saldo
                    nCandOp = total - total_aux
                    maior_desvalorizacao = maior_desvalorizacao - 2*custos
                    maior_valorizacao = maior_valorizacao - 2*custos

                    result.loc[i] = np.append(frame.loc[total_aux].values, 
                                          [data_entrada, data_saida, aux_evolucao_saldoSemCustos,
                                           aux_evolu_saldo, saldo, saldo_rel,maior_valorizacao - 2*custos,
                                           maior_desvalorizacao - 2*custos, nCandOp])

            i+=1
            if todas_entradas:
                total=total_aux ##ISSO AQUI DETERMINA SE O SALDO COM FILTRO IRÁ DAR CERTO. NÃO SE PODE ESPERAR QUE SEJA IGUAL SE NÃO PEGAR TODAS AS POSSÍVEIS ENTRADAS.
            total += 1        

        return result
                    

#######
##STOPS    
#######
    ##PONTOS
    def takeProfitPontos(self, comprado_vendido, take_profit_preco, preco_maximo, preco_minimo):
        if comprado_vendido == 'Operar comprado':
            if_1 = take_profit_preco <= preco_maximo
        else:
            if_1 = take_profit_preco >= preco_minimo
        return if_1

    def stopLossPontos(self, comprado_vendido, stop_loss_preco, preco_maximo, preco_minimo):
        if comprado_vendido == 'Operar comprado':
            if_1 = stop_loss_preco >= preco_minimo
        else:
            if_1 = stop_loss_preco <= preco_maximo
        return if_1
    def breakevenPontos(self, comprado_vendido, break_even_start, preco_maximo, preco_minimo):
        if comprado_vendido == 'Operar comprado':
            if_1 = break_even_start <= preco_maximo
        else:
            if_1 = break_even_start >= preco_minimo
        return if_1

    ##PERCENTUAL
    def takeProfitPercentual(self, comprado_vendido, preco_ref, preco_maximo, preco_minimo, var):
        if var == 0.0:
            return False
        else:
            if comprado_vendido == 'Operar comprado':
                if_1 = 100*(preco_maximo - preco_ref)/preco_ref >= var
            else:
                if_1 = 100*(preco_ref - preco_minimo)/preco_ref >= var
            return if_1

    def stopLossPercentual(self, comprado_vendido, preco_ref, preco_maximo, preco_minimo, var):
        if var == 0.0:
            return False
        else:
            if comprado_vendido == 'Operar comprado':
                if_1 = 100*(preco_minimo - preco_ref)/preco_ref <= var
            else:
                if_1 = 100*(preco_ref - preco_maximo)/preco_ref <= var
            return if_1













                
                
                
