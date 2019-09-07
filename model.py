import random

class Karta():
    def __init__(self, barva, vrednost):
        self.barva = barva
        self.vrednost = vrednost

    def __repr__(self):
        return "Karta({0},{1})".format(self.barva, self.vrednost)

    def __str__(self):
        return "{0} {1}".format(self.barva, self.vrednost)

class Kupcek():
    def __init__(self):
        self.karte = []
        self.generiraj_karte()
        self.premesaj()

    def __str__(self):
        return str(self.karte)

    def generiraj_karte(self):
        self.karte = [Karta(i, j) for i in ["srce","pik","kriz","karo"] for j in range(2,15)]

    def premesaj(self):
        random.shuffle(self.karte)

    def vleci(self):
        return self.karte.pop()

    def resetiraj_karte(self):
        self.generiraj_karte()
        self.premesaj()

class Igra:
    def __init__(self, stevilo_igralcev, zacetni_denar):
        self.zacetno_stevilo_igralcev = stevilo_igralcev
        self.igralci = [True] * stevilo_igralcev #igralci, ki še niso izgubili
        self.racunalnik = [False] * stevilo_igralcev #indeksi kjer igra racunalnik
        self.denar_igralcev = [zacetni_denar] * stevilo_igralcev
        self.vlozen_denar = [0] * stevilo_igralcev
        self.trenutna_stava = 0 #trenutna najvišja stava na mizi
        self.aktivni_igralci = [True] * stevilo_igralcev #igralci, ki niso predali kart
        self.karte_igralcev = [0] * stevilo_igralcev
        self.karte_na_mizi = []
        self.zacetni_denar = zacetni_denar
        self.big_blind = zacetni_denar / 100
        self.small_blind = zacetni_denar / 200
        self.delilec = 0 #indeks igralca, ki 'deli'
        self.igralec_na_potezi = 0
        self.zadnji_ki_je_povecal_vlozek = 0
        self.runda = 1
        self.kupcek = Kupcek()
        self.stevilo_iger = 0
        self.vmesni_del = True
        self.konec_runde = True
        self.zmagovalec_runde = None
        self.koncni_zmagovalec = None

    def razdelitev_kart(self):
        self.kupcek.resetiraj_karte()
        print(self.kupcek)
        self.karte_na_mizi = []
        for i in range(self.zacetno_stevilo_igralcev):
            if self.igralci[i]:
                self.karte_igralcev[i] = (self.kupcek.vleci(), self.kupcek.vleci())

    def karta_na_mizo(self):
        self.karte_na_mizi.append(self.kupcek.vleci())

    def nova_runda(self, konec=False):
        if konec:
            self.runda = 5
        if self.runda == 1:
            self.konec_runde = False
            for i in range(self.zacetno_stevilo_igralcev):
                if self.igralci[i]:
                    self.aktivni_igralci[i] = True
                else:
                    self.aktivni_igralci[i] = False
            print("Tuki to", self.igralci, self.aktivni_igralci)
            self.razdelitev_kart()
            self.delilec = self.naslednji_indeks(self.delilec)
            self.zacetni_vlozek()
            self.igralec_na_potezi = self.naslednji_indeks(self.naslednji_indeks(self.naslednji_indeks(self.delilec))) # tretji od delilca
            self.zadnji_ki_je_povecal_vlozek = self.naslednji_indeks(self.naslednji_indeks(self.delilec))
            self.runda += 1
        elif self.runda == 2:
            for _ in range(3):
                self.karta_na_mizo()
            self.runda += 1
            self.igralec_na_potezi = self.naslednji_indeks(self.delilec)
            self.zadnji_ki_je_povecal_vlozek = self.igralec_na_potezi
        elif self.runda == 3:
            self.karta_na_mizo()
            self.runda += 1
            self.igralec_na_potezi = self.naslednji_indeks(self.delilec)
            self.zadnji_ki_je_povecal_vlozek = self.igralec_na_potezi
        elif self.runda == 4:
            self.karta_na_mizo()
            self.igralec_na_potezi = self.naslednji_indeks(self.delilec)
            self.zadnji_ki_je_povecal_vlozek = self.igralec_na_potezi
            self.runda += 1
        elif self.runda == 5:
            self.runda = 1
            self.konec()

    def predaj_se(self): #fold
        self.aktivni_igralci[self.igralec_na_potezi] = False
        self.igralec_na_potezi = self.naslednji_indeks(self.igralec_na_potezi)
        if self.aktivni_igralci.count(False) == self.zacetno_stevilo_igralcev - 1:
            self.nova_runda(True)
            return
        if self.zadnji_ki_je_povecal_vlozek == self.igralec_na_potezi:
            self.nova_runda()

    def dvigni(self, kolicina=0): #call/raise bid
        kolicina = max(0, kolicina)
        dopolnitev = self.trenutna_stava + kolicina - self.vlozen_denar[self.igralec_na_potezi]
        print("Dopolnitev:", dopolnitev)
        if self.denar_igralcev[self.igralec_na_potezi] >= dopolnitev:
            self.vlozen_denar[self.igralec_na_potezi] += dopolnitev
            self.denar_igralcev[self.igralec_na_potezi] -= dopolnitev
            self.trenutna_stava = self.vlozen_denar[self.igralec_na_potezi]
            if kolicina > 0:
                self.zadnji_ki_je_povecal_vlozek = self.igralec_na_potezi
                self.igralec_na_potezi = self.naslednji_indeks(self.igralec_na_potezi)
            else:
                self.igralec_na_potezi = self.naslednji_indeks(self.igralec_na_potezi)
                if self.zadnji_ki_je_povecal_vlozek == self.igralec_na_potezi:
                    self.nova_runda()
            return True
        else: #Če nima dovolj denarja se vseeno vloži vse kar ima
            self.vlozen_denar[self.igralec_na_potezi] += self.denar_igralcev[self.igralec_na_potezi]
            self.denar_igralcev[self.igralec_na_potezi] = 0
            if self.trenutna_stava < self.vlozen_denar[self.igralec_na_potezi]:
                self.trenutna_stava = self.vlozen_denar[self.igralec_na_potezi]
                self.zadnji_ki_je_povecal_vlozek = self.igralec_na_potezi
                self.igralec_na_potezi = self.naslednji_indeks(self.igralec_na_potezi)
            else:
                self.igralec_na_potezi = self.naslednji_indeks(self.igralec_na_potezi)
                if self.zadnji_ki_je_povecal_vlozek == self.igralec_na_potezi:
                    self.nova_runda()
            return False

    def naslednji_indeks(self, n): #Vrne ciklično naslednji indeks in upošteva igralce, ki so izgubili
        for _ in range(self.zacetno_stevilo_igralcev):
            n = (n + 1) % self.zacetno_stevilo_igralcev
            if self.aktivni_igralci[n]:
                return n

    def zacetni_vlozek(self):
        sb = self.naslednji_indeks(self.delilec)
        bb = self.naslednji_indeks(sb)
        self.trenutna_stava = self.big_blind

        if self.denar_igralcev[sb] >= self.small_blind:
            self.vlozen_denar[sb] += self.small_blind
            self.denar_igralcev[sb] -= self.small_blind
        else:
            self.vlozen_denar[sb] += self.denar_igralcev[sb]
            self.denar_igralcev[sb] = 0
        if self.denar_igralcev[bb] >= self.big_blind:
            self.vlozen_denar[bb] += self.big_blind
            self.denar_igralcev[bb] -= self.big_blind
        else:
            self.vlozen_denar[bb] += self.denar_igralcev[bb]
            self.denar_igralcev[bb] = 0

    def konec(self): #Konec 1 runde igre
        zmag = self.zmagovalec()
        self.zmagovalec_runde = zmag
        self.konec_runde = True
        for i in range(self.zacetno_stevilo_igralcev):
            self.denar_igralcev[zmag] += self.vlozen_denar[i]
        if self.denar_igralcev.count(0) >= (self.zacetno_stevilo_igralcev - 1):
            self.konec_igre(zmag)
        else:
            for i in range(self.zacetno_stevilo_igralcev):
                if self.denar_igralcev[i] == 0:
                    self.igralci[i] = False
                    self.aktivni_igralci[i] = False
                else:
                    self.aktivni_igralci[i] = True
            self.vlozen_denar = [0] * self.zacetno_stevilo_igralcev
            self.stevilo_iger += 1
        
    def konec_igre(self, zmagovalec): #Konec celotne igre
        self.koncni_zmagovalec = zmagovalec

    def zmagovalec(self): #določi kdo ima zmagovalne karte
        if self.aktivni_igralci.count(True) == 1:
            return self.aktivni_igralci.index(True)
        indeksi_igralcev = [i for i in range(len(self.aktivni_igralci)) if self.aktivni_igralci[i]]
        indeksi_igralcev.sort(reverse = True, key = lambda a: self.ovrednotenje_kart(list(self.karte_igralcev[a]) + self.karte_na_mizi))
        return indeksi_igralcev[0]

    def poteza_racunalnika(self):
        if self.karte_na_mizi == []:
            if self.karte_igralcev[self.igralec_na_potezi][0].vrednost == self.karte_igralcev[self.igralec_na_potezi][1].vrednost:
                if self.trenutna_stava > self.big_blind:
                    self.dvigni(0)
                else:
                    self.dvigni(int(self.denar_igralcev[self.igralec_na_potezi] / 10))
            else:
                if self.trenutna_stava > self.big_blind and random.random() > 0.75:
                    self.predaj_se()
                elif random.random() > 0.9:
                    self.dvigni(int(self.denar_igralcev[self.igralec_na_potezi] / 10))
                else:
                    self.dvigni(0)
        elif len(self.karte_na_mizi) == 3:
            ovrednotenje = self.ovrednotenje_kart(list(self.karte_igralcev[self.igralec_na_potezi]) + self.karte_na_mizi)
            if ovrednotenje >= (3, [0,0,0,0,0]):
                if self.denar_igralcev[self.igralec_na_potezi] <= self.zacetni_denar / 10:
                    self.dvigni(0)
                else:
                    self.dvigni(int(self.denar_igralcev[self.igralec_na_potezi] / 2))
            elif ovrednotenje >= (2, [0,0,0,0,0]):
                if self.denar_igralcev[self.igralec_na_potezi] <= self.zacetni_denar / 2:
                    self.dvigni(0)
                else:
                    self.dvigni(int(self.denar_igralcev[self.igralec_na_potezi] / 5))
            elif ovrednotenje >= (1, [0,0,0,0,0]):
                self.dvigni(0)
            elif random.random() > 0.50:
                self.predaj_se()
            else:
                self.dvigni(0)
        else:
            ovrednotenje = self.ovrednotenje_kart(list(self.karte_igralcev[self.igralec_na_potezi]) + self.karte_na_mizi)
            if ovrednotenje >= (4, [0,0,0,0,0]):
                self.dvigni(self.zacetni_denar)
            elif ovrednotenje >= (3, [0,0,0,0,0]):
                if self.denar_igralcev[self.igralec_na_potezi] <= self.zacetni_denar / 10:
                    self.dvigni(0)
                else:
                    self.dvigni(int(self.denar_igralcev[self.igralec_na_potezi] / 2))
            elif ovrednotenje >= (2, [0,0,0,0,0]):
                self.dvigni(0)
            elif ovrednotenje >= (1, [0,0,0,0,0]):
                if self.denar_igralcev[self.igralec_na_potezi] <= self.zacetni_denar / 2:
                    self.dvigni(0)
                elif random.random() > 0.5:
                    self.predaj_se()
                else:
                    self.dvigni(0)
            elif random.random() > 0.5:
                self.dvigni(0)
            else:
                self.predaj_se()

    def ovrednotenje_kart(self, karte):
        karte = [(karta.vrednost, karta.barva) for karta in karte]
        karte.sort(reverse = True)
        karte_po_barvah = {} #Seznam z urejenimi seznami za vrednosti
        for i in karte:
            if i[1] in karte_po_barvah:
                karte_po_barvah[i[1]] += [i[0]]
            else:
                karte_po_barvah[i[1]] = [i[0]]
        karte_po_stevilkah = {}
        for i in karte:
            if i[0] in karte_po_stevilkah:
                karte_po_stevilkah[i[0]] += [i[1]]
            else:
                karte_po_stevilkah[i[0]] = [i[1]]

        for _, i in karte_po_barvah.items(): #Preveri če straight flush
            if len(i) >= 5:
                sez_kart = preveri_ce_zaporedne(i, 5)
                if len(sez_kart) > 0:
                    print("Straight flush", sez_kart)
                    return (9, sez_kart)

        for _, i in karte_po_stevilkah.items(): #Preveri če four of a kind
            if len(i) == 4:
                peta_karta = 0
                for karta in karte:
                    if karta[0] != i:
                        peta_karta = karta[0]
                        break
                print("Four of a kind", [i]*4 + [peta_karta])
                return (8, [i]*4 + [peta_karta])

        for i, j in karte_po_stevilkah.items():
            if len(j) == 3:
                vrednosti_parov = [] #Lahko se zgodi da bi imel še 2 različna para
                for a, b in slovar_odstrani_kljuc(karte_po_stevilkah, i).items():
                    if len(b) == 3:
                        print("Full house", [max([i, a])] * 3 + [min([i, a])])
                        return (7, [max([i, a])] * 3 + [min([i, a])])
                    if len(b) == 2:
                        vrednosti_parov.append(a)
                if len(vrednosti_parov) == 0:
                    break
                elif len(vrednosti_parov) == 1:
                    print("Full house", [i] * 3 + [vrednosti_parov[0]] * 2)
                    return (7, [i] * 3 + [vrednosti_parov[0]] * 2)
                else:
                    print("Full house", [i] * 3 + [max(vrednosti_parov)] * 2)
                    return (7, [i] * 3 + [max(vrednosti_parov)] * 2)

        for _, i in karte_po_barvah.items(): #Preveri če flush
            if len(i) >= 5:
                print("Flush", i[:5])
                return (6, i[:5])

        seznam_zaporednih = preveri_ce_zaporedne([karta[0] for karta in karte], 5)
        if len(seznam_zaporednih) > 0: #Preveri če straight
            print("Straight", seznam_zaporednih)
            return (5, seznam_zaporednih)

        for i, j in karte_po_stevilkah.items(): #Preveri če 3 of a kind
            if len(j) == 3:
                ostale_karte = [karta[0] for karta in karte if karta[0] != i][:2]
                print("3 of a kind", [i] * 3 + ostale_karte)
                return (4, [i] * 3 + ostale_karte)

        pari = []
        for i, j in karte_po_stevilkah.items():
            if len(j) == 2:
                pari.append(i)
        if len(pari) >= 2: #Preveri če 2 para
            a = max(pari)
            pari.remove(a)
            b = max(pari)
            peta_karta = [karta[0] for karta in karte if karta[0] != a and karta[0] != b][0]
            print("2 para", [a, a] + [b, b] + [peta_karta])
            return (3, [a, a] + [b, b] + [peta_karta])
        if len(pari) == 1: #Preveri če 1 par
            ostale_karte = [karta[0] for karta in karte if karta[0] not in pari][:3]
            print("1 par", [pari[0]] * 2 + ostale_karte)
            return (2, [pari[0]] * 2 + ostale_karte)

        print("Najvišja karta", [karta[0] for karta in karte[:5]])
        return (1, [karta[0] for karta in karte[:5]])

    #9:Straight Flush - 5 zaporednih iste barve
    #8:Four of a kind - 4 iste
    #7:Full house - 3 pari + 2 para
    #6:Flush 5 - iste barve
    #5:Straight - 5 zaporednih
    #4:Three of a kind - 3 pari
    #3:2 para
    #2:Par
    #1:Najvišja karta

    def slovar_odstrani_kljuc(slovar, kljuc):
        s = dict(slovar)
        del s[kljuc]
        return s

    def preveri_ce_zaporedne(seznam, n): #pregleda če obstaja n dolgo podzaporedje zaporednih številk, v urejenem seznamu, vrne seznam če obstaja
        seznam = list(dict.fromkeys(seznam)) #odstrani podvojene
        st_zaporednih = 1
        indeks = 0
        for i in range(len(seznam)-1):
            if seznam(i) - seznam(i + 1) == 1:
                st_zaporednih += 1
                if st_zaporednih == n:
                    return seznam[indeks:indeks + n]
            else:
                st_zaporednih = 1
                indeks = i + 1

        if seznam[0] == 14: #As se lahko šteje tudi kot 1
            st_zaporednih = 1
            indeks = 0
            seznam = seznam[1:] + [1]
            for i in range(len(seznam)-1):
                if seznam(i) - seznam(i + 1) == 1:
                    st_zaporednih += 1
                    if st_zaporednih == n:
                        return seznam[indeks:indeks + n]
                else:
                    st_zaporednih = 1
                    indeks = i + 1
        return []

def ovrednotenje(karte):
        karte = [(karta.vrednost, karta.barva) for karta in karte]
        karte.sort(reverse = True)
        print(karte)
        karte_po_barvah = {} #Seznam z urejenimi seznami za vrednosti
        for i in karte:
            if i[1] in karte_po_barvah:
                karte_po_barvah[i[1]] += [i[0]]
            else:
                karte_po_barvah[i[1]] = [i[0]]
        karte_po_stevilkah = {}
        for i in karte:
            if i[0] in karte_po_stevilkah:
                karte_po_stevilkah[i[0]] += [i[1]]
            else:
                karte_po_stevilkah[i[0]] = [i[1]]

        for _, i in karte_po_barvah.items(): #Preveri če straight flush
            if len(i) >= 5:
                sez_kart = preveri_ce_zaporedne(i, 5)
                if len(sez_kart) > 0:
                    print("Straight flush", sez_kart)
                    return (9, sez_kart)

        print(karte_po_stevilkah, karte_po_barvah)

        for _, i in karte_po_stevilkah.items(): #Preveri če four of a kind
            if len(i) == 4:
                peta_karta = 0
                for karta in karte:
                    if karta[0] != i:
                        peta_karta = karta[0]
                        break
                print("Four of a kind", [i]*4 + [peta_karta])
                return (8, [i]*4 + [peta_karta])

        for i, j in karte_po_stevilkah.items():
            if len(j) == 3:
                vrednosti_parov = [] #Lahko se zgodi da bi imel še 2 različna para
                for a, b in slovar_odstrani_kljuc(karte_po_stevilkah, i).items():
                    if len(b) == 3:
                        print("Full house", [max([i, a])] * 3 + [min([i, a])])
                        return (7, [max([i, a])] * 3 + [min([i, a])])
                    if len(b) == 2:
                        vrednosti_parov.append(a)
                if len(vrednosti_parov) == 0:
                    break
                elif len(vrednosti_parov) == 1:
                    print("Full house", [i] * 3 + [vrednosti_parov[0]] * 2)
                    return (7, [i] * 3 + [vrednosti_parov[0]] * 2)
                else:
                    print("Full house", [i] * 3 + [max(vrednosti_parov)] * 2)
                    return (7, [i] * 3 + [max(vrednosti_parov)] * 2)

        for _, i in karte_po_barvah.items(): #Preveri če flush
            if len(i) >= 5:
                print("Flush", i[:5])
                return (6, i[:5])

        seznam_zaporenih = preveri_ce_zaporedne([karta[0] for karta in karte], 5)
        if len(seznam_zaporenih) > 0: #Preveri če straight
            print("Straight", seznam_zaporednih)
            return (5, seznam_zaporenih)

        for i, j in karte_po_stevilkah.items(): #Preveri če 3 of a kind
            if len(j) == 3:
                ostale_karte = [karta[0] for karta in karte if karta[0] != i][:2]
                print("3 of a kind", [i] * 3 + ostale_karte)
                return (4, [i] * 3 + ostale_karte)

        pari = []
        for i, j in karte_po_stevilkah.items():
            if len(j) == 2:
                pari.append(i)
        if len(pari) >= 2: #Preveri če 2 para
            a = max[pari]
            pari.remove(a)
            b = max[pari]
            peta_karta = [karta[0] for karta in karte if karta[0] != a and karta[0] != b][0]
            print("2 para", [a, a] + [b, b] + [peta_karta])
            return (3, [a, a] + [b, b] + [peta_karta])
        if len(pari) == 1: #Preveri če 1 par
            ostale_karte = [karta[0] for karta in karte if karta[0] != a and karta[0] != b][:3]
            print("1 par", [pari[0]] * 2 + ostale_karte)
            return (2, [pari[0]] * 2 + ostale_karte)

        print("Najvišja karta", [karta[0] for karta in karte[:5]])
        return (1, [karta[0] for karta in karte[:5]])


def preveri_ce_zaporedne(seznam, n): #pregleda če obstaja n dolgo podzaporedje zaporednih številk, v urejenem seznamu, vrne seznam če obstaja
        print(seznam, "seznamček")
        seznam = list(dict.fromkeys(seznam)) #odstrani podvojene
        st_zaporednih = 1
        indeks = 0
        for i in range(len(seznam)-1):
            if seznam[i] - seznam[i + 1] == 1:
                st_zaporednih += 1
                if st_zaporednih == n:
                    return seznam[indeks:indeks + n]
            else:
                st_zaporednih = 1
                indeks = i + 1

        if seznam[0] == 14: #As se lahko šteje tudi kot 1
            st_zaporednih = 1
            indeks = 0
            seznam = seznam[1:] + [1]
            print(seznam, "seznamček")
            for i in range(len(seznam)-1):
                if seznam[i] - seznam[i + 1] == 1:
                    st_zaporednih += 1
                    if st_zaporednih == n:
                        return seznam[indeks:indeks + n]
                else:
                    st_zaporednih = 1
                    indeks = i + 1
        return []

