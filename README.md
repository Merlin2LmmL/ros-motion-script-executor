# 🤖 Dein erster ROS2-Knoten – Ein Schritt-für-Schritt-Tutorial

> **Zielgruppe:** Schülerinnen und Schüler mit Grundkenntnissen in Python, die noch keine Erfahrung mit Linux-Terminals oder ROS haben.
> **Ziel:** Am Ende dieses Tutorials hast du einen eigenen ROS2-Knoten gebaut, der einen (simulierten) Roboter bewegt!

---

## Inhaltsverzeichnis

1. [Linux-Grundlagen – Das Terminal verstehen](#1-linux-grundlagen--das-terminal-verstehen)
2. [ROS2 Jazzy installieren](#2-ros2-jazzy-installieren)
3. [Erste Schritte mit ROS2](#3-erste-schritte-mit-ros2)
4. [Ein ROS2-Paket erstellen](#4-ein-ros2-paket-erstellen)
5. [Den Knoten programmieren](#5-den-knoten-programmieren)
6. [Paket bauen mit Colcon](#6-paket-bauen-mit-colcon)
7. [Den Knoten testen – mit echtem Simulator!](#7-den-knoten-testen--mit-echtem-simulator)
8. [Bonus: JSON-Befehlsdateien](#8-bonus-json-befehlsdateien)

---

## 1. Linux-Grundlagen – Das Terminal verstehen

Bevor wir irgendetwas mit ROS machen können, müssen wir uns mit dem wichtigsten Werkzeug vertraut machen: dem **Terminal** (auch „Kommandozeile" oder „Shell" genannt).

Das Terminal ist kein Relikt aus der Steinzeit. In der Robotik, Systemadministration und Softwareentwicklung ist es das Zuhause der Profis. Du wirst es lieben lernen (müssen).

### Das Terminal öffnen

Auf Ubuntu kannst du das Terminal öffnen mit:
- **Tastenkombination:** `Strg + Alt + T`
- **Oder:** Rechtsklick auf den Desktop → „Open Terminal"
- **Oder:** Im App-Menü nach „Terminal" suchen

Du siehst dann so etwas:
```
deinname@deincomputer:~$
```
Das `~` steht für dein **Home-Verzeichnis** (`/home/deinname`). Das `$` zeigt an, dass du als normaler Benutzer eingeloggt bist.

---

### Die wichtigsten Befehle

#### Wo bin ich?
```bash
pwd
```
`pwd` steht für *Print Working Directory* – es zeigt dir, in welchem Ordner du dich gerade befindest.

#### Was ist hier drin?
```bash
ls
ls -l        # Detailansicht (Größe, Datum, Berechtigungen)
ls -la       # Auch versteckte Dateien anzeigen (beginnen mit .)
```

#### Ordner wechseln
```bash
cd Dokumente          # In den Ordner "Dokumente" wechseln
cd ..                 # Einen Ordner nach oben
cd ~                  # Direkt ins Home-Verzeichnis
cd /home/deinname/ros2_ws   # Absoluter Pfad
```

> 💡 **Tipp – Tab-Vervollständigung:** Wenn du den Anfang eines Ordner- oder Dateinamens tippst und dann `Tab` drückst, vervollständigt das Terminal automatisch! Wenn es mehrere Möglichkeiten gibt, drücke `Tab` zweimal und alle Optionen werden angezeigt. Das spart enorm viel Zeit!

#### Ordner erstellen
```bash
mkdir mein_ordner
mkdir -p pfad/zu/tiefem/ordner    # Erstellt alle Zwischenordner
```

#### Dateien und Ordner löschen
```bash
rm datei.txt              # Datei löschen
rm -r ordner/             # Ordner (und Inhalt) löschen
rm -rf ordner/            # Erzwungen löschen (VORSICHT! Kein Papierkorb!)
```

> ⚠️ **Achtung:** `rm` löscht dauerhaft, ohne Rückfrage. Es gibt keinen Papierkorb im Terminal! Führe niemals wahllos dir unbekannte Befehle aus dem Internet aus, die Wörter wie sudo, rm und -fr beinhalten. Die können **sehr** böse enden!

#### Dateien anzeigen und bearbeiten
```bash
cat datei.txt             # Inhalt ausgeben
nano datei.txt            # Datei im Terminal-Editor öffnen
```

**Nano** ist ein einfacher Texteditor, der direkt im Terminal läuft. Die wichtigsten Nano-Tasten:
- `Strg + O` → Speichern (dann `Enter` bestätigen)
- `Strg + X` → Beenden
- `Strg + K` → Zeile ausschneiden
- `Strg + W` → Suchen

---

### Sudo – Administratorrechte

Manche Befehle brauchen Administratorrechte. Dafür gibt es `sudo` (*Super User Do* bzw. *Substitute User Do* laut Linus):

```bash
sudo apt install irgendwas
```

> 🔐 **Wichtig:** Wenn du nach deinem Passwort gefragt wirst, siehst du **gar nichts** beim Tippen – keine Sterne, keine Punkte. Das ist normal! Tippe dein Passwort und drücke `Enter`.

---

### Prozesse stoppen

Wenn ein Programm im Terminal läuft und du es stoppen möchtest:
- `Strg + C` → Programm sofort beenden (das wirst du sehr oft brauchen!)

---

### Text kopieren und einfügen im Terminal

Das normale `Strg + C` / `Strg + V` funktioniert im Terminal **nicht** (da `Strg + C` ja Prozesse beendet!). Stattdessen:
- **Kopieren:** Text markieren (mit dem Cursor) → `Strg + SHIFT + C`
- **Einfügen:** `Strg + SHIFT + V`

---

### Mehrere Terminals gleichzeitig

Du wirst im Laufe dieses Tutorials mehrere Terminal-Fenster gleichzeitig brauchen. Du kannst entweder:
- Mehrere Terminal-Fenster nebeneinander öffnen
- Oder in einem Terminal-Fenster mit `Strg + Alt + T` ein neues öffnen

---

### Schnell-Referenz: Die wichtigsten Befehle

| Befehl | Bedeutung |
|--------|-----------|
| `pwd` | Aktuellen Pfad anzeigen |
| `ls` | Verzeichnisinhalt auflisten |
| `cd <ordner>` | Verzeichnis wechseln |
| `mkdir <name>` | Ordner erstellen |
| `rm <datei>` | Datei löschen |
| `cat <datei>` | Dateiinhalt anzeigen |
| `nano <datei>` | Datei bearbeiten |
| `Tab` | Autovervollständigung |
| `Strg + C` | Programm beenden |
| `Strg + Shift + V` | Einfügen im Terminal |
| `sudo <befehl>` | Als Administrator ausführen |

---

## 2. ROS2 Jazzy installieren

### Was ist ROS2 überhaupt?

**ROS** steht für *Robot Operating System* – aber es ist eigentlich kein Betriebssystem im klassischen Sinne, sondern ein **Framework** (ein Gerüst aus Werkzeugen, Bibliotheken und Konventionen), das die Entwicklung von Robotersoftware massiv vereinfacht.

Stell dir vor, du baust einen Roboter. Er hat Sensoren (Kamera, Lidar, GPS), Aktoren (Motoren, Greifer) und braucht eine Software, die alles koordiniert. ROS gibt dir:
- Einen standardisierten Weg, wie verschiedene Programmteile miteinander **kommunizieren**
- Fertige Treiber für Hunderte von Sensoren und Motoren
- Werkzeuge zum Visualisieren, Debuggen und Aufzeichnen von Daten
- Eine riesige Community und viele fertige Pakete

**ROS2 Jazzy** ist die aktuelle stabile Version (Stand 2024/2025), optimiert für Ubuntu 24.04.

### Installation

Die Installation von ROS2 ist normalerweise ein mühsamer Prozess mit vielen Schritten. Wir verwenden mein **Installations-Skript**, das alles automatisch erledigt.

Öffne ein Terminal und führe folgenden Befehl aus (alles in einer Zeile, oder kopiere den Block wie er ist):

```bash
curl -fsSL https://raw.githubusercontent.com/Merlin2LmmL/ROS2-Jazzy-Install-Script/refs/heads/main/ros2-jazzy-installer.sh \
  -o ros2-jazzy-installer.sh \
  && chmod +x ros2-jazzy-installer.sh \
  && ./ros2-jazzy-installer.sh
```

> Was macht dieser Befehl?
> - `curl -fsSL ...` lädt das Skript herunter
> - `-o ros2-jazzy-installer.sh` speichert es unter diesem Namen
> - `chmod +x` macht es ausführbar (wie eine `.exe` unter Windows)
> - `./ros2-jazzy-installer.sh ...` führt es aus


Die Installation dauert je nach Internetgeschwindigkeit und Rechner **2–10 Minuten**.

### Den Workspace einrichten

Nach der Installation brauchen wir einen **Workspace**. Das ist der Hauptordner, in dem alle deine ROS2-Projekte liegen werden.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

> Das `~` ist eine Abkürzung für `/home/deinbenutzername`. Du kannst den Workspace auch anders nennen, z.B. `ros2_jazzy_ws`.

### Umgebung sourcen

ROS2 stellt viele Befehle und Umgebungsvariablen bereit. Damit das Terminal diese kennt, müssen wir die ROS2-Umgebung einmalig **sourcen** (aktivieren):

```bash
source /opt/ros/jazzy/setup.bash
```

> 💡 **Tipp:** Du musst das in jedem neuen Terminal-Fenster wiederholen. Um das zu automatisieren, füge diese Zeile zu deiner `~/.bashrc` hinzu (diese Datei wird bei jedem neuen Terminal automatisch ausgeführt):
> ```bash
> echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
> source ~/.bashrc
> ```

Teste die Installation mit:
```bash
ros2 --version
```
Du solltest etwas wie `ros2 jazzy` sehen. 🎉

---

## 3. Erste Schritte mit ROS2

### Das wichtigste Konzept: Nodes, Topics und Messages

ROS2 basiert auf einem einfachen, aber mächtigen Konzept:

```
[Node A] ──publiziert Nachrichten──▶ [Topic] ──empfängt Nachrichten──▶ [Node B]
```

- **Node (Knoten):** Ein eigenständiges Programm, das eine bestimmte Aufgabe erfüllt (z.B. einen Motor ansteuern, Kamerabilder verarbeiten, Entscheidungen treffen)
- **Topic:** Ein benannter Kommunikationskanal. Nodes können Topics **publizieren** (senden) oder **subscriben** (empfangen)
- **Message:** Das Datenformat, das über ein Topic geschickt wird (z.B. eine Geschwindigkeit, ein Bild, ein Sensorwert)

Das ist wie ein **Schwarzes Brett**: Jeder kann Zettel anpinnen (publizieren) und jeder kann Zettel lesen (subscriben). Das "Schwarze Brett" selbst ist das Topic.

### Nützliche ROS2-Befehle

```bash
ros2 --help              # Alle verfügbaren Unterbefehle anzeigen
ros2 node list           # Alle laufenden Nodes anzeigen
ros2 topic list          # Alle aktiven Topics anzeigen
ros2 topic echo /topic   # Nachrichten auf einem Topic live anzeigen
ros2 topic info /topic   # Infos über ein Topic
```

### Turtlesim – ROS2's „Hello World"

Turtlesim ist ein kleines Demoprogramm, das mit ROS2 mitgeliefert wird: eine Schildkröte auf dem Bildschirm, die du über ROS2-Topics steuern kannst. Perfekt zum Lernen!

Du brauchst **drei Terminal-Fenster** gleichzeitig:

**Terminal 1 – Starte die Simulation:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 – Starte die Steuerung:**
```bash
ros2 run turtlesim turtle_teleop_key
```
Klicke in Terminal 2 und steuere die Schildkröte mit den Pfeiltasten!

**Terminal 3 – Schaue, was passiert:**
```bash
ros2 topic list
```

Du siehst mehrere Topics, unter anderem `/turtle1/cmd_vel`. Das ist der Kanal, über den Bewegungsbefehle gesendet werden!

Jetzt sieh dir an, was gesendet wird, wenn du die Schildkröte steuerst:
```bash
ros2 topic echo /turtle1/cmd_vel
```

Du wirst Ausgaben wie diese sehen:
```
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
```

Das ist eine **Twist-Message** – das Standardformat für Geschwindigkeitsbefehle in ROS2. `linear.x` ist die Vorwärtsbewegung, `angular.z` ist die Drehung. Merke dir das – wir werden es gleich selbst verwenden!

---

## 4. Ein ROS2-Paket erstellen

### Was ist ein Paket?

In ROS2 wird Code in **Paketen** organisiert. Ein Paket ist ein strukturierter Ordner mit deinem Code plus Metadaten (Name, Abhängigkeiten, Lizenz). Pakete haben viele Vorteile:
- Einfaches Teilen und Wiederverwenden
- Standardisierte Struktur
- Automatische Abhängigkeitsverwaltung
- `ros2 run` kann deine Nodes einfach finden

### Paket erstellen

Navigiere zunächst in den `src`-Ordner deines Workspaces:
```bash
cd ~/ros2_ws/src
```

Dann erstelle dein Paket. Ersetze die Platzhalter `<...>` mit deinen eigenen Angaben:

```bash
ros2 pkg create <paketname> \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs std_msgs \
  --license MIT \
  --maintainer-name "<Dein Name>" \
  --maintainer-email "<deine@email.de>" \
  --description "<Beschreibe, was dein Paket macht>" \
  --node-name <node_name>
```

**Beispiel (verwende deine eigenen Angaben!):**
```bash
ros2 pkg create mein_roboter_paket \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs std_msgs \
  --license MIT \
  --maintainer-name "Max Mustermann" \
  --maintainer-email "max@beispiel.de" \
  --description "Mein erster ROS2-Knoten, der einen Roboter bewegt." \
  --node-name bewegungssteuerung
```

> 💡 Paket- und Knotennamen sollten **nur Kleinbuchstaben, Zahlen und Unterstriche** enthalten (keine Leerzeichen, keine Umlaute).

### Die Paketstruktur erkunden

Wechsle in dein neues Paket und schau dir die Struktur an:
```bash
cd ~/ros2_ws/src/<paketname>
ls -la
```

Du siehst:
```
<paketname>/
├── package.xml          ← Metadaten (Name, Abhängigkeiten, Lizenz)
├── resource/
│   └── <paketname>      ← Marker-Datei für ROS2
├── setup.cfg            ← Konfiguration für ros2 run
├── setup.py             ← Python-Installationsanleitung
└── <paketname>/
    ├── __init__.py      ← Macht den Ordner zu einem Python-Paket
    └── <node_name>.py   ← HIER kommt dein Code!
```
> Solche sogenannten Verzeichnis Bäume kannst du dir auch ausgeben lassen mit dem Befehl `tree -L n`, wobei n die Anzahl der "Zweige" im Baum ist also wie Tief du in jeden Ordner maximal hineintauchen möchtest,

Öffne die Node-Datei und schau sie dir an:
```bash
nano <paketname>/<node_name>.py
```

Da steht schon ein bisschen Boilerplate-Code. Wir werden diese Datei jetzt komplett neu befüllen!

---

## 5. Den Knoten programmieren

Dies ist das Herzstück des Tutorials. Wir schreiben einen ROS2-Knoten, der eine Sequenz von Bewegungsbefehlen ausführt – wie ein kleines Programm, das dem Roboter sagt: „Fahre 2 Sekunden geradeaus, drehe dich, fahre nochmals geradeaus, stoppe."

### Was soll unser Knoten können?

Bevor wir coden, planen wir. Unser Knoten soll:

1. Eine Liste von Bewegungsanweisungen enthalten (z.B. „fahre 2 Sek. vorwärts, dann drehe dich 1,5 Sek.")
2. Diese Anweisungen nacheinander ausführen
3. Dafür Nachrichten an das Topic `/cmd_vel` schicken
4. Am Ende stoppen

### Die wichtigsten Konzepte vorab

#### Twist – Das Nachrichtenformat für Bewegung

Eine `Twist`-Nachricht hat zwei Teile:
- `linear`: Geschwindigkeit in x (vorwärts/rückwärts), y (seitwärts), z (hoch/runter) in **Meter pro Sekunde**
- `angular`: Drehrate um x (nicken), y (rollen), z (drehen) in **Radiant pro Sekunde**

Für die meisten Bodenroboter sind nur `linear.x` (Vorwärtsfahrt) und `angular.z` (Drehen) relevant.

```
linear.x  > 0  → vorwärts
linear.x  < 0  → rückwärts
angular.z > 0  → Drehung links (gegen den Uhrzeigersinn)
angular.z < 0  → Drehung rechts (im Uhrzeigersinn)
```

#### rclpy – Die ROS2-Bibliothek für Python

`rclpy` ist die offizielle Python-Bibliothek für ROS2. Du importierst sie, um:
- ROS2 zu initialisieren
- Nodes zu erstellen
- Publisher anzulegen
- Nachrichten zu verschicken
- Den Logger zu benutzen

📖 **Ressourcen:**
- [rclpy API-Dokumentation](https://docs.ros2.org/latest/api/rclpy/)
- [ROS2 Python-Tutorial (offiziell)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [geometry_msgs/Twist Dokumentation](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)

---

### Das Grundgerüst – dein Startpunkt

Ersetze den Inhalt von `<paketname>/<node_name>.py` mit diesem Grundgerüst. Öffne die Datei zuerst:

```bash
nano ~/ros2_ws/src/<paketname>/<paketname>/<node_name>.py
```

Kopiere dieses Grundgerüst hinein (es enthält bewusst Lücken, die du füllen sollst!):

```python
#!/usr/bin/env python3
"""
Bewegungssteuerung – ROS2 Node
================================
Führt eine Sequenz von Bewegungsanweisungen aus,
indem Nachrichten an /cmd_vel publiziert werden.
"""

import time
import sys

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


# =============================================================================
# AUFGABE 1: Definiere deine Bewegungsanweisungen hier!
# =============================================================================
#
# Jede Anweisung ist ein Dictionary mit diesen Schlüsseln:
#   "aktion"     (str)   : Ein beschreibender Name (nur für die Log-Ausgabe)
#   "linear_x"   (float) : Vorwärts-Geschwindigkeit in m/s (negativ = rückwärts)
#   "angular_z"  (float) : Drehgeschwindigkeit in rad/s (positiv = links)
#   "dauer"      (float) : Wie lange diese Anweisung ausgeführt wird (in Sekunden)
#
# Zum Vergleich: Die Turtlesim-Schildkröte verwendet Werte bis ~2.0 m/s.
# Ein echter Roboter fährt je nach Modell 0.1 bis 1.0 m/s.
#
# Beispiel (anpassen und erweitern!):
ANWEISUNGEN = [
    # TODO: Füge deine eigenen Anweisungen ein!
    # Tipp: Fange mit einfachen Bewegungen an und teste sie.
    {"aktion": "vorwaerts",  "linear_x":  ???, "angular_z":  ???, "dauer": ???},
    {"aktion": "links",      "linear_x":  ???, "angular_z":  ???, "dauer": ???},
    {"aktion": "stop",       "linear_x":  0.0, "angular_z":  0.0, "dauer": 0.5},
]


class BewegungsNode(Node):
    """
    ROS2-Node, der Bewegungsanweisungen sequenziell ausführt.
    
    Diese Klasse erbt von rclpy.node.Node – das macht sie zu einem
    vollwertigen ROS2-Knoten.
    """

    # Wie oft pro Sekunde schicken wir eine Nachricht? (Frequenz in Hz)
    PUBLISH_FREQUENZ = 10

    def __init__(self):
        # =============================================================================
        # AUFGABE 2: Node initialisieren
        # =============================================================================
        # Der Node braucht einen eindeutigen Namen. Dieser Name erscheint in
        # `ros2 node list`. Übergib ihn an super().__init__().
        #
        # Dokumentation: https://docs.ros2.org/latest/api/rclpy/api/node.html
        super().__init__("???")  # TODO: Gib deinem Node einen sinnvollen Namen!

        # Informiere den Benutzer, dass der Node gestartet ist
        self.get_logger().info(
            f"Node gestartet. {len(ANWEISUNGEN)} Anweisung(en) geladen."
        )

        # =============================================================================
        # AUFGABE 3: Publisher erstellen
        # =============================================================================
        # Ein Publisher sendet Nachrichten an ein bestimmtes Topic.
        # Wir brauchen einen Publisher für das Topic "/cmd_vel".
        #
        # Syntax:
        #   self.create_publisher(<NachrichtenTyp>, "<topic_name>", <queue_size>)
        #
        # - NachrichtenTyp: Twist (aus geometry_msgs.msg)
        # - topic_name: "/cmd_vel"
        # - queue_size: 10 (wie viele Nachrichten gepuffert werden)
        #
        # Dokumentation: https://docs.ros2.org/latest/api/rclpy/api/node.html#rclpy.node.Node.create_publisher
        
        self._publisher = self.create_publisher(???, ???, ???)  # TODO!

        # Starte die Ausführung kurz nach dem Start
        # (0.5 Sekunden Wartezeit, damit der Node vollständig initialisiert ist)
        self._timer = self.create_timer(0.5, self._starte_ausfuehrung)

    def _erstelle_twist(self, anweisung: dict) -> Twist:
        """
        Wandelt ein Anweisungs-Dictionary in eine Twist-Nachricht um.
        
        Args:
            anweisung: Ein Dictionary mit Schlüsseln wie "linear_x", "angular_z"
            
        Returns:
            Eine Twist-Nachricht, bereit zum Publizieren
        """
        # =============================================================================
        # AUFGABE 4: Twist-Nachricht erstellen
        # =============================================================================
        # Erstelle eine neue Twist-Nachricht und befülle sie mit den Werten
        # aus dem anweisung-Dictionary.
        #
        # Eine Twist-Nachricht hat diese Felder:
        #   msg.linear.x   (float) ← Vorwärtsgeschwindigkeit
        #   msg.linear.y   (float) ← Seitwärtsgeschwindigkeit (meist 0)
        #   msg.linear.z   (float) ← Vertikalgeschwindigkeit (meist 0)
        #   msg.angular.x  (float) ← Nickrate (meist 0)
        #   msg.angular.y  (float) ← Rollrate (meist 0)
        #   msg.angular.z  (float) ← Drehrate (links/rechts)
        #
        # Tipp: Verwende .get("schluessel", standardwert) – falls ein Schlüssel
        # im Dictionary fehlt, wird der Standardwert verwendet.
        # Beispiel: anweisung.get("linear_x", 0.0)
        
        msg = Twist()
        
        # TODO: Fülle die Felder der msg mit den Werten aus dem Dictionary!
        msg.linear.x  = ???
        msg.angular.z = ???
        # Alle anderen Felder bleiben 0.0 (Standardwert bei Twist)
        
        return msg

    def _fuehre_anweisung_aus(self, index: int, anweisung: dict) -> None:
        """
        Führt eine einzelne Anweisung für die angegebene Dauer aus.
        
        Args:
            index: Position der Anweisung in der Liste (für die Anzeige)
            anweisung: Das Anweisungs-Dictionary
        """
        # =============================================================================
        # AUFGABE 5: Anweisung ausführen
        # =============================================================================
        # Diese Funktion soll:
        # 1. Die Werte aus dem Dictionary lesen (Aktion, Dauer, Geschwindigkeiten)
        # 2. Eine Log-Nachricht ausgeben (welche Anweisung läuft gerade?)
        # 3. Die Twist-Nachricht erstellen (benutze _erstelle_twist!)
        # 4. Die Nachricht für die angegebene Dauer wiederholt publizieren
        #
        # Tipp für Schritt 4:
        # - Berechne das Zeitintervall: intervall = 1.0 / self.PUBLISH_FREQUENZ
        # - Berechne den Endzeitpunkt: endzeit = time.time() + dauer
        # - Solange time.time() < endzeit: publiziere und schlafe kurz
        #
        # Zur Erinnerung:
        # - self.get_logger().info("Nachricht")  ← Ausgabe im Terminal
        # - self._publisher.publish(nachricht)   ← Nachricht senden
        # - time.sleep(sekunden)                 ← Kurz warten
        
        aktion = anweisung.get("aktion", f"schritt_{index}")
        dauer  = float(anweisung["dauer"])
        
        # TODO: Log-Ausgabe (z.B.: "[1/5] 'vorwaerts' für 2.0s")
        self.get_logger().info(???)
        
        # TODO: Twist erstellen
        twist = ???
        
        # TODO: Nachricht für die Dauer "dauer" in einer Schleife publizieren
        # ...

    def _sende_stopp(self) -> None:
        """
        Sendet einen Stopp-Befehl (alle Geschwindigkeiten auf 0).
        Wichtig: Ohne diesen Befehl fährt ein echter Roboter weiter!
        """
        # =============================================================================
        # AUFGABE 6: Stopp-Befehl senden
        # =============================================================================
        # Erstelle eine leere Twist-Nachricht und publiziere sie.
        # Eine leere Twist-Nachricht hat automatisch alle Felder auf 0.0 gesetzt.
        
        # TODO: Stopp senden!
        self._publisher.publish(???)
        self.get_logger().info("Stopp-Befehl gesendet (alle Geschwindigkeiten = 0).")

    def _starte_ausfuehrung(self) -> None:
        """
        Wird einmalig nach dem Node-Start aufgerufen.
        Führt alle Anweisungen der Reihe nach aus.
        """
        # Der einmalige Timer wird nicht mehr gebraucht
        self._timer.cancel()

        try:
            # =============================================================================
            # AUFGABE 7: Alle Anweisungen ausführen
            # =============================================================================
            # Iteriere über alle Anweisungen in ANWEISUNGEN und rufe
            # für jede _fuehre_anweisung_aus() auf.
            #
            # Tipp: enumerate() gibt dir gleichzeitig Index und Wert:
            #   for i, anweisung in enumerate(ANWEISUNGEN):
            
            # TODO: Schleife über alle Anweisungen!
            
            self.get_logger().info("Alle Anweisungen abgeschlossen!")

        except KeyboardInterrupt:
            # Der Benutzer hat Strg+C gedrückt
            self.get_logger().info("Durch Benutzer unterbrochen.")
        finally:
            # Immer stoppen am Ende (egal ob fertig oder unterbrochen!)
            self._sende_stopp()
            rclpy.shutdown()


# =============================================================================
# Einstiegspunkt – hier startet das Programm
# =============================================================================

def main(args=None) -> None:
    """Initialisiert ROS2 und startet den Node."""
    rclpy.init(args=args)
    node = BewegungsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

### Deine Aufgaben – Schritt für Schritt

Fülle alle `???`-Stellen aus. Hier sind die Aufgaben nochmal übersichtlich zusammengefasst:

| # | Aufgabe | Hinweis |
|---|---------|---------|
| 1 | `ANWEISUNGEN` befüllen | Denke dir eine sinnvolle Bewegungssequenz aus. Mindestens 4 Anweisungen! |
| 2 | Node benennen | `super().__init__("dein_node_name")` |
| 3 | Publisher erstellen | `self.create_publisher(Twist, "/cmd_vel", 10)` |
| 4 | Twist-Nachricht befüllen | `msg.linear.x = anweisung.get("linear_x", 0.0)` |
| 5 | Anweisung ausführen | Schleife mit `time.time()` und `time.sleep()` |
| 6 | Stopp senden | `Twist()` erzeugt automatisch eine Null-Nachricht |
| 7 | Alle Anweisungen iterieren | `for i, a in enumerate(ANWEISUNGEN):` |

---

### Hilfreiche Code-Schnipsel

Falls du nicht weiterkommst, hier einige Bausteine (ohne die Lösung direkt zu verraten):

**Wie man eine Log-Nachricht formatiert:**
```python
self.get_logger().info(f"[{index + 1}/{len(ANWEISUNGEN)}] Führe '{aktion}' aus für {dauer:.1f}s")
```

**Wie eine Zeitschleife funktioniert:**
```python
endzeit = time.time() + dauer          # Berechne, wann wir fertig sind
intervall = 1.0 / self.PUBLISH_FREQUENZ  # z.B. 0.1 Sek. bei 10 Hz

while time.time() < endzeit:           # Solange die Zeit nicht abgelaufen ist:
    self._publisher.publish(nachricht)  # Nachricht senden
    time.sleep(intervall)               # Kurz warten
```

**Was `enumerate()` macht:**
```python
früchte = ["Apfel", "Banane", "Kirsche"]
for i, frucht in enumerate(früchte):
    print(f"{i}: {frucht}")
# Ausgabe:
# 0: Apfel
# 1: Banane
# 2: Kirsche
```

---

### Teste frühzeitig!

Du musst nicht alles fertig haben, um zu testen! Sobald du die Aufgaben 1–3 erledigt hast, kannst du schon zum nächsten Schritt springen, bauen und schauen, ob dein Publisher überhaupt Nachrichten sendet. Mit `ros2 topic echo /cmd_vel` kannst du das überprüfen – du musst dafür noch kein Simulator laufen haben.

---

### Hinweise für Fortgeschrittene (optional)

Wenn du alles fertig hast und noch mehr ausprobieren möchtest:

- **Parameter:** Kannst du die Anweisungsliste über einen ROS2-Parameter übergeben?
- **Logging:** Füge mehr Details zur Log-Ausgabe hinzu (aktuelle Geschwindigkeit, verbleibende Zeit)
- **Validierung:** Was passiert, wenn eine Anweisung kein `dauer`-Feld hat? Fange das ab!

---

## 6. Paket bauen mit Colcon

### Was ist Colcon?

**Colcon** ist das Build-System von ROS2. Es kompiliert und installiert deine Pakete in eine standardisierte Verzeichnisstruktur, sodass `ros2 run` und andere ROS2-Werkzeuge deine Nodes finden können.

Auch wenn Python-Code nicht wirklich „kompiliert" wird (Python ist interpretiert), braucht ROS2 den Build-Schritt trotzdem:
- Es werden symbolische Links und Konfigurationsdateien erstellt
- Entry Points werden registriert (damit `ros2 run` deine Node findet)
- Abhängigkeiten werden geprüft

### Immer aus dem Workspace-Root bauen!

> ⚠️ **Wichtig:** Führe `colcon build` **immer** aus dem Wurzelverzeichnis deines Workspaces aus (`~/ros2_ws`), nicht aus einem Unterordner! Sonst entstehen die `build/`, `install/` und `log/`-Ordner an der falschen Stelle.

```bash
cd ~/ros2_ws
```

### Das Paket bauen

Nur dein Paket bauen (schneller als alles zu bauen):
```bash
colcon build --packages-select <paketname>
```

Oder alles bauen:
```bash
colcon build
```

Eine erfolgreiche Ausgabe sieht so aus:
```
Starting >>> <paketname>
Finished <<< <paketname> [0.66s]          

Summary: 1 package finished [0.77s]
```

Falls Fehler auftauchen:
- `SyntaxError`: Python-Syntaxfehler in deinem Code – öffne die Datei und prüfe die markierte Zeile
- `ModuleNotFoundError`: Eine Abhängigkeit fehlt – prüfe `package.xml` und `setup.py`
- `KeyError`: Ein Dictionary-Schlüssel fehlt – prüfe deine `ANWEISUNGEN`

### Umgebung nach dem Bauen sourcen

Nach jedem Build **muss** du die Umgebung neu sourcen, damit ROS2 dein frisch gebautes Paket findet:

```bash
source install/setup.bash
```

> 💡 Tipp: Du kannst das auch automatisieren. Füge diese Zeile zu deiner `~/.bashrc` hinzu:
> ```bash
> source ~/ros2_ws/install/setup.bash
> ```
> Dann musst du es nur einmalig nach dem Start tun.

---

## 7. Den Knoten testen – mit echtem Simulator!

### Einfacher Test: Publiziert dein Node überhaupt?

Öffne zwei Terminal-Fenster:

**Terminal 1 – Node starten:**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run <paketname> <node_name>
```

**Terminal 2 – Nachrichten überwachen:**
```bash
ros2 topic echo /cmd_vel
```

Wenn alles korrekt ist, siehst du in Terminal 2 Nachrichten wie:
```yaml
linear:
  x: 0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
```

Super! Dein Node publiziert! Jetzt bringen wir einen echten (simulierten) Roboter zum Fahren.

---

### Den OHM-Mecanum-Simulator installieren

Die OHM Technische Hochschule Nürnberg hat einen 2D-Robotersimulator entwickelt, der sich perfekt für unsere Zwecke eignet. Wir installieren ihn als weiteres ROS2-Paket:

```bash
# 1. Quellcode herunterladen
cd ~/ros2_ws/src
git clone --branch ros2 https://github.com/autonohm/ohm_mecanum_sim.git

# 2. Workspace bauen
cd ~/ros2_ws
colcon build --symlink-install

# 3. Umgebung sourcen
source install/setup.bash

# 4. Pygame installieren (das Grafikframework für den Simulator)
pip3 install pygame --break-system-packages
```

### Das richtige Topic herausfinden

Starte den Simulator:
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

Ein Fenster mit dem Roboter öffnet sich. Jetzt finden wir heraus, welches Topic der Simulator für Bewegungsbefehle verwendet:

```bash
ros2 topic list
```

Du siehst eine Liste von Topics. Schau dir sie genau an – welches Topic klingt nach einem Bewegungsbefehl? Schaue, welches den Namen `cmd_vel` enthält...

> 🔍 **Aufgabe:** Finde das richtige `cmd_vel`-Topic des Simulators! (Hinweis: Es ist nicht `/cmd_vel`)

Du kannst auch mehr Informationen über ein Topic bekommen:
```bash
ros2 topic info /<topic_name>
```

---

### Alles zusammen starten

Sobald du das richtige Topic kennst, starte alles in drei Terminals:

**Terminal 1 – Dein Node (mit dem richtigen Topic!):**
```bash
ros2 run <paketname> <node_name> --ros-args \
  -p cmd_vel_topic:=/<das_richtige_topic>
```

> Warte – dein Node hat doch gar keinen `cmd_vel_topic`-Parameter! Das stimmt. Das ist eine optionale Erweiterungsaufgabe: Kannst du deinen Node so erweitern, dass das Topic über einen Parameter konfigurierbar ist?
>
> Alternativ: Ändere einfach `/cmd_vel` direkt im Code auf das richtige Topic.

**Terminal 2 – Der Simulator:**
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

**Terminal 3 (optional) – Topic überwachen:**
```bash
ros2 topic echo /<das_richtige_topic>
```

Wenn alles klappt, siehst du den Roboter im Simulator-Fenster die Bewegungen aus deiner `ANWEISUNGEN`-Liste ausführen! 🎉

---

## 8. Bonus: JSON-Befehlsdateien

Bisher sind unsere Anweisungen direkt im Python-Code eingebaut. Das ist unpraktisch: Jedes Mal, wenn wir die Route ändern wollen, müssen wir den Code editieren und neu bauen.

Eine elegantere Lösung: Die Anweisungen in einer **JSON-Datei** speichern und diese dem Node übergeben.

### Was ist JSON?

JSON (*JavaScript Object Notation*) ist ein einfaches Textformat für strukturierte Daten. Es sieht Python-Dictionaries sehr ähnlich:

```json
[
  {"aktion": "vorwaerts",  "linear_x": 0.3, "angular_z":  0.0, "dauer": 2.0},
  {"aktion": "links",      "linear_x": 0.0, "angular_z":  0.5, "dauer": 1.5},
  {"aktion": "vorwaerts",  "linear_x": 0.3, "angular_z":  0.0, "dauer": 2.0},
  {"aktion": "stopp",      "linear_x": 0.0, "angular_z":  0.0, "dauer": 0.5}
]
```

Speichere das in einer Datei, z.B. `~/meine_route.json`.

### JSON in Python laden

```python
import json

with open("/pfad/zur/datei.json", "r") as f:
    anweisungen = json.load(f)
```

Das war's! `json.load()` wandelt die JSON-Datei automatisch in Python-Dictionaries um.

### Erweiterungsaufgabe: JSON-Unterstützung einbauen

Kannst du deinen Node so erweitern, dass er wahlweise:
- Die eingebauten `ANWEISUNGEN` verwendet (wenn keine Datei angegeben ist)
- Oder eine JSON-Datei lädt (wenn ein Dateipfad angegeben wird)?

Tipp: Verwende einen ROS2-Parameter:
```python
self.declare_parameter("instructions_file", "")  # leer = eingebaute Anweisungen
datei_pfad = self.get_parameter("instructions_file").get_parameter_value().string_value

if datei_pfad:
    # Lade JSON-Datei
    ...
else:
    # Verwende ANWEISUNGEN
    ...
```

Verwendung dann so:
```bash
ros2 run <paketname> <node_name> --ros-args \
  -p instructions_file:=~/instructions.json
```

### GUI-Editor für Anweisungen

Damit du nicht manuell JSON schreiben musst, gibt es einen grafischen Editor:

🔗 **[Anweisungs-Editor (Web-App)](https://merlin2lmml.github.io/ros-motion-script-executor/)**

Dort kannst du deine Route visuell zusammenstellen und als JSON-Datei herunterladen. Die heruntergeladene Datei findest du dann in `~/Downloads/`.

---

## Glückwunsch!

Du hast erfolgreich:
- Das Linux-Terminal kennengelernt
- ROS2 Jazzy installiert
- Die Grundkonzepte von ROS2 verstanden (Nodes, Topics, Messages)
- Ein ROS2-Paket erstellt
- Deinen ersten eigenen ROS2-Knoten programmiert
- Das Paket gebaut und getestet
- Einen Roboter-Simulator gesteuert

Das ist eine solide Grundlage für alles, was in der Robotik noch kommt. Die nächsten Schritte könnten sein:
- Sensor-Daten empfangen (Subscribe auf Topics)
- Auf Sensordaten reagieren (z.B. stoppen, wenn ein Hindernis erkannt wird)
- Mehrere Nodes gleichzeitig laufen lassen und koordinieren
- ROS2 Launch-Files schreiben

---

## Anhang: Häufige Probleme und Lösungen

### „ros2: command not found"
ROS2-Umgebung wurde nicht gesourct. Ausführen:
```bash
source /opt/ros/jazzy/setup.bash
```

### „Package '<paketname>' not found"
Nach dem Build die install-Umgebung nicht gesourct:
```bash
cd ~/ros2_ws
source install/setup.bash
```

### Der Simulator startet, aber der Roboter bewegt sich nicht
- Prüfe, ob du das richtige Topic verwendest (`ros2 topic list`)
- Prüfe, ob dein Node wirklich publiziert (`ros2 topic echo /<topic>`)
- Prüfe, ob der Node überhaupt läuft (`ros2 node list`)

### `colcon build` schlägt fehl
- Achte darauf, dass du im richtigen Verzeichnis bist (`~/ros2_ws`)
- Prüfe auf Python-Syntaxfehler in deiner `.py`-Datei
- Lies die Fehlermeldung sorgfältig – sie zeigt meist genau die Zeile an

### Die Schildkröte/der Roboter bleibt nach dem Stoppen stehen, fährt aber weiter
- Dein `_sende_stopp()`-Aufruf fehlt oder funktioniert nicht
- Prüfe, ob `finally:` Block korrekt eingerückt ist

---

*Tutorial erstellt für das Robotik-Wahlfach. Viel Erfolg! 🤖*
