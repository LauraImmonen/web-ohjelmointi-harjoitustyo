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


Tämä on ensimmäinen web-sovellukseni, joten koodini on varmasti vielä kömpelöä ja vaikealukuista. Otan mielelläni vastaan vinkkejä/palautetta siitä, miten pystyisin parantamaan koodini toimivuutta ja luettavuutta. 


# Asennusohjeet

Postgresql asennusohjeet:

Voit luoda vertaisarviointia varten Postgresiin oman tietokannan seuraavasti
```
$ psql
user=# CREATE DATABASE <tietokannan-nimi>;
```

Luo vaadittavat taulut tietokantaan tiedostosta: schema.sql


Repositorio asennusohjeet:


Kloonaa repositorio omalle koneellesi komennolla

```
git clone https://github.com/LauraImmonen/LauraImmonen-web-ohjelmointi-harjoitustyo.git
```

Luo myös oma .env kansio tähän lokaaliin repoon, jonne teet oman salaisen avaimen seuraavasti:
```
SECRET_KEY=(itse luomasi sercetkey)
```
Lisää .env kansioon myös tekemäsi tietokannan osoite seuraavasti, esim: jos loit vertaisarviontia varten tietokannan nimeltä testi, tulisi uudeksi tietokannan osoitteeksi postgresql:///testi.
```
DATABASE_URL=postgresql:///testi
```


Luo virtuaaliympäristö komennolla:
```
python -m venv venv
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
(venv) $ pip install python-dotenv
```

Käynnistä sovellus 
```
flask run
```

