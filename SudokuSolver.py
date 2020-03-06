import numpy as np

class Sudoku:
    def __init__(self,main,size):
        self.cell=np.zeros([size,size])
        for i in main:
            self.cell[i[0]-1,i[1]-1]=main[i]
    def p(self,guess=False):
        print(self.cell)
    
    def solve(self,i,j):
        if self.cell[i-1,j-1]!=0:
            return 
        temp=[k for k in range(1,10)]
        #import pdb;pdb.set_trace()
        value_set=set(np.append(self.cell[i-1,:],self.cell[:,j-1]))
        (m,n)=((i-1)//3,(j-1)//3)
        for row in range(3):
            for col in range(3):
                value_set.add(self.cell[m*3+row,n*3+col])
        if len(value_set)==9 and 0 in value_set:
            self.cell[i-1,j-1]=list(set(range(1,10))-value_set)[0]
            return 

    def solver(self):
        for i in range(1,10):
            for j in range(1,10):
                self.solve(i,j)

main={(1,1):5,(1,2):3,(2,1):6,(3,2):9,(3,3):8,(1,5):7,(2,4):1,
(2,5):9,(2,6):5,(3,8):6,(4,1):8,(5,1):4,(6,1):7,(5,4):8,(4,5):6,
(6,5):2,(5,6):3,(4,9):3,(5,9):1,(6,9):6,(7,2):6,(8,4):4,(8,5):1,
(8,6):9,(9,5):8,(7,7):2,(7,8):8,(8,9):5,(9,8):7,(9,9):9}


game=Sudoku(main,9)
game.p()
for _ in range(5):
    #import pdb;pdb.set_trace()

    game.solver()
    game.p()
    print('-'*30)

