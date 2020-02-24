import numpy as np


# The Sudoku Labyrinth (sometime named: Snail or Magic Spiral) is a very addictive puzzle.
# Each grid contains a path that visits each cell of the grid. The beginning of the path is indicated by an arrow.
# The goal of the puzzle is to repeat the number sequence "1-2-3" in the path as many times as possible until the end of that path 
# each row and column have all the numbers of the sequence only once.
# it is square shape grid and only '1','2','3' for this puzzle. Sometime '4' will add.
# for empty space is represent as 'X'


class Snail:
    ## Do all the initialization and making the inserting the main cell into the cells

    Change=True

    def __init__(self,size,main):
        self.size=size
        self.MAIN_CELL=main
        self.fill_cell={}
        self.cell={}
        self.fill_list=np.zeros([2,self.size])
        self.empty_list=np.ones([2,self.size])*self.size
        for i in range(self.size**2):
            if (i//self.size,i%self.size) in self.MAIN_CELL:
                self.cell[i]={"main":self.MAIN_CELL[(i//self.size,i%self.size)],"guess":"null","fill":False}
            else:
                self.cell[i]={"main":-1,"guess":"-123","fill":False}
    ## Return the path of snail indexs
    def find_snall_path(self):
        path=[]
        now=0
        rep=5
        multi=1
        while(rep!=0):
            for i in range(rep):
                now=now+(multi*1)
                path.append(now)
            rep=rep-1
            for i in range(rep):
                now=now+(multi*5)
                path.append(now)
            multi=multi*-1
        return path

    ## Update the guess with the main cell . it is only ran once and at the starting.
    def update_main(self):
        for main in self.MAIN_CELL:
            self.fill_cell[main[0]*self.size+main[1]]=self.MAIN_CELL[main]
            self.fill_list[0,main[0]]+=1
            self.fill_list[1,main[1]]+=1
            self.empty_list[0,main[0]]-=1
            self.empty_list[1,main[1]]-=1
            for i in self.cell:
                if (i//self.size==main[0] or i%self.size==main[1]):
                    self.cell[i]["guess"]=self.cell[i]["guess"].replace(str(self.MAIN_CELL[main]),"")
                    self.Change=True

    ## conform the number if there are only one guess in the row and column
    def update_single_guess(self):
        guess_list={}
        for j in range(self.size):

            for i in range(self.size):
                guess_list[i]=self.cell[j*self.size+i]["guess"]
            #import pdb;pdb.set_trace()

            for k in range(1,4):
                if np.sum([str(k) in l for l in guess_list.values()])==1:
                    for i in range(self.size):
                        if str(k) in self.cell[j*self.size+i]["guess"]:
                            self.cell[j*self.size+i]["main"]=k
                            self.cell[j*self.size+i]["guess"]="null"
                            self.empty_list[0,j]-=1
                            self.empty_list[1,i]-=1
                            self.fill_cell[i]=self.cell[j*self.size+i]['main']
                            self.fill_list[0,j]+=1
                            self.fill_list[1,i]+=1
                            self.Change=True
                            break
            self.update_fill()
 
        guess_list={}
        for j in range(self.size):
            for i in range(self.size):
                guess_list[i]=self.cell[j+i*self.size]["guess"]
            for k in range(1,4):
                if np.sum([str(k) in l for l in guess_list.values()])==1:
                    for i in range(self.size):
                        if str(k) in self.cell[j+i*self.size]["guess"]:
                            self.cell[j+i*self.size]["main"]=k
                            self.cell[j+i*self.size]["guess"]="null"
                            self.empty_list[0,i]-=1
                            self.empty_list[1,j]-=1
                            self.fill_cell[j+i*self.size]=self.cell[j+i*self.size]['main']
                            self.fill_list[0,i]+=1
                            self.fill_list[1,j]+=1
                            self.Change=True
                            break
            self.update_fill()


    ## update the fill value if the remaining cell has to fill in a row or column
    def update_fill_para(self):
        emy=[]
        emy=self.empty_list+self.fill_list
        for i in range(len(emy[0])):
            if emy[0,i]==3:    
                for j in range(self.size):
                    if self.cell[i*5+j]["fill"]==False:
                        self.Change=True
                        self.cell[i*5+j]["fill"]=True
                
        for i in range(len(emy[1])):
            if emy[1,i]==3:
                for j in range(self.size):
                    if self.cell[j*5+i]["fill"]==False:
                        self.cell[j*5+i]["fill"]=True
                        self.Change=True

    ## update the guesses if any new value is added
    def update_fill(self):
        for j in self.fill_cell:
            for i in self.cell:
                    if ((i//self.size==j//self.size or i%self.size==j%self.size) ) and self.cell[i]["guess"]!=self.cell[i]["guess"].replace(str(self.fill_cell[j]),"") :
                        self.cell[i]["guess"]=self.cell[i]["guess"].replace(str(self.fill_cell[j]),"")
                        self.Change=True       
    
    ## update the value and guesses in the path consideration 
    def update_path(self):
        path=self.find_snall_path()
        order=1
        check=True
        for pos in path:
            #pdb.set_trace()

            if self.cell[pos-1]["main"]!=-1 and self.cell[pos-1]["main"]!=0 :
                order=(self.cell[pos-1]["main"]+1)%3 if self.cell[pos-1]["main"]!=2 else 3
                check=True
                continue
            if pos>1:
                if self.cell[path[path.index(pos)-1]-1]["main"]==-1 and check:
                    check=False
                    continue
            if check and self.cell[pos-1]["guess"]!="null":
                if str(order) not in self.cell[pos-1]["guess"]: 
                    self.cell[pos-1]["main"]=0
                    self.cell[pos-1]["guess"]="null"
                    self.empty_list[0,(pos-1)//self.size]-=1
                    self.empty_list[1,(pos-1)%self.size]-=1
                    self.Change=True
                else:                  
                    list_remove=['1','2','3']
                    list_remove.remove(str(order))
                    for k in list_remove:
                        self.cell[pos-1]["guess"]=self.cell[pos-1]["guess"].replace(k,'')
                    self.Change=True
    
    ## update the value and guesses in the path consideration but in the reverse direction
    def update_rev_path(self):
        path=self.find_snall_path()
        order=3
        check=True
        for pos in path[::-1]:
            #pdb.set_trace()

            if self.cell[pos-1]["main"]!=-1 and self.cell[pos-1]["main"]!=0 :
                order=(self.cell[pos-1]["main"]-1)%3 if self.cell[pos-1]["main"]!=1 else 3
                check=True
                continue
            if pos!=path[1] and pos!=path[-1]:
                if self.cell[path[path.index(pos)+1]-1]["main"]==-1 and check:
                    check=False
                    continue
            if check and self.cell[pos-1]["guess"]!="null":
                if str(order) not in self.cell[pos-1]["guess"]: 
                    self.cell[pos-1]["main"]=0
                    self.cell[pos-1]["guess"]="null"
                    self.empty_list[0,(pos-1)//self.size]-=1
                    self.empty_list[1,(pos-1)%self.size]-=1
                    self.Change=True
                else:
                    list_remove=['1','2','3']
                    list_remove.remove(str(order))
                    for k in list_remove:
                        self.cell[pos-1]["guess"]=self.cell[pos-1]["guess"].replace(k,'')
                    self.Change=True

    ## if the updated guesses have no value it will update with 0
    def update_guesses(self):
        for i in self.cell:
            if (self.cell[i]["guess"]=="-"):
                self.cell[i]["guess"]="null"
                self.cell[i]["main"]=0
                self.empty_list[0,i//self.size]-=1
                self.empty_list[1,i%self.size]-=1
                self.Change=True
            #pdb.set_trace()
            if self.cell[i]["fill"]==True and len(self.cell[i]["guess"].replace('-',''))==1:
                self.cell[i]['main']=int(self.cell[i]["guess"].replace('-',''))
                self.cell[i]['guess']='null'
                self.empty_list[0,i//self.size]-=1
                self.empty_list[1,i%self.size]-=1
                self.fill_cell[i]=self.cell[i]['main']
                self.fill_list[0,i//self.size]+=1
                self.fill_list[1,i%self.size]+=1
                self.Change=True

    ## print the matrix for underastanding 
    def p(self,guess=False):
        fig=np.ones([self.size,self.size])
        for i in self.cell:
            if guess==True and self.cell[i]["guess"]!="null" and self.cell[i]["guess"]!="-":
                fig[i//self.size,i%self.size]=self.cell[i]["guess"]
            else:
                fig[i//self.size,i%self.size]=self.cell[i]["main"]
                
        print(fig)


#TODO: make the '0' as 'x' in game print
#TODO: add comments



game=Snail(5,{(0,1):1,(2,2):3,(2,4):2,(4,1):2,(4,3):3}) # 1
#game=Snail(5,{(2,0):1,(3,2):2,(4,2):3}) # 2
#game=Snail(5,{(0,2):1,(1,1):2,(4,3):3}) # 3 not solved add new function for 2 cells ahead guess update 
#game=Snail(5,{(3,0):1,(2,2):3}) # 4 not solved

#game=Snail(5,{(0,1):1,(1,4):2}) # error
n=0
game.update_main()
while(game.Change and n<5):
    n+=1
    #import pdb;pdb.set_trace()
    game.Change=False
    game.update_path()
    game.update_rev_path()
    game.update_fill_para()
    game.update_guesses()
    game.update_fill()
    game.update_guesses()
    game.update_single_guess()
    game.update_guesses()
    game.p(True)
    
    print("")
