# -*- coding: utf-8 -*-
'''Module regroupant les sous-programmes permettant le calcul du vecteur poids à l'aide de la méthode naïve liste de listes (P).
'''


from entrees import recuperer_pages_cibles


def produit(m1, m2):
    ''' Calculer le produit de deux matrices.

    Paramètres
    ----------
    m1: list
        matrice au format liste de listes dont chaque sous-liste correspond à une ligne de la matrice m1
    m2: list  
        matrice au format liste de listes dont chaque sous-liste correspond à une ligne de la matrice m2

    Return
    ---------
    resultat_pdt: list
         résultat du produit matriciel m1 par m2
    '''
    resultat_pdt = [] # Initialiser la matrice qui contiendra le résultat du produit m1 par m2
    
    # Remplir resultat_pdt
    for i in range(len(m1)): # Pour chaque ligne i de m1
        # Remplir la ligne i de resultat_pdt
        ligne_resultat_pdt = [] # Initialiser une liste qui contiendra les éléments d'une ligne de resultat_pdt
        for j in range(len(m2[0])): # Pour chaque colonne j de m2
            element = 0 # Initialiser la nouvelle composante de resultat_pdt
            for k in range(len(m1[0])): # Pour chaque colonne j de m1 
                element += m1[i][k]*m2[k][j] # Incrémenter la composante de resultat_pdt par le produit entre la composante de m1 et de la composante de m2 (le numéro de colonne de la composante de m1 est égal au numéro de ligne de la composante de m2)
            ligne_resultat_pdt.append(element) # Ajouter la nouvelle composante à la ligne de resultat_pdt
        resultat_pdt.append(ligne_resultat_pdt) # Ajouter la ligne i à la matrice resultat_pdt
        
    return resultat_pdt


def somme_cte(m1, c2):
    ''' Calculer la somme d'une matrice à coefficients variables et d'une matrice à coefficients constants.

    Paramètres
    ----------
    m1: list
        matrice à coefficients variables au format liste de listes dont chaque sous-liste correspond à une ligne
    c2: float
        coefficient constant de la deuxième matrice

    Return
    ---------
    resultat_somme: list
        matrice m1 à laquelle on a ajouté le coefficient c2 pour toutes les composantes de m1
    '''
    
    resultat_somme = [] # Initialiser nouvelle matrice qui contiendra le resultat de la somme entre m1 et m2
    # Remplir resultat_somme
    for i in range(len(m1)): 
        resultat_somme.append([round(x+c2, 8) for x in m1[i]]) # Ajouter une ligne dont les composantes sont celles de m1 auxquelles on a ajouté c2 et on a arrondi a 10^-8
        
    return resultat_somme


def calculer_distance(m1, m2) -> float:   
    '''
    Calculer la plus grande des distances entre les composantes de deux matrices.

    Paramètres
    ----------
    m1: list
        1ère matrice au format liste de listes dont chaque sous-liste correspond à une ligne 
    m2: list  
        2ème matrice au format liste de listes dont chaque sous-liste correspond à une ligne 

    Return
    ---------
    distance: float
        distance maximale entre les composantes de m1 et m2        
    '''

    distance = 0 # Initialiser distance pour la première composante
    for j in range(len(m1[0])): # Pour chaque colonne j
        if abs(m1[0][j] - m2[0][j]) > distance:   # Si la nouvelle distance calculée est supérieure à l'actuelle distance maximale
            distance = abs(m1[0][j] - m2[0][j])   # Alors Affecter à distance la valeur de la nouvelle distance
                
    return distance 


def remplir_ligne(contenu_graphe, i, r, n, alpha):
    '''Remplir une ligne de la matrice à poids variables avec le bon poids suivant si le numéro de colonne est le numéro d'une page cible ou non. 
    
    Parametres
    ----------
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien)
    i: int
        numéro de la ligne de la matrice à poids variables à remplir  
    r: int
        dernier numéro de la liste "regardée" dans la liste de listes contenu_graphe, permet de continuer à parcourir contenu_graphe dans l'ordre
    n: int  
        nombre de pages
    alpha: float
        pondération ou dumping factor
        
    Return
    ----------
    tuple (l_poids_variables, r) avec: 
        l_poids_variables: list
            ligne i de la matrice à poids variables qu'on a rempli
        r: int
            dernier numéro de la liste "regardée" dans la liste de listes contenu_graphe, permet de continuer à parcourir contenu_graphe dans l'ordre
    '''    
    
    (pages_cibles, r) = recuperer_pages_cibles(contenu_graphe, i, r) # Créer la liste des pages cibles pour cette page origine
    l_poids_variables = [] # Initialiser une liste qui permettra de stocker les valeurs de la ligne i
    poids = 1 / len(pages_cibles) # Calculer le poids de la ligne
    for j in range(n): # j représente le numéro de colonne de la matrice à poids variables
        if j in pages_cibles:  # Si le numéro de colonne est un indice cible (pages vers lesquelles est dirigé le lien partant de la page i)
            l_poids_variables.append(alpha*(poids - (1/n)))  # Alors Attribuer alpha*(poids - (1/n)) à la composante (i, j) 
        else: # Sinon si le numéro de colonne n'est pas indice cible
            l_poids_variables.append((-alpha)/n)  # Alors Attribuer (-alpha)/n à la composante (i, j)
    
    return (l_poids_variables, r)
    

def calculer_g(contenu_graphe, pages_origines, n, alpha): 
    '''Créer la matrice de Google G.

    Paramètres
    ----------
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien) 
    pages_origines: set
        contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), non ordonné
    n: int  
        nombre de pages
    alpha: float
        pondération ou dumping factor

    Return
    ---------
    list
        matrice de Google au format liste de listes, chaque sous-liste correspond à une ligne 
    '''

    m_poids_variables = [] # Initialiser une matrice m_poids_variables qui contiendra tous les poids sauf le coefficient 1/n 
    r = 0 # Initialiser r qui représente le numéro de la liste "regardée" dans la liste de listes contenu_graphe
    for i in range(n): # i représente le numéro de ligne de la matrice à poids variables
        l_poids_variables = [] # Initialiser une liste qui permettra de stocker les valeurs de la ligne i
        if i in pages_origines: # Si la ligne i n'est pas un cul de sac
            (l_poids_variables, r) = remplir_ligne(contenu_graphe, i, r, n, alpha) # Remplir une ligne de la matrice à poids variables avec le bon poids suivant si le numéro de colonne est le numéro d'une page cible ou non.
        else: # Sinon si la ligne i est un cul de sac
            l_poids_variables.extend([0]*n) # Alors Remplir la ligne i de zéros
        m_poids_variables.append(l_poids_variables) # Ajouter chaque ligne de la matrice à poids variables
    
    return somme_cte(m_poids_variables, (1/n)) # Retourner G, résultat de la somme de la matrice à poids variables et de m2 (matrice constante de coefficients 1/n )


def calculer_pi_final(alpha, contenu_graphe, pages_origines, n, k, epsilon):
    '''Calculer le vecteur pi final après interruption du calcul par epsilon ou par k.

    Paramètres
    ----------
    alpha: float
        pondération ou dumping-factor
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien) 
    pages_origines: set
        contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), non ordonné 
    n: int
        nombre de pages dans le graphe
    k: int
        limite supérieure du nombre de termes pi_k calculés
    epsilon: float
        précision maximale qui permet d'interrompre le calcul si les vecteurs pi(k) et pi(k+1) sont suffisamment proches

    Return
    ---------
    pi_suivant : list
        vecteur ligne qui contient le poids de chaque page après interruption du calcul
    '''
    
    g = calculer_g(contenu_graphe, pages_origines, n, alpha) # Calculer G
    pi_precedent = [[(1/n)]*n] # Initialiser le vecteur ligne pi(0)
    pi_suivant = produit(pi_precedent, g)
    i =  1 # Initialiser compteur qui servira d'indice au calcul du vecteur pi

    if epsilon != 0: # Si une valeur pour epsilon a été indiquée en argument de la ligne de commande

        # Alors calculer vecteur pi tant qu'on ne dépasse pas l'indice k ou la précision 
        distance = calculer_distance(pi_suivant, pi_precedent)    # Initialiser la distance entre le vecteur pi suivant et le vecteur pi précédent à 0
        while distance > epsilon and i < k:
            pi = pi_suivant # Garder la valeur du vecteur pi précédent
            pi_suivant = produit(pi, g)  # Faire le produit du vecteur pi précédent par G pour obtenir vecteur pi suivant 
            distance = calculer_distance(pi, pi_suivant) # Calculer la distance entre le vecteur pi précédent et le suivant
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1

    else: # Si l’on a pas indiqué de valeur pour epsilon en argument de la ligne de commande

        # Alors calculer vecteur pi tant qu'on ne dépasse pas l'indice k
        while i < k:
            pi = pi_suivant # Garder la valeur du vecteur pi précédent
            pi_suivant = produit(pi, g)     # Faire le produit du vecteur pi précédent par G version naïve pour obtenir vecteur pi suivant
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1
            
    print("Le calcul du PageRank s'est arrêté à l'indice", i)  
    return pi_suivant


def sauvegarder_poids(pi_final):
    '''Sauvegarder les valeurs du vecteur pi final. 
    
    Paramètres
    ----------
    pi_final : list
        contient le poids de chaque page après interruption du calcul

    Return
    ---------
    registre_poids : dict
        contient en clef l'indice de la page et en valeur le poids associé
    '''
    
    registre_poids = {} # Initialiser dictionnaire des poids

    # Ranger les poids dans le dictionnaire des poids
    for j in range(len(pi_final[0])):
        registre_poids[str(j)] = pi_final[0][j] # Associer à chaque clé du dictionnaire (indice de chaque page) son poids 

    return registre_poids 