#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 13:56:28 2021

@author: brieuc
"""

import binarytree as bt

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
    x = liste[0].prob
    y = liste[1].prob
    n1 = liste[0]
    n2 = liste[1]
    l=[]
    for i in range(2, n):
        if(liste[i].prob < x):
            l.append(n1)
            x = liste[i].prob
            n1 = liste[i]
        elif (liste[i].prob < y):
            l.append(n2)
            y = liste[i].prob
            n2 = liste[i]
        else:
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
   return (cwd,lgth)


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



