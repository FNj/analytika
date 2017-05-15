#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dane.py

Daně v České republice
"""

from collections import namedtuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

DaňovéSchéma = namedtuple('DaňovéSchéma', 'hranice sazby')


def daň(schéma: DaňovéSchéma, mzdové_náklady: float) -> float:
    """Vrací daň při definovaném daňovém schématu a mzdových nákladech."""
    délka = len(schéma.hranice)
    tax = 0

    hranice = schéma.hranice + [np.inf]
    sazby = schéma.sazby

    for i in range(0, délka - 1):
        if hranice[i] <= mzdové_náklady <= hranice[i + 1]:
            tax += (mzdové_náklady - hranice[i]) * sazby[i]
        elif hranice[i + 1] < mzdové_náklady:
            tax += (hranice[i + 1] - hranice[i]) * sazby[i]
        elif mzdové_náklady < hranice[i]:
            break

    return tax


def mezní_sazba(schéma: DaňovéSchéma, mzdové_náklady: float) -> float:
    """Vrací mezní sazbu daně při definovaném daňovém schématu a mzdových nákladech."""
    délka = len(schéma.hranice)

    hranice = schéma.hranice + [np.inf]
    sazby = schéma.sazby

    for i in range(0, délka - 1):
        if hranice[i] <= mzdové_náklady <= hranice[i + 1]:
            return sazby[i]


# Platný stav

průměrná_hrubá_mzda = 28232.0  # Průměrná hrubá mzda
sleva = 2070  # Sleva na dani na poplatníka
k = 1.34  # Poměr superhrubé mzdy ku hrubé mzdě

H0 = 0.0  # Hraniční částka
s0 = 0.45 / k  # Sazba odvodů ? Proč se to zpátky dělí k? Nemá se to počítat ze superhrubé mzdy?

H1 = sleva / 0.15
s1 = (0.15 + 0.45 / k)  # ditto

H2 = 4 * průměrná_hrubá_mzda * k
k2 = 1.09  # Poměr části superhrubé mzdy nad hraniční částku ku hrubé mzdě nad hraniční částku ?
s2 = (0.15 + 0.135 / k2 + 0.07 / k2)  # ditto

schéma_nyní = DaňovéSchéma(hranice=[H0, H1, H2], sazby=[s0, s1, s2])

# ČSSD # význam analogicky tomu výše

H0 = 0
s0 = 0.45 / k

H1 = 17250
s1 = 0.12 + 0.45 / k

H2 = 40200
s2 = 0.15 + 0.45 / k

H3 = 53600
s3 = 0.25 + 0.45 / k

H4 = 67000
s4 = 0.32 + 0.45 / k

H5 = 4 * průměrná_hrubá_mzda * k
k2 = 1.09
s5 = (0.32 + 0.135 / k2 + 0.07 / k2)

schéma_ČSSD = DaňovéSchéma(hranice=[H0, H1, H2, H3, H4, H5], sazby=[s0, s1, s2, s3, s4, s5])

# ODS # význam analogicky tomu výše
# http://www.ods.cz/volby2017/kalkulacka


k = 1.32

H0 = 0.0
s0 = 0.43 / k

H1 = sleva / 0.15
s1 = (0.15 / k + 0.43 / k)  # mezní sazba 0.439

H2 = 4 * průměrná_hrubá_mzda * k
s2 = 0.15  # mezní sazba 0.15

schéma_ODS = DaňovéSchéma(hranice=[H0, H1, H2], sazby=[s0, s1, s2])

# Piráti # význam analogicky tomu výše

H0 = 0.0
s0 = 0.0

H1 = sleva / 0.47
s1 = 0.47

schéma_Piráti = DaňovéSchéma(hranice=[H0, H1], sazby=[s0, s1])

print('  mzda   nyní   ods    čssd   piráti')

for hrubá_mzda in range(14000, 80000, 2000):
    print('{0:6.0f} {1:6.0f} {2:6.0f} {3:6.0f} {4:6.0f}'.format(hrubá_mzda, daň(schéma_nyní, 1.34 * hrubá_mzda),
                                                                daň(schéma_ODS, 1.32 * hrubá_mzda), daň(schéma_ČSSD, 1.34 * hrubá_mzda),
                                                                daň(schéma_Piráti, 1.34 * hrubá_mzda)))

matplotlib.rc('font', family='Liberation Sans')


def vykresli_daně(hspace, label):
    _, axarr = plt.subplots(2, sharex=True)

    oldspace = [daň(schéma_nyní, h * 1.34) for h in hspace]
    odsspace = [daň(schéma_ODS, h * 1.32) for h in hspace]
    cssdspace = [daň(schéma_ČSSD, h * 1.34) for h in hspace]
    pirspace = [daň(schéma_Piráti, h * 1.34) for h in hspace]

    axarr[0].set_title('Zdanění práce – ' + label)
    axarr[0].plot(hspace, oldspace, color='darkgray')
    axarr[0].plot(hspace, odsspace, color='blue')
    axarr[0].plot(hspace, cssdspace, color='orange')
    axarr[0].plot(hspace, pirspace, color='black')
    axarr[0].set_ylabel('zdanění práce [Kč]')

    oldspace2 = [mezní_sazba(schéma_nyní, h * 1.34) for h in hspace]
    odsspace2 = [mezní_sazba(schéma_ODS, h * 1.32) for h in hspace]
    cssdspace2 = [mezní_sazba(schéma_ČSSD, h * 1.34) for h in hspace]
    pirspace2 = [mezní_sazba(schéma_Piráti, h * 1.34) for h in hspace]

    axarr[1].set_title('Mezní sazba daně  – ' + label)
    axarr[1].plot(hspace, oldspace2, color='darkgray')
    axarr[1].plot(hspace, odsspace2, color='blue')
    axarr[1].plot(hspace, cssdspace2, color='orange')
    axarr[1].plot(hspace, pirspace2, color='black')
    axarr[1].set_ylabel('mezní sazba daně [%]')

    plt.xlabel('dnešní hrubá mzda [Kč]')

    plt.savefig(label + '.png', dpi=600)
    # plt.show() # show the plot


hspace = np.linspace(12000, 20000, 1000)
vykresli_daně(hspace, 'nízkopříjmové skupiny')

hspace = np.linspace(20000, 50000, 1000)
vykresli_daně(hspace, 'střední třída')

hspace = np.linspace(12000, 300000, 1000)
vykresli_daně(hspace, 'vysokopříjmové skupiny')


def barva_sloupce(hodnota):
    if hodnota[1] >= 0:
        return 'g'
    else:
        return 'r'


def vykresli_výdělek(hspace, dopad, label):
    colors = [barva_sloupce(pár) for pár in zip(hspace, dopad)]
    plt.bar(hspace, dopad, width=2500, color=colors)

    # plt.set_title('Mezní sazba daně  – '+label)
    plt.xlabel('dnešní hrubá mzda [Kč]')
    plt.ylabel('kolik ušetří na daních [Kč]')
    plt.xlim([min(hspace), max(hspace) + 3000])
    plt.savefig('dopad ' + label + '.png', dpi=600)


tabelace_hrubé_mzdy = [0, 10000, 12000, 14000, 16000, 18000,
                       20000, 22000, 24000, 26000, 28000, 30000, 32000, 36000,
                       40000, 50000, 60000, 80000, 600000]
tabelace_percentilů = [3.7, 5.6, 6.1, 6.8, 7.5, 7.9, 7.9, 8.1,
                       7.7, 6.5, 5.5, 4.4, 6.3, 4.1, 5.6, 2.3, 2.0, 1.9]
# Nejsou to percentily, ale spíš relativní četnosti


def percentil_hrubé_mzdy(hrubá_mzda): # Tato funkce se nepoužívá.
    """Vrací percentil v závislosti na hrubá_mzda."""

    tabelace_hrubé_mzdy_upravená = [hodnota * průměrná_hrubá_mzda / 27002.0 for hodnota in tabelace_hrubé_mzdy]

    for i in range(0, len(tabelace_hrubé_mzdy_upravená) - 1):
        if tabelace_hrubé_mzdy_upravená[i] <= hrubá_mzda < tabelace_hrubé_mzdy_upravená[i + 1]:
            return tabelace_percentilů[i] / (tabelace_hrubé_mzdy_upravená[i + 1] - tabelace_hrubé_mzdy_upravená[i])


def hrubá_mzda_na_mzdové_náklady(hrubá_mzda):  # TODO: WTF? Neměla by funkce vracet spíš mzdové_náklady než hrubá_mzda?
    if hrubá_mzda <= 4 * průměrná_hrubá_mzda:
        mzdové_náklady = hrubá_mzda * 1.34
    else:
        mzdové_náklady = 1.34 * 4 * průměrná_hrubá_mzda + 0.135 * hrubá_mzda
    return hrubá_mzda


def percentil_mzdových_nákladů(mzdové_náklady):
    """Vrací percentil v závislosti na mzdové_náklady."""

    tabelace_mzdových_nákladů = [hodnota * průměrná_hrubá_mzda / 27002.0 for hodnota in
                                 tabelace_hrubé_mzdy]  # úprava pro roky 2014 až 2017
    tabelace_mzdových_nákladů = [hrubá_mzda_na_mzdové_náklady(hodnota) for hodnota in tabelace_mzdových_nákladů]

    for i in range(0, len(tabelace_mzdových_nákladů) - 1):
        if tabelace_mzdových_nákladů[i] <= mzdové_náklady < tabelace_mzdových_nákladů[i + 1]:
            # TODO: Zkontrolovat: Zde bylo původně hrubá_mzda, ne mzdové_náklady.
            return 0.01 * tabelace_percentilů[i] / (tabelace_mzdových_nákladů[i + 1] - tabelace_mzdových_nákladů[i])


def výnos(schéma):
    quad_result = integrate.quad(lambda m: daň(schéma, m) * percentil_mzdových_nákladů(m), 0, 600000,
                                 points=list(set().union(tabelace_hrubé_mzdy, schéma.hranice)))
    return 2900000 * quad_result[0]


hspace = np.linspace(12000, 130000, 30)
dopad = np.fromiter((daň(schéma_nyní, h * 1.34) - daň(schéma_Piráti, h * 1.34) for h in hspace), np.float64)

vykresli_výdělek(hspace, dopad, 'Piráti')

# Markův export
# for couple in zip(hspace,dopad):
#    print(str(couple[0])+';'+str(couple[1]))

# hrubá_mzda=126470
# print(dan(schéma_nyní,hrubá_mzda*1.34)-dan(schéma_Piráti,hrubá_mzda*1.34))
# print(percentil(20000))

print('old')
print(výnos(schéma_nyní))

print('pir')
print(výnos(schéma_Piráti))

print('ods')
print(výnos(schéma_ODS))

print('čssd')
print(výnos(schéma_ČSSD))
