# -*- coding: utf-8 -*-
'''Programme principal de l'algorithme PageRank. 
'''
import entrees, sorties, sys, cProfile, pstats 
import methode_p as mp
import methode_c as mc
import methode_n as mn


def main():
    
    
    parametres = entrees.analyse_commande(sys.argv) # Déterminer la méthode et les paramètres choisis par l'utilisateur et qui seront utilisés pour calculer le poids des pages
    
    if 'Erreur' in parametres: # Si on détecte une erreur dans la ligne de commande
        sys.exit() # Alors arrêter le programme
    else: # Sinon s'il n'y a pas d'erreur dans la ligne de commande
        (methode, alpha, k, epsilon, fichier_graphe) = parametres # Alors Attribuer les différentes valeurs aux paramètres qui sont des constantes donc en majuscule

        print("Calcul du PageRank lancé avec la méthode", methode)
        print("Loading 0%", end='\r')
        infos_graphe = entrees.det_infos_graphe(fichier_graphe) # Récupérer les informations du fichier graphe sous la forme d'un tuple contenant ... 
        
        if 'Erreur' in infos_graphe: # Si on détecte une erreur dans le fichier graphe
            sys.exit() # Alors arrêter le programme
        else: # Sinon s'il n'y a pas d'erreur dans le fichier graphe
            # Alors Attribuer un poids à chaque page suivant la méthode choisie	
            if methode == 'P':
                registre_poids = mp.sauvegarder_poids(mp.calculer_pi_final(alpha, infos_graphe[0], infos_graphe[1], infos_graphe[3], k, epsilon)) # dictionnaire contenant le numéro des pages comme clés et leur poids comme valeur associée
            elif methode == 'C':
                registre_poids = mc.calculer_pi_final(alpha, infos_graphe[0], infos_graphe[2], infos_graphe[3], k, epsilon, infos_graphe[4]) # vecteur pi final sous forme de dictionnaire contenant les cordonnées (i, j) comme clés et leur poids comme valeur associée
            elif methode == 'N' :
                registre_poids = mn.sauvegarder_poids(mn.calculer_pi_final(alpha, infos_graphe[0], infos_graphe[1], infos_graphe[3], k, epsilon)) # dictionnaire contenant le numéro des pages comme clés et leur poids comme valeur associée
        
            sorties.creer_fichier_poids(fichier_graphe, registre_poids, infos_graphe[3], alpha, k, epsilon)  # Créer le fichier Poids
            sorties.creer_fichier_pagerank(fichier_graphe, registre_poids, methode) # Créer le fichier PageRank


if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats(10)