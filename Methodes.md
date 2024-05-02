# Methodes
1. Detection Yolov8 entraine
2. Detection de movement > Deblattage > DeFMO > Detection Yolov8
3. Detection de movement > Deblattage > Parametrage de thresholds (taille / couleur) pour limiter aux balles > Echantillonage sur la trajectoire obtenu

### Detection
- Yolov8 > ROI
- Par soustraction du background (moyenne des frames precedentes) > ROI

### Autres
- DeFMO (Rozmunyi I / kornia X) > image defloute // Non concluant
- Deblattage > masque trajectoire / objet defloute

## Optimisations:
- Yolov8 :
  - Grossissement de l'objet pour une meilleur detection // Non concluant
- Detection de movement :
  - Limitation de la zone de recherche.
    - Exclusion des personnes ou autres objets (Yolov8) // Approuve Methode 3
    - Focus sur une zone au-dessus de la table
  - Exclue les ROIs detecte trop grandes / trop petites // Approuve Methode 3
  - Etablissement d'autres parametres pour valider la detection d'une balle de ping pong (couleur?) Solidity ? Circulariry ?
- DeFMO // Non concluant
- 