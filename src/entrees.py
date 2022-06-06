# -*- coding: utf-8 -*-
"""Module regroupant les sous-programmes permettant de récupérer les informations de la ligne de commande et du fichier graphe mais aussi de créer un fichier graphe.
"""


import os, random


def creer_fichier_graphe(nom_fichier, pages, liens_max):
    '''Créer un fichier graphe avec un nombre de pages et un nombre de liens maximum par page choisis. 

    Paramètres
    ----------
    nom_fichier: str
        nom du fichier où est enregistré le graphe, préciser .net
    pages: int
        nombre de pages voulues dans le fichier graphe
    liens_max: int
        nombre maximal de liens voulus par page dans le fichier graphe
        
    Return
    ----------
    None
    '''
    
    with open(nom_fichier, 'w') as graphe: # Ouvrir le fichier graphe en mode écriture
        graphe.write(str(pages)+'\n') # Ecrire le nombre de pages sur la 1ère ligne
        
        # Affecter à chaque page un nombre aléatoire de liens d'indice aléatoire
        for indice_origine in range(pages): # indice_origine représente le numéro de la page origine
            liens = random.randint(0, liens_max) # calculer de manière aléatoire le nombre de liens qu'aura la page i
            # Ecrire ces liens
            j = 0 # Initialiser j qui va permettre de compter le numéro de lien déjà écrit pour chaque page
            while j < liens:
                indice_cible = random.randint(0, pages-1) # calculer de manière aléatoire le numéro de la page cible 
                if indice_cible != indice_origine: # Si le numéro de la page cible est différente de celui de la page origine
                    graphe.write(str(indice_origine) + ' ' + str(indice_cible) + '\n') # Alors écrire le numéro de la page origine et de la page cible sur une ligne du fichier
                    j += 1


class Error(Exception):
    '''Classe de base pour définir nos propres exceptions. 
    '''
    pass


class BadTypeError(Error):
    '''Classe permettant de lever une exception lorsque l'utilisateur entre un objet n'ayant pas le bon type en argument. Créer cette classe permet d'identifier les erreurs spécifiques à notre programme et évite ainsi que les erreurs soient toutes regroupées dans les TypeError. Cela nous a permis d'éliminer les erreurs déjà gérées par cette classe si une TypeError était levée.
    '''
    def __init__(self, message, bad_type):
        self.__message = message
        self.__bad_type = bad_type

    @property
    def message(self):
        return self.__message
    
    @property
    def bad_type(self):
        return self.__bad_type
        

class BadIntervalError(Error):
    '''Classe permettant de lever une exception lorsque l'utilisateur entre un nombre dont la valeur ne respecte pas les conditions du sujet. Créer cette classe permet d'identifier les erreurs spécifiques à notre programme et évite ainsi que les erreurs soient toutes regroupées dans les ValueError. Cela nous a permis d'éliminer les erreurs déjà gérées par cette classe si une ValueError était levée.
    '''

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message


class GraphError(Error):
    '''Classe permettant de lever une exception lorsqu'une ligne du fichier graphe fournit par l'utilisateur ne respecte pas les conditions. Créer cette classe permet d'identifier les erreurs spécifiques à notre programme et évite ainsi que les erreurs soient toutes regroupées dans les ValueError. Cela nous a permis d'éliminer les erreurs déjà gérées par cette classe si une ValueError était levée.
    '''

    def __init__(self, message, numero):
        self.__message = message
        self.__numero = numero
        
    @property
    def message(self):
        return self.__message
    
    @property
    def numero(self):
        return self.__numero


def det_type(mon_objet):
    '''Déterminer le type d'un objet comme pourrait le faire la fonction native type mais en renvoyant un résultat 'plus propre'.
    
    Paramètres
    ----------
    mon_objet: pas de type défini
        nom de l'objet dont on veut déterminer le type
        
    Return
    ----------
    str
        type de l'objet
    '''

    if isinstance(mon_objet, int) == True: 
        return "nombre entier"
    elif isinstance(mon_objet, float) == True: 
        return "nombre flottant"
    elif isinstance(mon_objet, str) == True: 
        return "chaîne de caractères"
    elif isinstance(mon_objet, list) == True: 
        return "liste"
    elif isinstance(mon_objet, dict) == True: 
        return "dictionnaire"
    elif isinstance(mon_objet, tuple) == True: 
        return "tuple"


def analyse_commande(arguments): 
    '''Déterminer la méthode et les paramètres choisis par l'utilisateur qui seront utilisés pour calculer le poids des pages.

    Paramètres
    ----------
    arguments: list
        listes des arguments entrés par l'utilisateur dans la ligne de commande
    
    Return
    ----------
    tuple(methode, alpha, k, epsilon, fichier_graphe) avec:
    methode: str 
        methode choisie pour calculer le poids des pages
    alpha: float
        pondération ou dumping-factor
    k: int
        indice du vecteur poids final
    epsilon: float
        précision maximale
    fichier_graphe: str
        nom du fichier .net contenant le nombre de pages et le graphe des pages web
    '''

    # Définir les valeurs par défaut 
    methode = 'C'
    k = 150
    alpha = 0.85
    epsilon = 0
    fichier_graphe = "Erreur" # par défaut on a pas de fichier graphe choisi
    
    try:
        for i in range(len(arguments)):	
             
            if arguments[i] == '-P' or arguments[i] == '-N' or arguments[i] == '-C': # Si l'argument est une méthode
                methode = arguments[i].replace('-', '') # alors attribuer à la variable methode sa valeur

            elif arguments[i] == '-A':  # Si l'argument est alpha
                # Alors attribuer sa valeur à alpha
                if arguments[i+1].replace('.', '').replace('-', '').isdigit() == False:   # Si alpha n'est pas un nombre 
                    alpha = "Erreur"
                    raise BadTypeError("alpha doit être un nombre flottant, pas un(e)", det_type(arguments[i+1])) # Alors afficher l'erreur et arrêter le programme
                elif float(arguments[i+1]) <= 0 or float(arguments[i+1]) >= 1 : # Si alpha n'appartient pas à ]0;1[   
                    alpha = "Erreur"
                    raise BadIntervalError("alpha doit être compris entre 0 et 1 exclus.")  # Alors afficher l'erreur et arrêter le programme
                else :  # sinon attribuer à la variable alpha sa valeur
                    alpha = float(arguments[i+1])

            elif arguments[i] == '-K':    # si l'argument est k
                # Alors attribuer sa valeur à k
                if arguments[i+1].replace('.', '').replace('-', '').isdigit() == False or arguments[i+1].count('.') > 0:   # si k n'est pas un nombre entier 
                    k = "Erreur"
                    raise BadTypeError("k doit être un nombre entier, pas un(e)", det_type(arguments[i+1])) # alors afficher l'erreur et arrêter le programme   
                elif float(arguments[i+1]) <= 0: # si k est négatif ou nul 
                    k = "Erreur"
                    raise BadIntervalError("k ne peut être négatif ou nul.")  # alors afficher l'erreur et arrêter le programme
                else:   # sinon attribuer à la variable k sa valeur
                    k = int(arguments[i+1])

            elif arguments[i] == '-E' :     # si l'argument est epsilon
                # Alors attribuer sa valeur à epsilon
                if arguments[i+1].replace('.', '').replace('-', '').isdigit() == False:   # si epsilon n'est pas un nombre 
                    epsilon = "Erreur"
                    raise BadTypeError("epsilon doit être un nombre flottant, pas un(e)", det_type(arguments[i+1])) # alors afficher l'erreur et arrêter le programme      
                elif float(arguments[i+1]) < 0:     # si epsilon est négatif 
                    epsilon = "Erreur"
                    raise BadIntervalError("epsilon ne peut être négatif.") # alors afficher l'erreur et arrêter le programme
                else :  # sinon attribuer à la variable epsilon sa valeur 	
                    epsilon = float(arguments[i+1]) 
                    
            elif arguments[-1].endswith('.net') == False:
                raise OSError
                
            elif arguments[i].endswith('.net') == True :    # si l'argument est le nom du fichier graphe
                # Alors attribuer sa valeur à k
                if os.path.isfile(arguments[i]) == False:   # si le fichier graphe n'est pas enregistré dans le chemin donné 
                    raise OSError  # alors afficher l'erreur et arrêter le programme
                else:   # sinon attribuer à la variable fichier_graphe sa valeur
                    fichier_graphe = arguments[i]
                    
    # Gérer les exceptions 
    except BadTypeError as e1:
        print("Programme arrêté à cause d'une erreur dans la ligne de commande:", e1.message, e1.bad_type) # afficher un message adapté à l'erreur
    except BadIntervalError as e2:
        print("Programme arrêté à cause d'une erreur dans la ligne de commande:", e2.message) # afficher un message adapté à l'erreur
    except OSError:
        print("Programme arrêté à cause d'une erreur dans la ligne de commande : le nom du fichier graphe n'existe pas ou le chemin donné n'est pas le bon ou vous n'avez founi aucun nom de fichier.")
    
    finally:  
        return (methode, alpha, k, epsilon, fichier_graphe) 


def det_infos_graphe(fichier_graphe):
    '''Récupérer les lignes du fichier graphe dans une liste de listes, le numéro des pages depuis lesquelles partent des liens et le nombre total de pages du fichier graphe. 

    Paramètres
    ----------
    fichier_graphe: str
        nom du fichier .net contenant le nombre de pages et le graphe des pages web
    
    Return
    ----------
    tuple(contenu_graphe, ens_pages_origines, liste_pages_origines, nombre_pages) avec:
        contenu_graphe: list
            liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien) 
        ens_pages_origines: set
            contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), non ordonné
        liste_pages_origine: list
            contient le numéro de toutes les pages origines (pages depuis lesquelles partent des liens), ordonné dans l'ordre croissant
        nombre_pages: int  
            nombre total de pages du fichier graphe
    '''

    try:
        contenu_graphe = []  # Initialiser la liste contenu_graphe qui contiendra chaque ligne du fichier graphe avec en 1ère position le numéro de la page origine et en 2ème position le numéro de la page cible 
        ens_pages_origines = set() # Initialiser le set ens_pages_origines qui contiendra le numéro de toutes les pages origines
        
        # Ouvrir et récupérer les infos que l'on veut dans le fichier graphe
        with open(fichier_graphe, 'r') as graphe:  # Ouvrir le fichier .net en mode lecture 
            numero_ligne = 0 # Initialiser le numéro de ligne à 0, permettra de repérer à quelle ligne est l'erreur lorsqu'on l'affichera
            for ligne in graphe:
                couple = ligne.strip().split(' ') # Créer une liste qui contient chaque élément de la ligne à une position dans la liste
                if numero_ligne == 0: # Si on a pas encore lu le nombre de pages sur la 1ère ligne du fichier graphe
                    if couple[0].isdigit() == True: # Si on a bien le nombre total de pages sur la 1ère ligne et pas un des numéros de pages origines/cibles à la place
                        nombre_pages = int(couple[0]) # Alors lire le nombre de pages sur la 1ère ligne du fichier graphe
                    else:# Sinon si on a pas le nombre total de pages sur la 1ère ligne
                        nombre_pages = "Erreur"
                        raise GraphError("le nombre total de pages n'est pas un nombre entier ou n'est pas indiqué sur la ligne", numero_ligne+1)
                else: # Sinon si on a déjà lu le nombre de pages
                    if len(couple) != 2: # Si il n'est pas indiqué deux numéros de page sur la ligne
                        ens_pages_origines = "Erreur"
                        contenu_graphe = "Erreur"
                        raise GraphError("il n'y a pas été indiqué un numéro de page origine et un numéro de page cible sur la ligne", numero_ligne+1)
                    elif couple[0].isdigit() == False or couple[1].isdigit() == False: # Sinon si le numéro de page origine et de page cible ne sont pas des nombres entiers
                        ens_pages_origines = "Erreur"
                        contenu_graphe = "Erreur"
                        raise GraphError("le numéro de page origine et/ou de page cible ne sont pas des nombres entiers sur la ligne", numero_ligne+1)
                    elif int(couple[0]) >= nombre_pages or int(couple[1]) >= nombre_pages: # Sinon si le numéro de page origine et/ou de page cible est plus grand que le nombre total de pages
                        ens_pages_origines = "Erreur"
                        contenu_graphe = "Erreur"
                        raise GraphError("le numéro de page origine et/ou de page cible est plus grand que le nombre total de pages du fichier sur la ligne", numero_ligne+1)
                    else: # Sinon si le numéro de page origine et de page cible sont bien des nombres entiers
                        contenu_graphe.append(couple)  # Alors Ajouter les autres lignes à contenu_graphe 
                        ens_pages_origines.add(int(couple[0])) # Et ajouter le numéro des pages origines à ens_pages_origines
                numero_ligne += 1 
        
        contenu_graphe = sorted(contenu_graphe, key=lambda x: int(x[0])) # Ordonner contenu_graphe par ordre de numéro de page origine croissant, servira à remplir H dans l'ordre
        ens_lignes_nulles = {x for x in range(nombre_pages) if x not in ens_pages_origines}
    # Gérer les exceptions pour qu'elles s'affichent lisiblement
    except GraphError as e:
        print("Programme arrêté à cause d'une erreur dans le fichier graphe:", e.message, e.numero)
    
    # Renvoyer le tuple (contenu_graphe, ens_pages_origines, sorted(ens_pages_origines), nombre_pages) dans tous les cas
    finally: 
        return (contenu_graphe, ens_pages_origines, sorted(ens_pages_origines), nombre_pages, ens_lignes_nulles)


def recuperer_pages_cibles(contenu_graphe, indice_origine, r):
    '''Récupérer la liste des pages cibles pour une page origine donnée. 
    
    Parametres
    ----------
    contenu_graphe: list
        liste de listes, chaque sous-liste contient une ligne du fichier graphe avec en 1ère position le numéro de la page origine (page depuis laquelle part le lien) et en 2ème position le numéro de la page cible (page vers laquelle va le lien)
    indice_origine: int
        numéro de la page origine pour laquelle on veut récupérer la liste des pages cibles 
    r: int
        dernier numéro de la liste "regardée" dans la liste de listes contenu_graphe, permet de continuer à parcourir contenu_graphe dans l'ordre
    
    Return
    ----------
    tuple (pages_cibles, r) avec :
        pages_cibles: list
            contient le numéro des pages cibles liées à l'indice origine entré en paramètres
        r: int
            dernier numéro de la liste "regardée" dans la liste de listes contenu_graphe, permet de continuer à parcourir contenu_graphe dans l'ordre
    '''
    
    pages_cibles = [] # Initialiser liste pages_cibles qui contiendra les numéros des pages origines
    
    # Remplir la liste pages_cibles
    while r < len(contenu_graphe) and int(contenu_graphe[r][0]) == indice_origine: 
            if int(contenu_graphe[r][1]) not in pages_cibles: # Si le numéro de page cible n'a pas déjà été ajouté à la liste pages_cibles
                pages_cibles.append(int(contenu_graphe[r][1])) # Alors l'ajouter à la liste pages_cibles
            r += 1
            
    return (pages_cibles, r)