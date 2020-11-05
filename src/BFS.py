import numpy as np
import sys
class Node1():
    def __init__(self, x, y, dist, parent):
        self.x=x
        self.y=y
        self.dist=dist
        self.parent=parent
    def pstring(self):
        return "{%d, %d}"%(self.x, self.y)

M, N = (10, 10)
row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]

def isValid(mat, visited, row, col):
    return row>=0 and row<M and col>=0 and col<M and mat[row][col]==0 and not visited[row][col]

def BFS(mat, i, j, x, y):
    visited = [[False for ind in range(N)] for jnd in range(M)]
    q = list()

    visited[i][j] = True
    q.append(Node1(i, j, 0, None))

    min_dist = sys.maxsize
    node = None

    while(len(q)!=0):
        node = q.pop(0)

        i = node.x
        j = node.y
        dist = node.dist

        if i==x and j==y:
            min_dist = dist
            break

        for k in range(4):
            if isValid(mat, visited, i+row[k], j+col[k]):
                visited[i+row[k]][j+col[k]] = True
                q.append(Node1(i+row[k], j+col[k], dist+1, node))
    if min_dist != sys.maxsize:
        print("The shortest path from source to destination has length %d"%(min_dist))
        printPath(node)
    else:
        print("Destination cannot be reached from source")

def printPath(node):
    if node == None:
        return
    printPath(node.parent)
    print(node.pstring())

def main():
    mat = [
        [ 1, 1, 1, 1, 1, 0, 0, 1, 1, 1 ],
        [ 0, 1, 1, 1, 1, 1, 0, 1, 0, 1 ],
        [ 0, 0, 1, 0, 1, 1, 1, 0, 0, 1 ],
        [ 1, 0, 1, 1, 1, 0, 1, 1, 0, 1 ],
        [ 0, 0, 0, 1, 0, 0, 0, 1, 0, 1 ],
        [ 1, 0, 1, 1, 1, 0, 0, 1, 1, 0 ],
        [ 0, 0, 0, 0, 1, 0, 0, 1, 0, 1 ],
        [ 0, 1, 1, 1, 1, 1, 1, 1, 0, 0 ],
        [ 1, 1, 1, 1, 1, 0, 0, 1, 1, 1 ],
        [ 0, 0, 1, 0, 0, 1, 1, 0, 0, 1 ],
    ]
    graph = [[0, 0, 0, 1, 0, 0],
             [1, 0, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 1],
             [0, 0, 0, 1, 0, 0],
             [0, 1, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 0]
             ]
    BFS(mat, 1, 0, 3, 1)
if __name__=="__main__":
    main()