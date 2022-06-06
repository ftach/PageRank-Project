# -*- coding: utf-8 -*-
"""
Module contenant les tests des sous programmes de la méthode creuse.
"""


import entrees, sorties, math
import methode_c as mc


def test_calculer_distance():

    assert mc.calculer_distance({(0, 0): 1, (0, 1): 3}, {(0, 0): 2, (0, 1): 5}) == 2 
    assert mc.calculer_distance({(0, 0): -1, (0, 1): 3}, {(0, 0): 5, (0, 1): 5}) == 6 


def test_dict_de_dict():

    assert mc.dict_de_dict({(0, 0): 1, (1, 0): 2}) == {0: {0: 1}, 1: {0: 2}} # matrice avec le nombre de lignes en clé
    assert mc.dict_de_dict({(0, 0): 1, (1, 0): 2}, False) == {0: {0: 1, 1: 2}} # matrice avec le nombre de colonnes en clé


def test_produit_rapide():

    #assert mc.produit_rapide({0: {0: 1, 1: 1}, 1: {0: 2}}, {0: {0: 2, 1: 1}, 1: {0: 4, 1: 1}}) == {(0, 0): 10, (0, 1): 3, (1, 0): 2, (1, 1): 1} # matrice 2x2 fois matrice 2x2 
    assert mc.produit_rapide({0: {0: 1}, 1: {0: 2}}, {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}}) == {(0, 0): 7, (0, 1): 10} # matrice 1x2 fois matrice 2x2 
    #assert mc.produit_rapide({0: {0: 1}, 1: {0: 2}}, {0: {0: 3}, 1: {0: 4}}) == {(0, 0): 11} # matrice 1x2 fois matrice 2x1
    # on ne teste pas les matrices nulles


def test_somme_speciale():
    
    assert mc.somme_speciale({(0, 0): 1, (0, 1): 2, (1, 0): 5, (1, 1): 0}, {(0, 0): 1, (0, 1): 2, (1, 0): 5, (1, 1): 0}, 2) == {(0, 0): 3, (0, 1): 4, (1, 0): 7, (1, 1): 2} # matrice matrice dont on souhaite garder toutes les coordonnées = matrice dont on souhaite récupérer la valeur de chaque coefficient
    assert mc.somme_speciale({(0, 0): 1, (0, 1): 2, (1, 0): 5, (1, 1): 0}, {(0, 0): 1, (0, 1): 2}, 2) == {(0, 0): 3, (0, 1): 4, (1, 0): 2, (1, 1): 2} # matrice matrice dont on souhaite garder toutes les coordonnées != matrice dont on souhaite récupérer la valeur de chaque coefficient


def test_calculer_h():
    
    # Test sujet.net
    infos_graphe = entrees.det_infos_graphe('sujet.net')
    assert mc.calculer_h(infos_graphe[0], infos_graphe[2], 0.85) == {0: {1: 0.85*0.5, 2: 0.85*0.5}, 2: {0: 0.85*0.3333333333333333, 1: 0.85*0.3333333333333333, 4: 0.85*0.3333333333333333}, 3: {4: 0.85*0.5, 5: 0.85*0.5}, 4: {3: 0.85*0.5, 5: 0.85*0.5}, 5: {3: 0.85*1.0}}


def test_calculer_pi_final():
    
    # Test sujet.net 
    infos_graphe = entrees.det_infos_graphe('sujet.net')
    vrai_pi = sorties.recuperer_pi('sujet_prof.pr', 'sujet_prof.prw', 'C')
    pi_a_tester = mc.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[2], infos_graphe[3], 150, 0, infos_graphe[4])
    for (i, j) in vrai_pi:
        assert math.isclose(vrai_pi[(i, j)], pi_a_tester[(i, j)], rel_tol=1e-08) == True
        
    # Test worm.net
    infos_graphe = entrees.det_infos_graphe('worm.net')
    vrai_pi = sorties.recuperer_pi('worm_prof.pr', 'worm_prof.prw', 'C')
    pi_a_tester =  mc.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[2], infos_graphe[3], 150, 0, infos_graphe[4])
    for (i, j) in vrai_pi:
        assert math.isclose(vrai_pi[(i, j)], pi_a_tester[(i, j)], rel_tol=1e-08) == True
        
    # Test sujet3.net avec résultats du groupe A01 
    infos_graphe = entrees.det_infos_graphe('sujet3.net')
    vrai_pi = sorties.recuperer_pi('sujet3_groupeA01.pr', 'sujet3_groupeA01.prw', 'C')
    pi_a_tester = mc.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[2], infos_graphe[3], 150, 0, infos_graphe[4])
    for (i, j) in vrai_pi:
        assert math.isclose(vrai_pi[(i, j)], pi_a_tester[(i, j)], rel_tol=1e-08) == True
        
    # Test sujet6.net avec résultats du groupe A01 
    infos_graphe = entrees.det_infos_graphe('sujet6.net')
    vrai_pi = sorties.recuperer_pi('sujet6_epsilon_groupeA01.pr', 'sujet6_epsilon_groupeA01.prw', 'C')
    pi_a_tester = mc.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[2], infos_graphe[3], 150, 0.001, infos_graphe[4])
    for (i, j) in vrai_pi:
        assert math.isclose(vrai_pi[(i, j)], pi_a_tester[(i, j)], rel_tol=1e-08) == True