from heapq import heappush, heappop

# --- Configuration du taquin ---
ETAT_OBJECTIF3 = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

ETAT_OBJECTIF5 = (
    (1, 2, 3, 4, 5),   
    (6, 7, 8, 9, 10),
    (11, 12, 13, 14, 15),
    (16, 17, 18, 19, 20),
    (21, 22, 23, 24, 0)
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
    for i in range(3):
        for j in range(3):
            if etat[i][j] != 0 and etat[i][j] != ETAT_OBJECTIF3[i][j]:
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
                target_x = (valeur - 1) // n
                target_y = (valeur - 1) % n
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

def heuristique_ponderee(etat):
    """Q3 : Manhattan Pondérée (Weighted A*)."""
    h = heuristique_manhattan(etat)
    # Consigne : ne pas surestimer si < 10 coups restants
    if h < 10:
        return h
    # Sinon on booste pour accélérer (W = 1.4 par exemple)
    return h * 1.4


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

        if etat == ETAT_OBJECTIF3:
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

        for move, etat_suivant in chemin:
            print(f"Coup : {move} (heuristique = {heuristique(etat_suivant)}, heuristique Manhattan = {heuristique_manhattan(etat_suivant)}, heuristique Pondérée = {heuristique_ponderee(etat_suivant)})")
            afficher_taquin(etat_suivant)
            etat_courant = etat_suivant

        print("🎯 Taquin résolu !")
        print(f"Nombre final d'états dans open : {taille_open}")
        print(f"Nombre d'états visités : {taille_visited}")


if __name__ == "__main__":
    main()


