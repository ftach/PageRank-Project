# -*- coding: utf-8 -*-
'''Module regroupant les sous-programmes permettant le calcul du vecteur poids à l'aide de la méthode Numpy.
'''


from entrees import recuperer_pages_cibles
import numpy as np


def calculer_distance(m1, m2):
    '''
    Calculer la plus grande des distances entre les composantes de deux matrices lignes.

    Paramètres
    ----------
    m1: numpy.ndarray
        première matrice ligne
    m2: numpy.ndarray
        deuxième matrice ligne

    Return
    ----------
    distance: float
        distance maximale entre les composantes de m1 et m2
    '''
    
    distance = 0 # Initialiser distance pour la première composante 
    for j in range(np.size(m1, 1)): # Pour chaque colonne j
        if abs(m1[(0, j)] - m2[(0, j)]) > distance:    # Si la distance de la composante suivante est supérieure à l'actuelle distance maximale
            distance = abs(m1[(0, j)] - m2[(0, j)])   # Alors distance prend la valeur de la distance de la composante suivante
    
    return distance


def remplir_ligne(m_poids_variables, contenu_graphe, i, r, n, alpha):
    '''Remplir une ligne de la matrice à poids variables avec le bon poids suivant si le numéro de colonne est le numéro d'une page cible ou non. 
    
    Parametres
    ----------
    m_poids_variables: np.array
        matrice à poids variables dont on veut remplir la ligne i
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
    tuple (m_poids_variables, r) avec: 
        m_poids_variables: np.array
            matrice à poids variables dont on a rempli la ligne i
        r: int
            dernier numéro de la liste "regardée" dans la liste de listes contenu_graphe, permet de continuer à parcourir contenu_graphe dans l'ordre
    '''
        
    (pages_cibles, r) = recuperer_pages_cibles(contenu_graphe, i, r) # Créer la liste des pages cibles pour cette page origine
    poids = 1 / len(pages_cibles) # Calculer le poids de la ligne
    for j in range(n): # j représente le numéro de colonne de la matrice à poids variables
        if j in pages_cibles:  # Si le numéro de colonne est un numéro de page cible 
            m_poids_variables[(i, j)] = alpha*(poids - (1/n))  # Alors Attribuer alpha*(poids - (1/n)) à la composante (i, j) 
        else: # Sinon si le numéro de colonne n'est pas un numéro de page cible 
            m_poids_variables[(i, j)] = (-alpha)/n  # Alors Attribuer (-alpha)/n à la composante (i, j)
    
    return (m_poids_variables, r)


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
    np.array
        matrice de Google G
    '''

    m_poids_variables = np.zeros((n, n)) # Initialiser une matrice m_poids_variables, nulle et de taille n sur n, qui contiendra tous les poids de G sauf le coefficient 1/n 
    r = 0 # Initialiser r qui représente le numéro de la liste "regardée" dans la liste de listes contenu_graphe
    for i in range(n): # i représente le numéro de ligne de la matrice à poids variables
        if i in pages_origines: # Si la ligne i n'est pas un cul de sac
            (m_poids_variables, r) = remplir_ligne(m_poids_variables, contenu_graphe, i, r, n, alpha) # Remplir une ligne de la matrice à poids variables avec le bon poids suivant si le numéro de colonne est le numéro d'une page cible ou non.
# =============================================================================
#         else: # Sinon si la ligne i est un cul de sac
#             m_poids_variables[i, :] = 0 # Alors Remplir la ligne i de zéros
# =============================================================================
    
    return m_poids_variables + (1/n)*np.ones((n, n)) # Retourner G, résultat de la somme de m1 et de m2 (matrice constante de coefficients 1/n )


def calculer_pi_final(alpha, contenu_graphe, pages_origines, n, k, epsilon):
    '''Calculer le vecteur pi final après interruption du calcul par epsilon ou par k.
    
    Paramètres
    -----------
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
    ----------
    pi_suivant: np.array
        vecteur ligne qui contient le poids de chaque page après interruption du calcul
    '''
    
    g = calculer_g(contenu_graphe, pages_origines, n, alpha) # Calculer G
    pi_precedent = (1/n)*np.ones((1, n)) # Initialiser le vecteur ligne pi(0)
    pi_suivant = np.dot(pi_precedent, g) # # Initialiser le vecteur ligne pi(1)
    i = 1 # Initialiser compteur qui servira d'indice au calcul du vecteur pi
    
    if epsilon != 0: # Si une valeur pour epsilon a été indiquée en argument de la ligne de commande
	
        # Alors calculer vecteur pi tant qu'on ne dépasse pas l'indice k ou la précision 
        distance = calculer_distance(pi_precedent, pi_suivant) # Initialiser la distance entre le vecteur pi suivant et le vecteur pi précédent à 0
        while distance > epsilon and i < k:
            pi_precedent = pi_suivant # Garder la valeur du vecteur pi précédent
            pi_suivant = np.dot(pi_precedent, g)     # Faire le produit du vecteur pi précédent par G pour obtenir vecteur pi suivant  
            distance =  calculer_distance(pi_precedent, pi_suivant) # Calculer la distance entre le vecteur pi précédent et le suivant
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1
            
    else: # S'il n'a pas été indiqué de valeur pour epsilon en argument de la ligne de commande
        
    # Alors Calculer pi en prenant en compte k uniquement
        while i < k:
            pi = pi_suivant # Garder la valeur du vecteur pi précédent
            pi_suivant = np.dot(pi, g)   # Faire le produit du vecteur pi précédent par G pour obtenir vecteur pi suivant
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1
    
    print("Le calcul du PageRank s'est arrêté à l'indice", i)  
    return pi_suivant

    
def sauvegarder_poids(pi_final):
    '''Sauvegarder les valeurs du vecteur pi final. 

    Paramètres
    ----------
    pi_final : np.array
        contient le poids de chaque page après interruption du calcul

    Return
    ---------
    registre_poids : dict
        contient en clef l'indice de la page et en valeur le poids associé
        
    '''
    
    registre_poids = {} # Initialiser dictionnaire qui contient en clés l'indice de la page et en valeur associée son poids 

    # Ranger (sans les classer pour l'instant) les poids dans le dictionnaire 
    for j in range(np.size(pi_final, 1)):
        registre_poids[str(j)] = pi_final[(0, j)] # Associer à chaque clé du dictionnaire (indice de chaque page) son poids 
    
    return registre_poids 