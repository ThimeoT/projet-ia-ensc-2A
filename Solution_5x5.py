from heapq import heappush, heappop
import time

# --- Configuration Globale ---
# Sera défini dynamiquement selon la taille du puzzle
ETAT_OBJECTIF = None 

DEPLACEMENTS = {
    'Haut': (-1, 0),
    'Bas': (1, 0),
    'Gauche': (0, -1),
    'Droite': (0, 1)
}

# --- Fonctions utilitaires ---

def generer_objectif(n):
    """Génère l'état objectif pour une taille n donnée."""
    objectif = []
    cpt = 1
    for i in range(n):
        ligne = []
        for j in range(n):
            if i == n-1 and j == n-1:
                ligne.append(0)
            else:
                ligne.append(cpt)
                cpt += 1
        objectif.append(tuple(ligne))
    return tuple(objectif)

def lire_taquin():
    print("Entrez le nombre de lignes (ex: 3 pour 3x3, 5 pour 5x5) :")
    try:
        n = int(input())
    except ValueError:
        n = 3 # Valeur par défaut
        
    print(f"Entrez le taquin {n}x{n} ligne par ligne (avec 0 pour la case vide) :")
    etat = []
    for i in range(n):
        ligne = list(map(int, input().split()))
        if len(ligne) != n:
            print(f"Erreur : La ligne doit contenir {n} nombres.")
            return None
        etat.append(tuple(ligne))
    return tuple(etat)

def trouver_vide(etat):
    n = len(etat)
    for i in range(n):
        for j in range(n):
            if etat[i][j] == 0:
                return i, j

def deplacements_possibles(etat):
    """Retourne la liste des déplacements possibles à partir d'un état donné."""
    n = len(etat)
    x, y = trouver_vide(etat)
    deplacements = []

    for move, (dx, dy) in DEPLACEMENTS.items():
        nx, ny = x + dx, y + dy
        # Vérification des bornes dynamique (utilise n)
        if 0 <= nx < n and 0 <= ny < n:
            new_state = [list(row) for row in etat]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            new_state_tuple = tuple(tuple(row) for row in new_state)
            deplacements.append((move, new_state_tuple))

    return deplacements

# --- Heuristiques ---

def heuristique_mal_places(etat):
    """Heuristique : compte le nombre de tuiles mal placées."""
    mal_places = 0
    n = len(etat)
    for i in range(n):
        for j in range(n):
            # Attention : ETAT_OBJECTIF doit être défini globalement avant
            if etat[i][j] != 0 and etat[i][j] != ETAT_OBJECTIF[i][j]:
                mal_places += 1
    return mal_places

def heuristique_manhattan(etat):
    """Q2 : Distance de Manhattan."""
    distance = 0
    n = len(etat)
    for i in range(n):
        for j in range(n):
            valeur = etat[i][j]
            if valeur != 0:
                # Calcul de la position cible pour cette valeur
                # La valeur k se trouve à la ligne (k-1)//n et colonne (k-1)%n
                target_x = (valeur - 1) // n
                target_y = (valeur - 1) % n
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

def heuristique_ponderee(etat):
    """Q3/Q4 : Manhattan Pondérée (Weighted A*)."""
    h = heuristique_manhattan(etat)
    
    # Pour le 5x5, on applique un poids fort pour accélérer (Weighted A*)
    # Un poids de 3.0 rend la recherche très gloutonne et rapide
    # Un poids de 1.0 est l'A* standard (trop lent pour 5x5)
    POIDS = 3.0 
    
    # Consigne Q3 (optimisation fine): ne pas surestimer si proche du but (<5 coups)
    if h < 5:
        return h
    
    return h * POIDS

def afficher_taquin(etat):
    """Affiche joliment un état du taquin."""
    n = len(etat)
    for i in range(n):
        # Formatage pour aligner les nombres (utile pour 5x5 avec nombres à 2 chiffres)
        ligne = ' '.join(f"{x:2}" if x != 0 else '  ' for x in etat[i])
        print(ligne)
    print("-" * (n * 3))

# --- Algorithme A* ---

def a_etoile(initial, fonction_h):
    """
    Algorithme A* générique.
    Prend en paramètre la fonction heuristique à utiliser.
    """
    open_set = []
    # On stocke (f, g, etat, chemin)
    heappush(open_set, (fonction_h(initial), 0, initial, []))
    visited = set()
    
    # Compteur pour stat (optionnel)
    nodes_count = 0

    while open_set:
        f, g, etat, chemin = heappop(open_set)
        
        # Vérification si on a atteint l'objectif
        if etat == ETAT_OBJECTIF:
            return chemin, etat, len(open_set), len(visited)

        if etat in visited:
            continue

        visited.add(etat)
        nodes_count += 1
        
        # Sécurité pour éviter boucle infinie en cas de bug sur très gros puzzle
        if nodes_count > 2000000: 
            print("Arrêt de sécurité : trop de nœuds explorés.")
            return None, None, len(open_set), len(visited)

        for move, next_state in deplacements_possibles(etat):
            if next_state not in visited:
                new_g = g + 1
                h = fonction_h(next_state)
                # f = g + h
                heappush(open_set, (new_g + h, new_g, next_state, chemin + [(move, next_state)]))

    return None, None, 0, len(visited)

def main():
    global ETAT_OBJECTIF
    
    print("--- Résolution de Taquin (Générique) ---")
    initial = lire_taquin()
    
    if initial is None:
        return

    n = len(initial)
    ETAT_OBJECTIF = generer_objectif(n)
    
    print(f"\nConfiguration détectée : {n}x{n}")
    print("Objectif généré :")
    afficher_taquin(ETAT_OBJECTIF)
    
    # Sélection automatique de l'heuristique selon la taille
    if n <= 3:
        print("Taille petite (3x3) -> Utilisation Heuristique Manhattan Standard")
        h_choisie = heuristique_manhattan
    else:
        print(f"Taille grande ({n}x{n}) -> Utilisation Heuristique Pondérée (Weighted A*) pour performance")
        h_choisie = heuristique_ponderee

    print("\nRésolution en cours...\n")
    start_time = time.time()

    chemin, final, taille_open, taille_visited = a_etoile(initial, h_choisie)
    
    end_time = time.time()
    duree = end_time - start_time

    if chemin is None:
        print("Aucune solution trouvée ou abandon.")
    else:
        print(f"Solution trouvée en {len(chemin)} coups en {duree:.4f} secondes.")
        print(f"Nœuds explorés (visited) : {taille_visited}")
        
        # Affichage (optionnel si trop long)
        if len(chemin) < 100:
            choix = input("Afficher le détail des coups ? (o/n) : ")
            if choix.lower() == 'o':
                etat_courant = initial
                afficher_taquin(etat_courant)
                i = 1
                for move, etat_suivant in chemin:
                    print(f"Coup {i} : {move}")
                    afficher_taquin(etat_suivant)
                    etat_courant = etat_suivant
                    i += 1
        else:
            print("(Chemin trop long pour affichage complet)")

if __name__ == "__main__":
    main()