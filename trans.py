"""
Transformation XSLT : XML -> HTML
Utilise la bibliotheque lxml (pip install lxml)

Les 4 etapes de la transformation :
1. Le Parsing : Charger les fichiers XML et XSLT
2. L'Instanciation : Creer le processeur de transformation
3. L'Execution : Appliquer la transformation
4. La Serialisation : Ecrire le resultat en fichier HTML
"""
import os
import webbrowser

# Chemins des fichiers
BASE_DIR = os.path.dirname(__file__)
XML_PATH = os.path.join(BASE_DIR, "../XML/taches.xml")
XSL_PATH = os.path.join(BASE_DIR, "taches.xsl")
HTML_PATH = os.path.join(BASE_DIR, "../HTML/taches.html")


def transformer():
    """Effectue la transformation XSLT (XML -> HTML)."""
    try:
        from lxml import etree

        # Verifier que les fichiers existent
        if not os.path.exists(XML_PATH):
            print(f"  Erreur: Fichier XML introuvable : {os.path.abspath(XML_PATH)}")
            return
        if not os.path.exists(XSL_PATH):
            print(f"  Erreur: Fichier XSL introuvable : {os.path.abspath(XSL_PATH)}")
            return

        # === Etape 1 : Le Parsing ===
        # Charger et parser le fichier XML et le fichier XSLT
        donnees_xml = etree.parse(XML_PATH)
        regles_xslt = etree.parse(XSL_PATH)

        # === Etape 2 : L'Instanciation ===
        # Creer le processeur de transformation
        transformateur = etree.XSLT(regles_xslt)

        # === Etape 3 : L'Execution ===
        # Appliquer la transformation
        document_html = transformateur(donnees_xml)

        # === Etape 4 : La Serialisation ===
        # Ecrire le resultat en fichier HTML
        os.makedirs(os.path.dirname(os.path.abspath(HTML_PATH)), exist_ok=True)

        with open(HTML_PATH, "wb") as fichier_sortie:
            fichier_sortie.write(etree.tostring(document_html, pretty_print=True, method="html"))

        html_abs = os.path.abspath(HTML_PATH)
        print(f"  Transformation reussie!")
        print(f"  Fichier HTML genere : {html_abs}")

        # Proposer d'ouvrir dans le navigateur
        ouvrir = input("  Ouvrir dans le navigateur ? (o/n) : ").strip().lower()
        if ouvrir == 'o':
            webbrowser.open(f'file:///{html_abs}')

    except ImportError:
        print("  Erreur: la bibliotheque 'lxml' n'est pas installee.")
        print("  Installez-la avec : pip install lxml")
    except Exception as e:
        print(f"  Erreur lors de la transformation : {e}")


if __name__ == "__main__":
    print("=== Test de la transformation XSLT ===")
    transformer()