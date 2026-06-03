import os
import gestion_bdd

def lancer_test_manuel():
    print("=== DÉBUT DU TEST DE LA BASE DE DONNÉES ===")
    
    # 1. Initialisation de la base de données
    print("\n[Étape 1] Initialisation de la base de données...")
    gestion_bdd.init_database()
    
    # 2. Ajout de nouvelles tâches de test
    print("\n[Étape 2] Ajout de nouvelles tâches...")
    gestion_bdd.ajouter_tache(
        id_tache="T3",
        titre="Tâche de Test 3",
        description="Cette tâche sert à tester l'insertion",
        etat="A faire",
        priorite="basse",
        date_creation="2026-06-03"
    )
    gestion_bdd.ajouter_tache(
        id_tache="T4",
        titre="Tâche de Test 4",
        description="Une autre tâche de test",
        etat="En cours",
        priorite="moyenne",
        date_creation="2026-06-03"
    )

    # 3. Récupération et affichage des tâches en base de données
    print("\n[Étape 3] Contenu de la base de données après ajout :")
    taches = gestion_bdd.recuperer_taches()
    for tache in taches:
        print(f" - ID: {tache[0]} | Titre: {tache[1]} | État: {tache[3]} | Priorité: {tache[4]} | Date: {tache[5]}")

    # 4. Modification d'une tâche
    print("\n[Étape 4] Modification de la tâche T3...")
    gestion_bdd.modifier_tache(
        id_tache="T3",
        titre="Tâche de Test 3 (Modifiée)",
        description="Description mise à jour",
        etat="Terminée",
        priorite="haute",
        date_creation="2026-06-03"
    )

    # 5. Exportation de la base de données vers le fichier XML/taches.xml
    print("\n[Étape 5] Exportation des tâches (avec les modifications) vers le fichier XML...")
    gestion_bdd.exporter_bdd_en_xml()
    print("-> Fichier XML mis à jour avec les tâches temporaires.")

    # 6. Nettoyage : Suppression des tâches de test de la base de données (T3 et T4)
    print("\n[Étape 6] Nettoyage : Suppression des tâches de test (T3 et T4) de la base de données...")
    gestion_bdd.supprimer_tache("T3")
    gestion_bdd.supprimer_tache("T4")

    # 7. Nettoyage : Ré-exportation de la base de données vers le fichier XML/taches.xml
    print("\n[Étape 7] Nettoyage : Ré-exportation de la base de données vers le fichier XML...")
    gestion_bdd.exporter_bdd_en_xml()
    print("-> Fichier XML restauré à son état initial (uniquement tâches de production).")

    # 8. Affichage du contenu final de la base de données
    print("\n[Étape 8] Contenu final de la base de données :")
    taches_finales = gestion_bdd.recuperer_taches()
    for tache in taches_finales:
        print(f" - ID: {tache[0]} | Titre: {tache[1]} | État: {tache[3]} | Priorité: {tache[4]}")
        
    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    lancer_test_manuel()
