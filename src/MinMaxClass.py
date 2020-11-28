class MinMaxNode:
    def __init__(self,label,rank=0):
        self.label = label
        self.rank = rank
        self.children= []
    
    def get_label(self):
        return self.label
    
    def get_children(self):
        return self.children
    def set_rank(self,newRank):
        self.rank = newRank
    def addChild(self,label):
        c = self.checkIfChildExists(label)
        if c==False:
            x=MinMaxNode(label)
            self.children.append(x)
            return x
        return c
    def checkIfChildExists(self,label):
        for c in self.children:
            if c.label==label:
                return c
        return False
    def __str__(self, level=0):
        if level%2==0:
            c="Attacker"
        else:
            c="Defender"
        ret = "\t"*level+repr(self.label)+"("+repr(self.rank)+")-"+c+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        ret+="\n"
        return ret

    def __repr__(self):
        return '<tree node representation>'
    def isLeaf(self):
        if len(self.children)==0:
            return True
        return False


class MinMaxTree:
    def __init__(self,label):
        self.root = MinMaxNode(label)

