import bottle
import model

igra = model.Igra(6, 1000)

@bottle.get('/')
def index():
    return bottle.template('index.html')

@bottle.get('/img/<ime>')
def vrni_slike(ime):
    return bottle.static_file(ime, root="img")

@bottle.get('/igra/img/<ime>')
def vrni_slike(ime):
    return bottle.static_file(ime, root="img")

@bottle.get('/nova_igra/img/<ime>')
def vrni_slike(ime):
    return bottle.static_file(ime, root="img")

@bottle.get('/igra/img/<ime>')
def vrni_slike(ime):
    return bottle.static_file(ime, root="img")

@bottle.post('/nova_igra/')
def nova_igra():
    igra.__init__(6,1000)
    igra.igralci = [False] * 6
    bottle.redirect('/nova_igra/')

@bottle.get('/nova_igra/')
def nova_igra():
    return bottle.template('nastavitve.html', igra = igra)

@bottle.post('/igra/')
def igraj():
    igra.nova_runda()
    bottle.redirect('/igra/')

@bottle.post('/predaj/')
def predaj():
    igra.predaj_se()
    igra.vmesni_del = True
    bottle.redirect('/igra/')

@bottle.post('/klic/')
def klic():
    igra.dvigni()
    igra.vmesni_del = True
    bottle.redirect('/igra/')

@bottle.post('/dvig/')
def dvig():
    dvig = bottle.request.forms.getunicode('dvig')
    try:
        dvig = int(dvig)
    except ValueError:
        print("Ni int")
    if isinstance(dvig, int):
        igra.dvigni(dvig)
        igra.vmesni_del = True
    #print("dvig za:", dvig)
    bottle.redirect('/igra/')

@bottle.get('/igra/')
def prikazi_igro():
    return bottle.template('igra.html', igra = igra)

@bottle.post('/vmesni_del/')
def vmes():
    if igra.racunalnik[igra.igralec_na_potezi]:
        igra.poteza_racunalnika()
    else:
        igra.vmesni_del = False
    bottle.redirect('/igra/')

@bottle.post('/zacni_igro/')
def zacni():
    if igra.igralci.count(True) >= 2:
        bottle.redirect('/igra/')
    else:
        bottle.redirect('/nova_igra/')

#Za to zagotovo obstaja boljši način, ampak iz bottle dokumentacije se sploh ne znajdem
######

@bottle.post('/dodaj_igralca0/')
def dodaj_ig0():
    igra.igralci[0] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_igralca1/')
def dodaj_ig1():
    igra.igralci[1] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_igralca2/')
def dodaj_ig2():
    igra.igralci[2] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_igralca3/')
def dodaj_ig3():
    igra.igralci[3] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_igralca4/')
def dodaj_ig4():
    igra.igralci[4] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_igralca5/')
def dodaj_ig5():
    igra.igralci[5] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik0/')
def dodaj_rac0():
    igra.igralci[0] = True
    igra.racunalnik[0] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik1/')
def dodaj_rac1():
    igra.igralci[1] = True
    igra.racunalnik[1] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik2/')
def dodaj_rac2():
    igra.igralci[2] = True
    igra.racunalnik[2] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik3/')
def dodaj_rac3():
    igra.igralci[3] = True
    igra.racunalnik[3] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik4/')
def dodaj_rac4():
    igra.igralci[4] = True
    igra.racunalnik[4] = True
    bottle.redirect('/nova_igra/')

@bottle.post('/dodaj_racunalnik5/')
def dodaj_rac5():
    igra.igralci[5] = True
    igra.racunalnik[5] = True
    bottle.redirect('/nova_igra/')

bottle.run(reloader=True, debug=True)