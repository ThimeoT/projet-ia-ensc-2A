from heapq import heappush, heappop

# --- Configuration du taquin ---
ETAT_OBJECTIF = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

DEPLACEMENTS = {"Haut": (-1, 0), "Bas": (1, 0), "Gauche": (0, -1), "Droite": (0, 1)}

CONFIG_FINALE = {
    1: {"x": 0, "y": 0},
    2: {"x": 0, "y": 1},
    3: {"x": 0, "y": 2},
    4: {"x": 1, "y": 0},
    5: {"x": 1, "y": 1},
    6: {"x": 1, "y": 2},
    7: {"x": 2, "y": 0},
    8: {"x": 2, "y": 1},
}
ETATS_TEMOINS = ()

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
            if etat[i][j] != 0 and etat[i][j] != ETAT_OBJECTIF[i][j]:
                mal_places += 1
    return mal_places


def heuristique_mannathan(etat):
    """Heuristique de Mannathan : compte la somme des distances
    de mannathan pour chaque tuile à leur bonne place"""
    somme = 0
    for i in range(3):
        for j in range(3):
            if etat[i][j] != 0:
                somme += abs(i - CONFIG_FINALE[etat[i][j]]["x"])+ abs(j-CONFIG_FINALE[etat[i][j]]["y"])
    return somme

def afficher_taquin(etat):
    """Affiche joliment un état du taquin."""
    for i in range(3):
        ligne = " ".join(str(x) if x != 0 else " " for x in etat[i])
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
                heappush(
                    open_set,
                    (new_g + h, new_g, next_state, chemin + [(move, next_state)]),
                )

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
            print(f"Coup : {move} (heuristique = {heuristique(etat_suivant)})\n heuristique mannathan = {heuristique_mannathan(etat_suivant)} ")
            afficher_taquin(etat_suivant)
            etat_courant = etat_suivant

        print("🎯 Taquin résolu !")
        print(f"Solution trouvée en {len(chemin)} coups :\n")
        print(f"Nombre final d'états dans open : {taille_open}")
        print(f"Nombre d'états visités : {taille_visited}")

print("heuristique mannathan")
print(heuristique_mannathan(((1,2,4),(3,5,6),(8,7,0))))

if __name__ == "__main__":
    main()


### But du prochain code

# prendre 10 configs initiales
# récupérer les valeurs à chaque étape du chemin pour une heuristique
# retourner un tableau d'éléments
# combiner deux tableaux d'éléments
# former un graphe avec

# voir comment assembler plusieurs graphes ensembles

