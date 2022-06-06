# -*- coding: utf-8 -*-
'''Module regroupant les sous-programmes permettant le calcul du vecteur poids à l'aide de la méthode creuse (C).
'''


from entrees import recuperer_pages_cibles



def calculer_distance(m1, m2):
    '''Calculer la plus grande des distances entre les composantes de deux matrices. 
    
    Paramètres
    ----------
    m1: dict   
        1ère matrice au format dictionnaire 'simple' {(i1, j1): v11, ..., (in, jn): vnn}
    m2: dict
        2ème matrice au format dictionnaire 'simple' {(i1, j1): v11, ..., (in, jn): vnn}
    
    Return
    ---------
    distance: float
        distance maximale entre les composantes de m1 et m2
    '''
    
    distance = 0 # Initialiser la distance entre les deux matrices 
    for j in range(len(m1)):
        if abs(m1[(0, j)] - m2[(0, j)]) > distance: # Si la distance de la composante suivante est supérieure à l'actuelle distance maximale
            distance = abs(m1[(0, j)] - m2[(0, j)]) # Alors distance prend la valeur de la distance de la composante 
            
    return distance
    

def dict_de_dict(m_simple, ligne=True):
    '''Transformer une matrice au format dictionnaire 'simple' en une matrice au format dictionnaire de dictionnaires.
    
    Paramètres 
    ----------
    m_simple: dict
        matrice au format dictionnaire 'simple' {(i1, j1): v11, ..., (in, jn): vnn}
    ligne: bool optionnel
        format voulu pour le dictionnaire de dictionnaire: False pour avoir les numéros de colonne en clé et True pour avoir les numéros de ligne en clé
    
    Return
    ----------
    m_dict_de_dict: dict
        matrice au format dictionnaire de dictionnaires {i1: {j1: v11, ..., jn: v1n}, ..., in: {j1: vn1, ..., jn: vnn}} ou {j1: {i1: v11, ..., in: v1n}, ..., jn: {i1: vn1, ..., in: vnn}}
    '''

    m_dict_de_dict = {} # Initialiser la matrice transformée en dictionnaire de dictionnaires
    
    if ligne == True: # Si on veut le numéro de ligne comme clé du dictionnaire m_dict_de_dict
    
        # Alors Remplir le dictionnaire pour qu'il ai i en clé, le format {i1: {j1: v11, ..., jn: v1n}, ..., in: {j1: vn1, ..., jn: vnn}}
        for (i, j), v in m_simple.items():
            if i not in m_dict_de_dict: # Si la clé ligne n'a pas déjà été ajoutée au dictionnaire
                m_dict_de_dict[i] = {j: v} # Alors la créer et lui donner en valeur un dictionnaire ayant pour clés les numéros de colonne des coefficients non nuls de cette ligne
            else: # Sinon si la clé ligne a déjà été ajoutée au dictionnaire
                m_dict_de_dict[i][j] = v # Alors donner en valeur à cette clé ligne un dictionnaire ayant pour clés les numéros de colonne des coefficients non nuls de cette ligne
    
    else: # Sinon si on veut le numéro de colonne comme clé du dictionnaire m_dict_de_dict
        
    # Alors Remplir le dictionnaire pour qu'il ai j en clé :le format {j1: {i1: v11, ..., in: v1n}, ..., jn: {i1: vn1, ..., in: vnn}}
        for (i, j), v in m_simple.items():
            if j not in m_dict_de_dict: # Si la clé colonne n'a pas déjà été ajoutée au dictionnaire
                m_dict_de_dict[j] = {i: v} # Alors la créer et lui donner en valeur un dictionnaire ayant pour clés les numéros de ligne des coefficients non nuls de cette colonne
            else:  # Sinon si la clé colonne a déjà été ajoutée au dictionnaire
                m_dict_de_dict[j][i] = v # Alors donner en valeur à cette clé colonne un dictionnaire ayant pour clés les numéros de ligne des coefficients non nuls de cette ligne
    
    return m_dict_de_dict


def produit_rapide(m_colonne, m_ligne):
    '''Calculer rapidement le produit de deux matrices.

    Paramètres
    ----------
    m_colonne: dict
        matrice au format dictionnaire de dictionnaires et avec les numéros de colonne en clé {j1: {i1: v11, ..., in: v1n}, ..., jn: {i1: vn1, ..., in: vnn}}
    m_ligne: dict
        matrice au format dictionnaire de dictionnaires et avec les numéros de ligne en clé {i1: {j1: v11, ..., jn: v1n}, ..., in: {j1: vn1, ..., jn: vnn}}
        
    Return
    ----------
    resultat_pdt: dict
        produit de m1 et m_ligne au format dictionnaire 'simple' {(i1, j1): v11, ..., (in, jn): vnn}
    '''
    
    resultat_pdt = {} # Initialiser matrice qui contiendra le résultat du produit m_colonne fois m_ligne
    
    # Multiplier entre eux les composantes de m_colonne et de m_ligne pour lesquels le numéro de colonne de m_colonne est égal au numéro de ligne de m_ligne
    for k, v in m_colonne.items():
        if k in m_ligne: # Si le numéro de colonne de m_colonne est aussi un numéro de ligne pour m_ligne
            # Alors Multiplier entre eux les composantes de m_colonne et de m_ligne pour donner la composante (i,j) de la nouvelle matrice résultat
            for v1 in v.values(): 
                for j, v2 in m_ligne[k].items(): 
                    if (0, j) in resultat_pdt: # Si la clé (i, j) est déjà dans la matrice résultat
                        resultat_pdt[(0, j)] += v1 * v2 # Alors Ajouter v1 * v2 à cette clé
                    else: # Sinon si la clé (i, j) n'est pas déjà dans la matrice résultat
                        resultat_pdt[(0, j)] = v1 * v2 # Alors Créer la clé (i, j) et lui attribuer v1 * v2 comme valeur

    return resultat_pdt


def somme_speciale(m_forme, m_creuse, coef_constant):
    '''Calculer la somme d'une matrice creuse à coefficients variables et d'une matrice pleine à coefficients constants.
    
    Paramètres
    ----------
    m_forme: dict
        matrice au format dictionnaire 'simple' dont on souhaite garder toutes les coordonnées (clés) ie la forme pleine
    m_creuse: dict
        matrice creuse au format dictionnaire 'simple' dont on souhaite récupérer la valeur de chaque coefficient
    coef_constant: float
        coefficient de la matrice pleine à coefficients constants
        
    Return
    ----------
    resultat_somme: dict
        matrice au format dictionnaire 'simple' contenant le résultat de la somme de la matrice creuse à coefficients variables et de la matrice pleine à coefficients constants'''

    resultat_somme = {} # Initialiser la matrice qui contiendra le résultat de la somme
    
    # Faire la somme 
    for (i, j) in m_forme.keys():
        if (i, j) in m_creuse: # Si la cordonnée de la matrice forme est présente dans la matrice creuse
            resultat_somme[(i, j)] = m_creuse[(i, j)] + coef_constant # Alors ajouter le coefficient de la matrice creuse et le coefficient constant de la matrice pleine
        else: # Sinon si la cordonnée de la matrice forme n'est pas présente dans la matrice creuse
            resultat_somme[(i, j)] = coef_constant # Ajouter juste le coefficient (puisque le coefficient de la matrice creuse vaut alors 0)
    
    return resultat_somme


def calculer_h(contenu_graphe, liste_pages_origine, alpha):
    '''Créer la matrice H creuse.
    
    Paramètres
    ----------
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien) 
    liste_pages_origine: list
        contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), ordonnées dans l'ordre croissant

    Return
    ---------
    h: dict
        matrice H creuse au format dictionnaire 'simple'
    '''
    
    h = {} # Initialiser h comme un dictionnaire
    r = 0 # Initialiser r qui représente le numéro de la liste "regardée" dans la liste de listes contenu_graphe
    for indice_origine in liste_pages_origine:
        h[indice_origine] = {} # Créer un sous-dictionnaire pour chaque numéro de page origine
        (pages_cibles, r) = recuperer_pages_cibles(contenu_graphe, indice_origine, r) # Récupérer, en lisant les lignes du fichier graphes, la liste des pages cibles pour le numéro de page origine indice_origine.

        # Remplir le sous-dictionnaire pour la ligne indice_origine
        if len(pages_cibles) > 0: # Si la ligne de H n'est pas un cul-de-sac
            # Alors remplir la ligne avec le poids de la ligne aux bonnes coordonnées
            poids = 1 / len(pages_cibles) # Calculer le poids de la ligne
            # Attribuer le poids à chaque numéro de colonne qui est un numéro de page cible
            for j in pages_cibles: 
                h[indice_origine][j] = alpha*poids
                #h[(indice_origine, j)] = alpha*poids
    return h

                    
def calculer_ieme_pi(pi_precedent, h, n, alpha, ens_lignes_nulles):
    '''Calculer le ième vecteur pi 
    
    Parametres
    ----------
    pi_precedent: dict
        vecteur pi d'indice i-1 au format dictionnaire 'simple' 
    h: dict
        matrice h creuse au format dictionnaire 'simple' 
    n: int 
        nombre de pages du fichier graphe et nombre de colonne du vecteur pi 
    alpha: float
        pondération ou dumping-factor
    lignes_non_nulles: set
        contient le numéro des pages cul-de-sac et donc des lignes nulles de H
        
    Return
    ----------
    dict: 
        ième vecteur pi au format dictionnaire 'simple'
    '''
    
    pi_h = produit_rapide(dict_de_dict(pi_precedent, False), h) # Faire le produit du vecteur pi par H pour obtenir vecteur pi*H en format dictionnaire simple 
    poids_ligne_nulle = sum([pi_precedent[(0, x)] for x in range(n) if x in ens_lignes_nulles]) # Calculer la somme des poids pour chaque poids d'indice i avec i n'appartenant pas a lignes_non_nulles    
    c = (alpha/n)*poids_ligne_nulle + ((1-alpha)/n) # Calculer coefficient constant qu'on ajoutera à alpha*pi*H
    
    return somme_speciale(pi_precedent, pi_h, c) # renvoyer vecteur pi_k+1 égal à la somme spéciale de pi_h et du coefficient constant c


def calculer_pi_final(alpha, contenu_graphe, liste_pages_origine, n, k, epsilon, ens_lignes_nulles):
    '''Calculer vecteur pi final après interruption du calcul par epsilon ou par k.

    Paramètres
    ----------
    alpha: float
        pondération ou dumping-factor
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien) 
    set_lignes_non_nulles: set
        contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), non ordonné 
    liste_pages_origine: list
        contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), ordonné dans l'ordre croissant
    n: int
        nombre de pages dans le graphe
    k: int
        limite supérieure du nombre de termes pi_k calculés
    epsilon: float
        précision maximale qui permet d'interrompre le calcul si les vecteurs pi(k) et pi(k+1) sont suffisamment proches
    
    Return
    ----------
    dict
        vecteur poids final au format dictionnaire 'simple' 
    '''

    # Initialiser les constantes utiles aux calculs des vecteurs pi
    h = calculer_h(contenu_graphe, liste_pages_origine, alpha)# Créer H en version dictionnaire de dictionnaires {i1: {j1: v11, ..., jn: v1n}, ..., in: {j1: vn1, ..., jn: vnn}}
    pi_precedent = {(0, j): (1/n) for j in range(n)} # Initialiser le vecteur ligne pi_0 sous forme de dictionnaire de dictionnaire
    pi_suivant = calculer_ieme_pi(pi_precedent, h, n, alpha, ens_lignes_nulles) # calculer pi_1
    i = 1 # Initialiser compteur
    
    # Calculer vecteur pi jusqu'à interruption
    if epsilon != 0: 	
        distance = calculer_distance(pi_precedent, pi_suivant) # Initialiser distance 
        while distance > epsilon and i < k: 
            pi_precedent = pi_suivant # Garder la valeur du vecteur pi précédemment calculé
            pi_suivant = calculer_ieme_pi(pi_precedent, h, n, alpha, ens_lignes_nulles) # Calculer ième vecteur pi 
            distance = calculer_distance(pi_precedent, pi_suivant) # Calculer la distance entre le vecteur pi précédent et le suivant 
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1
    else: # Si l’on a pas indiqué de précision maximale en argument de la ligne de commande
        # progressions = [x for x in range(101) if x % 10 == 0]
        while i < k: 
            pi_precedent = pi_suivant # Garder la valeur du vecteur pi précédemment calculé
            pi_suivant = calculer_ieme_pi(pi_precedent, h, n, alpha, ens_lignes_nulles) # Calculer ième vecteur pi
            print("Loading ", round((i/k)*100), " %", end='\r')
            i += 1
            
    print("Le calcul du PageRank s'est arrêté à l'indice", i)      
    return pi_suivant