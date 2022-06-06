# -*- coding: utf-8 -*-
"""Module contenant les tests du module sorties.
"""


import sorties


def test_recuperer_pi():
    
    # test sujet.net avec méthode C
    assert sorties.recuperer_pi('sujet_prof.pr', 'sujet_prof.prw', 'C') == {(0, 3): 0.3487036852148166, (0, 5): 0.26859608185465605, (0, 4): 0.19990381197331833, (0, 1): 0.07367926270375533, (0, 2): 0.057412412496432724, (0, 0): 0.05170474575702129}
    
    # test sujet.net avec méthode P
    assert sorties.recuperer_pi('sujet_prof.pr', 'sujet_prof.prw', 'P') == [[0.05170474575702129, 0.07367926270375533, 0.057412412496432724, 0.3487036852148166, 0.19990381197331833, 0.26859608185465605]]
