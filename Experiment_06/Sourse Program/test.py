import sys
import test01_ui
from PyQt5.QtWidgets import QApplication, QDialog,QMessageBox
import requests
import time
import math
import random

NULL = -1
minColumn = 0
maxColumn = 2
minRow = 0
maxRow = 2
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

DFS=0
BFS=1
BestFirstSearch=2
BranchAndBound=3

class node:
    def __init__(self, e):
        self.element = e
        self.leftnode = NULL
        self.rightnode = NULL


class BST:
    def __init__(self):
        self.root = NULL
        self.num = 0

    def insert(self, n, e):
        self.num += 1
        if n == NULL:
            return node(e)
        else:
            if e - n.element < -0.0001:
                n.leftnode = self.insert(n.leftnode, e)
            else:
                n.rightnode = self.insert(n.rightnode, e)
            return n

    def search(self, n, e):
        if n == NULL:
            return False
        if e - n.element > -0.0001 and e - n.element < 0.0001:
            return True
        if e - n.element < -0.0001:
            return self.search(n.leftnode, e)
        if e - n.element > 0.0001:
            return self.search(n.rightnode, e)


def new_state(eight_puzzle_state, dir, global_StateID, type=1):
    temp = eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c]
    if dir == LEFT:
        if eight_puzzle_state.c - 1 < minColumn:
            return False
        else:
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = \
                eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c - 1]
            eight_puzzle_state.c -= 1
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = temp
    if dir == RIGHT:
        if eight_puzzle_state.c + 1 > maxColumn:
            return False
        else:
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = \
                eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c + 1]
            eight_puzzle_state.c += 1
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = temp
    if dir == UP:
        if eight_puzzle_state.r - 1 < minRow:
            return False
        else:
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = \
                eight_puzzle_state.state[eight_puzzle_state.r - 1][eight_puzzle_state.c]
            eight_puzzle_state.r -= 1
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = temp
    if dir == DOWN:
        if eight_puzzle_state.r + 1 > maxRow:
            return False
        else:
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = \
                eight_puzzle_state.state[eight_puzzle_state.r + 1][eight_puzzle_state.c]
            eight_puzzle_state.r += 1
            eight_puzzle_state.state[eight_puzzle_state.r][eight_puzzle_state.c] = temp
    eight_puzzle_state.calculateStateID()
    # if global_StateID.search(global_StateID.root, eight_puzzle_state.stateID):
    #     return False
    # global_StateID.root = global_StateID.insert(global_StateID.root, eight_puzzle_state.stateID)
    if global_StateID[eight_puzzle_state.stateID]==True:
        return False
    global_StateID[eight_puzzle_state.stateID]=True
    if type == 2:
        eight_puzzle_state.calculateF()
    if type == 3:
        eight_puzzle_state.calculate()
        if not eight_puzzle_state.partial:
            return False
    if type == 4:
        eight_puzzle_state.calculateF(4)
    return True


def swap(list):
    p = random.randint(0, len(list) - 1)
    q = random.randint(0, len(list) - 1)
    while p == q:
        q = random.randint(0, len(list) - 1)
    temp = list[p]
    list[p] = list[q]
    list[q] = temp


class eight_puzzle_state:
    def __init__(self):
        self.state = [[],[],[]]
        self.r = 0
        self.c = 0
        self.stateID = 0
        self.next = NULL
        self.parent = NULL
        self.f = 0
        self.h = 0
        self.partial=True
        self.deepth=0

    def random_init(self):
        list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for i in range(0, 100):
            swap(list)
        for i in range(0, 3):
            templist = []
            for j in range(0, 3):
                templist.append(list[j + 3 * i])
                if list[j + 3 * i] == 0:
                    self.r = i
                    self.c = j
            self.state[i][:]=(templist.copy())

    def calculateStateID(self):
        self.stateID = 0
        # for i in range(0, 3):
        #     for j in range(0, 3):
        #         self.stateID += (j + i * 3) * math.exp(self.state[i][j])
        m=1
        for i in range(0,3):
            for j in range(0,3):
                if not j+i*3==0:
                    m*=(j+i*3)
                    self.stateID+=(self.state[i][j]+1)*m




    def check(self):
        flag = True
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] != (i * 3 + j):
                    flag = False
                    break
        return flag

    def calculateF(self,type=1):
        if type==1:
            count = 0
            if self.state[0][0] == 0: count += 1
            if self.state[0][1] == 1: count += 1
            if self.state[0][2] == 2: count += 1
            if self.state[1][0] == 3: count += 1
            if self.state[1][1] == 4: count += 1
            if self.state[1][2] == 5: count += 1
            if self.state[2][0] == 6: count += 1
            if self.state[2][1] == 7: count += 1
            if self.state[2][2] == 8: count += 1
            self.f = self.h + count
        else:
            distance=0
            for i in range(0,3):
                for j in range(0,3):
                    distance+=pow((self.state[i][j]%3)-j,2)+pow((self.state[i][j]//3)-i,2)
            self.f=distance

    def calculate(self):
        p=0
        for i1 in range(0,3):
            for i2 in range(0,3):
                if self.state[i1][i2]==0:
                    continue
                for j2 in range(i2,3):
                    if j2 == i2:
                        continue
                    if self.state[i1][j2] == 0:
                        continue
                    if self.state[i1][j2] < self.state[i1][i2]:
                        p += 1
                if i1==3:
                    pass
                else:
                    for j1 in range(i1+1,3):
                        for j2 in range(0,3):
                            if self.state[j1][j2]==0:
                                continue
                            if self.state[j1][j2]<self.state[i1][i2]:
                                p+=1
        #print(p)
        if p%2==0:
            self.partial=True
        else:
            self.partial=False



class stack:
    def __init__(self):
        self.top = NULL
        self.size = 0

    def push(self, link):
        link.next = self.top
        self.top = link
        self.size += 1

    def pop(self):
        if self.top == NULL:
            return NULL
        else:
            temp = self.top
            self.top = self.top.next
            self.size -= 1
            return temp

    def length(self):
        return self.size


class queue:
    def __init__(self):
        self.front = NULL
        self.rear = NULL
        self.size = 0

    def push(self, link):
        if self.rear == NULL:
            self.rear = link
            self.front = link
            self.size += 1
        else:
            self.rear.next = link
            self.rear = link
            self.size += 1

    def pop(self):
        if self.front == NULL:
            return NULL
        else:
            temp = self.front
            self.front = self.front.next
            self.size -= 1
            if self.front == NULL:
                self.rear = NULL
            return temp

    def length(self):
        return self.size


def DFS_eight_puzzle(ep):
    # global_StateID = BST()
    global_StateID=[False]*1000000
    ep.calculateStateID()
    global_StateID[ep.stateID]=True
    # global_StateID.root = global_StateID.insert(global_StateID.root, ep.stateID)
    s = stack()
    path = []
    s.push(ep)
    while s.length() != 0:
        temp_pop = s.pop()
        if temp_pop.check():
            while temp_pop != ep:
                path.append(temp_pop.state)
                temp_pop = temp_pop.parent
            break
        else:
            for i in range(0, 4):
                temp = eight_puzzle_state()
                temp.state[0][:]=(temp_pop.state[0][:].copy())
                temp.state[1][:]=(temp_pop.state[1][:].copy())
                temp.state[2][:]=(temp_pop.state[2][:].copy())
                temp.r = temp_pop.r
                temp.c = temp_pop.c
                if new_state(temp, i, global_StateID):
                    temp.parent = temp_pop
                    s.push(temp)
    return path


def BFS_eight_puzzle(ep):
    # global_StateID = BST()
    global_StateID = [False] * 1000000
    ep.calculateStateID()
    global_StateID[ep.stateID] = True
    # global_StateID.root = global_StateID.insert(global_StateID.root, ep.stateID)
    s = queue()
    path = []
    s.push(ep)
    while s.length() != 0:
        temp_pop = s.pop()
        if temp_pop.check():
            while temp_pop != ep:
                path.append(temp_pop.state)
                temp_pop = temp_pop.parent
            break
        else:
            for i in range(0, 4):
                temp = eight_puzzle_state()
                temp.state[0][:] = (temp_pop.state[0][:].copy())
                temp.state[1][:] = (temp_pop.state[1][:].copy())
                temp.state[2][:] = (temp_pop.state[2][:].copy())
                temp.r = temp_pop.r
                temp.c = temp_pop.c
                if new_state(temp, i, global_StateID):
                    temp.parent = temp_pop
                    s.push(temp)
    return path

def BoundBFS_eight_puzzle(ep):
    # global_StateID = BST()
    global_StateID = [False] * 1000000
    ep.calculateStateID()
    global_StateID[ep.stateID] = True
    # global_StateID.root = global_StateID.insert(global_StateID.root, ep.stateID)
    s = queue()
    path = []
    ep.calculate()
    if not ep.partial:
        return path
    s.push(ep)
    while s.length() != 0:
        temp_pop = s.pop()
        if temp_pop.check():
            while temp_pop != ep:
                path.append(temp_pop.state)
                temp_pop = temp_pop.parent
            break
        else:
            for i in range(0, 4):
                temp = eight_puzzle_state()
                temp.state[0][:] = (temp_pop.state[0][:].copy())
                temp.state[1][:] = (temp_pop.state[1][:].copy())
                temp.state[2][:] = (temp_pop.state[2][:].copy())
                temp.r = temp_pop.r
                temp.c = temp_pop.c
                if new_state(temp, i, global_StateID,3):
                    temp.parent = temp_pop
                    s.push(temp)
    return path

class Heap:
    def __init__(self):
        self.h = []

    def parent(self, cur):
        return math.floor((cur - 1) / 2)

    def leftchild(self, cur):
        return (cur + 1) * 2 - 1

    def rightchild(self, cur):
        return (cur + 1) * 2

    def length(self):
        return len(self.h)

    def push(self, e):
        self.h.append(e)
        cur = len(self.h) - 1
        par = self.parent(cur)
        while cur > 0:
            if self.h[cur].f >= self.h[par].f:
                break
            else:
                temp = self.h[cur]
                self.h[cur] = self.h[par]
                self.h[par] = temp
                cur = par
                par = self.parent(cur)
        return True

    def pop(self):
        if len(self.h) == 0:
            return NULL
        mine = self.h[0]
        if len(self.h) > 1:
            self.h[0] = self.h.pop()
            cur = 0
            left = self.leftchild(cur)
            right = self.rightchild(cur)
            if right >= len(self.h):
                cur = left
            elif self.h[left].f > self.h[right].f:
                cur = right
            else:
                cur = left
            par = self.parent(cur)
            while cur < len(self.h):
                if self.h[cur].f >= self.h[par].f:
                    break
                else:
                    temp = self.h[cur]
                    self.h[cur] = self.h[par]
                    self.h[par] = temp
                    left = self.leftchild(cur)
                    right = self.rightchild(cur)
                    if left >= len(self.h) and right >= len(self.h):
                        break
                    elif right >= len(self.h):
                        cur = left
                    elif self.h[left].f > self.h[right].f:
                        cur = right
                    else:
                        cur = left
                    par = self.parent(cur)
        else:
            self.h.pop()
        return mine


def BestFS_eight_puzzle(ep):
    # global_StateID = BST()
    global_StateID = [False] * 1000000
    ep.calculateStateID()
    global_StateID[ep.stateID] = True
    # global_StateID.root = global_StateID.insert(global_StateID.root, ep.stateID)
    ep.calculateF()
    s = Heap()
    path = []
    s.push(ep)
    while s.length() != 0:
        temp_pop = s.pop()
        if temp_pop.check():
            while temp_pop != ep:
                path.append(temp_pop.state)
                temp_pop = temp_pop.parent
            break
        else:
            for i in range(0, 4):
                temp = eight_puzzle_state()
                temp.state[0][:] = (temp_pop.state[0][:].copy())
                temp.state[1][:] = (temp_pop.state[1][:].copy())
                temp.state[2][:] = (temp_pop.state[2][:].copy())
                temp.r = temp_pop.r
                temp.c = temp_pop.c
                if new_state(temp, i, global_StateID, 2):
                    temp.parent = temp_pop
                    s.push(temp)
    return path

def BranchFS_eight_puzzle(ep):
    # global_StateID = BST()
    lowerbound=999999
    global_StateID = [False] * 1000000
    ep.calculateStateID()
    global_StateID[ep.stateID] = True
    # global_StateID.root = global_StateID.insert(global_StateID.root, ep.stateID)
    ep.calculateF(4)
    s = Heap()
    path = []
    s.push(ep)
    while s.length() != 0:
        temp_pop = s.pop()
        if temp_pop.deepth>=lowerbound:
            continue
        if temp_pop.check():
            path=[]
            lowerbound=temp_pop.deepth
            while temp_pop != ep:
                path.append(temp_pop.state)
                temp_pop = temp_pop.parent
        else:
            for i in range(0, 4):
                temp = eight_puzzle_state()
                temp.state[0][:] = (temp_pop.state[0][:].copy())
                temp.state[1][:] = (temp_pop.state[1][:].copy())
                temp.state[2][:] = (temp_pop.state[2][:].copy())
                temp.r = temp_pop.r
                temp.c = temp_pop.c
                temp.deepth=temp_pop.deepth+1
                if new_state(temp, i, global_StateID, 4) and temp.deepth<lowerbound:
                    temp.parent = temp_pop
                    s.push(temp)
    return path

test = eight_puzzle_state()
test.random_init()

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = test01_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label_0.setText(str(test.state[0][0]))
        self.ui.label_1.setText(str(test.state[0][1]))
        self.ui.label_2.setText(str(test.state[0][2]))
        self.ui.label_3.setText(str(test.state[1][0]))
        self.ui.label_4.setText(str(test.state[1][1]))
        self.ui.label_5.setText(str(test.state[1][2]))
        self.ui.label_6.setText(str(test.state[2][0]))
        self.ui.label_7.setText(str(test.state[2][1]))
        self.ui.label_8.setText(str(test.state[2][2]))
        test.calculate()
        if not test.partial:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")

    def initial(self):
        self.ui.label_time.clear()
        self.ui.label_time_2.clear()
        test.random_init()
        self.ui.label_0.setText(str(test.state[0][0]))
        self.ui.label_1.setText(str(test.state[0][1]))
        self.ui.label_2.setText(str(test.state[0][2]))
        self.ui.label_3.setText(str(test.state[1][0]))
        self.ui.label_4.setText(str(test.state[1][1]))
        self.ui.label_5.setText(str(test.state[1][2]))
        self.ui.label_6.setText(str(test.state[2][0]))
        self.ui.label_7.setText(str(test.state[2][1]))
        self.ui.label_8.setText(str(test.state[2][2]))
        test.calculate()
        if not test.partial:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")

    def run(self):
        self.ui.label_0.clear()
        self.ui.label_1.clear()
        self.ui.label_2.clear()
        self.ui.label_3.clear()
        self.ui.label_4.clear()
        self.ui.label_5.clear()
        self.ui.label_6.clear()
        self.ui.label_7.clear()
        self.ui.label_8.clear()

        self.ui.label_0.setText(str(test.state[0][0]))
        self.ui.label_1.setText(str(test.state[0][1]))
        self.ui.label_2.setText(str(test.state[0][2]))
        self.ui.label_3.setText(str(test.state[1][0]))
        self.ui.label_4.setText(str(test.state[1][1]))
        self.ui.label_5.setText(str(test.state[1][2]))
        self.ui.label_6.setText(str(test.state[2][0]))
        self.ui.label_7.setText(str(test.state[2][1]))
        self.ui.label_8.setText(str(test.state[2][2]))
        if not test.partial:
            return
        if self.ui.checkBox_dfs.checkState()==1:
            self.dfs(test)
        if self.ui.checkBox_bfs.checkState()==1:
            self.bfs(test)
        if self.ui.checkBox_A.checkState()==1:
            self.A(test)
        if self.ui.checkBox_B.checkState()==1:
            self.branchandbound(test)

    def dfs(self,test):
        time_start=time.time()
        p = DFS_eight_puzzle(test)
        time_end=time.time()
        if len(p) == 0:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")
        else:
            p.reverse()
            process = str(test.state[0][:]) + '\n' + str(test.state[1][:]) + '\n' + str(test.state[2][:]) + '\n' + '\n'
            for i in range(0, len(p)):
                process += str(p[i][0][:]) + '\n' + str(p[i][1][:]) + '\n' + str(p[i][2][:]) + '\n' + '\n'
            self.ui.textEdit.setText(process)
            self.ui.label_time.setText(str(format(time_end-time_start, '.5f'))+" s")
            self.ui.label_time_2.setText(str(len(p)))


    def bfs(self,test):
        time_start = time.time()
        p = BFS_eight_puzzle(test)
        time_end = time.time()
        if len(p) == 0:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")
        else:
            p.reverse()
            process = str(test.state[0][:]) + '\n' + str(test.state[1][:]) + '\n' + str(test.state[2][:]) + '\n' + '\n'
            for i in range(0, len(p)):
                process += str(p[i][0][:]) + '\n' + str(p[i][1][:]) + '\n' + str(p[i][2][:]) + '\n' + '\n'
            self.ui.textEdit.setText(process)
            self.ui.label_time.setText(str(format(time_end - time_start, '.5f')) + " s")
            self.ui.label_time_2.setText(str(len(p)))

    def A(self,test):
        time_start = time.time()
        p = BestFS_eight_puzzle(test)
        time_end = time.time()
        if len(p) == 0:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")
        else:
            p.reverse()
            process = str(test.state[0][:]) + '\n'+str(test.state[1][:]) + '\n'+str(test.state[2][:]) + '\n'+'\n'
            for i in range(0, len(p)):
                process += str(p[i][0][:]) + '\n'+str(p[i][1][:]) + '\n'+str(p[i][2][:]) + '\n'+'\n'
            self.ui.textEdit.setText(process)
            self.ui.label_time.setText(str(format(time_end - time_start, '.5f')) + " s")
            self.ui.label_time_2.setText(str(len(p)))


    def branchandbound(self,test):
        time_start = time.time()
        p = BranchFS_eight_puzzle(test)
        time_end = time.time()
        if len(p) == 0:
            self.ui.label_time.setText("No Solution")
            self.ui.label_time_2.setText("No Solution")
        else:
            p.reverse()
            process = str(test.state[0][:]) + '\n'+str(test.state[1][:]) + '\n'+str(test.state[2][:]) + '\n'+'\n'
            for i in range(0, len(p)):
                process += str(p[i][0][:]) + '\n'+str(p[i][1][:]) + '\n'+str(p[i][2][:]) + '\n'+'\n'
            self.ui.textEdit.setText(process)
            self.ui.label_time.setText(str(format(time_end - time_start, '.5f')) + " s")
            self.ui.label_time_2.setText(str(len(p)))

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())