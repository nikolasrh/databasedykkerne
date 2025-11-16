# Task B: Paginer gjennom seller reviews med minimum rating

Når vi filtrerer på rating minsker sjansen for at raden vi sjekker blir med i resultatet.
Det vil si at PostgreSQL scanner indeksen mye lenger før den finner 1000 matchende rader.

Dette gjelder også når den regner ut offset, som skjer hver spørring.

Eksempel:
Man er kun ute etter rating=5.
Det finnes like mange rader av hver rating -> 20% sjanse for å treffe.
Må i snitt sjekke 5.000 rader for å finne de første 1000.
Må i snitt sjekke 500.000 rader for å finne page nummer 100.

Hvis man ikke filtrerte på rating blir det 1.000 og 100.000.

Problemet blir værre når man må gjøre mer table access for å avgjøre om raden skal med, f.eks. ved joining av flere tabeller.

Men hovedproblemet er at man må regne ut offset-en for hver spørring, slik at senere sider går treigere.
