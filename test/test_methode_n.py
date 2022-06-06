# -*- coding: utf-8 -*-
'''Module contenant les tests des sous programmes de la méthode Numpy.'''


import entrees, sorties
import methode_n as mn
import numpy as np 


def test_calculer_distance(): 
    
    assert mn.calculer_distance(np.array([[1, 2, 3]]), np.array([[2, 3, 5]])) == 2   # matrice ligne
    assert mn.calculer_distance(np.array([[-1, 2, 3]]), np.array([[5, 3, 5]])) == 6   # matrice ligne


def test_calculer_g():
    
    # Test sujet.net
	infos_graphe = entrees.det_infos_graphe('sujet.net')
	assert np.allclose(mn.calculer_g(infos_graphe[0], infos_graphe[1], infos_graphe[3], 0.85), np.array([[0.025, 0.45, 0.45, 0.025, 0.025, 0.025], 
    [0.16666667, 0.16666667, 0.16666667, 0.16666667, 0.16666667, 0.16666667], 
    [0.30833333, 0.30833333, 0.025, 0.025, 0.30833333, 0.025], 
    [0.025, 0.025, 0.025, 0.025, 0.45, 0.45], 
    [0.025, 0.025, 0.025, 0.45, 0.025, 0.45], 
    [0.025, 0.025, 0.025, 0.875, 0.025, 0.025]]))


def test_calculer_pi_final():

    # Test sujet.net
    vrai_pi = np.array(sorties.recuperer_pi('sujet_prof.pr', 'sujet_prof.prw', 'N'))
    infos_graphe = entrees.det_infos_graphe('sujet.net')
    pi_a_tester = mn.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    assert np.allclose(vrai_pi, pi_a_tester) == True
    
    # Test worm.net
    vrai_pi = np.array(sorties.recuperer_pi('worm_prof.pr', 'worm_prof.prw', 'N'))
    infos_graphe = entrees.det_infos_graphe("worm.net")
    pi_a_tester = mn.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    assert np.allclose(vrai_pi, pi_a_tester) == True
    
    # Test sujet3.net avec résultats du groupe A01, calcul uniquement avec k
    vrai_pi = np.array(sorties.recuperer_pi('sujet3_groupeA01.pr', 'sujet3_groupeA01.prw', 'N'))
    infos_graphe = entrees.det_infos_graphe("sujet3.net")
    pi_a_tester = mn.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0)
    assert np.allclose(vrai_pi, pi_a_tester) == True
    
    # Test sujet3.net avec résultats du groupe A01, calcul avec k et epsilon
    vrai_pi = np.array(sorties.recuperer_pi('sujet3_epsilon_groupeA01.pr', 'sujet3_epsilon_groupeA01.prw', 'N'))
    infos_graphe = entrees.det_infos_graphe("sujet3.net")
    pi_a_tester = mn.calculer_pi_final(0.85, infos_graphe[0], infos_graphe[1], infos_graphe[3], 150, 0.001)
    assert np.allclose(vrai_pi, pi_a_tester) == True


def test_sauvegarder_poids():
    
    assert mn.sauvegarder_poids(np.array([[1, 2, 3, 4, 5]])) == {'0': 1, '1': 2, '2': 3, '3': 4, '4': 5}
    assert mn.sauvegarder_poids(np.array([[0.01, 0.002, 0.0003, 0.00004, 0.000005]])) == {'0': 0.01, '1': 0.002, '2': 0.0003, '3': 0.00004, '4': 0.000005}