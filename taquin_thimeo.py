from heapq import heappush, heappop
import pandas as pd  # pour manipuler et analyser les données
import matplotlib.pyplot as plt  # pour créer des graphes
import seaborn as sns  # surcouche de matplotlib pour de meilleurs rendus visuels (combiner nuage de points de plusieurs population avec régression)

sns.set_style("darkgrid")
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
ETATS_TEMOINS = (
    ((2, 5, 1), (6, 0, 4), (7, 3, 8)),
    ((4, 6, 2), (1, 5, 8), (7, 3, 0)),
    ((8, 0, 5), (4, 1, 7), (2, 6, 3)),
    ((4, 1, 5), (0, 8, 7), (6, 2, 3)),
    ((6, 3, 2), (5, 1, 7), (0, 8, 4)),
    ((7, 6, 5), (2, 4, 1), (3, 8, 0)),
    ((1, 7, 4), (8, 0, 2), (3, 6, 5)),
    ((2, 0, 5), (6, 7, 3), (4, 1, 8)),
    ((5, 3, 6), (8, 1, 7), (0, 4, 2)),
    ((5, 2, 1), (3, 0, 4), (8, 7, 6)),
)


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


def heuristique_manhattan(etat):
    """Heuristique de manhattan : compte la somme des distances
    de manhattan pour chaque tuile à leur bonne place"""
    somme = 0
    for i in range(3):
        for j in range(3):
            if etat[i][j] != 0:
                somme += abs(i - CONFIG_FINALE[etat[i][j]]["x"]) + abs(
                    j - CONFIG_FINALE[etat[i][j]]["y"]
                )
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
            print(
                f"Coup : {move} (heuristique = {heuristique(etat_suivant)})\n heuristique manhattan = {heuristique_manhattan(etat_suivant)} "
            )
            afficher_taquin(etat_suivant)
            etat_courant = etat_suivant

        print("🎯 Taquin résolu !")
        print(f"Solution trouvée en {len(chemin)} coups :\n")
        print(f"Nombre final d'états dans open : {taille_open}")
        print(f"Nombre d'états visités : {taille_visited}")


### But du prochain code
def recuperer_data_heuristiques(etat_initial=ETATS_TEMOINS[1]):
    # prendre 10 configs initiales (on commence par une)
    chemin, final, taille_open, taille_visited = a_etoile(etat_initial)
    chemin = [x[1] for x in chemin]  # pour n'avoir que les tuples de chaque config
    # récupérer les valeurs à chaque étape du chemin pour les 3 heuristiques
    resultat = pd.DataFrame(
        columns=["coups restants", "heuristique", "type d'heuristique"]
    )
    for i in range(len(chemin)):
        resultat.loc[i * 2] = [len(chemin) - i - 1, heuristique(chemin[i]), "position"]
        resultat.loc[(i * 2) + 1] = [
            len(chemin) - i - 1,
            heuristique_manhattan(chemin[i]),
            "manhattan",
        ]
    return resultat


def recuperer_data_coup_heuristique_manhattan(etat_initial=ETATS_TEMOINS[1]):
    # prendre 10 configs initiales (on commence par une)
    chemin, final, taille_open, taille_visited = a_etoile(etat_initial)
    chemin = [x[1] for x in chemin]  # pour n'avoir que les tuples de chaque config
    # récupérer les valeurs à chaque étape du chemin pour les 3 heuristiques
    resultat = pd.DataFrame(
        columns=["coups restants", "heuristique simple", "heuristique manhattan"]
    )
    for i in range(len(chemin)):
        # on veut que le dernier état ait "coups restants" = 0
        resultat.loc[i] = [
            len(chemin) - i - 1,
            heuristique(chemin[i]),
            heuristique_manhattan(chemin[i]),
        ]
    return resultat


def recuperer_data_moyennes_heuristiques():
    """
    Retourne les valeurs regroupées en fonction du nombre de coups pour les deux types d'heuristiques
    """
    df = pd.DataFrame(
        columns=["coups restants", "heuristique simple", "heuristique manhattan"]
    )
    for etat in ETATS_TEMOINS:
        data = recuperer_data_coup_heuristique_manhattan(etat)
        df = pd.concat((df, data), ignore_index=True)
    # regrouper par 'coups restants' et calculer la moyenne pour chaque groupe
    means_grouped = df.groupby("coups restants").mean().reset_index()
    return means_grouped


def tracer_moyennes(df):

    plt.plot(
        "coups restants",
        "heuristique simple",
        data=df,
        marker="o",  # marker type
        markerfacecolor="blue",  # color of marker
        markersize=12,  # size of marker
        color="skyblue",  # color of line
        linewidth=4,  # change width of line
    )
    plt.plot(
        "coups restants",
        "heuristique manhattan",
        data=df,
        marker="p",  # marker type
        markerfacecolor="red",  # color of marker
        markersize=12,  # size of marker
        color="darkred",  # color of line
        linewidth=4,  # change width of line
    )
    plt.plot(
        "coups restants",
        "coups restants",
        data=df,
        marker="",  # marker type
        color="olive",  # color of line
    )
    # show legend
    plt.legend()

    # show graph
    plt.show()

    # for i in range(len(chemin)):
    #     resultat.loc[i * 2] = [len(chemin) - i, heuristique(chemin[i]), "position"]
    #     resultat.loc[(i * 2) + 1] = [
    #         len(chemin) - i,
    #         heuristique_manhattan(chemin[i]),
    #         "manhattan",
    #     ]


def tracer_plot_coups_heuristiques():
    # créer le graphe des données à partir du tableau
    data = recuperer_data_heuristiques()
    sns.lmplot(
        x="coups restants",
        y="heuristique",
        data=data,
        hue="type d'heuristique",
    )
    plt.show()
    print(data)


tracer_moyennes(recuperer_data_moyennes_heuristiques())
# retourner un tableau d'éléments
# combiner deux tableaux d'éléments
# former un graphe avec

# voir comment assembler plusieurs graphes ensembles
