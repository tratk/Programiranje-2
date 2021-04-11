import datetime
import matplotlib.pyplot as plt
import math
import re
import requests

#stran, kjer je obrazložitev podatkov: http://exoplanet.eu/readme/
#masa_sini: https://en.wikipedia.org/wiki/Minimum_mass
#perioda: obhodni čas planeta
#velika polos: daljša stranica elipse, ki predstavlja orbito
#ekscentričnost: 'sploščenost' orbite
#inklčinacija: kot med ravnino orbite planeta in daljico zemlja-zvezda
#kotna razdalja: kot med daljicama zvezda-zemlja, planet-zemlja
#albedo: https://en.wikipedia.org/wiki/Albedo
#rektascenzija: https://en.wikipedia.org/wiki/Right_ascension
#deklinacija: https://en.wikipedia.org/wiki/Declination
#magnituda: https://en.wikipedia.org/wiki/Apparent_magnitude
#razmerje kovin = https://en.wikipedia.org/wiki/Metallicity
#spektralni tip: https://en.wikipedia.org/wiki/Stellar_classification#Spectral_types

class Planet: 
    def __init__(self, ime, masa, masa_sini, radij, perioda, velika_polos, ekscentricnost, inklinacija, \
        kotna_razdalja, odkritje, izracunana_T, izmerjena_T, albedo, gravitacija, detekcija, \
            masa_detekcija, radij_detekcija, zvezda):
        
        self.ime = ime
        if masa == 'None': #maso in maso_sini oboje shranim v eno spremenljivko
            if masa_sini == 'None':
                self.masa = None
            else:
                self.masa = float(masa_sini)
        else:
            self.masa = float(masa)
        
        if radij == 'None':
            self.radij = None
        else:
            self.radij = float(radij)
        
        if perioda == 'None':
            self.perioda = None
        else:
            self.perioda = float(perioda)
        
        if velika_polos == 'None':
            self.velika_polos = None
        else:
            self.velika_polos = float(velika_polos)
        
        if ekscentricnost == 'None':
            self.ekscentricnost = None
        else:
            self.ekscentricnost = float(ekscentricnost)
        
        if inklinacija == 'None':
            self.inklinacija = None
        else:
            self.inklinacija = float(inklinacija)

        if kotna_razdalja == 'None':
            self.kotna_razdalja = None
        else:
            self.kotna_razdalja = float(kotna_razdalja)
        
        if odkritje == 'None':
            self.leto_odkritja = None
        else:
            self.leto_odkritja = int(odkritje)
        
        if izracunana_T == 'None':
            self.izracunana_temperatura = None
        else:
            self.izracunana_temperatura = float(izracunana_T)

        if izmerjena_T == 'None':
            self.izmerjena_temperatura = None
        else:
            self.izmerjena_temperatura = float(izmerjena_T)
        
        if albedo == 'None':
            self.albedo = None
        else:
            self.albedo = float(albedo)
        
        if gravitacija == 'None':
            self.gravitacija = None
        else:
            self.gravitacija = float(gravitacija)

        self.detekcija = detekcija
        self.masa_detekcija = masa_detekcija
        self.radij_detekcija = radij_detekcija
        self.zvezda = zvezda
        self.ostali_planeti = set()

    def dodaj_planet(self, planet_ime):
        self.ostali_planeti.add(planet_ime)


    def __str__(self):
        ostali_planeti = 'None'
        for el in self.ostali_planeti:
            if len(ostali_planeti) == 0:
                ostali_planeti = el
            else:
                ostali_planeti += ', {}'.format(el)
        return 'Ime: {}\nMasa: {} [mJup]\nRadij: {} [rJup]\n'.format(self.ime, self.masa, self.radij) +\
            'Perioda: {} [dni]\nVelika polos: {} [AU]\n'.format(self.perioda, self.velika_polos) +\
                'Ekscentričnost: {}\nInklinacija: {} [°]\n'.format(self.ekscentricnost, self.inklinacija) +\
                    'Kotna razdalja: {} [arcsec]\nLeto odkritja: {}\nIzračunana temperatura: {} [K]\n'.format(self.kotna_razdalja, self.leto_odkritja, self.izracunana_temperatura) +\
                        'Izmerjena temperatura: {} [K]\nAlbedo: {}\n'.format(self.izmerjena_temperatura, self.albedo) +\
                            'Gravitacija na površju: {} [g]\nNačin detekcije: {}\n'.format(self.gravitacija, self.detekcija) +\
                                'Način detekcije mase: {}\nNačin detekcije radija: {}\n'.format(self.masa_detekcija, self.radij_detekcija) +\
                                    'Zvezda: {}\nOstali planeti: {}'.format(self.zvezda, ostali_planeti)
    

    def __repr__(self):
        return 'Planet({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'\
            .format(self.ime, self.masa, self.radij, self.perioda, self.velika_polos, self.ekscentricnost, \
                self.inklinacija, self.kotna_razdalja, self.leto_odkritja, self.izracunana_temperatura, \
                    self.izmerjena_temperatura, self.albedo, self.gravitacija, self.masa_detekcija, \
                        self.radij_detekcija, self.zvezda, self.ostali_planeti)
    
    def podobnost(self, other):
        '''Izracuna podobnost med dvema planetoma, tako da za določene parametre izračuna relativno razdaljo
        med parametrom enega in drugega planeta vr = (|a-b|/max(|a|, |b|)) in jih sešteje. Različni parametri imajo različno utež.
        Večja kot je vrednost, bolj sta podobna'''
        vr = 0
        if self.masa != None and other.masa != None: #samo če imata oba planeta definirani masi
            vr += (1 - abs(self.masa - other.masa) / max(self.masa, other.masa)) * 2 #utež *2, saj je masa bolj pomembna za določanje podobnosti
        
        if self.radij != None and other.radij != None:
            vr += (1 - abs(self.radij - other.radij) / max(self.radij, other.radij)) * 2 #večino vrednosti ni treba dajati v absolutno vrednost, saj niso nikoli negativne
        
        if self.perioda != None and other.perioda != None:
            vr += (1 - abs(self.perioda - other.perioda) / max(self.perioda, other.perioda)) * 2
        
        if self.velika_polos != None and other.velika_polos != None:
            vr += (1 - abs(self.velika_polos - other.velika_polos) / max(self.velika_polos, other.velika_polos)) * 2
        
        if self.ekscentricnost != None and other.ekscentricnost != None:
            if self.ekscentricnost == 0 and other.ekscentricnost == 0:
                vr += 1
            else:
                vr += 1 - abs(self.ekscentricnost - other.ekscentricnost) / max(self.ekscentricnost, other.ekscentricnost)
        
        if self.izmerjena_temperatura != None and other.izmerjena_temperatura != None: #izračunano in izmerjeno temperaturo obravnavam z isto vrednostjo
            vr += (1 - abs(self.izmerjena_temperatura - other.izmerjena_temperatura) / max(self.izmerjena_temperatura, other.izmerjena_temperatura)) * 2
        elif self.izracunana_temperatura != None and other.izracunana_temperatura != None:
            vr += (1 - abs(self.izracunana_temperatura - other.izracunana_temperatura) / max(self.izracunana_temperatura, other.izracunana_temperatura)) * 2
        
        if self.albedo != None and other.albedo != None:
            if self.albedo == 0 and other.albedo == 0:
                vr += 1
            else:
                vr += 1 - abs(self.albedo - other.albedo) / max(self.albedo, other.albedo)
        
        if len(self.ostali_planeti) == len(other.ostali_planeti) == 0:
            vr += 1
        else:
            vr += 1 - abs(len(self.ostali_planeti) - len(other.ostali_planeti)) / max(len(self.ostali_planeti), len(other.ostali_planeti))
        return vr



class Zvezda:
    def __init__(self, ime, rektascenzija, deklinacija, magnituda, oddaljenost, razmerje_kovin, masa, radij, \
        spektralni_tip, starost, efektivna_T, planet):

        self.ime = ime
        
        if rektascenzija == 'None':
            self.rektascenzija = None
        else:
            self.rektascenzija = float(rektascenzija)
        
        if deklinacija == 'None':
            self.deklinacija = None
        else:
            self.deklinacija = float(deklinacija)
        
        if magnituda == 'None':
            self.magnituda = None
        else:
            self.magnituda = float(magnituda)
        
        if oddaljenost == 'None':
            self.oddaljenost = None
        else:
            self.oddaljenost = float(oddaljenost)
        
        if razmerje_kovin == 'None':
            self.razmerje = None
        else:
            self.razmerje = float(razmerje_kovin)

        if masa == 'None':
            self.masa = None
        else:
            self.masa = float(masa)
        
        if radij == 'None':
            self.radij = None
        else:
            self.radij = float(radij)
        
        self.spektalni_tip = spektralni_tip

        if starost == 'None':
            self.starost = None
        else:
            self.starost = float(starost)
        
        if efektivna_T == 'None':
            self.temperatura = None
        else:
            self.temperatura = float(efektivna_T)

        self.planeti = set()
        self.planeti.add(planet)

    def dodaj_planet(self, planet_ime):
        self.planeti.add(planet_ime)
    

    def __str__(self):
        planeti = 'None'
        for el in self.planeti:
            if planeti == 'None':
                planeti = el
            else:
                planeti += ', {}'.format(el)
            
        return 'Ime: {}\nRektascenzija: {} [°]\nDeklinacja: {} [°]\n'.format(self.ime, self.rektascenzija, self.deklinacija) +\
            'Magnituda v vidnem: {}\nOddaljenost: {} [pc]\nRazmerje kovin proti vodiku: {}\n'.format(self.magnituda, self.oddaljenost, self.razmerje) +\
                'Masa: {} [mSonca]\nRadij: {} [rSonca]\nSpektralni tip: {}\n'.format(self.masa, self.radij, self.spektalni_tip) +\
                    'Starost: {} [Glet]\nTemperatura: {} [K]\nPlaneti: {}'.format(self.starost, self.temperatura, planeti)

    
    def __repr__(self):
        return 'Zvezda({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.ime, self.rektascenzija, \
            self.deklinacija, self.magnituda, self.oddaljenost, self.razmerje, self. masa, self.radij, \
                self.spektalni_tip, self.starost, self.temperatura, self.planeti)
    
    def podobnost(self, other):
        '''Enako kot pri planetu izracuna podobnost med dvema zvezdama, z drugačnimi utežmi.'''
        vr = 0
        
        if self.oddaljenost != None and other.oddaljenost != None:
            vr += (1 - abs(self.oddaljenost - other.oddaljenost) / max(self.oddaljenost, other.oddaljenost)) * 0.5
        
        if self.razmerje != None and other.razmerje != None:
            if self.razmerje == other.razmerje == 0:
                vr += 1
            else:
                vr += 1 - abs(self.razmerje - other.razmerje) / max(abs(self.razmerje), abs(other.razmerje)) #razmerje je lahko negativno
    
        if self.masa != None and other.masa != None:
            vr += (1 - abs(self.masa- other.masa) / max(self.masa, other.masa)) * 2
        
        if self.radij != None and other.radij != None:
            vr += (1 - abs(self.radij - other.radij) / max(self.radij, other.radij)) * 2
        
        if self.starost != None and other.starost != None:
            vr += (1 - abs(self.starost - other.starost) / max(self.starost, other.starost)) * 2
        
        if self.temperatura != None and other.temperatura != None:
            vr += (1 - abs(self.temperatura - other.temperatura) / max(self.temperatura, other.temperatura)) * 2
    
        return vr
        



        


def ustvari_razrede():
    '''Iz podatkov v datoteki ustvari razred za planet in zvezdo ter jih shrani v seznam oblike ime:razred.'''
    planeti_podatki = dict()
    zvezde_podatki = dict()

    for vrstica in open('podatki.txt', 'r'):
        podatki = vrstica.split(',')
        if podatki[0] == '# name': #preskočim prvo vrstico
            continue
        planet = Planet(podatki[0], podatki[1], podatki[2], podatki[3], podatki[4], podatki[5], podatki[6], \
            podatki[7], podatki[8], podatki[9], podatki[10], podatki[11], podatki[12], podatki[13], podatki[14], \
                podatki[15], podatki[16], podatki[17])
    
        zvezda = Zvezda(podatki[17], podatki[18], podatki[19], podatki[20], podatki[21], podatki[22], podatki[23], \
            podatki[24], podatki[25], podatki[26], podatki[27].rstrip(), podatki[0])
    

        planeti_podatki[podatki[0]] = planet
        if podatki[17] not in zvezde_podatki: #če ni še te zvezde v seznamu, jo dodam
            zvezde_podatki[podatki[17]] = zvezda
        else: #če je že v seznamu, pa zvezdi dodam ta planet in planetu dodam ostale planete iz tega sistema
            for el in zvezde_podatki[podatki[17]].planeti:
                planeti_podatki[el].dodaj_planet(podatki[0])
                planet.dodaj_planet(el)
            zvezde_podatki[podatki[17]].dodaj_planet(podatki[0])
    return planeti_podatki, zvezde_podatki


def narisi_graf(x_os, y_os, shrani, x_log, y_log):
    '''Narise graf podanih parametrov.'''
    moznosti = {'masa planeta' : (1, 'mJupitra'), 'radij planeta' : (3, 'rJupitra'), 'perioda planeta' : (4, 'dni'), \
        'velika polos planeta' : (5, 'AU'), 'ekscentricnost planeta' : (6, ''), 'inklinacija planeta': (7, '°'), \
            'kotna razdalja planeta' : (8, 'arcsec'), 'leto odkritja planeta' : (9, 'leto'), 'izracunana temperatura planeta' : (10, 'K'), \
            'izmerjena temperatura planeta' : (11, 'K'), 'albedo planeta' : (12, ''), 'gravitacija planeta' : (13, 'g'), \
                'rektascenzija zvezde' : (18, '°'), 'deklinacija zvezde' : (19, '°'), 'magnituda zvezde' : (20, ''), \
                    'oddaljenost zvezde' : (21, 'pc'), 'razmerje kovin zvezde' : (22, ''), 'masa zvezde' : (23, 'mSonca'), \
                        'radij zvezde' : (24, 'rSonca'), 'starost zvezde' : (26, 'Glet'), 'temperatura zvezde' : (27, 'K')}

    if x_os not in moznosti or y_os not in moznosti:
        raise Exception('Izberi x-os in y-os iz seznama.')
    
    i_x = moznosti[x_os][0] #indeks, na katerem najdem podatek za to os ko razdelim posamezno vrstico s split(',')
    i_y = moznosti[y_os][0]

    enota_x = moznosti[x_os][1]
    enota_y = moznosti[y_os][1]
    x_vrednosti = []
    y_vrednosti = []
    for vrstice in open('podatki.txt', 'r'): #grem čez vse podatke in dodam v tabeli obe vrednosti, če sta obe podani
        vrstica = vrstice.rstrip().split(',')
        if vrstica[0] == '# name': #preskočim prvo vrstico
            continue
        if x_os == 'masa planeta' and y_os == 'masa planeta': #masa in masa_sini se shrani kot ista vrednost, zato moram posebej obravnavati
            if vrstica[1] == 'None':
                if vrstica[2] == 'None': #če katera od vrednosti ni podana nadaljujem
                    continue
                else:
                    x_vrednosti.append(float(vrstica[2]))
                    y_vrednosti.append(float(vrstica[2]))
            else:
                x_vrednosti.append(float(vrstica[1]))
                y_vrednosti.append(float(vrstica[1]))
        elif x_os == 'masa planeta' and y_os != 'masa planeta':
            if vrstica[i_y] == 'None': #če katera od vrednosti ni podana nadaljujem
                continue
            else:
                if vrstica[1] == 'None':
                    if vrstica[2] == 'None': #ne masa ne masa_sini nista podani
                        continue
                    else:
                        x_vrednosti.append(float(vrstica[2]))
                        y_vrednosti.append(float(vrstica[i_y]))
                else:
                    x_vrednosti.append(float(vrstica[1]))
                    y_vrednosti.append(float(vrstica[i_y]))
        elif x_os != 'masa_planeta' and y_os == 'masa planeta':
            if vrstica[i_x] == 'None':
                continue
            else:
                if vrstica[1] == 'None':
                    if vrstica[2] == 'None': #ne masa ne masa_sini nista podani
                        continue
                    else:
                        x_vrednosti.append(float(vrstica[i_x]))
                        y_vrednosti.append(float(vrstica[2]))
                else:
                    x_vrednosti.append(float(vrstica[i_x]))
                    y_vrednosti.append(float(vrstica[1]))
        else:
            if vrstica[i_x] == 'None' or vrstica[i_y] == 'None':
                continue
            else:
                x_vrednosti.append(float(vrstica[i_x]))
                y_vrednosti.append(float(vrstica[i_y]))
    
    if x_log or y_log:
        j = 0
        for i in range(len(x_vrednosti)):
            if x_log and y_log:
                try: #vrednosti, ki so negativne, ne morem narisati na logaritmiran graf, zato jih izbrišem
                    x_vrednosti[j] = math.log10(x_vrednosti[j])
                    y_vrednosti[j] = math.log10(y_vrednosti[j])
                    j += 1
                except:
                    del x_vrednosti[j]
                    del y_vrednosti[j]
            elif x_log: #vrednosti, ki so negativne, ne morem narisati na logaritmiran graf, zato jih izbrišem
                try:
                    x_vrednosti[j] = math.log10(x_vrednosti[j])
                    j += 1
                except:
                    del x_vrednosti[j]
                    del y_vrednosti[j]
            elif y_log:
                try: #vrednosti, ki so negativne, ne morem narisati na logaritmiran graf, zato jih izbrišem
                    y_vrednosti[j] = math.log10(y_vrednosti[j])
                    j += 1
                except:
                    del x_vrednosti[j]
                    del y_vrednosti[j]

    
    plt.scatter(x_vrednosti, y_vrednosti, s = 2)
    plt.xlabel('{} [{}]'.format(x_os, enota_x))
    plt.ylabel('{} [{}]'.format(y_os, enota_y))
    if x_log:
        plt.xscale('log')
    if y_log:
        plt.yscale('log')
    if shrani:
        plt.savefig('{}-{}.png'.format(x_os, y_os))
    plt.show()


def poisci_podobne(objekt, planeti, zvezde):
    '''Ustvari seznam, kjer za vsak planet ali zvezdo v podatkih izračuna podobnost s podanim objektom z ugrajeno
     funkcijo razreda in jo shrani v seznam vrednost:ime'''
    podobnosti = dict()
    if isinstance(objekt, Planet):
        for planet in planeti.values():
            vrednost = planet.podobnost(objekt)
            podobnosti[vrednost] = planet.ime
    else:
        for zvezda in zvezde.values():
            vrednost = zvezda.podobnost(objekt)
            podobnosti[vrednost] = zvezda.ime
    return podobnosti



def poisci_planet(zvezda, planeti, zvezde):
    '''Za podano zvezdo poišče planet, ki ga lahko pričakujemo ob taki zvezdi. Izračuna povprečje podatkov planetov, ki
    so zraven zvezd, ki so dovolj podobne podani zvezdi'''
    podatki = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] #[masa, radij, perioda, velika polos, ekscentričnost, temperatura, albedo]
    podobnosti = poisci_podobne(zvezda, planeti, zvezde)
    for vrednost, ime in podobnosti.items():
        if vrednost < 6: #ni dovolj podobna
            continue
        for el in zvezde[ime].planeti: #vai planeti zraven te zvezde
            planet = planeti[el]
            for i in range(7):
                if i == 0:
                    if planet.masa != None:
                        podatki[0][0] += planet.masa
                        podatki[0][1] += 1
                if i == 1:
                    if planet.radij != None:
                        podatki[1][0] += planet.radij
                        podatki[1][1] += 1
                if i == 2:
                    if planet.perioda != None:
                        podatki[2][0] += planet.perioda
                        podatki[2][1] += 1
                if i == 3:
                    if planet.velika_polos != None:
                        podatki[3][0] += planet.velika_polos
                        podatki[3][1] += 1
                if i == 4:
                    if planet.ekscentricnost != None:
                        podatki[4][0] += planet.ekscentricnost
                        podatki[4][1] += 1
                if i == 5:
                    if planet.izmerjena_temperatura != None:
                        podatki[5][0] += planet.izmerjena_temperatura
                        podatki[5][1] += 1
                    elif planet.izracunana_temperatura != None:
                        podatki[5][0] += planet.izracunana_temperatura
                        podatki[5][1] += 1
                if i == 6:
                    if planet.albedo != None:
                        podatki[6][0] += planet.albedo
                        podatki[6][1] += 1
    for i in range(7):
        if podatki[i][1] == 0: #če ni imel noben preiskan planet podano to vrednost
            podatki[i][1] = 1
    
    return Planet('planet', round(podatki[0][0]/podatki[0][1], 2), 'None', round(podatki[1][0]/podatki[1][1], 2), round(podatki[2][0]/podatki[2][1], 2), \
        round(podatki[3][0]/podatki[3][1], 2), round(podatki[4][0]/podatki[4][1], 2), 'None', 'None', 'None', round(podatki[5][0]/podatki[5][1], 2), \
            round(podatki[5][0]/podatki[5][1], 2), round(podatki[6][0]/podatki[6][1], 2), 'None', 'None', 'None', 'None', 'zvezda')

#podatki, ki sem jih izbral
pod = ['# name', 'mass', 'mass_sini', 'radius', 'orbital_period', 'semi_major_axis', 'eccentricity', \
'inclination', 'angular_distance', 'discovered', 'temp_calculated', 'temp_measured', \
    'geometric_albedo', 'log_g', 'detection_type', 'mass_detection_type', 'radius_detection_type', \
        'star_name', 'ra', 'dec', 'mag_v', 'star_distance', 'star_metallicity', 'star_mass', 'star_radius', \
             'star_sp_type', 'star_age', 'star_teff']

#pridobivanje podatkov iz interneta in zapisovanje v datoteko
r = requests.get('http://exoplanet.eu/catalog/csv').text.split('\n')
podatki1 = r[0].split(',')
indeksi = []
for el in pod: #indeksi, na katerih najdem izbrane podatke
    indeksi.append(podatki1.index(el))

f = open('podatki.txt', 'w', encoding = 'utf-8')
f1 = open('nefiltrirani_podatki.txt', 'w', encoding = 'utf-8')
for i in range(len(r) - 1):
    f1.write(r[i])
    if re.search('".+?"', r[i]) == None: #nekateri podatki imajo več vrednosti v "" ločenimi z vejicami, kar ne morem ločiti s split(','), zato jih zamenjam s ''
        vrstica = r[i]
    else:
        vrstica = re.sub('".+?"', '', r[i])
    podatki = vrstica.rstrip().split(',')
    for el in indeksi:
        if podatki[el] == '': #za nepodane podatke zamenjam '' s None za lepšo preglednost in da se izognem težavam na koncu vrstic
            podatki[el] = 'None'
    if i != len(r) - 1:
        f.write(','.join([podatki[j] for j in indeksi]) + '\n')
    else:
        f.write(','.join([podatki[j] for j in indeksi]))
f.close()
f1.close()


planeti, zvezde = ustvari_razrede()
#del, ki sprašuje uporabnika, kaj hoče narediti
print('Živijo!')
while True:
    print('Kaj bi rad naredil?\n1 - poišči planet ali zvezdo po imenu\n2 - ustvari graf glede na izbrane parametre\n' + \
        '3 - ustvari planet ali zvezdo in poišči podobne objekte ali v kakšnih sistemih jih lahko pričakuješ\n4 - končaj program')
    while True:
        vnos = input('Vnesi število: ')
        if vnos != '1' and vnos != '2' and vnos != '3'and vnos != '4':
            print('Napačen vnos!')
        else:
            break
    if vnos == '4':
        break

    elif vnos == '1': #iskanje po imenu
        while True:
            ime = input('Vnesi ime planeta ali zvezde: ')
            if ime not in planeti and ime not in zvezde:
                print('Planeta ali zvezde s takim imenom ni v podatkih.')
            elif ime in planeti:
                print('\n' + str(planeti[ime]) + '\n')
            elif ime in zvezde:
                print('\n' + str(zvezde[ime]) + '\n')
            while True:
                koncaj = input('Bi rad poiskal še kaj drugega? (ja/ne): ')
                if koncaj != 'ne' and koncaj != 'ja':
                    print('Vnesi ja ali ne.')
                else:
                    break
            if koncaj == 'ne':
                break
    
    elif vnos == '2': #risanje grafov
        while True:
            print('Možnosti izbire za x-os in y-os:')
            izbira = ['masa planeta', 'radij planeta', 'perioda planeta', 'velika polos planeta', \
                'ekscentricnost planeta', 'inklinacija planeta', 'kotna razdalja planeta', 'leto odkritja planeta', \
                    'izracunana temperatura planeta', 'izmerjena temperatura planeta', 'albedo planeta', 'gravitacija planeta', \
                        'rektascenzija zvezde', 'deklinacija zvezde', 'magnituda zvezde', 'oddaljenost zvezde', 'razmerje kovin zvezde', \
                            'masa zvezde', 'radij zvezde', 'starost zvezde', 'temperatura zvezde']
            print(izbira)
            while True:
                x_os = input('\nVnesi x-os (s točnimi besedami kot v tabeli izbir): ')
                if x_os not in izbira:
                    print('{} ni v tabeli izbir.'.format(x_os))
                else:
                    break
            while True:
                log_x = input('Hočeš logaritemsko skalo na x-osi? (ja/ne): ')
                if log_x != 'ja' and log_x != 'ne':
                    print('Vnesija ali ne!')
                else:
                    if log_x == 'ja':
                        log_x = True
                    else:
                        log_x = False
                    break
        
            while True:
                y_os = input('Vnesi y-os (s točnimi besedami kot v tabeli izbir): ')
                if y_os not in izbira:
                    print('{} ni v tabeli izbir.'.format(y_os))
                else:
                    break
            while True:
                log_y = input('Hočeš logaritemsko skalo na y-osi? (ja/ne): ')
                if log_y != 'ja' and log_y != 'ne':
                    print('Vnesija ali ne!')
                else:
                    if log_y == 'ja':
                        log_y = True
                    else:
                        log_y = False
                    break

            while True:
                shrani = input('Hočeš shraniti graf kot sliko? (ja/ne): ')
                if shrani != 'ja' and shrani != 'ne':
                    print('Vnesija ali ne!')
                else:
                    if shrani == 'ja':
                        shrani = True
                    else:
                        shrani = False
                    break
        
            narisi_graf(x_os, y_os, shrani, log_x, log_y)
            while True:
                nadaljuj = input('\nHočeš ustvariti še kak graf? (ja/ne): ')
                if nadaljuj != 'ja' and nadaljuj != 'ne':
                    print('Vnesija ali ne!')
                else:
                    break
            if nadaljuj == 'ne':
                break
    elif vnos == '3': #ustvarjanje objektov
        while True:
            print('\nKaj bi rad naredil?\n1 - ustvari planet\n2 - ustvari zvezdo\n3 - končaj')
            while True:
                vnos2 = input('Vnesi število: ')
                if vnos2 != '1' and vnos2 != '2' and vnos2 != '3':
                    print('Napačen vnos!')
                else:
                    break
            
            if vnos2 == '3':
                break
            elif vnos2 == '1':
                print('ČE BOŠ VNAŠAL NESMISELNE PODATKE, NE BOŠ DOBIL SMISELNIH REZULTATOV.')
                #Nekaj omejitev podatkov sem dodal, glede na to kaj je smiselno, kot recimo masa ne more biti manj od nič,
                #in glede na podatke, ki so podani. Lahko pa še vedno podajaš zelo nesmiselne podatke, recimo masa zvezde = 30 mas sonca
                #in radij = 1 meter.
                print('\n')
                while True:
                    m = input('Vnesi maso planeta (0 - 80 mJup ali None): ')
                    try:
                        M = float(m)
                        if M <= 0 or M > 80:
                            print('Masa mora biti večja od 0 in manj od 80.')
                        else:
                            break
                    except:
                        if m == 'None':
                            M = m
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    r = input('Vnesi radij planeta (0 - 15 rJup ali None): ')
                    try:
                        R = float(r)
                        if R <= 0 or R > 15:
                            print('Radij mora biti večji od 0 in manjši ali enak 15.')
                        else:
                            break
                    except:
                        if r == 'None':
                            R = r
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    p = input('Vnesi periodo planeta (0 - 1000000 dni ali None): ')
                    try:
                        P = float(p)
                        if P <= 0 or P > 1000000:
                            print('Perioda mora biti večja od 0 in manjša od 1000000.')
                        else:
                            break
                    except:
                        if p == 'None':
                            P = p
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    vp = input('Vnesi veliko polos planeta (0 - 10000 AU ali None): ')
                    try:
                        VP = float(vp)
                        if VP <= 0 or VP > 10000:
                            print('Velika polos mora biti večja od 0 in manjša od 10000.')
                        else:
                            break
                    except:
                        if vp == 'None':
                            VP = vp
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    ek = input('Vnesi ekscentričnost planeta (0 - 1) ali None: ')
                    try:
                        EK = float(ek)
                        if EK < 0 or EK > 1:
                            print('Ekscentričnost mora biti večja ali enaka 0 in manjša ali enaka 1.')
                        else:
                            break
                    except:
                        if ek == 'None':
                            EK = ek
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    t = input('Vnesi temperaturo planeta (0 - 4000 K ali None): ')
                    try:
                        T = float(t)
                        if T <= 0 or T > 4000:
                            print('Temperatura mora biti večja od 0 in manjša ali enaka 4000.')
                        else:
                            break
                    except:
                        if t == 'None':
                            T = t
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    a = input('Vnesi albedo planeta (0 - 1) ali None: ')
                    try:
                        A = float(a)
                        if A < 0 or A > 1:
                            print('Albedo mora biti večji ali enak 0 in manjši ali enak 1.')
                        else:
                            break
                    except:
                        if a == 'None':
                            A = a
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    st_p = input('Vnesi število ostalih planetov v sistemu (0 - 10): ')
                    try:
                        ST_P = int(st_p)
                        if ST_P < 0 or ST_P > 10:
                            print('Število planetov mora biti večje ali enako 0 in manjše ali enako 10.')
                        else:
                            break
                    except:
                        print('Število planetov mora biti celo število.')
                #ustvarim planet s temi podatki
                planet = Planet('None', M, 'None', R, P, VP, EK, 'None', 'None', 'None', T, T, A, 'None', 'None', 'None', 'None', 'None')
                for i in range(ST_P):
                    planet.dodaj_planet('')
                #poiščem najbloj podobnega in izpišem
                podobni = poisci_podobne(planet, planeti, zvezde)
                print('\nNajbolj podoben planet: ')
                print('\n')
                print(planeti[podobni[max(podobni.keys())]])
                print('\n')

        
            elif vnos2 == '2':
                print('ČE BOŠ VNAŠAL NESMISELNE PODATKE, NE BOŠ DOBIL SMISELNIH REZULTATOV.')
                print('\n')
                while True:
                    m = input('Vnesi maso zvezde (0 - 30 mSonca) ali None: ')
                    try:
                        M = float(m)
                        if M < 0 or M > 30:
                            print('Masa mora biti večja od 0 in manjša ali enaka 30')
                        else:
                            break
                    except:
                        if m == 'None':
                            M = m
                            break

                while True:
                    r = input('Vnesi radij zvezde (0 - 90 rSonca) ali None: ')
                    try:
                        R = float(r)
                        if R <= 0 or R > 90:
                            print('Radij mora biti večji od 0 in manjši ali enak 90.')
                        else:
                            break
                    except:
                        if r == 'None':
                            R = r
                            break
                        else:
                            print('Nepravilen vnos.')

                while True:
                    t = input('Vnesi temperaturo zvezde (0 - 100000 K) ali None: ')
                    try:
                        T = float(t)
                        if T <= 0 or T > 100000:
                            print('Temperatura mora biti večja od 0 in manjši ali enaka 100000.')
                        else:
                            break
                    except:
                        if t == 'None':
                            T = t
                            break
                        else:
                            print('Nepravilen vnos.')

                while True:
                    s = input('Vnesi starost zvezde (0 - 13.8 Glet) ali None: ')
                    try:
                        S = float(s)
                        if S <= 0 or S > 13.8:
                            print('Starost mora biti večja od 0 in manjša ali enaka 13.8.')
                        else:
                            break
                    except:
                        if s == 'None':
                            S = s
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    raz = input('Vnesi razmerje kovin zvezde (-3 - 2) ali None: ')
                    try:
                        RAZ = float(raz)
                        if RAZ < -3 or RAZ > 2:
                            print('Razmerje mora biti večje ali enako -3 in manjše ali enako 2.')
                        else:
                            break
                    except:
                        if raz == 'None':
                            RAZ = raz
                            break
                        else:
                            print('Nepravilen vnos.')
                
                while True:
                    d = input('Vnesi oddaljenost zvezde (1.3 - 25000 pc) ali None: ')
                    try:
                        D = float(d)
                        if D <= 1.3 or D > 25000:
                            print('Oddaljenost mora biti več od 1.3 in manj ali enaka 25000')
                        else:
                            break
                    except:
                        if d == 'None':
                            D = d
                            break
                        else:
                            print('Nepravilen vnos.')
                            
                while True:
                    st_p = input('Vnesi število planetov v sistemu (1 - 10): ')
                    try:
                        ST_P = int(st_p)
                        if ST_P < 1 or ST_P > 10:
                            print('Število planetov mora biti večje ali enako 1 in manjše ali enako 10.')
                        else:
                            break
                    except:
                        print('Število planetov mora biti celo število.')
                
                zvezda = Zvezda('None', 'None', 'None', 'None', D, RAZ, M, R, 'None', S, T, ST_P)
                
                print('Kaj bi rad naredil?\n1 - poišči podobno zvezdo\n2 - poišči planet, ki ga lahko pričakuješ v sistemu take zvezde')
                while True:
                    vnos3 = input('Vnesi število: ')
                    if vnos3 != '1' and vnos3 != '2':
                        print('Napačen vnos.')
                    else:
                        break
                if vnos3 == '1': #iskanje podobne zvezde in izpis
                    podobni = poisci_podobne(zvezda, planeti, zvezde)
                    print('\nNajbolj podobna zvezda:\n')
                    print(zvezde[podobni[max(podobni.keys())]])
                    print('\n')
                else: #Izpise planet, ki ga lahko pričakujemo pri taki zvezdi
                    print('\nPri taki zvezdi lahko pričakuješ:\n')
                    print(poisci_planet(zvezda, planeti, zvezde))
                    print('\n')    