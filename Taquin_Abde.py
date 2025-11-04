from heapq import heappush, heappop

import math

# --- Configuration du taquin ---
ETAT_OBJECTIF = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

DEPLACEMENTS = {
    'Haut': (-1, 0),
    'Bas': (1, 0),
    'Gauche': (0, -1),
    'Droite': (0, 1)
}

# --- Fonctions utilitaires ---

def lire_taquin():
    print("Entrez le taquin initial ligne par ligne (avec 0 pour la case vide) :")
    etat = []
    for i in range(3):
        ligne = list(map(int, input().split()))
        etat.append(tuple(ligne))
    return tuple(etat)


def trouver_vide(etat):
    for i in range(3):
        for j in range(3):
            if etat[i][j] == 0:
                return i, j


def deplacements_possibles(etat):
    """Retourne la liste des déplacements possibles à partir d'un état donné."""
    x, y = trouver_vide(etat)
    deplacements = []

    for move, (dx, dy) in DEPLACEMENTS.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in etat]
            # Échange de la case vide avec la case cible
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            new_state_tuple = tuple(tuple(row) for row in new_state)
            deplacements.append((move, new_state_tuple))

    return deplacements


def heuristique(etat):
    """Heuristique : compte le nombre de tuiles mal placées."""
    mal_places = 0
    for i in range(len(etat)):
        for j in range(len(etat[i])):
            if etat[i][j] != 0 and etat[i][j] != ETAT_OBJECTIF[i][j]:
                mal_places += 1
    return mal_places



# Reponse a la question 2 : heuristique de la distance de Manhattan

def heuristique_manhattan(etat):
    distance = 0
    for i in range(3):
        for j in range(3):
            valeur = etat[i][j]
            if valeur != 0:
                x_goal, y_goal = divmod(valeur - 1, 3)
                distance += abs(i - x_goal) + abs(j - y_goal)
    return distance




def heuristique_combined(etat):
    return math.floor(0.2 * heuristique(etat) + 0.8 * heuristique_manhattan(etat))






def afficher_taquin(etat):
    """Affiche joliment un état du taquin."""
    for i in range(3):
        ligne = ' '.join(str(x) if x != 0 else ' ' for x in etat[i])
        print(ligne)
    print("-------")


# --- Algorithme A* ---

def a_etoile(initial):
    open_set = []
    heappush(open_set, (heuristique(initial), 0, initial, []))
    visited = set()

    while open_set:
        f, g, etat, chemin = heappop(open_set)

        if etat == ETAT_OBJECTIF:
            return chemin, etat, len(open_set), len(visited)

        if etat in visited:
            continue

        visited.add(etat)

        for move, next_state in deplacements_possibles(etat):
            if next_state not in visited:
                new_g = g + 1
                h = heuristique(next_state)
                heappush(open_set, (new_g + h, new_g, next_state, chemin + [(move, next_state)]))

    return None, None, 0, len(visited)


def main():
    initial = lire_taquin()
    print("\nRésolution en cours...\n")

    chemin, final, taille_open, taille_visited = a_etoile(initial)

    if chemin is None:
        print("Aucune solution trouvée.")
    else:
        print(f"Solution trouvée en {len(chemin)} coups :\n")
        etat_courant = initial
        afficher_taquin(etat_courant)

        i = 1
        for move, etat_suivant in chemin:
            print(f"Coup {i} : {move} (h = {heuristique(etat_suivant)}) (h_m = {heuristique_manhattan(etat_suivant)}) (h_c = {heuristique_combined(etat_suivant)}) (coups restants = {len(chemin) - i})")
            afficher_taquin(etat_suivant)
            etat_courant = etat_suivant
            i += 1

        print("🎯 Taquin résolu !")
        print(f"Nombre final d'états dans open : {taille_open}")
        print(f"Nombre d'états visités : {taille_visited}")






etat = (
    (8, 6, 7),
    (2, 5, 4),
    (0, 3, 1)
)


main()

"""
print(heuristique(etat))  # Devrait afficher 2 (les tuiles 5 et 6 sont mal placées)

print(heuristique_manhattan(etat)) 
"""


"""
config 1 : 14.5 / 24 // 16
config 2 : 12 / 22 // 13
config 3 : 19.5 / 23 // 20
config 4 : 20 / 21 // 21
config 5 : 18.5 / 22 // 19
"""