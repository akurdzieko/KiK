import pygame as pg, sys, time 
import os
from pygame.locals import *

#ustawienia początkowe - tworzymy najważniejsze zmienne
CzyjaTura = 'x'
KtoWygral = None
Remis = False
Szerokosc = 400
Wysokosc = 400 
#RGB
Bialy = (255, 255, 255)
Czerwony = (255, 0, 0)
Czarny = (0, 0, 0)
Fioletowy = (184, 3, 255)

PunktyX = 0
PunktyO = 0
Plansza = [[None ]* 3,[None ]* 3,[None ]* 3]
pg.init()
FPS = 30
Zegar = pg.time.Clock()
Ekran = pg.display.set_mode((Szerokosc, Wysokosc + 200),0,32 )
pg.display.set_caption(";) Kolko i Krzyzyk Alicji")
#ladujemy obrazki do zmiennych
PlanszaStartowa = pg.image.load('PlanszaStartowa.png')
ObrazekX = pg.image.load('X.png')
ObrazekO = pg.image.load('O.png')
#ustawiamy nowe wymiary obrazkow
PlanszaStartowa = pg.transform.scale(PlanszaStartowa,  (Szerokosc, Wysokosc + 200))
ObrazekX = pg.transform.scale(ObrazekX,  (80,80 ))
ObrazekO = pg.transform.scale(ObrazekO,  (80,80 ))

def RysujPlansze():
    Ekran.blit(PlanszaStartowa, (0,0))
    pg.display.update()
    Ekran.fill(Fioletowy)
    pg.time.delay(2000)
    #rysujemy linie
    pg.draw.line(Ekran, Czarny, (Szerokosc / 3, 0),  (Szerokosc / 3,  Wysokosc), 7) 
    pg.draw.line(Ekran, Czarny, (Szerokosc / 3 * 2, 0),  (Szerokosc / 3 * 2,  Wysokosc), 7)

    #rysowanie lini
    pg.draw.line(Ekran, Czarny, (0, Wysokosc / 3),  (Szerokosc,  Wysokosc / 3), 7) 
    pg.draw.line(Ekran, Czarny, (0, Wysokosc / 3 * 2),  (Szerokosc,  Wysokosc / 3 * 2), 7)
    
    pg.display.update()
    RysujDodatkoweInformacje()

def RysujDodatkoweInformacje():
    global Remis

    if KtoWygral is None:
                TrescWiadomosci = "Twoja tura: " + CzyjaTura.upper()
    else:           
                TrescWiadomosci = KtoWygral.upper() + " wygrales!"
    if Remis:       
                TrescWiadomosci = "Remis!"

    Czcionka = pg.font.Font(None, 30)
    Wiadomosc = Czcionka.render(TrescWiadomosci, True, Bialy)

    Punkty = "X: "  + str(PunktyX) + " <----> O:" +str(PunktyO)
    PunktyWiadomosc = Czcionka.render(Punkty, True, Czarny)

    ObramowanieNaWiadomosc = Wiadomosc.get_rect(center = (Szerokosc/2,500-50))
    ObramowanieNaPunkty = PunktyWiadomosc.get_rect(center = (Szerokosc/2,600-50))
    
    Ekran.fill((0,0,0), (0, 400, 500, 100))
    Ekran.blit(Wiadomosc, ObramowanieNaWiadomosc)
    Ekran.blit(PunktyWiadomosc, ObramowanieNaPunkty)

    pg.display.update()                                                                                                                                                

def SprawdzWygrana():
                global Plansza, KtoWygral, Remis
                #sprawdzamy wygranej w pozimie
                for wiersz in range (0,3):
                                if ((Plansza[wiersz] [0] == Plansza[wiersz] [1] == Plansza[wiersz] [2]) and (Plansza [wiersz] [0] is not None)):
                                                KtoWygral = Plansza[wiersz] [0]
                                                pg.draw.line(Ekran, (128, 0, 0), (0, (wiersz + 1) * Wysokosc / 3 - Wysokosc / 6),  (Szerokosc, (wiersz + 1) *Wysokosc / 3 - Wysokosc / 6), 4)

                                                break

                #sprawdzamy wygranej w pionie

                for Kolumna in range (0,3):
                                if((Plansza[0][Kolumna] == Plansza[1][Kolumna] == Plansza[2][Kolumna])  and (Plansza[0][Kolumna] is not None)):
                                                KtoWygral = Plansza[0][Kolumna]
                                                pg.draw.line(Ekran, (128,0, 0), ((Kolumna + 1) *Szerokosc / 3 - Szerokosc / 6, 0), ((Kolumna + 1) * Szerokosc / 3 - Szerokosc / 6, Szerokosc), 4)
                                                break 

                
            #sprawdzamy wygranej na ukos
            
                if((Plansza[0][0] == Plansza[1][1] == Plansza[2][2]) and (Plansza[0][0] is not None)):
                                 KtoWygral = Plansza[0][0]   
                                 pg.draw.line(Ekran, (128, 0, 0), (50,50), (350,350), 4)                    
                
                if((Plansza[0][2] == Plansza[1][1] == Plansza[2][0]) and (Plansza[0][2] is not None)):
                                 KtoWygral = Plansza[0][2]   
                                 pg.draw.line(Ekran, (128, 0, 0), (50,350), (350,50), 4) 

                 #jeżeli nikt nie wygrał
                if(all([all(wiersz) for wiersz in Plansza]) and KtoWygral is None):
                               Remis = True

                RysujDodatkoweInformacje()
def NarysujSymbol(Wiersz,Kolumna):              
                                                
                global Plansza, CzyjaTura
                
                #PozycjaX
                if Wiersz == 1:
                                PozycjaX = 30
                elif Wiersz == 2:
                                PozycjaX = Szerokosc / 3 + 30
                elif Wiersz == 3:
                                PozycjaX = Szerokosc / 3 * 2 + 30
               
               #pozycjaY
                if Kolumna == 1:
                                Pozycjay = 30
                elif Kolumna == 2:
                                Pozycjay = Szerokosc / 3 + 30
                elif Kolumna == 3:
                                Pozycjay = Szerokosc / 3 * 2 + 30
               #ustawiamy flage,że dane pole jest już zajęte
                Plansza[Wiersz - 1] [Kolumna - 1] = CzyjaTura                          
               
               #rysujemy odpowiedni symmbol
                
                if(CzyjaTura == 'x'):
                                Ekran.blit(ObrazekX, (Pozycjay, PozycjaX))
                                CzyjaTura = 'o'
                elif(CzyjaTura == 'o'):
                                Ekran.blit(ObrazekO, (Pozycjay, PozycjaX))
                                CzyjaTura = 'x'
                pg.display.update()
def SprawdzPole():
                 #czytamy koordynaty myszki
                 X,Y = pg.mouse.get_pos()
                  #wspolrzeda x
                 if(X < Szerokosc / 3) :
                    Kolumna = 1
                 elif(X < Szerokosc / 3 * 2):
                    Kolumna = 2
                 elif(X < Szerokosc) :
                    Kolumna = 3
                 else:      
                    Kolumna = None
                 #wspulrzedna y                 
                 if(Y < Wysokosc / 3) :
                                 Wiersz = 1
                 elif(Y < Wysokosc / 3 * 2):
                                Wiersz = 2
                 elif(Y < Wysokosc) :
                                Wiersz = 3
                 else: 
                                Wiersz=None
   # "print(Kolumna,Wiersz)"to bez # działa                  
                 #print(Kolumna,Wiersz) 
             
                 if(Wiersz and Kolumna and Plansza[Wiersz - 1][Kolumna - 1] is None):              
                     global CzyjaTura

                     NarysujSymbol(Wiersz,Kolumna)
                     SprawdzWygrana()
def RestartujGre():
                 
                 global Plansza, KtoWygral, CzyjaTura, Remis, PunktyX, PunktyO
                 time.sleep(5)
                 CzyjaTura = 'x'
                 Remis = False
                 if KtoWygral == 'x':
                               PunktyX += 1
                 elif KtoWygral == 'o':
                            PunktyO += 1

                 KtoWygral = None
                 Plansza = [[None] *3, [None] *3, [None] *3]
                 Ekran.fill(Bialy)
                 RysujPlansze()
RysujPlansze()
#RUN APPLICATION
while(True):
    for zdarzenie in pg.event.get():
        if zdarzenie.type == QUIT:
            pg.quit()
            sys.exit()
        elif zdarzenie.type is MOUSEBUTTONDOWN:
            if(zdarzenie.button == 1):
                SprawdzPole()   
                if(KtoWygral or Remis): 
                               RestartujGre()       
    
pg.display.update()
Zegar.tick(FPS) 


#EkranPoczatkowy() 
#pg.display.update() 
#time.sleep(4)
#RysujPlansze()
#pg.display.update()
#time.sleep(4)
# def AlicjaRysyje():
#     Ekran.fill(Bialy)
#     pg.display.update()
#     time.sleep(4)
#     Ekran.fill(Czerwony)
#     pg.display.update()
#     time.sleep(4)
#     Ekran.fill(Fioletowy)
#     pg.display.update()
#     time.sleep(4)