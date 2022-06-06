# -*- coding: utf-8 -*-
"""
Module regroupant les sous-programmes permettant de trier et ranger les poids des pages dans des fichiers.
"""

def creer_fichier_poids(nom_fichier, registre_poids, n, alpha, k, epsilon):
    '''Créer le fichier Poids contenant:
    - sur la 1ère ligne: nombre de page alpha k epsilon
    - dans le reste du fichier: les poids classés par ordre décroissant. 

    Paramètres 
    ----------
    nom_fichier: str
        nom du fichier Poids
    registre_poids: dict 
        dictionnaire ayant comme clé l'indice de la page et en valeur le poids associé à cette page
    n: int
        taille du graphe
    alpha: float
        pondération ou dumping-factor
    k: int
        indice du vecteur poids final
    epsilon: float
        précision maximale

    Returns
    ----------
    None
    '''
    nom_fichier = nom_fichier.strip('net') + 'prw'
    ligne1 = str(n) + ' ' + str(alpha) + ' ' + str(k) + ' ' + str(epsilon) + '\n' # Créer chaîne de caractères contenant les paramètres utilisés
    # En ouvrant le fichier Poids en mode write 	
    with open(nom_fichier, 'w') as fichier_poids: 
        fichier_poids.write(ligne1) # Ecrire les paramètres sur 1ère ligne du fichier Poids 
        for poids in sorted(registre_poids.values(), reverse=True): # Pour chaque poids dans le dictionnaire de poids ordonné de manière décroissante
            # Ajouter le poids de la page correspondante sur une ligne du fichier Poids 	
            ligne = str(poids) + '\n'
            fichier_poids.write(ligne)


def creer_fichier_pagerank(nom_fichier, registre_poids, methode):
    '''Créer le fichier PageRank contenant le numéro des pages classées par popularité décroissante.

    Paramètres
    ----------
    nom_fichier: str
        nom du fichier pagerank
    registre_poids: dict 
        dictionnaire ayant comme clé l'indice de la page et en valeur le poids associé à cette page
    methode: str 
        methode choisie pour calculer le poids des pages

    Returns
    ----------
    None
    '''
    nom_fichier = nom_fichier.strip('net') + 'pr'
    with open(nom_fichier, 'w') as fichier_pagerank: 
        for indice, poids in sorted(registre_poids.items(), key=lambda x: x[1], reverse=True): # Pour chaque indice et poids dans le dictionnaire de poids ordonné de manière décroissante
            # On ne reçoit pas les mêmes dictionnaires suivant les méthodes
            if methode == 'C':
                ligne = str(indice[1]) + '\n' # Ajouter l'indice de la page correspondante sur une ligne du fichier PageRank
            elif methode == 'P' or methode == 'N':
                ligne = str(indice) + '\n'
            fichier_pagerank.write(ligne)
            
            
def recuperer_pi(fichier_pr, fichier_prw, methode):
    '''Récupérer le vecteur pi qui est à l'origine de la création des fichiers Pagerank et Poids afin de faire les tests des sous-programmes calculer_pi_final.
    
    Paramètres
    ----------
    fichier_pr: str
        nom du fichier Poids dont on veut comparer le vecteur pi
    fichier_prw: str
        nom du fichier Pagerank dont on veut comparer le vecteur pi    
    methode: str
        méthode utilisée pour calculer pi dans notre test 
    
    Returns
    ----------
    pi: dict (si methode = 'C') ou list (si methode = 'N' ou si methode = 'P') 
        vecteur poids final
    '''
     
    # Récupérer dans une liste les numéros des pages de la manière dont elles ont été rangées dans le fichier Pagerank
    indices_pages = [] 
    with open(fichier_pr, 'r') as f_pr:
        for ligne in f_pr:
            indices_pages.append(ligne.strip())
            
    # Récupérer dans une liste les poids des pages de la manière dont ils ont été rangés dans le fichier Poids
    poids = []
    with open(fichier_prw, 'r') as f_prw:
        for ligne in f_prw:
            poids.append(ligne.strip())
    
    # Récupérer vecteur pi sous sa forme originelle
    if methode == 'C': # Si on réalise le test avec la methode C
        pi = {} # Alors Initialiser pi comme un dictionnaire vide
        # Ranger les poids comme ils l'étaient dans pi ie un vecteur ligne contenant à chaque indice du numéro de page son poids
        for i in indices_pages:
            indice_poids = indices_pages.index(i) + 1
            pi[(0, int(i))] = float(poids[indice_poids])
    else: # Sinon si on réalise le test avec la methode N ou P
        pi = [[0]*len(indices_pages)] # Alors Initialiser pi comme une liste de listes vide
        # Ranger les poids comme ils l'étaient dans pi ie un vecteur ligne contenant à chaque indice du numéro de page son poids
        for i in indices_pages:
            indice_poids = indices_pages.index(i) + 1
            pi[0][int(i)] = float(poids[indice_poids])
           
    
    return pi