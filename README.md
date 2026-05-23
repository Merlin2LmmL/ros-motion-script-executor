# Dein erster ROS2-Knoten – Ein Schritt-für-Schritt-Tutorial

**Zielgruppe:** Schülerinnen und Schüler mit Grundkenntnissen in Python, die noch keine Erfahrung mit Linux-Terminals oder ROS haben.

**Ziel:** Am Ende dieses Tutorials hast du einen eigenen ROS2-Knoten gebaut, der einen simulierten Roboter bewegt.

---

## Inhaltsverzeichnis

1. [Linux-Grundlagen Das Terminal verstehen](#1-linux-grundlagen--das-terminal-verstehen)
2. [ROS2 Jazzy installieren](#2-ros2-jazzy-installieren)
3. [Erste Schritte mit ROS2](#3-erste-schritte-mit-ros2)
4. [Ein ROS2-Paket erstellen](#4-ein-ros2-paket-erstellen)
5. [Den Knoten programmieren](#5-den-knoten-programmieren)
6. [Paket bauen mit Colcon](#6-paket-bauen-mit-colcon)
7. [Den Knoten testen mit echtem Simulator](#7-den-knoten-testen--mit-echtem-simulator)
8. [Bonus: JSON-Befehlsdateien](#8-bonus-json-befehlsdateien)

---

## 1. Linux-Grundlagen – Das Terminal verstehen

Bevor wir irgendetwas mit ROS machen können, müssen wir uns mit dem wichtigsten Werkzeug vertraut machen: dem **Terminal** (auch „Kommandozeile" oder „Shell" genannt).

Das Terminal ist kein Relikt aus der Vergangenheit. In der Robotik, Systemadministration und Softwareentwicklung ist es das wichtigste Arbeitsmittel. Mit etwas Übung wird es sich schnell selbstverständlich anfühlen.

### Das Terminal öffnen

Auf Ubuntu kannst du das Terminal öffnen mit:
- **Tastenkombination:** `Strg + Alt + T`
- Rechtsklick auf den Desktop → „Open Terminal"
- Im App-Menü nach „Terminal" suchen

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

> **Tipp – Tab-Vervollständigung:** Wenn du den Anfang eines Ordner- oder Dateinamens tippst und dann `Tab` drückst, vervollständigt das Terminal automatisch. Wenn es mehrere Möglichkeiten gibt, drücke `Tab` zweimal und alle Optionen werden angezeigt. Das spart enorm viel Zeit.

#### Ordner erstellen
```bash
mkdir mein_ordner
mkdir -p pfad/zu/tiefem/ordner    # Erstellt alle Zwischenordner
```

#### Dateien und Ordner löschen
```bash
rm datei.txt              # Datei löschen
rm -r ordner/             # Ordner (und Inhalt) löschen
rm -rf ordner/            # Erzwungen löschen – VORSICHT, kein Papierkorb!
```

> **Achtung:** `rm` löscht dauerhaft, ohne Rückfrage. Es gibt keinen Papierkorb im Terminal. Führe niemals Befehle aus dem Internet aus, die du nicht verstehst – vor allem solche, die `sudo`, `rm` und `-rf` in Kombination enthalten.

#### Dateien anzeigen und bearbeiten
```bash
cat datei.txt             # Inhalt ausgeben
nano datei.txt            # Datei im Terminal-Editor öffnen
```

**Nano** ist ein einfacher Texteditor, der direkt im Terminal läuft. Die wichtigsten Tasten:
- `Strg + O` → Speichern (dann `Enter` bestätigen)
- `Strg + X` → Beenden
- `Strg + K` → Zeile ausschneiden
- `Strg + W` → Suchen

---

### Sudo – Administratorrechte

Manche Befehle brauchen Administratorrechte. Dafür gibt es `sudo` (*Super User Do*):

```bash
sudo apt install irgendwas
```

> **Hinweis:** Wenn du nach deinem Passwort gefragt wirst, siehst du beim Tippen gar nichts – keine Sterne, keine Punkte. Das ist normal und beabsichtigt. Tippe dein Passwort und drücke `Enter`.

---

### Prozesse stoppen

Wenn ein Programm im Terminal läuft und du es stoppen möchtest:
- `Strg + C` – Programm sofort beenden. Diesen Shortcut wirst du sehr häufig verwenden.

---

### Text kopieren und einfügen im Terminal

Das normale `Strg + C` / `Strg + V` funktioniert im Terminal nicht, weil `Strg + C` ja Prozesse beendet. Stattdessen:
- **Kopieren:** Text markieren → `Strg + Shift + C`
- **Einfügen:** `Strg + Shift + V`

---

### Mehrere Terminals gleichzeitig

Im Laufe dieses Tutorials wirst du mehrere Terminal-Fenster gleichzeitig brauchen. Du kannst beliebig viele Fenster öffnen und nebeneinander anordnen.

---

### Schnell-Referenz

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

**ROS** steht für *Robot Operating System* – ist aber kein Betriebssystem im klassischen Sinne, sondern ein **Framework**: ein Gerüst aus Werkzeugen, Bibliotheken und Konventionen, das die Entwicklung von Robotersoftware massiv vereinfacht.

Stell dir vor, du baust einen Roboter. Er hat Sensoren (Kamera, Lidar, GPS), Aktoren (Motoren, Greifer) und braucht eine Software, die alles koordiniert. ROS gibt dir dafür:
- einen standardisierten Weg, wie verschiedene Programmteile miteinander kommunizieren
- fertige Treiber für Hunderte von Sensoren und Motoren
- Werkzeuge zum Visualisieren, Debuggen und Aufzeichnen von Daten
- eine große Community und viele fertige Pakete

**ROS2 Jazzy** ist die aktuelle stabile Version (Stand 2024/2025), optimiert für Ubuntu 24.04.

### Installation

Die Installation von ROS2 ist normalerweise ein aufwendiger Prozess mit vielen manuellen Schritten. Wir verwenden ein Installations-Skript, das alles automatisch erledigt.

Öffne ein Terminal und führe folgenden Befehl aus (alles in einer Zeile, oder kopiere den Block wie er ist):

```bash
curl -fsSL https://raw.githubusercontent.com/Merlin2LmmL/ROS2-Jazzy-Install-Script/refs/heads/main/ros2-jazzy-installer.sh \
  -o ros2-jazzy-installer.sh \
  && chmod +x ros2-jazzy-installer.sh \
  && ./ros2-jazzy-installer.sh
```

Was dieser Befehl tut:
- `curl -fsSL ...` lädt das Skript herunter
- `-o ros2-jazzy-installer.sh` speichert es unter diesem Namen
- `chmod +x` macht es ausführbar (vergleichbar mit einer `.exe` unter Windows)
- `./ros2-jazzy-installer.sh` führt es aus

Die Installation dauert je nach Internetgeschwindigkeit und Rechner 2–10 Minuten.

### Den Workspace einrichten

Nach der Installation brauchen wir einen **Workspace** – den Hauptordner, in dem alle deine ROS2-Projekte liegen werden.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

Das `~` ist eine Abkürzung für `/home/deinbenutzername`. Du kannst den Workspace auch anders nennen, z.B. `ros2_jazzy_ws`.

### Umgebung sourcen

ROS2 stellt viele Befehle und Umgebungsvariablen bereit. Damit das Terminal diese kennt, muss die ROS2-Umgebung **gesourct** (aktiviert) werden:

```bash
source /opt/ros/jazzy/setup.bash
```

> **Tipp:** Du musst das in jedem neuen Terminal-Fenster wiederholen. Um das zu automatisieren, füge diese Zeile zur Datei `~/.bashrc` hinzu (diese Datei wird bei jedem neuen Terminal automatisch ausgeführt):
> ```bash
> echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
> source ~/.bashrc
> ```

Teste die Installation mit:
```bash
ros2 --help
// ODER
echo $ROS_DISTRO
```
Mit ersterem sollte dir Hilfe zu den Befehlen mit ros2 gegeben werden und mit zweiterem solltest etwas wie `jazzy` sehen.

---

## 3. Erste Schritte mit ROS2

### Das wichtigste Konzept: Nodes, Topics und Messages

ROS2 basiert auf einem einfachen, aber mächtigen Konzept:

```
[Node A] -- publiziert Nachrichten --> [Topic] -- empfängt Nachrichten --> [Node B]
```

- **Node (Knoten):** Ein eigenständiges Programm, das eine bestimmte Aufgabe erfüllt (z.B. einen Motor ansteuern, Kamerabilder verarbeiten, Entscheidungen treffen)
- **Topic:** Ein benannter Kommunikationskanal. Nodes können Topics **publizieren** (senden) oder **subscriben** (empfangen). Stell es dir wie einen gemeinsamen "Chat" vor, auf den verschiedene Knoten Zugriff haben. 
- **Message:** Das Datenformat, das über ein Topic geschickt wird (z.B. eine Geschwindigkeit, ein Bild, ein Sensorwert). Stell es dir wie die Sprache im Chat vor.

#### Weitere Verdeutlichung:
Das Prinzip ist ähnlich wie ein Schwarzes Brett: Jeder kann Zettel anpinnen (publizieren) und jeder kann Zettel lesen (subscriben). Das Schwarze Brett selbst ist das Topic.

### Nützliche ROS2-Befehle

```bash
ros2 --help              # Alle verfügbaren Unterbefehle anzeigen
ros2 node list           # Alle laufenden Nodes anzeigen
ros2 topic list          # Alle aktiven Topics anzeigen
ros2 topic echo /topic   # Nachrichten auf einem Topic live anzeigen
ros2 topic info /topic   # Infos über ein Topic
```

### Turtlesim – ROS2's „Hello World"

Turtlesim ist ein kleines Demoprogramm, das mit ROS2 mitgeliefert wird: eine Schildkröte auf dem Bildschirm, die du über ROS2-Topics steuern kannst. Es eignet sich gut zum ersten Kennenlernen.

Du brauchst **drei Terminal-Fenster** gleichzeitig:

**Terminal 1 – Simulation starten:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 – Steuerung starten:**
```bash
ros2 run turtlesim turtle_teleop_key
```
Klicke in Terminal 2 und steuere die Schildkröte mit den Pfeiltasten.

**Terminal 3 – Nachschauen, was passiert:**
```bash
ros2 topic list
```

Du siehst mehrere Topics, unter anderem `/turtle1/cmd_vel`. Das ist der Kanal, über den Bewegungsbefehle gesendet werden.

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

Das ist eine **Twist-Message** – das Standardformat für Geschwindigkeitsbefehle in ROS2. `linear.x` ist die Vorwärtsbewegung, `angular.z` ist die Drehung. Dieses Format werden wir gleich selbst verwenden.

---

## 4. Ein ROS2-Paket erstellen

### Was ist ein Paket?

In ROS2 wird Code in **Paketen** organisiert. Ein Paket ist ein strukturierter Ordner mit deinem Code plus Metadaten (Name, Abhängigkeiten, Lizenz). Pakete haben mehrere Vorteile:
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

**Beispiel (verwende deine eigenen Angaben):**
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

> Paket- und Knotennamen sollten nur Kleinbuchstaben, Zahlen und Unterstriche enthalten – keine Leerzeichen, keine Umlaute.

### Die Paketstruktur erkunden

Wechsle in dein neues Paket und schau dir die Struktur an:
```bash
cd ~/ros2_ws/src/<paketname>
ls -la
```

Solche Verzeichnisbäume lassen sich auch direkt ausgeben mit dem Befehl `tree -L n`, wobei `n` die maximale Tiefe angibt:

```
<paketname>/
├── package.xml          <- Metadaten (Name, Abhängigkeiten, Lizenz)
├── resource/
│   └── <paketname>      <- Marker-Datei für ROS2
├── setup.cfg            <- Konfiguration für ros2 run
├── setup.py             <- Python-Installationsanleitung
└── <paketname>/
    ├── __init__.py      <- Macht den Ordner zu einem Python-Paket
    └── <node_name>.py   <- Hier kommt dein Code!
```

Öffne die Node-Datei und schau sie dir an:
```bash
nano <paketname>/<node_name>.py
```

Da steht schon etwas Boilerplate-Code. Wir werden diese Datei jetzt komplett neu befüllen.

---

## 5. Den Knoten programmieren

Dies ist das Herzstück des Tutorials. Wir schreiben einen ROS2-Knoten, der eine Sequenz von Bewegungsbefehlen ausführt – wie ein kleines Programm, das dem Roboter sagt: „Fahre 2 Sekunden geradeaus, drehe dich, fahre nochmals geradeaus, stoppe."

### Was soll unser Knoten können?

Bevor wir programmieren, planen wir kurz. Unser Knoten soll:

1. Eine Liste von Bewegungsanweisungen enthalten (z.B. „fahre 2 Sek. vorwärts, dann drehe dich 1,5 Sek.")
2. Das Ziel-Topic über einen konfigurierbaren Parameter entgegennehmen
3. Die Anweisungen nacheinander ausführen
4. Dafür Nachrichten an das konfigurierte Topic schicken
5. Am Ende stoppen

### Die wichtigsten Konzepte vorab

#### Twist – Das Nachrichtenformat für Bewegung

Eine `Twist`-Nachricht hat zwei Teile:
- `linear`: Geschwindigkeit in x (vorwärts/rückwärts), y (seitwärts), z (hoch/runter) in Meter pro Sekunde
- `angular`: Drehrate um x (nicken), y (rollen), z (drehen) in Radiant pro Sekunde

Für die meisten Bodenroboter sind nur `linear.x` (Vorwärtsfahrt) und `angular.z` (Drehen) relevant:

```
linear.x  > 0  ->  vorwärts
linear.x  < 0  ->  rückwärts
angular.z > 0  ->  Drehung links (gegen den Uhrzeigersinn)
angular.z < 0  ->  Drehung rechts (im Uhrzeigersinn)
```

#### rclpy – Die ROS2-Bibliothek für Python

`rclpy` ist die offizielle Python-Bibliothek für ROS2. Du importierst sie, um ROS2 zu initialisieren, Nodes zu erstellen, Publisher anzulegen, Nachrichten zu verschicken und den Logger zu benutzen.

Weiterführende Dokumentation:
- [rclpy API-Dokumentation](https://docs.ros2.org/latest/api/rclpy/)
- [ROS2 Python-Tutorial (offiziell)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [geometry_msgs/Twist Dokumentation](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)

#### ROS2-Parameter

In ROS2 können Nodes **Parameter** deklarieren – Einstellungen, die beim Start des Nodes von außen übergeben werden können, ohne den Code zu ändern. Das ist nützlich für Dinge wie das Ziel-Topic.

Ein Parameter wird so deklariert und gelesen:
```python
self.declare_parameter("mein_parameter", "standardwert")
wert = self.get_parameter("mein_parameter").get_parameter_value().string_value
```

Beim Start des Nodes übergibt man den Wert mit:
```bash
ros2 run <paket> <node> --ros-args -p mein_parameter:=wert
```

---

### Das Grundgerüst – dein Startpunkt

Öffne die Datei:
```bash
nano ~/ros2_ws/src/<paketname>/<paketname>/<node_name>.py
```

Ersetze den gesamten Inhalt mit folgendem Grundgerüst. Es enthält bewusst Lücken (markiert mit `???`), die du schrittweise füllen sollst.

```python
#!/usr/bin/env python3
"""
Bewegungssteuerung – ROS2 Node
================================
Führt eine Sequenz von Bewegungsanweisungen aus,
indem Nachrichten an ein konfigurierbares cmd_vel-Topic publiziert werden.
"""

import time
import sys

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


# =============================================================================
# AUFGABE 1: Bewegungsanweisungen definieren
# =============================================================================
#
# Jede Anweisung ist ein Dictionary mit folgenden Schlüsseln:
#
#   "aktion"     (str)   : Beschreibender Name – nur für die Log-Ausgabe
#   "linear_x"   (float) : Vorwärts-Geschwindigkeit in m/s (negativ = rückwärts)
#   "angular_z"  (float) : Drehgeschwindigkeit in rad/s (positiv = links)
#   "dauer"      (float) : Wie lange diese Anweisung ausgeführt wird (in Sekunden)
#
# Hinweis: Die Turtlesim-Schildkröte nutzt Werte bis ca. 2.0 m/s.
# Ein echter Roboter fährt je nach Modell 0.1 bis 1.0 m/s.
#
# Mindestanforderung: Definiere mindestens 4 sinnvolle Anweisungen.
#
ANWEISUNGEN = [
    # TODO: Füge hier deine eigenen Anweisungen ein!
    {"aktion": "vorwaerts",  "linear_x": ???, "angular_z": ???, "dauer": ???},
    {"aktion": "links",      "linear_x": ???, "angular_z": ???, "dauer": ???},
    {"aktion": "stop",       "linear_x": 0.0, "angular_z": 0.0, "dauer": 0.5},
]


class BewegungsNode(Node):
    """
    ROS2-Node, der Bewegungsanweisungen sequenziell ausführt.
    Erbt von rclpy.node.Node – das macht sie zu einem vollwertigen ROS2-Knoten.
    """

    # Wie oft pro Sekunde wird eine Nachricht gesendet? (Frequenz in Hz)
    PUBLISH_FREQUENZ = 10

    def __init__(self):
        # -----------------------------------------------------------------------
        # AUFGABE 2: Node benennen
        # -----------------------------------------------------------------------
        # Der Node braucht einen eindeutigen Namen. Dieser Name erscheint
        # in `ros2 node list`. Übergib ihn an super().__init__().
        #
        # Dokumentation: https://docs.ros2.org/latest/api/rclpy/api/node.html
        #
        super().__init__("???")  # TODO: Gib deinem Node einen sinnvollen Namen!

        self.get_logger().info(
            f"Node gestartet. {len(ANWEISUNGEN)} Anweisung(en) geladen."
        )

        # -----------------------------------------------------------------------
        # AUFGABE 3: Ziel-Topic per Parameter konfigurierbar machen
        # -----------------------------------------------------------------------
        # Unterschiedliche Simulatoren und echte Roboter verwenden unterschied-
        # liche Topic-Namen für Bewegungsbefehle. Damit wir den Node flexibel
        # einsetzen können, soll das Topic nicht fest im Code stehen, sondern
        # über einen ROS2-Parameter übergeben werden.
        #
        # Gehe wie folgt vor:
        #   1. Deklariere einen Parameter "cmd_vel_topic" mit dem Standardwert
        #      "/cmd_vel" (wird genutzt, wenn nichts übergeben wird).
        #   2. Lies den Wert des Parameters aus.
        #   3. Gib das verwendete Topic per Log-Nachricht aus, damit der Nutzer
        #      beim Start sieht, welches Topic verwendet wird.
        #
        # Syntax zum Deklarieren und Lesen eines String-Parameters:
        #   self.declare_parameter("parametername", "standardwert")
        #   wert = self.get_parameter("parametername").get_parameter_value().string_value
        #
        # Dokumentation:
        #   https://docs.ros2.org/latest/api/rclpy/api/node.html#rclpy.node.Node.declare_parameter
        #
        self.declare_parameter("cmd_vel_topic", ???)       # TODO
        self._topic = self.get_parameter(???).get_parameter_value().string_value  # TODO
        self.get_logger().info(f"Verwende Topic: {???}")   # TODO

        # -----------------------------------------------------------------------
        # AUFGABE 4: Publisher erstellen
        # -----------------------------------------------------------------------
        # Ein Publisher sendet Nachrichten an ein bestimmtes Topic.
        # Verwende jetzt self._topic als Topic-Namen (nicht den hartkodierten
        # String "/cmd_vel"), damit der Parameter aus Aufgabe 3 tatsächlich
        # genutzt wird.
        #
        # Syntax:
        #   self.create_publisher(<NachrichtenTyp>, "<topic_name>", <queue_size>)
        #
        #   NachrichtenTyp : Twist (aus geometry_msgs.msg)
        #   topic_name     : self._topic
        #   queue_size     : 10
        #
        # Dokumentation:
        #   https://docs.ros2.org/latest/api/rclpy/api/node.html#rclpy.node.Node.create_publisher
        #
        self._publisher = self.create_publisher(???, ???, ???)  # TODO

        # Starte die Ausführung 0.5 Sekunden nach dem Start,
        # damit der Node vollständig initialisiert ist.
        self._timer = self.create_timer(0.5, self._starte_ausfuehrung)

    # ---------------------------------------------------------------------------
    # AUFGABE 5: Twist-Nachricht erstellen
    # ---------------------------------------------------------------------------
    def _erstelle_twist(self, anweisung: dict) -> Twist:
        """
        Wandelt ein Anweisungs-Dictionary in eine Twist-Nachricht um.

        Args:
            anweisung: Dictionary mit Schlüsseln wie "linear_x", "angular_z"

        Returns:
            Eine Twist-Nachricht, bereit zum Publizieren
        """
        # Eine Twist-Nachricht hat folgende Felder:
        #
        #   msg.linear.x   (float)  <- Vorwärtsgeschwindigkeit
        #   msg.linear.y   (float)  <- Seitwärtsgeschwindigkeit (meist 0)
        #   msg.linear.z   (float)  <- Vertikalgeschwindigkeit  (meist 0)
        #   msg.angular.x  (float)  <- Nickrate  (meist 0)
        #   msg.angular.y  (float)  <- Rollrate  (meist 0)
        #   msg.angular.z  (float)  <- Drehrate links/rechts
        #
        # Tipp: Verwende .get("schluessel", standardwert) – falls ein Schlüssel
        # im Dictionary fehlt, wird der Standardwert verwendet.
        # Beispiel: anweisung.get("linear_x", 0.0)
        #
        msg = Twist()
        msg.linear.x  = ???   # TODO
        msg.angular.z = ???   # TODO
        # Alle anderen Felder bleiben 0.0 (Standardwert bei Twist)
        return msg

    # ---------------------------------------------------------------------------
    # AUFGABE 6: Einzelne Anweisung ausführen
    # ---------------------------------------------------------------------------
    def _fuehre_anweisung_aus(self, index: int, anweisung: dict) -> None:
        """
        Führt eine einzelne Anweisung für die angegebene Dauer aus.

        Args:
            index    : Position der Anweisung in der Liste (für die Anzeige)
            anweisung: Das Anweisungs-Dictionary
        """
        # Diese Funktion soll:
        #   1. Die Werte aus dem Dictionary lesen (Aktion, Dauer, Geschwindigkeiten)
        #   2. Eine Log-Nachricht ausgeben, welche Anweisung gerade läuft
        #   3. Die Twist-Nachricht erstellen (benutze _erstelle_twist!)
        #   4. Die Nachricht für die angegebene Dauer wiederholt publizieren
        #
        # Tipp für Schritt 4 – Zeitschleife:
        #   endzeit  = time.time() + dauer
        #   intervall = 1.0 / self.PUBLISH_FREQUENZ   # z.B. 0.1 s bei 10 Hz
        #   while time.time() < endzeit:
        #       self._publisher.publish(nachricht)
        #       time.sleep(intervall)
        #
        # Nützliche Methoden:
        #   self.get_logger().info("Nachricht")  <- Ausgabe im Terminal
        #   self._publisher.publish(nachricht)   <- Nachricht senden
        #   time.sleep(sekunden)                 <- Kurz warten
        #
        aktion = anweisung.get("aktion", f"schritt_{index}")
        dauer  = float(anweisung["dauer"])

        self.get_logger().info(???)   # TODO: z.B. "[1/5] 'vorwaerts' für 2.0s"

        twist = ???                   # TODO: Twist erstellen

        # TODO: Nachricht für "dauer" Sekunden in einer Schleife publizieren
        # ...

    # ---------------------------------------------------------------------------
    # AUFGABE 7: Stopp-Befehl senden
    # ---------------------------------------------------------------------------
    def _sende_stopp(self) -> None:
        """
        Sendet einen Stopp-Befehl (alle Geschwindigkeiten auf 0).
        Ohne diesen Befehl fährt ein echter Roboter weiter!
        """
        # Eine leere Twist-Nachricht hat automatisch alle Felder auf 0.0.
        # Erstelle eine solche Nachricht und publiziere sie.
        #
        self._publisher.publish(???)  # TODO
        self.get_logger().info("Stopp-Befehl gesendet (alle Geschwindigkeiten = 0).")

    # ---------------------------------------------------------------------------
    # AUFGABE 8: Alle Anweisungen der Reihe nach ausführen
    # ---------------------------------------------------------------------------
    def _starte_ausfuehrung(self) -> None:
        """
        Wird einmalig nach dem Node-Start aufgerufen.
        Führt alle Anweisungen der Reihe nach aus.
        """
        self._timer.cancel()  # Einmaliger Timer wird nicht mehr gebraucht

        try:
            # Iteriere über alle Anweisungen in ANWEISUNGEN und rufe
            # für jede _fuehre_anweisung_aus() auf.
            #
            # Tipp: enumerate() gibt dir gleichzeitig Index und Wert:
            #   for i, anweisung in enumerate(ANWEISUNGEN):
            #       ...
            #
            # TODO: Schleife über alle Anweisungen!

            self.get_logger().info("Alle Anweisungen abgeschlossen!")

        except KeyboardInterrupt:
            self.get_logger().info("Durch Benutzer unterbrochen.")
        finally:
            # Immer stoppen am Ende – egal ob fertig oder unterbrochen!
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

### Deine Aufgaben – Übersicht

| Nr. | Aufgabe | Was du tun musst |
|-----|---------|-----------------|
| 1 | `ANWEISUNGEN` befüllen | Mindestens 4 sinnvolle Bewegungsanweisungen definieren |
| 2 | Node benennen | `super().__init__("dein_node_name")` |
| 3 | Topic-Parameter anlegen | Parameter deklarieren, auslesen und im Log ausgeben |
| 4 | Publisher erstellen | `self.create_publisher(Twist, self._topic, 10)` |
| 5 | Twist-Nachricht befüllen | Felder `linear.x` und `angular.z` aus dem Dictionary setzen |
| 6 | Anweisung ausführen | Log-Ausgabe, Twist erstellen, Zeitschleife |
| 7 | Stopp senden | Leere `Twist()`-Nachricht publizieren |
| 8 | Alle Anweisungen iterieren | `for i, a in enumerate(ANWEISUNGEN):` |

---

### Hilfreiche Code-Schnipsel

Falls du bei einzelnen Aufgaben nicht weiterkommst, findest du hier Bausteine als Orientierung – ohne direkte Lösungen.

**Log-Nachricht mit Positionsangabe:**
```python
self.get_logger().info(
    f"[{index + 1}/{len(ANWEISUNGEN)}] Führe '{aktion}' aus für {dauer:.1f}s"
)
```

**Zeitschleife zum wiederholten Publizieren:**
```python
endzeit   = time.time() + dauer
intervall = 1.0 / self.PUBLISH_FREQUENZ  # z.B. 0.1 s bei 10 Hz

while time.time() < endzeit:
    self._publisher.publish(nachricht)
    time.sleep(intervall)
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

### Frühzeitig testen

Du musst nicht alle Aufgaben fertig haben, um zu testen. Sobald die Aufgaben 1–4 erledigt sind, kannst du das Paket bauen und mit `ros2 topic echo /cmd_vel` prüfen, ob dein Publisher Nachrichten sendet. Dafür braucht es noch keinen laufenden Simulator.

---

### Erweiterungsideen (optional)

Wenn du alles fertig hast und mehr ausprobieren möchtest:

- **Detaillierteres Logging:** Gib in der Schleife die verbleibende Zeit mit aus
- **Validierung:** Was passiert, wenn eine Anweisung kein `dauer`-Feld hat? Fange das ab
- **JSON-Unterstützung:** Siehe Kapitel 8

---

## 6. Paket bauen mit Colcon

### Was ist Colcon?

**Colcon** ist das Build-System von ROS2. Es installiert deine Pakete in eine standardisierte Verzeichnisstruktur, sodass `ros2 run` und andere ROS2-Werkzeuge deine Nodes finden können.

Auch wenn Python-Code nicht wirklich kompiliert wird, braucht ROS2 den Build-Schritt trotzdem:
- Symbolische Links und Konfigurationsdateien werden erstellt
- Entry Points werden registriert (damit `ros2 run` deine Node findet)
- Abhängigkeiten werden geprüft

### Immer aus dem Workspace-Root bauen

> **Wichtig:** Führe `colcon build` immer aus dem Wurzelverzeichnis deines Workspaces aus (`~/ros2_ws`), nicht aus einem Unterordner. Sonst entstehen die Ordner `build/`, `install/` und `log/` an der falschen Stelle.

```bash
cd ~/ros2_ws
```

### Das Paket bauen

Wenn du später einmal mehrere Pakete selbst gebaut hast, ist es sinnvoll, nur das Paket zu bauen, an dem du aktuell arbeitest. Nutze dafür die flag --packages-select. Aber Achtung: Du kannst dir hier deinen Paketnamen nicht vervollständigen lassen:
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

Häufige Fehler:
- `SyntaxError`: Python-Syntaxfehler – öffne die Datei und prüfe die angegebene Zeile
- `ModuleNotFoundError`: Eine Abhängigkeit fehlt – prüfe `package.xml` und `setup.py`
- `KeyError`: Ein Dictionary-Schlüssel fehlt – prüfe deine `ANWEISUNGEN`

### Umgebung nach dem Bauen sourcen

Nach jedem Build muss die Umgebung neu gesourct werden, damit ROS2 dein frisch gebautes Paket findet:

```bash
source install/setup.bash
```

> Tipp: Du kannst das automatisieren. Füge diese Zeile zur `~/.bashrc` hinzu:
> ```bash
> source ~/ros2_ws/install/setup.bash
> ```

---

## 7. Den Knoten testen – mit echtem Simulator

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

---

### Den OHM-Mecanum-Simulator installieren

Die OHM Technische Hochschule Nürnberg hat einen 2D-Robotersimulator entwickelt, der sich gut aufgrund seiner Einfachheit für unsere Zwecke eignet. Wir installieren ihn als weiteres ROS2-Paket:

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
> Anmerkung: Die flag "--break-system-packages" klingt sehr gefährlich, ist sie aber in diesem Fall gar nicht. Sie wurde beabsichtigt so abschreckend benannt, um vor den gebrauch ab zu schrecken, da dringend empfohlen wird, pip Pakete in einem sog. venv zu installieren. Da das Einrichten eines Venvs allerdings 1-2 extra Kapitel erfordern würde, weichen wir aus Zeit- und Komplexitätsgründen darauf zurück, das die Library global auf dem Rechner zu installieren. Falls jemand dagegen einen Einwand haben sollte, steht es demjenigen frei, stattdessen Pycharm in einem Venv zu installieren.


### Das richtige Topic herausfinden

Starte den Simulator:
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

Ein Fenster mit dem Roboter öffnet sich. Jetzt finden wir heraus, welches Topic der Simulator für Bewegungsbefehle verwendet:

```bash
ros2 topic list
```

Schau dir die Liste an. Welches Topic enthält `cmd_vel`? Es ist nicht einfach `/cmd_vel`.

Du kannst auch mehr Informationen über ein Topic bekommen:
```bash
ros2 topic info /<topic_name>
```

---

### Alles zusammen starten

Sobald du das richtige Topic kennst, starte alles in zwei (oder drei) Terminals:

**Terminal 1 – Node mit dem richtigen Topic starten:**
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run <paketname> <node_name> --ros-args \
  -p cmd_vel_topic:=/<das_richtige_topic>
```

Da du in Aufgabe 3 den `cmd_vel_topic`-Parameter implementiert hast, kannst du das Ziel-Topic jetzt beim Start bequem von außen übergeben – ohne den Code anfassen zu müssen.

**Terminal 2 – Der Simulator:**
```bash
ros2 run ohm_mecanum_sim ohm_mecanum_sim_node
```

**Terminal 3 (optional) – Topic überwachen:**
```bash
ros2 topic echo /<das_richtige_topic>
```

Wenn alles klappt, siehst du den Roboter im Simulator-Fenster die Bewegungen aus deiner `ANWEISUNGEN`-Liste ausführen.

---

## 8. Bonus: JSON-Befehlsdateien

Bisher sind die Anweisungen direkt im Python-Code eingebaut. Das ist unpraktisch: Jedes Mal, wenn wir die Route ändern wollen, müssen wir den Code editieren und neu bauen.

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

`json.load()` wandelt die JSON-Datei automatisch in Python-Dictionaries um – kein weiterer Aufwand.

### Erweiterungsaufgabe: JSON-Unterstützung einbauen

Erweitere deinen Node so, dass er wahlweise die eingebauten `ANWEISUNGEN` verwendet, oder eine JSON-Datei lädt, wenn ein Dateipfad angegeben wird.

Tipp: Nutze einen zweiten ROS2-Parameter:
```python
self.declare_parameter("instructions_file", "")
datei_pfad = self.get_parameter("instructions_file").get_parameter_value().string_value

if datei_pfad:
    # JSON-Datei laden
    with open(datei_pfad, "r") as f:
        anweisungen = json.load(f)
else:
    # Eingebaute Anweisungen verwenden
    anweisungen = ANWEISUNGEN
```

Verwendung dann so:
```bash
ros2 run <paketname> <node_name> --ros-args \
  -p cmd_vel_topic:=/<das_richtige_topic> \
  -p instructions_file:=~/meine_route.json
```

### Grafischer Editor für Anweisungen

Damit du nicht manuell JSON schreiben musst, steht ein grafischer Editor zur Verfügung:

**[Anweisungs-Editor (Web-App)](https://merlin2lmml.github.io/ros-motion-script-executor/)**

Dort kannst du deine Route visuell zusammenstellen und als JSON-Datei herunterladen. Die heruntergeladene Datei findest du dann in `~/Downloads/`.

---

## Glückwunsch!

Du hast erfolgreich:
- Das Linux-Terminal kennengelernt
- ROS2 Jazzy installiert
- Die Grundkonzepte von ROS2 verstanden (Nodes, Topics, Messages)
- Ein ROS2-Paket erstellt
- Deinen ersten eigenen ROS2-Knoten mit konfigurierbarem Topic-Parameter programmiert
- Das Paket gebaut und getestet
- Einen Roboter-Simulator gesteuert

Das ist eine solide Grundlage für alles, was in der Robotik noch kommt. Mögliche nächste Schritte:
- Sensor-Daten empfangen (Subscribe auf Topics)
- Auf Sensordaten reagieren (z.B. stoppen, wenn ein Hindernis erkannt wird)
- Mehrere Nodes gleichzeitig laufen lassen und koordinieren
- ROS2 Launch-Files schreiben

---

## Anhang: Häufige Probleme und Lösungen

### „ros2: command not found"
ROS2-Umgebung wurde nicht gesourct:
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
- Prüfe, ob das richtige Topic verwendet wird (`ros2 topic list`)
- Prüfe, ob der Node das Topic korrekt ausgibt (Log-Ausgabe beim Start)
- Prüfe, ob dein Node wirklich publiziert (`ros2 topic echo /<topic>`)
- Prüfe, ob der Node überhaupt läuft (`ros2 node list`)

### `colcon build` schlägt fehl
- Stelle sicher, dass du dich im richtigen Verzeichnis befindest (`~/ros2_ws`)
- Prüfe auf Python-Syntaxfehler in deiner `.py`-Datei
- Die Fehlermeldung zeigt meist genau die betroffene Zeile an

### Der Roboter fährt nach dem Stoppen weiter
- Dein `_sende_stopp()`-Aufruf fehlt oder funktioniert nicht
- Prüfe, ob der `finally:`-Block korrekt eingerückt ist

---

*Tutorial erstellt für das Robotik-Wahlfach. **Autor: Merlin Ortner <ortnermerlin@gmail.com>***
