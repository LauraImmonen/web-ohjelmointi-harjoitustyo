# koulusovellus

Harjoitustyöni yliopistokurssille Tietokannat ja web-ohjelmointi

Ideana on koulusovellus

admin = opettaja ja user = opiskelija.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- opettaja (admin) voi luoda/muokata/poistaa kursseja, joille oppilaat voivat ilmoittautua.
- opettaja (admin) näkee ketä on ilmoittautunut kurssille.
- opettaja (admin) pystyy antamaan oppilaalle arvosanan suoritetusta kurssista.
- Opiskelija näkee listan kursseista ja voi liittyä kurssille.
- opiskelija (user) pystyy tarkastelemaan omia tietojaan (omat kurssit, arvosanat).

Ottaen huomioon, kuinka vähän aikaa tällä kurssilla oli sovellukset valmistamiseen (7vko) ja siihen, että tämän on ensimmäinen web-sovellukseni, olen tyytyväinen lopputulokseen. Sain sovellukseni kaikki ominaisuudet toimimaan kuten suunnittelin, ja mielestäni tietoturva ominaisuudet ovat sovelluksessa kunnossa.
Sovelluksessa on kuitenkin vielä odotettavasti paljon parantamista/ominaisuuksia joita voisi hioa ja lisätä. Varsinkin sovelluksen ulkoasun tekemisessä on minulla vielä opeteltavaa.

Otan mielelläni vastaan vinkkejä/palautetta siitä, miten pystyisin parantamaan koodini toimivuutta ja ymmärrettävyyttä.

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
