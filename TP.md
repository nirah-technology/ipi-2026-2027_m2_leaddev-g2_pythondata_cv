# **TP OpenCV : Traitement d'image et Analyse d'une Scène**

**Objectif :** Prendre en main les fonctionnalités de base d'OpenCV en Python (*RGB/HSV, filtrage, seuillage, contours*) pour automatiser la détection et le comptage d'objets dans une image.

**Prérequis :** Python 3.x, opencv-python, numpy, matplotlib.

### 

### **Étape 1 –  Chargement et Prise en Main**

> 1. Chargez une image de votre choix (ex. objets.jpg) avec cv2.imread().  
> 2. Affichez ses dimensions (hauteur, largeur, canaux) et son type de données avec NumPy.  
> 3. Affichez l'image dans une fenêtre avec cv2.imshow().  
> 4. **Attention :** OpenCV charge les images en **BGR** et non en RGB. Convertissez l'image en RGB et affichez-la avec matplotlib.pyplot. Observez la différence si vous n'effectuez pas la conversion.

### 

### **Étape 2 –  Espaces de Couleurs et Traitement du Bruit**

> 1. Convertissez l'image d'origine en niveaux de gris (cv2.COLOR\_BGR2GRAY).  
> 2. Appliquez un **flou gaussien** (cv2.GaussianBlur) avec un noyau de taille \$5 \\times 5\$ pour réduire le bruit.  
> 3. Comparez le résultat visuel du flou gaussien avec un **filtre médian** (cv2.medianBlur). Dans quel cas le filtre médian est-il plus adapté ?

### 

### **Étape 3 – Seuillage et Segmentations**

> 1. À partir de l'image en niveaux de gris floutée, appliquez un seuillage binaire manuel (cv2.threshold) pour isoler les objets du fond.  
> 2. Appliquez ensuite le **seuillage d'Otsu** (cv2.THRESH\_OTSU). Quel est l'avantage de cette méthode ?  
> 3. Convertissez l'image initiale dans l'espace **HSV** (cv2.COLOR\_BGR2HSV).  
> 4. À l'aide de la fonction cv2.inRange(), isolez uniquement les objets d'une couleur spécifique (ex. le rouge ou le bleu) en définissant une plage de teintes (\$H\$).

### 

### **Étape 4 – Détection de Contours et Comptage**

> 1. Sur l'image binaire obtenue à l'étape précédente, isolez les contours des objets avec cv2.findContours().  
> 2. Filtrez les contours par leur aire (cv2.contourArea()) afin d'éliminer le bruit résiduel (ex. garder uniquement les contours dont l'aire est supérieure à 100 pixels).  
> 3. Dessinez les contours retenus en vert sur l'image d'origine avec cv2.drawContours().  
> 4. Affichez dans la console le nombre total d'objets détectés.  
> 5. **Bonus :** Encadrez chaque objet détecté par une boîte englobante droite (cv2.boundingRect) et ajoutez un texte avec son identifiant (cv2.putText).

### 

### **Étape 5 – Exercice d'Application (À ne pas rendre)**

Développez un script autonome detecteur\_objets.py qui prend une image en entrée, applique la chaîne de traitement complète, puis sauvegarde l'image annotée sous resultat.png avec :

* Les objets encadrés en vert.  
* Le nombre total d'objets écrit en haut à gauche de l'image.