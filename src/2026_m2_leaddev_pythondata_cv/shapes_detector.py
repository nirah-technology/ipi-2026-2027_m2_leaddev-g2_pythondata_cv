import cv2
import numpy as np

class ShapeDetector:
    def __init__(
            self, 
            epsilon_factor: float = 0.04, 
            square_tolerance: float = 0.08,
            circle_min_radius: float = 0.85):
        self.epsilon_factor = epsilon_factor
        self.square_tolerance = square_tolerance
        self.circle_min_radius = circle_min_radius

    def is_triangle(self, frame, contour: np.ndarray) -> bool:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, (self.epsilon_factor * perimeter), True)
        is_triangle = len(approx) == 3
        if (is_triangle):
            cv2.drawContours(frame, [contour], -1, (0, 255, 255), 2)
        return is_triangle


    def is_square(self, frame, contour: np.ndarray) -> bool:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, (self.epsilon_factor * perimeter), True)

        is_square = False
        if len(approx) == 4:
            x, y, width, height = cv2.boundingRect(approx)
            aspect_ratio = float(width) / height
            is_square = abs(1.0 - aspect_ratio) <= self.square_tolerance
            if is_square:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 1)
        return is_square


    def is_circle(self, frame, contour: np.ndarray) -> bool:

        if len(contour) < 8:
            return False

        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return False
        area = cv2.contourArea(contour)
        cirularite = (4 * np.pi * area) / (perimeter ** 2)
        is_circle = cirularite >= self.circle_min_radius

        if is_circle:
            cv2.drawContours(frame, [contour], -1, (255, 0, 255), 2)

        return is_circle

    def is_ellipse(self, frame, contour: np.ndarray) -> bool:

        # 1. Filtre anti-bruit : une vraie ellipse a un contour continu riche en points
        if len(contour) < 16:
            return False

        contour_area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if contour_area < 10 or perimeter == 0:
            return False

        # 2. Ajustement de l'ellipse
        # cv2.fitEllipse retourne un RotatedRect : Tuple[Point2f, Size2f, float]
        # - center : (x, y)
        # - size   : (largeur_totale, hauteur_totale)
        # - angle  : orientation en degrés
        center, size, angle = cv2.fitEllipse(contour)
        width, height = size

        if width == 0 or height == 0:
            return False

        # 3. Calcul de l'aire de l'ellipse théorique (Pi * demi-grand_axe * demi-petit_axe)
        ellipse_area = np.pi * (width / 2.0) * (height / 2.0)
        
        # Sécurité anti-division par zéro
        if ellipse_area == 0:
            return False

        ratio_area = contour_area / ellipse_area

        # 4. Tolérance de correspondance (ici 5%)
        ratio_threshold = 0.05
        correspond_a_ellipse = (1 - ratio_threshold <= ratio_area <= 1 + ratio_threshold)

        # 5. Exclusion du cercle (l'ellipse doit être écrasée)
        circularite = (4 * np.pi * contour_area) / (perimeter ** 2)
        nest_pas_un_cercle = circularite < self.circle_min_radius

        # 6. Validation finale
        is_valid_ellipse = correspond_a_ellipse and nest_pas_un_cercle

        # Bonus : Dessin de debug directement intégré si la frame est passée en argument
        if is_valid_ellipse and frame is not None:
            # cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
            # Optionnel : dessiner l'ellipse théorique pour comparer
            cv2.ellipse(frame, (center, size, angle), (0, 0, 255), 1)

        return is_valid_ellipse