# -*- coding: utf-8 -*-
"""
Module contenant les tests du module entrees.
"""


import entrees


def test_det_type():
    
    assert entrees.det_type('a') == "chaîne de caractères" 
    assert entrees.det_type(1) == "nombre entier"   
    assert entrees.det_type(0.01) == "nombre flottant"
    assert entrees.det_type([1, 2, 3]) == "liste"
    assert entrees.det_type({1: 3}) == "dictionnaire"
    assert entrees.det_type((0, 1)) == "tuple"


def test_analyse_commande(): # on ne teste pas de mettre autre chose que des chaîne de caractère en paramètre de det_arguments car elle reçoit sys.argv en paramètre et cela ne peut donner qu'une liste
    
    assert entrees.analyse_commande(['-E', '0.01', '-K', '30', '-N', '-A', '1', 'sujet.net']) == ('N', 'Erreur', 30, 0.01, 'Erreur') # alpha est supérieur ou égal à 1
    assert entrees.analyse_commande(["-A", "-0.5"]) == ('C', 'Erreur', 150, 0, 'Erreur') # alpha est inférieur ou égal à 0
    assert entrees.analyse_commande(["-A", "valeur de alpha"]) == ('C', 'Erreur', 150, 0, 'Erreur') # alpha n'est pas un nombre flottant
    assert entrees.analyse_commande(["-K", "0.4"]) == ('C', 0.85, 'Erreur', 0, 'Erreur') # k n'est pas un nombre entier
    assert entrees.analyse_commande(["-K", "500", "-K", "-10", "-A", "2.5", "-C", "exemple3.txt"]) == ('C', 0.85, 'Erreur', 0, 'Erreur') # k est inférieur ou égal à 0
    assert entrees.analyse_commande(["-E", "-0.03"]) == ('C', 0.85, 150, 'Erreur', 'Erreur') # epsilon est inférieur ou égal à 0
    assert entrees.analyse_commande(["-E", "je suis epsilon"]) ==  ('C', 0.85, 150, 'Erreur', 'Erreur') # epsilon n'est pas un nombre flottant
    assert entrees.analyse_commande(['blablabla.net']) ==  ('C', 0.85, 150, 0, 'Erreur') # le fichier graphe n'existe pas
    assert entrees.analyse_commande(['sujet.net']) == ('C', 0.85, 150, 0, 'sujet.net') # test des valeurs par défaut
    assert entrees.analyse_commande(['-P', '-A', '0.9', '-K', '20', 'sujet.net']) == ('P', 0.9, 20, 0, 'sujet.net') 
    assert entrees.analyse_commande(["sujet3.net", "-E", "0.002", "-N"]) == ("N", 0.85, 150, 0.002, 'sujet3.net')
    assert entrees.analyse_commande(['-N', '-E', '0.0001','-K', '20', '-E', '0.001', '-A', '0.7', '-C', 'sujet.net']) == ('C', 0.7, 20, 0.001, 'sujet.net') # teste si l'ordre des arguments rentrés est bien pris en compte
    
    
def test_det_infos_graphe():
    
    assert entrees.det_infos_graphe('erreur_ligne1.net') == ([], set(), [], 'Erreur')
    assert entrees.det_infos_graphe('erreur_1_seul_numero_de_page.net') == ('Erreur', 'Erreur', ['E', 'e', 'r', 'r', 'r', 'u'], 3)
    assert entrees.det_infos_graphe('erreur_numero_de_page_pas_entier.net') == ('Erreur', 'Erreur', ['E', 'e', 'r', 'r', 'r', 'u'], 3)
    assert entrees.det_infos_graphe('erreur_numero_de_page_trop_grand.net') == ('Erreur', 'Erreur', ['E', 'e', 'r', 'r', 'r', 'u'], 3)

    
def test_recuperer_pages_cibles():
    
    # Test sujet.net 
    infos_graphe = entrees.det_infos_graphe('sujet.net')
    assert entrees.recuperer_pages_cibles(infos_graphe[0], 0, 0) == ([1, 2], 2)
    assert entrees.recuperer_pages_cibles(infos_graphe[0], 1, 2) == ([], 2)
    assert entrees.recuperer_pages_cibles(infos_graphe[0], 2, 2) == ([0, 1, 4], 5)
