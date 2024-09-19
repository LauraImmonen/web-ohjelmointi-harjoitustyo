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
  
# Asennusohjeet

Kloonaa repositorio omalle koneellesi komennolla

```
git clone https://github.com/LauraImmonen/LauraImmonen-web-ohjelmointi-harjoitustyo.git
```

Luo virtuaaliympäristö komennolla 
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

Käynnistä sovellus 
```
flask run
```

# koulusovellus
Harjoitustyöni yliopistokurssille Tietokannat ja web-ohjelmointi

Ideana on koulusovellus

admin = opettaja ja user = opiskelija. 

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- opettaja (admin) voi luoda/muokata/poistaa kursseja, joille oppilaat voivat ilmoittautua.
- opettaja (admin) näkee ketä on ilmoittautunut kurssille.
- opettaja (admin) pystyy merkitsemään kurssin suoritetuksi ja antamaan oppilaalle arvosanan sekä opintopisteet suoritetusta kurssista. 
- Opiskelija näkee listan kursseista ja voi liittyä kurssille.
- opiskelija (user) pystyy tarkastelemaan omia tietojaan (omat kurssit, arvosanat).


Tämä on ensimmäinen web-sovellukseni, joten koodini on varmasti vielä hieman kömpelöä. Otan mielelläni vastaan palautetta/vinkkejä, siitä miten voisin parantaa koodini tehokkuutta ja luettavuutta.
  

# Asennusohjeet

Kloonaa repositorio omalle koneellesi komennolla

```
git clone https://github.com/LauraImmonen/LauraImmonen-web-ohjelmointi-harjoitustyo.git
```

Luo virtuaaliympäristö komennolla 
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

Käynnistä sovellus 
```
flask run
```
