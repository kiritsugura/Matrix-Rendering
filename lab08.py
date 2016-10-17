
from math3d import *
class Polymesh():
    def __init__(self,filename,scale,trans=None):
        self.verticies=[]
        self.normals=[]
        self.normalvals=[]
        self.uv=[]
        self.faces=[]
        self.textures=[]
        self.materials=[]
        self.colors=[]
        self.transform=trans
        self.children=[]
        self.currentRender=[]
        if filename!=None:
            with open(filename) as f:
                length=None
                index=0
                for line in f:
                    lineSplit=line.split(' ')
                    if line[0:6]=='mtllib':
                        self.read_mtl(lineSplit[1].strip('\n'))
                    if line[0]=='v':
                        self.verticies.append(VectorN(float(lineSplit[1])*scale,float(lineSplit[2])*scale,float(lineSplit[3])*scale,1.0))
                    if line[0:2]=='vn':
                        self.normals.append(VectorN(float(lineSplit[1])*scale,float(lineSplit[2])*scale,float(lineSplit[3])*scale,1.0))
                    if line[0]=='f':
                        if line.count('//')>0:
                            list=[]
                            for item in range(1,len(lineSplit)):
                                items=lineSplit[item].split('//')
                                list.append((int(items[0])-1))
                            self.normalvals.append(int(items[1])-1)
                            self.faces.append(list)
                            print(list)
                            self.colors.append(self.materials[index])
                        elif line.count('/')==0:
                            list=[]
                            for item in range(1,len(lineSplit)):
                                list.append((int(lineSplit[item])-1))
                            self.faces.append(list)
                            self.colors.append(self.materials[index])
                        elif line.count(' ')+1==line.count('/'):
                            list=[]
                            for item in range(1,len(lineSplit)):
                                items=lineSplit[item].split('/')
                                list.append((int(items[0])-1))
                            self.faces.append(list)
                            self.uv.append(int(items[1]-1))
                            self.colors.append(self.materials[index])
                        else:
                            list=[]
                            for item in range(1,len(lineSplit)):
                                items=lineSplit[item].split('/')
                                list.append((int(items[0])-1))
                            self.normalvals.append(int(items[2])-1)
                            self.uv.append(int(items[1])-1)
                            self.faces.append(list)
                            print(list)
                            self.colors.append(self.materials[index])
                    if line[0:6]=='usemtl':
                        index=self.materialIndex(line.split()[1])
                        # print(index)
    def read_mtl(self,filename):
        name,ns,ka,kd,ks,ke,ni,d,illum=None,None,None,None,None,None,None,None,None
        with open(filename) as f:
            for line in f:
                lineSplit=line.split(' ')
                if line[0:6]=='newmtl':
                    name=lineSplit[1].strip('\n')
                if line[0:2]=='Ns':
                    ns=float(lineSplit[1])
                if line[0:2]=='Ka':
                    ka=VectorN(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
                if line[0:2]=='Kd':
                    kd=VectorN(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
                if line[0:2]=='Ks':
                    ks=VectorN(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
                if line[0:2]=='Ke':
                    ke=VectorN(float(lineSplit[1]),float(lineSplit[2]),float(lineSplit[3]))
                if line[0:2]=='Ni':
                    ni=float(lineSplit[1])
                if line[0]=='d':
                    d=float(lineSplit[1])
                # print(line[0:6])
                if line[0:5]=='illum':
                    illum=float(lineSplit[1])
                if illum!=None:
                    self.materials.append(MtlFile(name,ns,ka,kd,ks,ke,ni,d,illum))
                    illum=None
    def getMaterial(self,name):
        for item in self.materials:
            if item.name==name:
                return item
        return None
    def materialIndex(self,name):
        for item in range(len(self.materials)):
            if self.materials[item].name==name:
                return item
        return None
    def render(self,surface,transform):
        index,matLeng=0,0
        total=self.transform*transform
        for item in self.faces:
            plist=[]
            for vert in item:
                row=self.verticies[vert]*total
                plist.append(VectorN(row[0],row[1],row[2]))
            p1=plist[0]-plist[1]
            p2=plist[0]-plist[2]
            if p1.cross(p2)[2]>0:
                list=[]
                for item in range(len(plist)):
                    list.append((plist[item][0],plist[item][1]))
                pygame.draw.polygon(surface,self.colors[index].diffuse*255,list,1)
            index+=1
        for ch in self.children:
            ch.render(surface,total)
    def addDescendent(self,child):
        self.children.append(child)
class MtlFile():
    def __init__(self,name,ns,ka,kd,ks,ke,ni,d,illum):
        self.name=name
        self.specualarPower=ns
        self.ambient=ka
        self.diffuse=kd
        self.specualr=ks
        self.missive=ke
        self.ni=ni
        self.d=d
        self.illum=illum

#todo: other file io stuff.

def pygameCenterMatrix(ww,wh):
    return MatrixN.translate(False,VectorN(ww/2,wh/2,0,0))

if __name__=="__main__":
    pygame.init()

    ww,wh=1200,800
    window=pygame.display.set_mode((ww,wh))
    angle,worldYa=0,0
    startY=0
    Rotating=False
    running=True
    clk=pygame.time.Clock()

    centralMatrix=pygameCenterMatrix(ww,wh)
    sunMatrix=MatrixN.rotate(False,90)*MatrixN.rotateX(False,-90)*MatrixN.rotateY(False,90)
    saturnMatrix=MatrixN.translate(False,VectorN(-300,0,0,0))
    ship1Matrix=MatrixN.rotateX(False,90)*MatrixN.translate(False,VectorN(300,0,0,0))
    ship2Matrix=MatrixN.rotateX(False,90)*MatrixN.translate(False,VectorN(100,0,0,0))
    saum=MatrixN.rotate(False,0)
    sh1um=MatrixN.rotate(False,180)
    sh2um=MatrixN.rotate(False,0)

    saturnUpdate=Polymesh(None,0,saum)
    sh1Update=Polymesh(None,0,sh1um)
    sh2Update=Polymesh(None,0,sh2um)
    saturn=Polymesh('saturn.obj',40.0,saturnMatrix)
    sun=Polymesh('sun.obj',95.0,sunMatrix)
    ship1=Polymesh('ship.obj',12.0,ship1Matrix)
    ship2=Polymesh('ship.obj',8.0,ship2Matrix)

    sun.addDescendent(saturnUpdate)
    sun.addDescendent(sh1Update)
    saturnUpdate.addDescendent(saturn)
    saturn.addDescendent(sh2Update)
    sh2Update.addDescendent(ship2)
    sh1Update.addDescendent(ship1)

    while running:
        elapsed=clk.tick()/1000
        evt=pygame.event.poll()
        if evt.type==pygame.QUIT:
            running=False
        if evt.type==pygame.MOUSEBUTTONDOWN:
            startY=evt.pos[1]
            Rotating=True
        elif evt.type==pygame.MOUSEBUTTONUP:
            Rotating=False
        if Rotating:
            y=pygame.mouse.get_pos()[1]
            ydiff=y-startY
            worldYa=ydiff%360
        angle+=elapsed*100
        if angle>360:
            angle-=360
        worldYTransform=MatrixN.rotateY(False,worldYa)
        trans=MatrixN.rotateY(False,-angle)
        saturnUpdate.transform=MatrixN.rotateX(False,angle)*trans
        sh1Update.transform=trans
        sh2Update.transform=trans
        window.fill((0,0,0))
        sun.render(window,worldYTransform*centralMatrix)
        pygame.display.flip()
    pygame.quit()
