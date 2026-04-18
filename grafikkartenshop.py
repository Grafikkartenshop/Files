from grafikkarte import Grafikkarte

class Grafikkartenshop:

    def __init__(self, name):
        self.__shopID = None
        self.__name = name
        self.__umsatz = None
        self.__budget = None
        self.__alleGrafikkarten = []

    def getShopID(self):
        return self.__shopID
    
    def getName(self):
        return self.__name
    
    def getUmsatz(self):
        return self.__umsatz
    
    def getBudget(self):
        return self.__budget
    
    def setShopID(self, shopID):
        self.__shopID = shopID

    def setName(self, name):
        self.__name = name

    def setUmsatz(self, umsatz):
        self.__umsatz = umsatz

    def setBudget(self, budget):
        self.__budget = budget

    def grafikkarteEinkaufen(self, artikelNr, menge) -> bool:
        pass

    def grafikkarteVerkaufen(self, artikelNr, menge) -> bool:
        pass

    def addGrafikkarte(self, modell, hersteller, marke, vramGroesse, speichertyp, einkaufspreis, verkaufspreis) -> bool:
        pass

    def sucheGrafikkarte(self, artikelNr) -> Grafikkarte:
        pass

    def getAlleGrafikkarten(self):
        return self.__alleGrafikkarten
    
    def removeGrafikkarte(self, artikelNr) -> bool:
        pass

    @staticmethod
    def main():
        print("Willkommen beim Grafikkartenshop")

Grafikkartenshop.main()