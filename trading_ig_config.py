#!/usr/bin/env python
#-*- coding:utf-8 -*-

class config(object):
    username = "xxxx"
    password = "xxxx"
    api_key = "xxxx"
    acc_type = "DEMO" # LIVE / DEMO
    acc_number = "xxxx"

class config2(object):
    username = "xxxx"
    password = "xxxx"
    api_key = "xxxx"
    acc_type = "DEMO" # LIVE / DEMO
    acc_number = "xxxx"
    
class epics(object):
    epics = {
        'https://www.ig.com/fr/indices/marches-indices/allemagne-30':'IX.D.DAX.IFMM.IP',
        'https://www.ig.com/fr/indices/marches-indices/wall-street':  'IX.D.DOW.IFE.IP',
        'https://www.ig.com/fr/indices/marches-indices/france-40':'IX.D.CAC.IMF.IP',
        'https://www.ig.com/fr/indices/marches-indices/japon-225':'IX.D.NIKKEI.IFM.IP',
        'https://www.ig.com/fr/indices/marches-indices/us-spx-500':'IX.D.SPTRD.IFE.IP',

        'https://www.ig.com/fr/indices/marches-indices/ftse-100-au-comptant':'IX.D.FTSE.IFE.IP',
        'https://www.ig.com/fr/indices/marches-indices/hong-kong-hs42':'IX.D.HANGSENG.IFM.IP',
        'https://www.ig.com/fr/indices/marches-indices/us-tech-100':'IX.D.NASDAQ.IFE.IP',
        'https://www.ig.com/fr/indices/marches-indices/eu-stocks-50':'IX.D.STXE.IFM.IP',

        'https://www.ig.com/fr/forex/marches-forex/spot-eur-usd':'CS.D.EURUSD.CFD.IP',
        'https://www.ig.com/fr/forex/marches-forex/spot-gbp-usd':'CS.D.GBPUSD.CFD.IP',
        'https://www.ig.com/fr/forex/marches-forex/spot-usd-jpy':'CS.D.USDJPY.CFD.IP',
        'https://www.ig.com/fr/forex/marches-forex/spot-aud-usd':'CS.D.AUDUSD.CFD.IP',

        'https://www.ig.com/fr/matieres-premieres/marches-matieres-premieres/us-brut-leger':'CC.D.CL.UME.IP',
        'https://www.ig.com/fr/matieres-premieres/marches-matieres-premieres/brut-brent':'CC.D.LCO.UME.IP',
        'https://www.ig.com/fr/matieres-premieres/marches-matieres-premieres/argent-au-comptant-5-000oz':'CS.D.CFDSILVER.CFDSI.IP',
        'https://www.ig.com/fr/matieres-premieres/marches-matieres-premieres/or-au-comptant':'CS.D.CFEGOLD.CFE.IP',
    }
