class Grafikkarte:

    def __init__(self, modell, hersteller, marke, vramGroesse, speichertyp, einkaufspreis, verkaufspreis):
        self.__artikelNr = None
        self.__modell = modell
        self.__hersteller = hersteller
        self.__marke = marke
        self.__vramGroesse = vramGroesse
        self.__speichertyp = speichertyp
        self.__einkaufspreis = einkaufspreis
        self.__verkaufspreis = verkaufspreis
        self.__bestand = None

    def getArtikelNr(self):
        return self.__artikelNr
    
    def getModell(self):
        return self.__modell
    
    def getHersteller(self):
        return self.__hersteller
    
    def getMarke(self):
        return self.__marke
    
    def getVramGroesse(self):
        return self.__vramGroesse
    
    def getSpeichertyp(self):
        return self.__speichertyp
    
    def getEinkaufspreis(self):
        return self.__einkaufspreis
    
    def getVerkaufspreis(self):
        return self.__verkaufspreis
    
    def getBestand(self):
        return self.__bestand
    
    def setArtikelNr(self, artikelNr):
        self.__artikelNr = artikelNr

    def setModell(self, modell):
        self.__modell = modell

    def setHersteller(self, hersteller):
        self.__hersteller = hersteller

    def setMarke(self, marke):
        self.__marke = marke

    def setVramGroesse(self, vramGroesse):
        self.__vramGroesse = vramGroesse

    def setSpeichertyp(self, speichertyp):
        self.__speichertyp = speichertyp

    def setEinkaufspreis(self, einkaufspreis):
        self.__einkaufspreis = einkaufspreis

    def setVerkaufspreis(self, verkaufspreis):
        self.__verkaufspreis = verkaufspreis

    def setBestand(self, bestand):
        self.__bestand = bestand
