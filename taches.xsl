<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <!-- Modele racine -->
    <xsl:template match="/">
        <html>
            <head>
                <title>Liste des Taches</title>
                <style>
                    body { font-family: Verdana, sans-serif; padding: 20px; background: #f5f5f5; }
                    h1 { color: #572a67; text-align: center; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th { background-color: rgb(251, 200, 240); padding: 10px; text-align: left; }
                    td { padding: 8px; border-bottom: 1px solid #ddd; }
                    tr:hover { background-color: #f0f0f0; }
                    .etat-afaire { color: black; font-weight: bold; }
                    .etat-encours { color: black; font-weight: bold; }
                    .etat-terminee { color: black; font-weight: bold; }
                    .priorite-haute { color: rgb(212, 81, 186);font-weight: bold; }
                    .priorite-moyenne { color: rgb(239, 124, 216);font-weight: bold; }
                    .priorite-basse { color: rgb(232, 157, 217);font-weight: bold; }
                    .footer { text-align: center; margin-top: 20px; color: gray; font-size: 0.8em; }
                </style>
            </head>
            <body>
                <h1>Liste des Taches - To-Do List</h1>
                <p style="text-align:center;">
                    Total : <xsl:value-of select="count(taches/tache)"/> tache(s)
                </p>

                <table border="1">
                    <tr bgcolor="#ffbdf2">
                        <th>ID</th>
                        <th>Titre</th>
                        <th>Description</th>
                        <th>Etat</th>
                        <th>Priorite</th>
                        <th>Date</th>
                    </tr>

                    <!-- Boucle sur chaque tache -->
                    <xsl:for-each select="taches/tache">
                        <tr>
                            <td><xsl:value-of select="@id"/></td>
                            <td><strong><xsl:value-of select="titre"/></strong></td>
                            <td><xsl:value-of select="description"/></td>
                            <td>
                                <!-- Mise en forme conditionnelle de l'etat -->
                                <xsl:choose>
                                    <xsl:when test="etat = 'A faire'">
                                        <span class="etat-afaire"><xsl:value-of select="etat"/></span>
                                    </xsl:when>
                                    <xsl:when test="etat = 'En cours'">
                                        <span class="etat-encours"><xsl:value-of select="etat"/></span>
                                    </xsl:when>
                                    <xsl:when test="etat = 'Terminee'">
                                        <span class="etat-terminee"><xsl:value-of select="etat"/></span>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="etat"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </td>
                            <td>
                                <!-- Mise en forme conditionnelle de la priorite -->
                                <xsl:choose>
                                    <xsl:when test="@priorite = 'haute'">
                                        <span class="priorite-haute"><xsl:value-of select="@priorite"/></span>
                                    </xsl:when>
                                    <xsl:when test="@priorite = 'moyenne'">
                                        <span class="priorite-moyenne"><xsl:value-of select="@priorite"/></span>
                                    </xsl:when>
                                    <xsl:when test="@priorite = 'basse'">
                                        <span class="priorite-basse"><xsl:value-of select="@priorite"/></span>
                                    </xsl:when>
                                </xsl:choose>
                            </td>
                            <td><xsl:value-of select="dateCreation"/></td>
                        </tr>
                    </xsl:for-each>
                </table>

                <p class="footer">
                    Projet To-Do List XML 
    realise par: Khalid LAMACHI,Yasser FOUDIL,Salma MOUHNI, Houda MOUJANE.
                </p>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>