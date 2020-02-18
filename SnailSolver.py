import numpy as np

class Snail:

    def __init__(self,size,main):
        self.size=(size,size)
        self.MAIN_CELL=main
        self.fill_cell={}
        self.cell={}
        self.fill_list=np.zeros([2,self.size[0]])
        self.empty_list=np.ones([2,self.size[0]])*self.size[0]
        for i in range(self.size[0]*self.size[1]):
            if (i//self.size[0],i%self.size[0]) in self.MAIN_CELL:
                self.cell[i]={"main":self.MAIN_CELL[(i//self.size[0],i%self.size[0])],"guess":"null","fill":False}
            else:
                self.cell[i]={"main":-1,"guess":"-123","fill":False}
            
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

    def update_main(self):
        for main in self.MAIN_CELL:
            #
            self.fill_cell[main[0]*self.size[0]+main[1]]=self.MAIN_CELL[main]
            self.fill_list[0,main[0]]+=1
            self.fill_list[1,main[1]]+=1
            self.empty_list[0,main[0]]-=1
            self.empty_list[1,main[1]]-=1
            #
            for i in self.cell:
                if (i//self.size[0]==main[0] or i%self.size[0]==main[1]):
                    self.cell[i]["guess"]=self.cell[i]["guess"].replace(str(self.MAIN_CELL[main]),"")

    #def update_value(self):

    def update_fill_para(self):
        emy=[]
        # for i in self.fill_cell.keys():
        #     self.fill_list[0,i//self.size[0]]+=1
        #     self.fill_list[1,i%self.size[0]]+=1
        emy=self.empty_list+self.fill_list
        for i in range(len(emy[0])):
            if emy[0,i]==3:    
                for j in range(self.size[0]):
                    self.cell[i*5+j]["fill"]=True
        for i in range(len(emy[1])):
            if emy[1,i]==3:
                for j in range(self.size[1]):
                    self.cell[j*5+i]["fill"]=True

    def update_fill(self):
        for j in self.fill_cell:
            for i in self.cell:
                    if (i//self.size[0]==j//self.size[0] or i%self.size[0]==j%self.size[0]):
                        self.cell[i]["guess"]=self.cell[i]["guess"].replace(str(self.fill_cell[j]),"")       
        
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
                    self.empty_list[0,(pos-1)//self.size[0]]-=1
                    self.empty_list[1,(pos-1)%self.size[0]]-=1
                else:
                    list_remove=['1','2','3']
                    list_remove.remove(str(order))
                    for k in list_remove:
                        self.cell[pos-1]["guess"]=self.cell[pos-1]["guess"].replace(k,'')
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
                    self.empty_list[0,(pos-1)//self.size[0]]-=1
                    self.empty_list[1,(pos-1)%self.size[0]]-=1
                else:
                    list_remove=['1','2','3']
                    list_remove.remove(str(order))
                    for k in list_remove:
                        self.cell[pos-1]["guess"]=self.cell[pos-1]["guess"].replace(k,'')


    def update_guesses(self):
        for i in self.cell:
            if (self.cell[i]["guess"]=="-"):
                self.cell[i]["guess"]="null"
                self.cell[i]["main"]=0
                self.empty_list[0,i//self.size[0]]-=1
                self.empty_list[1,i%self.size[0]]-=1
            #pdb.set_trace()
            if self.cell[i]["fill"]==True and len(self.cell[i]["guess"].replace('-',''))==1:
                self.cell[i]['main']=int(self.cell[i]["guess"].replace('-',''))
                self.cell[i]['guess']='null'
                self.empty_list[0,i//self.size[0]]-=1
                self.empty_list[1,i%self.size[0]]-=1
                self.fill_cell[i]=self.cell[i]['main']
                self.fill_list[0,i//self.size[0]]+=1
                self.fill_list[1,i%self.size[0]]+=1

    def p(self,guess=False):
        fig=np.ones(self.size)
        for i in self.cell:
            if guess==True and self.cell[i]["guess"]!="null" and self.cell[i]["guess"]!="-":
                fig[i//self.size[0],i%self.size[0]]=self.cell[i]["guess"]
            else:
                fig[i//self.size[0],i%self.size[0]]=self.cell[i]["main"]
                
        print(fig)
#TODO: make the size in all tuple to change from size[0]to size[1]
#game=Snail(5,{(0,1):1,(2,2):3,(2,4):2,(4,1):2,(4,3):3}) # 1
#game=Snail(5,{(2,0):1,(3,2):2,(4,2):3}) # 2 not solved 
game=Snail(5,{(0,2):1,(1,1):2,(4,3):3}) # 3 not solved row only possible. two rows two col posible 

#game=Snail(5,{(3,0):1,(2,2):3})

#game=Snail(5,{(0,1):1,(1,4):2})

game.update_main()
for i in range(5):
    pdb.set_trace()
    game.update_path()
    game.update_rev_path()
    game.update_fill_para()
    game.update_guesses()
    game.update_fill()
    game.update_guesses()
    game.update_fill_para()
    game.p(True)
