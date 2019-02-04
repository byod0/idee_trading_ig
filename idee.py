from bs4 import BeautifulSoup
import requests
import unicodedata
import datetime
import os
from trading_ig_config import config2, epics
from trading_ig import IGService

page_sites = {
    "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-indices": "indices.csv",
    "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-forex" : "forex.csv",
    "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-matieres-premieres": "matieres-premieres.csv",
}
racine = 'https://www.ig.com'

class Ayam:
    def __init__(self):
        self.ig_service = IGService(username=config2.username,
                            password=config2.password,
                            api_key=config2.api_key,
                            acc_type=config2.acc_type)
        self.ig_service.create_session()

    def create_position(self, epic, direction, objectif, currency_info, qty):
        otc = self.ig_service.create_open_position(
            direction=direction,
            currency_code=currency_info,
            order_type="MARKET",
            size=qty,
            force_open=True,
            expiry="-",
            guaranteed_stop=False,
            epic= epic,
            limit_level=objectif,
            level=None,
            limit_distance=None,
            quote_id=None,
            stop_distance=None,
            stop_level=None,
        )
        return otc



def clear_data(input_str):
    r1 = remove_accents(input_str)
    r2= remove_upper(r1)
    return r2

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def remove_upper(input_str):
    return str.lower(input_str)

def get_all_links_on_page(page):
    r = requests.get(page)
    soup = BeautifulSoup(r.content, "html.parser")
    all_a = soup.find_all("a")
    link_list = list()
    for a in all_a:
        if "idee de trading :" in clear_data(a.text):
            link_list.append(racine + a.attrs['href'])
    return link_list

def delete_spec(input_str):
    my_str = input_str
    my_str1 = my_str.replace('points', '')
    my_str2 = my_str1.replace(':', '')
    my_str3 = my_str2.replace('$', '')
    my_str4 = my_str3.replace('¥', '')
    my_str5 = my_str4.replace('€', '')
    return my_str5

def parse_string(input_str):
    str1 = delete_spec(input_str)
    str2 = str1.split()
    if len(str2) == 2:
        decimal1 = str2[1]
        del str2[1]
        decimal_final = float(str(decimal1))
        str2.append(decimal_final)
    if len(str2) == 3:
        decimal1 = str2[1]
        decimal2 = str2[2]
        del str2[1:3]
        decimal_final = float(str(decimal1 + decimal2))
        str2.append(decimal_final)
    return str2

def get_date_page(idea_page):
    date_doc = idea_page[-6:]
    return datetime.datetime.strptime(date_doc, '%y%m%d')

def get_epic_link(soup):
    all_a = soup.find_all("a", {"class": "insight-link"})
    for asp in all_a:
        return racine + asp['href']

def parse_one_page(idea_page):
    res = dict()
    res['date'] = get_date_page(idea_page).strftime('%Y-%m-%d')

    r = requests.get(idea_page)
    soup = BeautifulSoup(r.content, "html.parser")
    res['epic_link'] = get_epic_link(soup)
    res['epic_code'] = get_epic(None, res['epic_link'] )
    res['link_id'] = idea_page

    datas = soup.find_all("p")
    for d in datas:
        if "Objectif" in d.text:
            my_str = d.get_text().replace(",",".")
            str_tree_part = my_str.split("\n")


            if len(str_tree_part) == 2:
                l = []
                objectif = d.text.replace(",",".").replace("\n","")
                l.append(objectif)
                stop = d.find_next_sibling("p").text.replace(",",".").replace("\n","")
                l.append(stop)
                str_tree_part = l

            for ss in str_tree_part:
                if "Objectif" in ss:
                    res['objectif'] = parse_string(ss)[1]
                if "Stop" in ss or "Invalidation" in ss:
                    res['stop'] = parse_string(ss)[1]
    return res

def check_existance_file(idea_page, ):
    filename = page_sites[idea_page]
    dir_filename = './{}'.format(filename)
    exist = os.path.isfile(dir_filename)
    if exist == False:
        with open(filename, 'a') as fd:
            fd.write('link_id'+'\n')
    return filename

def check_existing_record(filename, link_id):
    with open(filename) as f:
        for i, line in enumerate(f):
            if line.replace("\n","") == link_id:
                return True
    return False

def get_direction(res):
    if res['objectif'] > res['stop'] :
        return 'BUY'
    else:
        return 'SELL'

def get_epic(res, epic_ig_site):
    if epic_ig_site :
        if epics.epics[epic_ig_site]:
            return epics.epics[epic_ig_site]
    return False

ayam = Ayam()
def main():
    for page in page_sites:
        link_list = get_all_links_on_page(page)
        for idea_page in link_list:
            res = parse_one_page(idea_page)
            filename = check_existance_file(page)
            exist_link_id = check_existing_record(filename, res['link_id'])

            if exist_link_id == False:
                market_infos = ayam.ig_service.fetch_market_by_epic(res['epic_code'])
                currency_info = market_infos['instrument']['currencies'][0]['name']
                size_min = market_infos['dealingRules']['minDealSize']['value']

                if size_min > 1.0 :
                    pass
                else:
                    size_min = 1.0

                if res['epic_code'] == "CC.D.LCO.UME.IP":
                    obj = res['objectif']
                    res['objectif'] = obj * 100
                    stop = res['objectif']
                    res['stop'] = stop * 100

                otc = ayam.create_position(epic=res['epic_code'],
                                           objectif=res['objectif'],
                                           direction=get_direction(res),
                                           currency_info=currency_info,
                                           qty=size_min)
                print(datetime.datetime.today(), otc)
                if otc['reason'] == 'SUCCESS':
                    with open(filename, 'a') as fd:
                        fd.write(res['link_id']+'\n')

            # except:
            #     print('Bug sur la page:', idea_page)


main()

# res_ok = parse_one_page("https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-indices/idee-de-trading---achat-allemagne-30-au-comptant-190125")
# print(res_ok)
# print()
# res = parse_one_page("https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-forex/idee-trading-eur-usd-190122")
# print(res)

# import_json('IX.D.CAC.IMF.IP','files/france40.json')
# import_json('IX.D.DAX.IFMM.IP','files/allemagne_30.json')
# import_json('IX.D.DOW.IFE.IP','files/wall_street.json')
# import_json('IX.D.FTSE.IFE.IP','files/ftse_100.json')
# import_json('IX.D.HANGSENG.IFM.IP','files/hong_kong_hs50.json')
# import_json('IX.D.NASDAQ.IFE.IP','files/us_tech_100.json')
# import_json('IX.D.NIKKEI.IFM.IP','files/japon_225.json')
# import_json('IX.D.SPTRD.IFE.IP','files/us_spx_500.json')
# import_json('IX.D.STXE.IFM.IP','files/eu_stock_50.json')
#
# import_json('CS.D.EURUSD.CFD.IP','files/eur_usd.json')
# import_json('CS.D.GBPUSD.CFD.IP','files/gbp_usd.json')
# import_json('CS.D.USDJPY.CFD.IP','files/usd_jpy.json')
# import_json('CS.D.AUDUSD.CFD.IP','files/aud_usd.json')
#
# import_json('CC.D.CL.UME.IP','files/brut_leger.json')
# import_json('CC.D.LCO.UME.IP','files/brut_brent.json')
# import_json('CS.D.CFDSILVER.CFDSI.IP','files/argent_5000.json')
# import_json('CS.D.CFEGOLD.CFE.IP','files/or.json')

# def scan_all_pages():
#     import csv
#     # page_sites_indice = "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-indices/page-%s"
#     page_sites_forex = "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-forex/page-%s"
#     page_sites_matiere = "https://www.ig.com/fr/marche-actualites-et-idees-de-trading/actu-matieres-premieres/page-%s"
#
#     fields = ['epic_link', 'epic_code','date','objectif','stop']
#
#     with open('indice_1_19.csv', 'w') as csvfile:
#         filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#         filewriter.writerow(fields)
#         for i in range(1,20): #limit 70 pour indice
#             link_list = get_all_links_on_page(page_sites_matiere % i)
#             for idea_page in link_list:
#                 try:
#                     res = parse_one_page(idea_page)
#                     print(res)
#                     filewriter.writerow(
#                         [str(res['epic_link']),
#                         str(res['epic_code']),
#                         str(res['date']),
#                         str(res['objectif']),
#                         str(res['stop'])]
#                         )
#
#                 except:
#                     pass
# scan_all_pages()