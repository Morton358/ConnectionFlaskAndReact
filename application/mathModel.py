# -*- coding: utf-8 -*-
import random
import itertools
import math
from pandas import *
from operator import add

class Modell:
    'Mathemetical model of problem'

    def __init__(self, arr):
        self.I = arr[0]
        self.R = arr[1]
        self.E = arr[2]

        #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        #Mathemetical model of problem
        #//////////////////////////////
        #def mathematicalModel(countI, countR, countE):
        #I = 3 #random.randint(2, 20) # 3
        #R = 3 #random.randint(2, 10) # 3
        #E = 5 #random.randint(2, 50) # 5
        self.i = [] # numery jednostek sprzedajacej surowiec
        self.r = [] # numery/indeksy jednostek produkcyjnych
        self.e = [] # numery/indeksy klientow ktorzy tworza zapotrzebowanie w produkcii jednostek produkcyjnych
        self.W = [] # ilosc surowca u kazdego z sprzedawcow
        self.G = [] # obserwowana produkcyjna moc kazdego z zakladow produkcyjnych
        self.K = [] # obserwowany popyt/zapotrzebowanie na produkcje przedsiebiorstwa kazdego klienta
        self.V = [] # wspolczynnik produkcji dla przeliczania ilosci surowca na ilosc produktu na kazdym zakladzie produkcyjnym
        self.J1_I = [] # koszt jednostkowy surowca u kazdego sprzedawcy
        self.J1_R = [] # koszt jednostkowy przetworstwa owocowo-warzywnej produkcji na kazdym zakladzie produkcyjnym
        self.J1_R__1_I_arr = [] # koszt jednostkowy przejazdu od sprzedawcow do zakladow produkcyjnych (jeden ciag kosztow)
        self.J1_R__1_I = [] # koszt jednostkowy przejazdu od sprzedawcow do zakladow produkcyjnych (podzielono od kazdej ...
        # jednostki sprzedajacej surowiec do wszystkich zalladow produkcyjnych)
        self.J1_R__1_E_arr = [] # koszt jednostkowy przejazdu od zakladow produkcyjnych do klientow (jeden ciag kosztow)
        self.J1_R__1_E = [] # koszt jednostkowy przejazdu od zakladow produkcyjnych do klientow (podzielono od kazdego zakladu
        #  produkcyjnego do wszystkich klientow)
        self.M1_R__1_I = [] # dystans od sprzedawca do zakladu produkcyjnego
        self.M1_R__1_E = [] # dystans od zakladu produkcyjnego do jednostki, sprzedajacej gotowa produkcje
        self.S = [] # koszty uruchomienia zakladow produkcyjnych
        self.Q = 500 # pojemnosc auta dla transportowania gotowej produkcji (w litrach)
        self.Q_TIR = 200 # 2400 pojemnosc auta, ktore transportuje surowiec (w kilogramach)
        # Q_TIR_all = [1/Q_TIR] * I * R  # dla zapisywania w funkcje celu
        self.Z = [] # ilosci juz zakupionych surowcow u sprzedawcow (kg)
        self.Z1_R = [] # ilosc juz przywiezionego surowca do zakladow produkcyjnych (kg)
        self.Z1_R_in_l = [] # ilosc juz pfladow produkcyjnych (l)
        self.Y = [] # ilosc juz wyprodukowanych produktow na zakladach produkcyjnych ale nie dowiezionych jeszcze do klientow
        self.A1_R__1_I_arr = [] # ogolna ilosc surowca, ktora bylo przetransportowano od sprzedawcow do zakladow produkcyjnych
        # (jeden ciag ilosci)
        self.A1_R__1_I = [] # ogolna ilosc surowca, ktora bylo przetransportowano od sprzedawcow do zakladow produkcyjnych
        self.A1_R__1_E_arr = [] # ogolna ilosc produktu, ktora bylo przetransportowano od zakladow produkcyjnych
        # do klientow (jeden ciag ilosci)
        self.A1_R__1_E = [] #  ogolna ilosc produktu, ktora bylo przetransportowano od zakladow produkcyjnych
        # do klientow (lists of lists)
        self.c1_R__1_I_arr = [] # strata przy transportowaniu surowca od sprzedawcow do zakladow produkcyjnych (jeden ciag strat)
        self.c1_R__1_I = [] # strata przy transportowaniu surowca od sprzedawcow do zakladow produkcyjnych (lists of lists)
        self.c1_R__1_E_arr = [] # strata przy transportowaniu produktow od zakladow produkcyjnych do klientow (jeden ciag strat)
        self.c1_R__1_E = [] # strata przy transportowaniu produktow od zakladow produkcyjnych do klientow (lists of lists)
        self.C = [] # strata przy produkcji, na zakladach produkcyjnych
        self.X1_R__1_I_arr = [] # ogolna ilosc surowca, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy
        # od sprzedawcow do zakladow produkcyjnych (jeden ciag ilosci)
        self.X1_R__1_I = [] # ogolna ilosc surowca, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy
        # od sprzedawcow do zakladow produkcyjnych (lists of lists)
        self.X1_R__1_E_arr = [] # ogolna ilosc produktu, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy
        # od zakladow produkcyjnych do klientow (jeden ciag ilosci)
        self.X1_R__1_E = [] # ogolna ilosc produktu, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy
        # od zakladow produkcyjnych do klientow (lists of lists)
        self.W1_I = [] # ogolna ilosc surowca, ktorego juz kupilismy oraz bedziemy kupowac u sprzedawcow
        self.D1_R = [] # ogolna ilosc produktu, co wyprodukowalismy oraz bedziemy produkowac na zakladach produkcyjnych
        self.W_all = 0 # ogolna dostepna ilosc surowca do przetwarzania (u sprzedawcow i na zakladach produkcyjnych)
        self.K_all = 0 # ilosc produktu ktora jeszcze trzeba wyprodukowac, zeby spelnic ogolne zapotrzebowanie klientow
        self.G_all = 0 # suma produkcyjnej mocy wszystkich zakladow produkcyjnych
        self.P1_I = [] # koszty zakupionych surowcow od 0 do i-ego sprzedawcy
        self.P1_R = [] # koszty produkowania produktow od 0 do r-ego zakladow produkcyjnych
        self.P1_R__1_I_arr = [] # koszt przewozu surowca od i-ego sprzedawcy do r-ego zakladu produkcyjnego (jeden ciag kosztow)
        self.P1_R__1_I = [] # koszt przewozu surowca od i-ego sprzedawcy do r-ego zakladu produkcyjnego (list of lists)
        self.P1_R__1_E_arr = [] # koszt przewozu produktow z r-ego zakladu produkcyjnego do e-ego klienta (jeden ciag kosztow)
        self.P1_R__1_E = [] # koszt przewozu produktow z r-ego zakladu produkcyjnego do e-ego klienta (list of lists)
        self.P_all = [] # koszt calkowity


        for k in range(self.I):
            self.i.append(k)
            Wi = random.randint(1000, 10000) # Ilosc surowca w kg.
            self.W.append(Wi)
            Ji = round(random.uniform(0.5, 3.0), 2) # koszt surowca od 0.5 zl do 3 zl za kilogram
            self.J1_I.append(Ji)
            for k in range(self.R):
                Jri = round(random.uniform(2, 4.5), 2) # cena za 1 km przewozu surowca autem ciezarowym
                self.J1_R__1_I_arr.append(Jri)
                Mri = round(random.uniform(8.0, 35.5), 1) # odleglosc od i-ego sprzdawcy do r-ego przedsiebiorstwa
                self.M1_R__1_I.append(Mri)
                Ari = random.randint(0, 50000) # ogolna ilosc surowca, ktora bylo przetransportowano od i-ego sprzedawcy
                # do r-ego zakladu produkcyjnego
                self.A1_R__1_I_arr.append(Ari)
                cri = random.randint(0, 50000) # strata przy transportowaniu surowca od i-ego sprzedawcy do r-ego
                # zakladu produkcyjnego
                self.c1_R__1_I_arr.append(cri)
                Xri = random.randint(0, 100000) # ogolna ilosc surowca, ktora trzeba przetransportowac oraz ktora
                # juz przetransportowalismy od i-ego sprzedawcy do r-ego zakladu produkcyjnego
                self.X1_R__1_I_arr.append(Xri)

            Zi = random.randint(1000, 10000) # Ilosc juz zakupionego surowca u I-ego sprzedawcy w kg.
            self.Z.append(Zi)

        J1_R__1_I = [self.J1_R__1_I_arr[y:y + self.R] for y in range(0, len(self.J1_R__1_I_arr), self.R)]
        self.A1_R__1_I = [self.A1_R__1_I_arr[t:t + self.R] for t in range(0, len(self.A1_R__1_I_arr), self.R)]
        c1_R__1_I = [self.c1_R__1_I_arr[p:p + self.R] for p in range(0, len(self.c1_R__1_I_arr), self.R)]
        X1_R__1_I = [self.X1_R__1_I_arr[c:c + self.R] for c in range(0, len(self.X1_R__1_I_arr), self.R)]


        for k in range(self.R):
            self.r.append(k)
            Gr = random.randint(50000, 100000) # Produkcyjna moc zakladu produkcyjnego w l. na miesiac
            Vr = round(random.uniform(1, 2.5), 2) # wspolczynnik produkcji surowiec na produkt (od 1 do 2)
            self.G.append(Gr)
            self.V.append(Vr)
            Jr = round(random.uniform(1, 1.9), 2) # cena od 1 do 1.9 zl za wyprodukowania 1 l. soku
            self.J1_R.append(Jr)
            for k in range(self.E):
                Jre = round(random.uniform(0.4, 2.5), 2) # cena za 1 km przewozu produkcji
                self.J1_R__1_E_arr.append(Jre)
                Mre = round(random.uniform(1.5, 13.5), 1)  # odleglosc od r-ego przedsiebiorstwa do e-go sprzedawcy
                self.M1_R__1_E.append(Mre)
                Are = random.randint(0, 5000) # ogolna ilosc produktu, ktora bylo przetransportowano
                # od r-ego zakladu produkcyjnego do e-ego klienta
                self.A1_R__1_E_arr.append(Are)
                cre = random.randint(0, 5000) # strata przy transportowaniu produktu
                # od r-ego zakladu produkcyjnego do e-ego klienta
                self.c1_R__1_E_arr.append(cre)
                Xre = Xri = random.randint(0, 50000) # ogolna ilosc produktu, ktora trzeba przetransportowac oraz
                # ktora juz przetransportowalismy od r-ego zakladu produkcyjnego do e-ego klienta
                self.X1_R__1_E_arr.append(Xre)

            Sr = random.randint(3500, 6500) # koszt uruchomienia zakladow produkcyjnych
            self.S.append(Sr)
            Zr = random.randint(1000, 8000) # Ilosc juz przywiezionego surowca do R-ego zakladu produkcyjnego w kg.
            self.Z1_R.append(Zr)
            Yr = random.randint(500, 5000)  # ilosc wyprodukowanego produktu na r-ym zakladzie produkcyjnym (w l.)
            self.Y.append(Yr)
            Cr = random.randint(500, 5000) # strata przy produkcji, na r-ym zakladzie produkcyjnym
            self.C.append(Cr)

        J1_R__1_E = [self.J1_R__1_E_arr[y:y + self.E] for y in range(0, len(self.J1_R__1_E_arr), self.E)]
        self.A1_R__1_E = [self.A1_R__1_E_arr[t:t + self.E] for t in range(0, len(self.A1_R__1_E_arr), self.E)]
        c1_R__1_E = [self.c1_R__1_E_arr[p:p + self.E] for p in range(0, len(self.c1_R__1_E_arr), self.E)]
        X1_R__1_E = [self.X1_R__1_E_arr[c:c + self.E] for c in range(0, len(self.X1_R__1_E_arr), self.E)]

        for k in range(self.E):
            self.e.append(k)
            Ke = random.randint(100, 5000) #Popyt klienta na produkcje przedsiebiorstwa w l.
            self.K.append(Ke)

        W1_I = [sum(b) for b in X1_R__1_I] # ogolna ilosc surowca, ktorego juz kupilismy oraz bedziemy kupowac u sprzedawcow

        D1_R = [sum(c) for c in X1_R__1_E] # ogolna ilosc produktu, co wyprodukowalismy oraz bedziemy produkowac
        # na zakladach produkcyjnych

        W_all = sum(itertools.chain(self.W, self.Z, self.Z1_R)) # ogolna dostepna ilosc surowca
        # do przetwarzania (u sprzedawcow i na zakladach produkcyjnych);

        K_all = sum(self.K) - sum(self.Y) # ilosc produktu ktora jeszcze trzeba wyprodukowac,
        # zeby spelnic ogolne zapotrzebowanie klientow

        ki = 0
        for k in self.Z1_R:
            self.Z1_R_in_l.append(k/self.V[ki])
            ki += 1

        G_all = sum(self.G) - sum(self.Z1_R_in_l) # suma produkcyjnej mocy wszystkich zakladow produkcyjnych

        ki = 0
        for k in W1_I:
            self.P1_I.append(k * self.J1_I[ki])
            ki += 1

        ki = 0
        for k in D1_R:
            self.P1_R.append((k * self.J1_R[ki]) + self.S[ki])
            ki += 1

        list_index = 0
        for list in X1_R__1_I:
            number_index = 0
            for number in list:
                self.P1_R__1_I_arr.append((math.ceil(number / self.Q_TIR)) * J1_R__1_I[list_index][number_index])
                number_index += 1
            list_index += 1

        P1_R__1_I = [self.P1_R__1_I_arr[y:y + self.R] for y in range(0, len(self.P1_R__1_I_arr), self.R)]

        list_index = 0
        for list in X1_R__1_E:
            number_index = 0
            for number in list:
                self.P1_R__1_E_arr.append((math.ceil(number / self.Q) * J1_R__1_E[list_index][number_index]))
                number_index += 1
            list_index += 1

        P1_R__1_E = [self.P1_R__1_E_arr[z:z + self.E] for z in range(0, len(self.P1_R__1_E_arr), self.E)]


        P_all = sum(self.P1_I) + sum(self.P1_R) + sum(self.P1_R__1_I_arr) + sum(self.P1_R__1_E_arr)

        print('numery jednostek sprzedajacej surowiec: ', "\n",
              self.i, "\n",
              'numery/indeksy jednostek produkcyjnych: ', "\n",
              self.r, "\n",
              'numery/indeksy klientow ktorzy tworza zapotrzebowanie w produkcii jednostek produkcyjnych: ', "\n",
              self.e, "\n",
              'ilosc surowca u kazdego z sprzedawcow:', "\n",
              self.W, "\n",
              'W: ', self.W, "\n",
              'obserwowana produkcyjna moc kazdego z zakladow produkcyjnych: ', "\n",
              self.G, "\n",
              'obserwowany popyt/zapotrzebowanie na produkcje przedsiebiorstwa kazdego klienta: ', "\n",
              self.K, "\n",
              'wspolczynnik produkcji dla przeliczania ilosci surowca na ilosc produktu '
              'na kazdym zakladzie produkcyjnym:', "\n",
              self.V, "\n",
              'koszt jednostkowy surowca u kazdego sprzedawcy: ', "\n",
              self.J1_I, "\n",
              'koszt jednostkowy przetworstwa owocowo-warzywnej produkcji na kazdym zakladzie produkcyjnym: ', "\n",
              self.J1_R, "\n",
              'koszt jednostkowy przejazdu od sprzedawcow do zakladow produkcyjnych: ', "\n",
              DataFrame(J1_R__1_I), "\n",
              'J1_R__1_I: ', J1_R__1_I, "\n",
              'J1_R__1_I_arr: ', self.J1_R__1_I_arr, "\n",
              'koszt jednostkowy przejazdu od zakladow produkcyjnych do klientow: ', "\n",
              DataFrame(J1_R__1_E), "\n",
              'J1_R__1_E: ', J1_R__1_E, "\n",
              'J1_R__1_E_arr: ', self.J1_R__1_E_arr, "\n",
              'odleglosc od i-ego sprzdawcy do r-ego przedsiebiorstwa: ', "\n",
              self.M1_R__1_I, "\n",
              'odleglosc od r-ego przedsiebiorstwa do e-go sprzedawcy: ', "\n",
              self.M1_R__1_E, "\n",
              'koszty uruchomienia zakladow produkcyjnych: ', "\n",
              self.S, "\n",
              'pojemnosc auta dla transportowania gotowej produkcji (w litrach): ', "\n",
              self.Q, "\n",
              'pojemnosc auta, ktore transportuje surowiec (w kilogramach): ', "\n",
              self.Q_TIR, "\n",
              'ilosci juz zakupionych surowcow u sprzedawcow (kg): ', "\n",
              self.Z, "\n",
              'ilosc juz przywiezionego surowca do zakladow produkcyjnych (kg): ', "\n",
              self.Z1_R, "\n",
              'Z1_R:', self.Z1_R, "\n",
              'A1_R__1_E_arr:', self.A1_R__1_E_arr, "\n",
              'A1_R__1_I_arr', self.A1_R__1_I_arr, "\n",
              'ilosc juz wyprodukowanych produktow na zakladach produkcyjnych '
              'ale nie dowiezionych jeszcze do klientow (l): ', "\n",
              self.Y, "\n",
              'ogolna ilosc surowca, ktora bylo przetransportowano od sprzedawcow do zakladow produkcyjnych: ', "\n",
              DataFrame(self.A1_R__1_I), "\n",
              self.A1_R__1_I, "\n",
              'ogolna ilosc produktu, ktora bylo przetransportowano od zakladow produkcyjnych do klientow: ', "\n",
              DataFrame(self.A1_R__1_E), "\n",
              'A1_R__1_E: ', self.A1_R__1_E, "\n",
              'strata przy transportowaniu surowca od sprzedawcow do zakladow produkcyjnych: ', "\n",
              DataFrame(c1_R__1_I), "\n",
              'strata przy transportowaniu produktow od zakladow produkcyjnych do klientow: ', "\n",
              DataFrame(c1_R__1_E), "\n",
              'strata przy produkcji, na zakladach produkcyjnych: ', "\n",
              self.C, "\n",
              'ogolna ilosc surowca, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy '
              'od sprzedawcow do zakladow produkcyjnych: ', "\n",
              DataFrame(X1_R__1_I), "\n",
              'ogolna ilosc produktu, ktora trzeba przetransportowac oraz ktora juz przetransportowalismy '
              'od zakladow produkcyjnych do klientow: ', "\n",
              DataFrame(X1_R__1_E), "\n",
              'ogolna ilosc surowca, ktorego juz kupilismy oraz bedziemy kupowac u sprzedawcow: ', "\n",
              W1_I, "\n",
              'ogolna ilosc produktu, co wyprodukowalismy oraz bedziemy produkowac na zakladach produkcyjnych: ', "\n",
              D1_R, "\n",
              'ogolna dostepna ilosc surowca do przetwarzania: ', "\n",
              W_all, "\n",
              'ilosc produktu ktora jeszcze trzeba wyprodukowac, zeby spelnic ogolne zapotrzebowanie klientow: ', "\n",
              K_all, "\n",
              'suma produkcyjnej mocy wszystkich zakladow produkcyjnych: ', "\n",
              G_all, "\n",
              'koszty zakupionych surowcow od 0 do i-ego sprzedawcy:', "\n",
              self.P1_I, "\n",
              'koszty produkowania produktow od 0 do r-ego zakladow produkcyjnych:', "\n",
              self.P1_R, "\n",
              'koszty przewozu surowca od i-ych sprzedawcow do r-ych zakladow produkcyjnych:', "\n",
              DataFrame(P1_R__1_I), "\n",
              'koszty przewozu produktow z r-ych zakladow produkcyjnych do e-ych klientow:', "\n",
              DataFrame(P1_R__1_E), "\n",
              'koszt calkowity. Parametr funkcji celu:', "\n",
              P_all, "\n")


        # \\\\\\\\\\\\
        # some tests
        # ////////////

        if sum(self.P1_I) == sum([self.J1_I[elem] * W1_I[elem] for elem in range(len(W1_I))]):
            print('the mathematical model is correct')
        else:
            print('something goes wrong with mathematical Model!')

        if len(self.A1_R__1_I_arr) + len(self.A1_R__1_E_arr) == self.I * self.R + self.R * self.E:
            print('the mathematical model is correct')
        else:
            print('something goes wrong with mathematical Model')




