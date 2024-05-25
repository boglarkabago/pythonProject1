from abc import ABC, abstractmethod
from datetime import datetime, date
import sys

# Abstract Room class
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def get_ar(self):
        pass

    @abstractmethod
    def get_agyak_szama(self):
        pass

# Single Room class
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(40000, szobaszam)  # 40.000 Ft az egyágyas szoba ára

    def get_ar(self):
        return self.ar

    def get_agyak_szama(self):
        return 1

# Double Room class
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(50000, szobaszam)  # 50.000 Ft a kétágyas szoba ára

    def get_ar(self):
        return self.ar

    def get_agyak_szama(self):
        return 2

# Hotel class
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
        self.silent_mode = False

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        if datum <= date.today():
            if not self.silent_mode:
                print("Hiba: A foglalás dátuma a mai napnál későbbi kell, hogy legyen.")
            return None

        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                if not self.silent_mode:
                    print("Hiba: A szoba már foglalt a megadott dátumra.")
                return None

        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                uj_foglalas = Foglalas(szobaszam, datum, szoba.get_ar())
                self.foglalasok.append(uj_foglalas)
                if not self.silent_mode:
                    print(f"A foglalás sikeres. Ár: {szoba.get_ar()} HUF")
                return szoba.get_ar()

        if not self.silent_mode:
            print("Hiba: Nincs ilyen szobaszám.")
        return None

    def foglalas_lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                print("A foglalás lemondása sikeres.")
                return True

        print("Hiba: Nincs ilyen foglalás.")
        return False

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
        else:
            for foglalas in self.foglalasok:
                print(f"Szobaszám: {foglalas.szobaszam}, Dátum: {foglalas.datum}, Ár: {foglalas.ar} HUF")

    def listaz_szobak(self):
        print("Elérhető szobák:")
        for szoba in self.szobak:
            agyak_szama = "egyágyas" if szoba.get_agyak_szama() == 1 else "kétágyas"
            print(f"Szobaszám: {szoba.szobaszam}, Típus: {agyak_szama}, Ár: {szoba.get_ar()} HUF")

# Booking class
class Foglalas:
    def __init__(self, szobaszam, datum, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.ar = ar

# Simple User Interface
def felhasznaloi_felulet(szalloda):
    while True:
        print("\n1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válasszon egy lehetőséget (1-4): ")

        if valasztas == '1':
            szalloda.listaz_szobak()
            try:
                szobaszam = int(input("Adja meg a szobaszámot: "))
                datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d").date()
                szalloda.foglalas(szobaszam, foglalas_datum)
            except ValueError:
                print("Hibás dátum formátum. Próbálja újra.")
        elif valasztas == '2':
            szalloda.listaz_szobak()
            try:
                szobaszam = int(input("Adja meg a szobaszámot: "))
                datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d").date()
                szalloda.foglalas_lemondas(szobaszam, foglalas_datum)
            except ValueError:
                print("Hibás dátum formátum. Próbálja újra.")
        elif valasztas == '3':
            szalloda.listaz_foglalasok()
        elif valasztas == '4':
            print("Kilépés...")
            sys.exit()
        else:
            print("Érvénytelen választás. Próbálja újra.")

# Main function to initialize the system with data
def main():
    szalloda = Szalloda("Hotel Firenze Budapest")

    szalloda.add_szoba(EgyagyasSzoba(101))
    szalloda.add_szoba(KetagyasSzoba(102))
    szalloda.add_szoba(EgyagyasSzoba(103))

    szalloda.silent_mode = True  # Disable printing for predefined bookings
    szalloda.foglalas(101, date(2024, 5, 30))
    szalloda.foglalas(102, date(2024, 6, 15))
    szalloda.foglalas(103, date(2024, 7, 1))
    szalloda.foglalas(101, date(2024, 8, 20))
    szalloda.foglalas(102, date(2024, 9, 5))
    szalloda.silent_mode = False  # Enable printing for user interactions

    felhasznaloi_felulet(szalloda)

if __name__ == "__main__":
    main()
