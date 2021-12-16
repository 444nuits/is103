#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:56:28 2021

@author: brieuc
"""
import PIL as pil
#import binarytree as bt
import numpy as np

class Node:
    def __init__(self, l=None, r=None, i=0, p=0):
        self.left = l
        self.right = r
        self.prob = p
        self.key = i
        
#tree = Node(l=Node(), r=Node(l=Node(), r=Node(l=Node(), r=Node())))

#p = tree.right.right.left.prob

def pluspetits(liste):
    n = len(liste)
    if(n<2):
        return liste[0]
    x = 2
    y = 2
    n1 = liste[0]
    n2 = liste[1]
    l=[]
    for i in range(0, n):
        if(liste[i].prob < x):
            x = liste[i].prob
            n1 = liste[i]
    for i in range(0, n):
        if(liste[i] != n1):
            if(liste[i].prob < y):
                y = liste[i].prob
                n2 = liste[i]
    for i in range(0, n):
        if(liste[i] != n1 and liste[i] != n2):
            l.append(liste[i])
    return (x, n1, y, n2, l)

def initfloor(liste):
    n = len(liste)
    L = [0]*n
    for i in range(0, n):
        L[i] = Node(i=i, p=liste[i])
    return L

def printtree(tree):
    print(tree.prob, tree.key)
    if(tree.left != None):
        print("gauche")
        printtree(tree.left)
    if(tree.right != None):
        print("droite")
        printtree(tree.right)
        
def huffman_tree(proba):
    tree = Node()
    n = len(proba)
    l=[0]*n
    l=initfloor(proba)
    for i in range (0, n-2):
        liste = l
        x, n1, y, n2, l = pluspetits(liste)
        noeud = Node(l=n1, r=n2, p=x+y)
        l.append(noeud)
        liste = l
    tree.right = l[1]
    tree.left = l[0]
    tree.prob = 1
    return tree


def get_cwd_rec(node, string, L):
    if(node.left != None):
        stringleft = string+ "1"
        get_cwd_rec(node.left, stringleft, L)
    if(node.right != None):
        stringright = string + "0"
        get_cwd_rec(node.right, stringright, L)
    else:
        L.append(string)
    return


def get_cwd(tree):
    L=[]
    string = ""
    get_cwd_rec(tree, string, L)
    return L

"""
def huffman_code(proba):
   tree= huffman_tree(proba)
   cwd= get_cwd(tree)
   lgth=0;
   for i in range(len(cwd)):
       l=len(cwd[i])
       p='tree.'
       for j in range(l):
           if l[j]== '0':
               p+='right.'
           else:
               p+='left.'
       p.append('prob')
       lgth+=l*p
   return (cwd,lgth)"""

def build_proba_list_rec(node, L):
    if(node.left != None):
        build_proba_list_rec(node.left, L)
    if(node.right != None):
        build_proba_list_rec(node.right, L)
    else :
        L.append(node.prob)
    

def build_proba_list(tree):
    L=[]
    build_proba_list_rec(tree, L)
    return L

def huffman_code(proba):
    cwd = get_cwd(huffman_tree(proba))
    l = len(cwd)
    L = build_proba_list(huffman_tree(proba))
    print(cwd, L)
    s = 0
    for i in range(0, l):
        s+= (len(cwd[i]) * L[i])
    return cwd, s/l

#algorithmes necessitant le module "binarytree" permettant d'afficher des arbres
"""
def build_tree_rec(root, node):
    if(node.right != None):
        root.right = bt.Node(node.right.prob)
        build_tree_rec(root.right, node.right)
    if(node.left != None):
        root.left = bt.Node(node.left.prob)
        build_tree_rec(root.left, node.left)
    else :
        root = bt.Node(node.prob)
    return

def prettyprint(tree):
    root = bt.Node(tree.prob)
    build_tree_rec(root, tree)
    print(root)
    
"""

def calcullmax(cwd):
    res=0
    for i in range(len(cwd)):
        if len(cwd[i])>res:
            res=len(cwd[i])
    return res
    
def huffman_tree2(cwd):
    R=[]
    L=[]
    if len(cwd)==1:
        return Node()
    else :
        for j in range(len(cwd)):
            if ((cwd[j][0]) == "1"):
                L.append(cwd[j][1:])
            else :
                R.append(cwd[j][1:])
    return Node(l= huffman_tree2(L), r= huffman_tree2(R))

"""
    elif (len(cwd)==1 and len(cwd[0])==1):
        if cwd[0]==1:
            return Node(l=Node(l=Node(),r=Node()),r=Node())
        else :
            return Node(l=Node(),r=Node(l=Node(),r=Node()))
"""
        
def cwd_detect_rec(node, seq, i):
    if(node.left == None and node.right == None):
        return seq[:i]
    if(seq[i] == "1"):
        return cwd_detect_rec(node.left, seq, i+1)
    if(seq[i] == "0"):
        return cwd_detect_rec(node.right, seq, i+1)

def cwd_detect(tree, seq):
    cwd = cwd_detect_rec(tree, seq, 0)
    return cwd

def get_symb(word, cwd, symb):
    lc = len(cwd)
    for i in range(0, lc):
        if(word == cwd[i]):
            return symb[i]
    print(word, cwd)
    print("word not in cwd")
    return False

def build_string(charL):
    l = len(charL)
    msg = ""
    for i in range(0, l):
        msg += charL[i]
    return msg

def huffman_decode(seq, symb, cwd):
    tree = huffman_tree2(cwd)
    cidx = 0
    Lsymb = []
    lseq = len(seq)
    while(cidx<lseq):
        word = cwd_detect(tree, seq[cidx :])
        cidx += len(word)
        Lsymb.append(get_symb(word, cwd, symb))
    #msg = build_string(Lsymb)
    return Lsymb

def is_in(char, symb):
    l = len(symb)
    for i in range(0, l):
        if(char == symb[i]):
            return True
    return False


#Création des listes proba et symb

def get_symb_list(seq):
    l = len(seq)
    symb = []
    for i in range(0, l):
        if(is_in(seq[i], symb) == False):
            symb.append(seq[i])
    return symb

def get_proba(seq, char):
    s=0
    l = len(seq)
    for i in range(0, l):
        if(seq[i] == char):
            s+=1
    return s/l

def get_probas(seq, symb):
    proba=[]
    lsymb = len(symb)
    for i in range(0, lsymb):
        proba.append(get_proba(seq, symb[i]))
    return proba

#encode de la sequence choisie, symb et cwd a dispositions

def get_index(letter, symb):
    lsymb = len(symb)
    for i in range(0, lsymb):
        if(letter == symb[i]):
            return i
    print(letter)
    print("lettre pas dans symbole")
    return False

def huffman_encode(seq, symb, cwd):
    lseq = len(seq)
    encseq = ""
    for i in range(0, lseq):
        idx = get_index(seq[i], symb)
        encseq += cwd[idx]
    return encseq

seq = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
symb = get_symb_list(seq)
proba = get_probas(seq, symb)

cwd = get_cwd(huffman_tree(proba))
encseq = huffman_encode(seq, symb, cwd)
    
print("message à coder puis decoder :", seq)
print()
print("message encodé avec methode de huffman :", encseq)
print()
print("les probas associées a chaque symbole sont:")
print(symb)
print(proba)
print()
print("le mot de code est :", cwd)
print()
print("on peut decoder le message et le restituer", huffman_decode(encseq, symb, cwd))
print()
#--------------------------------------------------------#

img = list(pil.Image.open('./moon.png').getdata())

histo = np.histogram(img, bins=256)
histo2 = np.histogram(img, bins=255)

def count(histo):
    s=0
    l=len(histo)
    for i in range(0, l):
        s+=histo[i]
    return s

pxlcount = count(histo[0])

clrproba = histo[0]/pxlcount

def get_round(histo):
    l = len(histo)
    L=[]
    for i in range(0, l):
        L.append(round(histo[i]))
    return L

clrsymb = get_round(histo2[1])

clrcwd = get_cwd(huffman_tree(clrproba))
print("encodage...")
new_image_enc = huffman_encode(img, clrsymb, clrcwd)
print("decodage...")
new_image = huffman_decode(new_image_enc, clrsymb, clrcwd)
print("fin")

def build_array(width, height, img):
    IMG = [[0 for i in range(0, width)] for i in range(0, height)]
    for i in range(0, height):
        for k in range(0, width):
            IMG[i][k] = img[i*width + k]
    return IMG

new_image_array = build_array(726, 543, new_image)

new_image_toshow = pil.Image.fromarray(np.array(new_image_array, dtype=np.uint8))
new_image_toshow.save("mymoon.png")

print("sequence encodée dans new_image_enc ")
print("fichier décodé dans mymoon.png")

