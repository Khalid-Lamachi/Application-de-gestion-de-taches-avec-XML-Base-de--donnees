import os
import sys
from datetime import date

# Ajouter les dossiers au path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'BDD'))
sys.path.insert(0, os.path.join(BASE_DIR, 'XSLT'))

import gestion_bdd
import trans



def generer_id():
    """Genere un ID unique pour une nouvelle tache."""
    taches = gestion_bdd.recuperer_taches()
    if not taches:
        return "T1"
    ids = []
    for t in taches:
        try:
            ids.append(int(t[0].replace("T", "")))
        except ValueError:
            continue
    return f"T{max(ids) + 1}" if ids else "T1"


def saisir_priorite():
    """Demande a l'utilisateur de choisir une priorite."""
    while True:
        print("  Priorite : 1=basse, 2=moyenne, 3=haute")
        choix = input("  Choix : ").strip()
        if choix == "1":
            return "basse"
        elif choix == "2":
            return "moyenne"
        elif choix == "3":
            return "haute"
        print("  Choix invalide.")


def saisir_etat():
    """Demande a l'utilisateur de choisir un etat."""
    while True:
        print("  Etat : 1=A faire, 2=En cours, 3=Terminee")
        choix = input("  Choix : ").strip()
        if choix == "1":
            return "A faire"
        elif choix == "2":
            return "En cours"
        elif choix == "3":
            return "Terminee"
        print("  Choix invalide.")


def ajouter_tache():
    """Ajouter une nouvelle tache."""
    print("\n--- AJOUTER UNE TACHE ---")
    id_tache = generer_id()
    print(f"  ID : {id_tache}")

    titre = input("  Titre : ").strip()
    if not titre:
        print("  Erreur: titre obligatoire.")
        return

    description = input("  Description : ").strip()
    priorite = saisir_priorite()
    etat = saisir_etat()
    date_creation = date.today().isoformat()

    gestion_bdd.ajouter_tache(id_tache, titre, description, etat, priorite, date_creation)
    gestion_bdd.exporter_bdd_en_xml()


def lister_taches():
    """Afficher toutes les taches."""
    print("\n--- LISTE DES TACHES ---")
    taches = gestion_bdd.recuperer_taches()
    if not taches:
        print("  Aucune tache.")
        return

    print(f"  {'ID':<5} {'Titre':<20} {'Etat':<12} {'Priorite':<10} {'Date':<12}")
    
    for t in taches:
        print(f"  {t[0]:<5} {t[1]:<20} {t[3]:<12} {t[4]:<10} {t[5]:<12}")
    print(f"\n  Total : {len(taches)} tache(s)")


def modifier_tache():
    """Modifier une tache existante."""
    print("\n--- MODIFIER UNE TACHE ---")
    id_tache = input("  ID de la tache : ").strip().upper()
    tache = gestion_bdd.recuperer_tache_par_id(id_tache)
    if not tache:
        print(f"  Tache {id_tache} introuvable.")
        return

    print(f"  Tache actuelle : {tache[1]} [{tache[3]}] - {tache[4]}")
    print("  (Laisser vide = garder la valeur)")

    titre = input(f"  Titre [{tache[1]}] : ").strip() or tache[1]
    description = input(f"  Description [{tache[2]}] : ").strip() or tache[2]

    print(f"  Changer priorite ? (actuelle: {tache[4]})")
    chg = input("  (o/n) : ").strip().lower()
    priorite = saisir_priorite() if chg == 'o' else tache[4]

    print(f"  Changer etat ? (actuel: {tache[3]})")
    chg = input("  (o/n) : ").strip().lower()
    etat = saisir_etat() if chg == 'o' else tache[3]

    gestion_bdd.modifier_tache(id_tache, titre, description, etat, priorite, tache[5])
    gestion_bdd.exporter_bdd_en_xml()


def changer_etat():
    """Changer l'etat d'une tache."""
    print("\n--- CHANGER L'ETAT ---")
    id_tache = input("  ID de la tache : ").strip().upper()
    tache = gestion_bdd.recuperer_tache_par_id(id_tache)
    if not tache:
        print(f"  Tache {id_tache} introuvable.")
        return

    print(f"  Tache : {tache[1]} - Etat actuel : {tache[3]}")
    nouvel_etat = saisir_etat()
    gestion_bdd.modifier_etat_tache(id_tache, nouvel_etat)
    gestion_bdd.exporter_bdd_en_xml()


def supprimer_tache():
    """Supprimer une tache."""
    print("\n--- SUPPRIMER UNE TACHE ---")
    id_tache = input("  ID de la tache : ").strip().upper()
    tache = gestion_bdd.recuperer_tache_par_id(id_tache)
    if not tache:
        print(f"  Tache {id_tache} introuvable.")
        return

    print(f"  Tache : {tache[1]} [{tache[3]}]")
    confirm = input("  Confirmer suppression ? (o/n) : ").strip().lower()
    if confirm == 'o':
        gestion_bdd.supprimer_tache(id_tache)
        gestion_bdd.exporter_bdd_en_xml()
    else:
        print("  Annule.")


def generer_html():
    """Generer la page HTML via XSLT."""
    print("\n--- GENERER HTML (XSLT) ---")
    # D'abord s'assurer que le XML est a jour
    gestion_bdd.exporter_bdd_en_xml()
    # Lancer la transformation
    trans.transformer()


def afficher_menu():
    """Afficher le menu principal."""
    print("\n" + "=" * 50)
    print("  MENU PRINCIPAL - GESTIONNAIRE DE TACHES")
    print("=" * 50)
    print("  1. Ajouter une tache")
    print("  2. Lister les taches")
    print("  3. Modifier une tache")
    print("  4. Changer l'etat d'une tache")
    print("  5. Supprimer une tache")
    print("  6. Afficher les taches (en HTML)")
    print("  7. Quitter")
    print("~" * 50)


def main():
    """Programme principal."""
    print("=" * 50)
    print("  GESTIONNAIRE DE TACHES - TO-DO LIST")
    print("=" * 50)

    # Initialiser la BDD
    gestion_bdd.init_database()

    # Si BDD vide, importer depuis XML
    if not gestion_bdd.recuperer_taches():
        print("  Base vide, importation depuis XML...")
        gestion_bdd.importer_xml_en_bdd()

    while True:
        afficher_menu()
        choix = input("\n  Votre choix : ").strip()

        if choix == "1":
            ajouter_tache()
        elif choix == "2":
            lister_taches()
        elif choix == "3":
            modifier_tache()
        elif choix == "4":
            changer_etat()
        elif choix == "5":
            supprimer_tache()
        elif choix == "6":
            generer_html()
        elif choix == "7":
            print("\n  Au revoir!")
            break
        else:
            print("\n  Choix invalide.")

        input("\n  Appuyez sur Entree...")


if __name__ == "__main__":
    main()