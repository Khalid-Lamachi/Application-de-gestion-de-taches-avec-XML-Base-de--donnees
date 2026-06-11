<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" encoding="UTF-8" />
<xsl:template match="/">
    <html>
        <head>
            <title>Liste des Taches</title>
        </head>
        <body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">

            <h1 style="color: #572a67; text-align: center;">
                Liste des Taches - To-Do List
            </h1>
        <p style="text-align:center;">
                Total : <xsl:value-of select="count(taches/tache)"/> tache(s)
            </p>
         <table border="1" style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background-color: #ffbdf2;">
                    <th style="padding: 10px; text-align: left;">ID</th>
                    <th style="padding: 10px; text-align: left;">Titre</th>
                    <th style="padding: 10px; text-align: left;">Description</th>
                    <th style="padding: 10px; text-align: left;">Etat</th>
                    <th style="padding: 10px; text-align: left;">Priorite</th>
                    <th style="padding: 10px; text-align: left;">Date</th>
                </tr>
             <xsl:for-each select="taches/tache">
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 8px;"><xsl:value-of select="@id"/></td>
                        <td style="padding: 8px;"><strong><xsl:value-of select="titre"/></strong></td>
                        <td style="padding: 8px;"><xsl:value-of select="description"/></td>
                        <td style="padding: 8px;">
                            <xsl:choose>
                                <xsl:when test="@etat = 'A faire'">
                                    <span style="color: black ; font-weight: bold;">
                                        <xsl:value-of select="@etat"/>
                                    </span>
                                </xsl:when>
                                <xsl:when test="@etat = 'En cours'">
                                    <span style="color: black; font-weight: bold;">
                                        <xsl:value-of select="@etat"/>
                                    </span>
                                </xsl:when>
                                <xsl:when test="@etat = 'Terminee'">
                                    <span style="color: black; font-weight: bold;">
                                        <xsl:value-of select="@etat"/>
                                    </span>
                                </xsl:when>
                            </xsl:choose>
                        </td>
                        <td style="padding: 8px;">
                            <xsl:choose>
                                <xsl:when test="@priorite = 'haute'">
                                    <span style="color: rgb(212, 81, 186); font-weight: bold;">
                                        <xsl:value-of select="@priorite"/>
                                    </span>
                                </xsl:when>
                                <xsl:when test="@priorite = 'moyenne'">
                                    <span style="color: rgb(239, 124, 216); font-weight: bold;">
                                        <xsl:value-of select="@priorite"/>
                                    </span>
                                </xsl:when>
                                <xsl:when test="@priorite = 'basse'">
                                    <span style="color: rgb(232, 157, 217); font-weight: bold;">
                                        <xsl:value-of select="@priorite"/>
                                    </span>
                                </xsl:when>
                            </xsl:choose>
                        </td>
                        <td style="padding: 8px;"><xsl:value-of select="dateCreation"/></td>
                    </tr>
                </xsl:for-each>
            </table>

            <p style="text-align: center; margin-top: 20px; color: gray; font-size: 0.8em;">
                Projet To-Do List XML realise par: Khalid LAMACHI, Yasser FOUDIL, Salma MOUHNI, Houda MOUJANE.
            </p>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>
