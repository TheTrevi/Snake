from dataclasses import dataclass
from colorama import init, Fore
import time

init(autoreset=True)

@dataclass
class Posizione:
    x: int
    y: int

class Game:

    def __init__(self,n,m, start,end,dd, vincVerticale, vincOrizontale, caselleNere):
        self.board = [[0 for i in range(n)] for _ in range(m)]
        self.board[start.x][start.y] = 1
        self.board[end.x][end.y] = dd

        for i in caselleNere:
            self.board[i.x][i.y] = -1

        self.start = start
        self.end = end
        self.m = m
        self.n = n
        self.dd =dd
        self.vincoloX = vincOrizontale
        self.vincoloY = vincVerticale
        self.colonne = {n:0 for n in range(n)}
        self.righe = {n:0 for n in range(m)}


        self.temp = 0

        self.lati = [Posizione(0,1),Posizione(0,-1),Posizione(-1,0),Posizione(1,0)]
        self.angoli = [Posizione(-1,-1),Posizione(-1,1),Posizione(1,1),Posizione(1,-1)]
        self.all = []
        self.all.extend(self.angoli)
        self.all.extend(self.lati)

    def stampa(self):
        for n,i in enumerate(self.board):
            print(f"{Fore.GREEN}{self.vincoloY[n]}{Fore.WHITE}",end=" [")
            for ii in i[:-1]:
                colore = Fore.CYAN if ii != 0 else Fore.WHITE
                if ii == -1: colore = Fore.RED
                print(f'{colore}{ii:^{3}}{Fore.WHITE},',end="")

            colore = Fore.CYAN if i[-1] != 0 else Fore.WHITE
            if i[-1] == -1: colore = Fore.RED
            print(f'{colore}{i[-1]:^{3}}{Fore.WHITE}]',end="")

            print("")
        print("    ",end="")
        for n in self.vincoloX:
            print(f"{Fore.GREEN}{n}{Fore.WHITE}",end="   ")
        print("\n=====================================")
    
    def continuare(self, pos):
        """Ritorna le caselle che condividono un lato a una data posizione che non sono 0"""
        disp = []

        for i in self.lati:
            newPos = (pos.x+i.x, pos.y+i.y) 

            if newPos[0] >= self.m or newPos[0] < 0:
                continue
            if newPos[1] >= self.n or newPos[1] < 0:
                continue

            if self.board[newPos[0]][newPos[1]] != 0:
                continue

            disp.append(newPos)

        return disp
    
    def addiacente(self, pos):
        """ Controlla che tutte le caselle addiacenti ad una casella siano o 0 o abbiano una differenza di valore di 1 sui lati
            e di due se si toccano per gli angoli"""
        for i in self.lati:
            newPos = (pos.x+i.x, pos.y+i.y)

            if newPos[0] >= self.m or newPos[0] < 0:
                continue
            if newPos[1] >= self.n or newPos[1] < 0:
                continue

            if self.board[newPos[0]][newPos[1]] == 0 or self.board[newPos[0]][newPos[1]] == -1: continue

            diff = self.board[pos.x][pos.y] - self.board[newPos[0]][newPos[1]]
            if abs(diff) == 1:
                continue

            return False
        
        for i in self.angoli:
            newPos = (pos.x+i.x, pos.y+i.y)

            if newPos[0] >= self.m or newPos[0] < 0:
                continue
            if newPos[1] >= self.n or newPos[1] < 0:
                continue

            if self.board[newPos[0]][newPos[1]] == 0 or self.board[newPos[0]][newPos[1]] == -1: continue

            diff = self.board[pos.x][pos.y] - self.board[newPos[0]][newPos[1]]
            if abs(diff) == 2:
                continue

            return False

        return True

    def finito(self):
        """ Controllo finale se nella casella finale è addiacente al valore finale-1"""
        for i in self.lati:
            newPos = (self.end.x+i.x, self.end.y+i.y)

            if newPos[0] >= self.m or newPos[0] < 0:
                continue
            if newPos[1] >= self.n or newPos[1] < 0:
                continue

            if self.board[newPos[0]][newPos[1]] == 0 or self.board[newPos[0]][newPos[1]] == -1: continue

            diff = self.board[self.end.x][self.end.y] - self.board[newPos[0]][newPos[1]]
            # checkAll si può anche togliere controlla che i multipli siano giusti ma sono sempre giusti
            if abs(diff) == 1: #and self.checkAll()
                return True
            
        return False
    
    def checkAll(self):
        """Controlla tutti i multipli di 3"""
        nn =0
        for n,riga in enumerate(self.board):
            for i in riga:
                if i!=0 and i%3 == 0: nn += 1
            if nn > self.vincoloY[n]: return False
            nn = 0

        for n,col in enumerate(zip(*self.board)):
            for i in col:
                if i!=0 and i%3 == 0: nn += 1
            if nn > self.vincoloX[n]: return False
            nn = 0

        return True

    def checkVincolo(self, pos):
        """ Controlla i multipli di 3 in una specifica posizione quindi in quella riga e colonna
            Questa funzione viene chiamata ogni volta che viene aggiunto un numero, più veloce sarebbe tenere una cache del numero
            di multipli in ogni riga e colonna in una hashmap
        """
        nn = 0
        for i in self.board[pos.x]:
            if i!=0 and i%3==0: nn+=1
        if nn>self.vincoloY[pos.x]: return False

        nn = 0
        for n,col in enumerate(zip(*self.board)):
            if n!=pos.y: continue
            for i in col:
                if i!=0 and i%3 == 0: nn += 1
            if nn > self.vincoloX[n]: return False
            nn = 0
        return True
    
        # """Con Hashset"""
        # if self.board[pos.x][pos.y]%3 == 0:
        #     self.colonne[pos.y] +=1
        #     self.righe[pos.x] +=1
        #     if self.colonne[pos.y] > self.vincoloX[pos.y] or self.colonne[pos.x] > self.vincoloY[pos.x]:
        #         return False
        # return True
    
    def delete(self, pos):
        # if self.board[pos.x][pos.y]%3 ==0:
        #     self.colonne[pos.y] -=1
        #     self.righe[pos.x] -=1
        self.board[pos.x][pos.y]=0

    def avvio(self, pos, num):
        """Start search"""
        disp = self.continuare(pos)
        for i in disp:
            self.temp+=1
            pp = Posizione(i[0],i[1])
            self.board[pp.x][pp.y] = num
            if not self.addiacente(pp):
                self.delete(pp)
                continue
            if not self.checkVincolo(pp):
                self.delete(pp)
                continue
            if num == self.dd-1 and self.finito(): self.stampa()
            self.avvio(pp,num+1)
            self.delete(pp)

    def visualAvvio(self,pos,num):
        """Start search"""
        disp = self.continuare(pos)
        for i in disp:
            self.temp+=1
            pp = Posizione(i[0],i[1])
            self.board[pp.x][pp.y] = num
            if not self.addiacente(pp):
                self.delete(pp)
                continue
            if not self.checkVincolo(pp):
                self.delete(pp)
                continue
            if num == self.dd-1 and self.finito(): self.stampa()
            self.stampa()
            print(self.colonne)
            print(self.righe)
            time.sleep(1)
            self.visualAvvio(pp,num+1)
            self.delete(pp)

if __name__ == "__main__":
    start = Posizione(2,0)
    end = Posizione(4,0)

    vincVerticale = [2,1,2,1,1,1,1,1]#[5 for _ in range(8)]
    vincOrizontale = [1,2,1,3,0,1,1,1]#[5 for _ in range(8)]

    caselleNere = [(3,0)]
    caselleNere = [Posizione(n[0],n[1]) for n in caselleNere]
                

    game = Game(8,8,start,end,31, vincVerticale, vincOrizontale, caselleNere)


    game.stampa()
    # print(game.continuare(Posizione(0,0)))
    # print(game.addiacente(Posizione(0,0)))
    game.avvio(start,2)
    # game.visualAvvio(start,2)
    # game.checkVincolo(Posizione(0,1))
    # print(game.temp)  