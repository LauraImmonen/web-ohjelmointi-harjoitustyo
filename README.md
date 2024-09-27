# koulusovellus
Harjoitustyöni yliopistokurssille Tietokannat ja web-ohjelmointi

Ideana on koulusovellus

admin = opettaja ja user = opiskelija. 

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- opettaja (admin) voi luoda/muokata/poistaa kursseja, joille oppilaat voivat ilmoittautua.
- opettaja (admin) näkee ketä on ilmoittautunut kurssille.
- opettaja (admin) pystyy merkitsemään kurssin suoritetuksi ja antamaan oppilaalle arvosanan suoritetusta kurssista. 
- Opiskelija näkee listan kursseista ja voi liittyä kurssille.
- opiskelija (user) pystyy tarkastelemaan omia tietojaan (omat kurssit, arvosanat).


Tämä on ensimmäinen web-sovellukseni, joten koodini on varmasti vielä kömpelöä. Otan mielelläni vastaan vinkkejä/palautetta siitä, miten pystyisin parantamaan koodini toimivuutta ja luettavuutta. 

Tällä hetkellä sovelluksessa pystyy luomaan käyttäjän, kirjautumaan sisään sovellukseen ja opettajilla ja opiskelijoilla on omat etusivunsa. Opettaja pystyy luomaan, muokkaamaan ja poistamaan kursseja, ja oppilas pystyy ilmoittautumaan niille. Muita toimintoja en ole vielä ehtinyt tekemään. 


# Asennusohjeet

Postgresql asennusohjeet:

Voit luoda vertaisarviointia varten Postgresiin oman tietokannan seuraavasti
```
$ psql
user=# CREATE DATABASE <tietokannan-nimi>;
```

Repositorio asennusohjeet:

Luo hakemisto tälle repolle esim:
```
mkdir testi
```
ja luo reitti sille:
```
cd testi
```

Kloonaa repositorio omalle koneellesi komennolla

```
git clone https://github.com/LauraImmonen/LauraImmonen-web-ohjelmointi-harjoitustyo.git
```

Tämän jälkeen avaa reitti hakemistoon
```
cd testi/
```
(näet komennolla ls, oletko repositiossa, pitäisi näkyä kaikki sovelluksen osat esim app.py, schema.sql yms. Jos ei näy, niin sinun pitää mennä ns syvemmälle, avaa siis tiedosto koneella ja katso reitti, se voi olla esim. Documents/testi/repon_nimi/ ja yritä sitten: cd Documents/testi/repon_nimi/) 

Luo myös oma .env kansio tähän lokaaliin repoon, jonne teet oman salaisen avaimen seuraavasti:
```
SECRET_KEY=(itse luomasi sercetkey)
```
Lisää .env kansioon myös tekemäsi tietokannan osoite seuraavasti, esim: jos loit vertaisarviontia varten tietokannan nimeltä testi, tulisi uudeksi tietokannan osoitteeksi postgresql:///testi.
```
DATABASE_URL=postgresql:///testi
```


Luo schemat tietokantaan ensin ja sitten virtuaaliympäristö komennoilla:

```
psql -d (oman tietokannan nimi) < schema.sql
```

```
python3 -m venv venv
```

Aktivoi virtuaaliympäristö
```
# Linuxissa tai Macissa
source venv/bin/activate
```

Asenna riippuvuudet komennolla
```
pip install -r requirements.txt
```

python-dotenv tulee myös olla asennettuna
```
pip install python-dotenv
```

Käynnistä sovellus 
```
flask run
```

