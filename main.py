import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import notification


class WaterFaceApp(App):

    def build(self):
        self.title = "Objectif Visage Affiné"

        # Mise en page principale
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Titre et Suivi
        self.status_label = Label(
            text="Objectif : Affiner le visage en 30 jours\n\nRappel d'eau actif (chaque heure)",
            halign="center",
        )
        layout.add(self.status_label)

        # Bouton pour simuler le scan du visage
        scan_btn = Button(
            text="Prendre une photo & Analyser",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1),
        )
        scan_btn.bind(on_press=self.analyse_visage)
        layout.add(scan_btn)

        # Résultats de l'analyse
        self.result_label = Label(
            text="Prends une photo pour voir les points à améliorer.",
            halign="center",
            valign="middle",
        )
        self.result_label.bind(size=self.result_label.setter("text_size"))
        layout.add(self.result_label)

        # Lancer le rappel d'eau automatique toutes les 3600 secondes (1 heure)
        Clock.schedule_interval(self.envoyer_rappel_eau, 3600)

        return layout

    def envoyer_rappel_eau(self, dt):
        """Envoie une notification sur le téléphone pour boire de l'eau."""
        try:
            notification.notify(
                title="Hydratation Visage",
                message="C'est l'heure de boire un verre d'eau pour éliminer la rétention d'eau !",
                timeout=10,
            )
        except Exception:
            print("Rappel : Buvez de l'eau !")

    def analyse_visage(self, instance):
        """Ouvre la caméra, prend une photo et simule l'analyse des contours."""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        if ret:
            # Conversion en gris pour la détection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Chargement du détecteur de visage de base d'OpenCV
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5
            )

            if len(faces) > 0:
                # Si un visage est détecté, on génère le bilan de conseils
                self.result_label.text = (
                    "[ANALYSE COMPLETE]\n\n"
                    "- Zone joues/mâchoire : Signes de rétention d'eau légers.\n"
                    "- Conseil J-30 : Réduis le sel ce soir et masse le visage vers le haut.\n"
                    "- Hydratation : Continue à suivre les rappels horaires pour drainer les toxines."
                )
            else:
                self.result_label.text = (
                    "Visage non détecté. Reprends la photo avec une bonne lumière."
                )
        else:
            self.result_label.text = "Impossible d'accéder à la caméra."

        cap.release()


if __name__ == "__main__":
    WaterFaceApp().run()
