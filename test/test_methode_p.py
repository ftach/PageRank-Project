# -*- coding: utf-8 -*-
'''Module contenant les tests associés aux sous-programmes de la méthode naïve P. '''


import methode_p as mp
import entrees, sorties, math


def test_somme_cte():

    assert mp.somme_cte([[0, 0]], 2) == [[2, 2]] # matrice ligne et coefficient entier
    assert mp.somme_cte([[0], [0]], 3.72) == [[3.72], [3.72]] # matrice colonne et coefficient à virgule
    assert mp.somme_cte([[1, 2], [1, 0]], 1.25) == [[2.25, 3.25], [2.25, 1.25]] # matrice carrée et coefficient à virgule
        

def test_produit():

    assert mp.produit([[1, 2], [1, 0]], [[2, 1], [4, 1]]) == [[10, 3], [2, 1]] # matrice carrée 2x2 fois matrice carrée 2x2
    assert mp.produit([[1, 2]], [[1, 2], [3, 4]]) == [[7, 10]] # matrice ligne 1x2 fois matrice carrée 2x2 
    assert mp.produit([[1, 2]], [[3], [4]]) == [[11]] # matrice ligne 1x2 fois matrice colonne 2x1
    assert mp.produit([[0, 0]], [[0], [0]]) == [[0]] # matrices nulles


def test_calculer_distance(): 
    
    assert mp.calculer_distance([[1, 3]], [[2, 5]]) == 2 # matrices lignes
    assert mp.calculer_distance([[-1, 3]], [[5, 5]]) == 6   # matrices lignes
    

def test_calculer_g(): 
    
    # Test sujet.net
    infos_graphe = entrees.det_infos_graphe("sujet.net")
    assert mp.calculer_g(infos_graphe[0], infos_graphe[1], infos_graphe[3], 0.85) == [[0.025, 0.45, 0.45, 0.025, 0.025, 0.025], 
    [0.16666667, 0.16666667, 0.16666667, 0.16666667, 0.16666667, 0.16666667], 
    [0.30833333, 0.30833333, 0.025, 0.025, 0.30833333, 0.025], 
    [0.025, 0.025, 0.025, 0.025, 0.45, 0.45], 
    [0.025, 0.025, 0.025, 0.45, 0.025, 0.45], 
    [0.025, 0.025, 0.025, 0.875, 0.025, 0.025]]
    

def test_calculer_pi_final():
    
    # Test sujet.net
    vrai_pi = sorties.recuperer_pi('sujet_prof.pr', 'sujet_prof.prw', 'P')
    infos_graphe = entrees.det_infos_graphe("sujet.net")
    pi_a_tester = mp.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    for i in range(len(vrai_pi[0])):
        assert math.isclose(vrai_pi[0][i], pi_a_tester[0][i], rel_tol=1e-05) == True
        
    # Test worm.net
    vrai_pi = sorties.recuperer_pi('worm_prof.pr', 'worm_prof.prw', 'P')
    infos_graphe = entrees.det_infos_graphe("worm.net")
    pi_a_tester = mp.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    for i in range(len(vrai_pi[0])):
        assert math.isclose(vrai_pi[0][i], pi_a_tester[0][i], rel_tol=1e-03) == True

    # Test sujet3.net avec résultats du groupe A01, calcul uniquement avec k
    vrai_pi = sorties.recuperer_pi('sujet3_groupeA01.pr', 'sujet3_groupeA01.prw', 'P')
    infos_graphe = entrees.det_infos_graphe("sujet3.net")
    pi_a_tester = mp.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    for i in range(len(vrai_pi[0])):
        assert math.isclose(vrai_pi[0][i], pi_a_tester[0][i], rel_tol=1e-05) == True
        
    # Test sujet3.net avec résultats du groupe A01, calcul avec k et epsilon 
    vrai_pi = sorties.recuperer_pi('sujet3_epsilon_groupeA01.pr', 'sujet3_epsilon_groupeA01.prw', 'P')
    infos_graphe = entrees.det_infos_graphe("sujet3.net")
    pi_a_tester = mp.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0.001)
    for i in range(len(vrai_pi[0])):
        assert math.isclose(vrai_pi[0][i], pi_a_tester[0][i], rel_tol=1e-05) == True
        
        
def test_sauvegarder_poids():
    
    assert mp.sauvegarder_poids([[1, 2, 3, 4, 5]]) == {'0': 1, '1': 2, '2': 3, '3': 4, '4': 5}
    assert mp.sauvegarder_poids([[0.01, 0.002, 0.0003, 0.00004, 0.000005]]) == {'0': 0.01, '1': 0.002, '2': 0.0003, '3': 0.00004, '4': 0.000005}