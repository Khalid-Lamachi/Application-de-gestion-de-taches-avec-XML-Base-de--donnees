import sqlite3
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

DB_Folder = os.path.dirname(__file__)
DB_File = "taches.db"
DB_Path = os.path.join(DB_Folder, DB_File)
XML_Path = os.path.join(DB_Folder, "../XML/taches.xml")


def init_database():
    """Initialise la base de données et crée la table avec des contraintes alignées sur le DTD."""
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS taches (
            id TEXT PRIMARY KEY,
            titre TEXT NOT NULL,
            description TEXT,
            etat TEXT NOT NULL,
            priorite TEXT CHECK(priorite IN ('basse', 'moyenne', 'haute')) NOT NULL,
            dateCreation TEXT NOT NULL
        );
        """)
        conn.commit()
    print(f"Database initialized successfully! : {DB_Path}")


def ajouter_tache(id_tache, titre, description, etat, priorite, date_creation):
    """Ajoute une tache à la base de données"""
    try:
        with sqlite3.connect(DB_Path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO taches (id, titre, description, etat, priorite, dateCreation) VALUES (?, ?, ?, ?, ?, ?);
            """, (id_tache, titre, description, etat, priorite, date_creation))
            conn.commit()
        print(f"Task {id_tache} was added successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error: Task {id_tache} already exists or invalid priority / missing field. Details: {e}")


def recuperer_taches():
    """Recupere toutes les taches de la base de données"""
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM taches")
        taches = cursor.fetchall()
    return taches

def recuperer_tache_par_id(id_tache):
    """Recupere une tache par son ID."""
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM taches WHERE id = ?", (id_tache,))
        tache = cursor.fetchone()
    return tache

def modifier_tache(id_tache, titre, description, etat, priorite, date_creation):
    """Modifie une tache dans la base de données"""
    try:
        with sqlite3.connect(DB_Path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE taches SET titre = ?, description = ?, etat = ?, priorite = ?, dateCreation = ? WHERE id = ?;
            """, (titre, description, etat, priorite, date_creation, id_tache))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"Task {id_tache} does not exist!")
            else:
                print(f"Task {id_tache} was modified successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error: Integrity constraint violated (check if priority is basse/moyenne/haute). Details: {e}")

def modifier_etat_tache(id_tache, nouvel_etat):
    """Modifie uniquement l'etat d'une tache."""
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE taches SET etat = ? WHERE id = ?;", (nouvel_etat, id_tache))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Tache {id_tache} introuvable!")
        else:
            print(f"Etat de la tache {id_tache} change en '{nouvel_etat}'.")


def supprimer_tache(id_tache):
    """Supprime une tache de la base de données"""
    with sqlite3.connect(DB_Path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM taches WHERE id = ?;", (id_tache,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Task {id_tache} does not exist!")
        else:
            print(f"Task {id_tache} was deleted successfully!")


def importer_xml_en_bdd():
    """Importe les taches depuis XML/taches.xml dans la base de données."""
    if not os.path.exists(XML_Path):
        print(f"Error: XML file not found at {XML_Path}")
        return
    
    try:
        tree = ET.parse(XML_Path)
        root = tree.getroot()
        imported_count = 0
        
        with sqlite3.connect(DB_Path) as conn:
            cursor = conn.cursor()
            for tache in root.findall('tache'):
                id_tache = tache.get('id')
                priorite = tache.get('priorite')
                titre = tache.find('titre').text if tache.find('titre') is not None else ""
                description = tache.find('description').text if tache.find('description') is not None else ""
                etat = tache.find('etat').text if tache.find('etat') is not None else ""
                date_creation = tache.find('dateCreation').text if tache.find('dateCreation') is not None else ""
                
                cursor.execute("""
                INSERT OR REPLACE INTO taches (id, titre, description, etat, priorite, dateCreation)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (id_tache, titre, description, etat, priorite, date_creation))
                imported_count += 1
            conn.commit()
        print(f"Imported {imported_count} tasks from XML to DB successfully!")
    except Exception as e:
        print(f"Failed to import XML: {e}")


def exporter_bdd_en_xml():
    """Exporte les taches de la base de données vers XML/taches.xml en préservant le DOCTYPE."""
    try:
        taches = recuperer_taches()
        root = ET.Element('taches')
        
        for row in taches:
            id_tache, titre, description, etat, priorite, date_creation = row
            tache_el = ET.SubElement(root, 'tache', id=id_tache, priorite=priorite)
            
            ET.SubElement(tache_el, 'titre').text = titre
            ET.SubElement(tache_el, 'description').text = description if description else ""
            ET.SubElement(tache_el, 'etat').text = etat
            ET.SubElement(tache_el, 'dateCreation').text = date_creation
            
        #   Serialisation en chaine et mise en forme
        raw_xml = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(raw_xml)
        pretty_xml = reparsed.toprettyxml(indent="    ")
        
        # Nettoyage et ajout du DOCTYPE
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        
        if lines[0].startswith('<?xml'):
            lines.insert(1, '<!DOCTYPE taches SYSTEM "taches.dtd">')
        else:
            lines.insert(0, '<!DOCTYPE taches SYSTEM "taches.dtd">')
            
        with open(XML_Path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Exported database tasks to XML successfully! : {XML_Path}")
    except Exception as e:
        print(f"Failed to export XML: {e}")


if __name__ == "__main__":
    init_database()
    
