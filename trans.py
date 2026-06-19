import os
import webbrowser
def transformer():
    from lxml import etree
    if not os.path.exists("XML/taches.xml"):
        print("Erreur: Fichier XML introuvable")
        return
    if not os.path.exists("taches.xsl"):
        print("Erreur: Fichier XSL introuvable")
        return
    donnees_xml = etree.parse("XML/taches.xml")
    regles_xslt = etree.parse("taches.xsl")
    transformateur = etree.XSLT(regles_xslt)
    document_html = transformateur(donnees_xml)
    os.makedirs("HTML", exist_ok=True)
    with open("HTML/taches.html", "wb") as fichier_sortie:
        fichier_sortie.write(etree.tostring(document_html, pretty_print=True, method="html"))
    html = os.path.abspath("HTML/taches.html")
    print("Transformation reussie!")
    ouvrir = input("Ouvrir dans le navigateur ? (o/n) : ").strip().lower()
    if ouvrir == 'o':
        webbrowser.open(f'file:///{html}')


    
