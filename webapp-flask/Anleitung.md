# Anleitung Umlagerungstool Küblbeck

Um die Analyse erfolgreich durchzuführen, nutzen Sie bitte die folgende Anleitung. Sollten unerwartete Probleme oder Fragen auftreten, klicken Sie einfach auf den Schriftzug "Capstone Küblbeck" unten rechts für einen Link zu unserem GitHub Repository. In dem dortigen README finden Sie neben weiteren Informationen zum Projekt auch die LinkedIn Kontaktdaten unseres Teams. Melden Sie sich gerne bei uns!


1. Exportieren Sie die Daten zum Lagerbestand, den Verkäufen und die Lieferantenübersicht aus Qlikview oder ggf. anderen Quellen. Optimalerweise speichern Sie die Tabelleneinstellungen in Qlikview und passen jeweils nur die zu untersuchenden Zeiträume an (Tag des Lagerbestands und Verkaufszeitraum).
2. Bevor Sie die Tabellen hochladen, stellen Sie bitte sicher, dass die folgenden Anforderungen erfüllt sind:
    * Daten liegen in einem der folgenden Formate vor: .xls, .xlsx, .csv oder .txt.
    * Für .csv und .txt Dateien: Die einzelnen Spalten müssen je Datei einheitlich mit einem _,_ oder _;_ getrennt sein (z.B. _Lfnr;Artnr;Index;Beschr.;etc._).
        * Dies können Sie prüfen, wenn Sie die Datei im Windows Editor öffnen (_Rechtsklick -> Öffnen mit -> Programm/App auswählen_)
    * Zur Zeit ist die Auswertung nur möglich für die neun deutschen Standorte.
    * Für die einzelnen Tabellen müssen die folgenden Spalten mit genau diesen Bezeichnungen gegeben sein\
    (für .csv und .txt: Spalten können getrennt sein mit _,_ oder _;_):
        * Lagerbestand:\
        _Lfnr, Artnr, Index, Beschr., BKZ, VPE, St.gr., Ltz. VK ges., Basispreis, Basispr. Summe, Gesamt,_\
        _WEN,Ltz. VK WEN,RGB,Ltz. VK RGB,AMB,Ltz. VK AMB,[...],ROS,Ltz. VK ROS_
        * Verkäufe:\
        _Lfr., Art.nr., Ind., Beschreibung, WAWI_Artikel.Einstandspreis (fest), Gesamt, WEN, RGB, STR, PAS, AMB, CHA, LAN, MÜH, ROS_
        * Lieferantenübersicht:\
        _Lfnr, Beschreibung_
    * In der ersten Zeile unter den Spaltenüberschriften sollte sich eine Summenzeile befinden (nur Werte für Spalten mit Mengen- oder Preisangaben).
    * __ACHTUNG: Stimmen die Spalten nicht überein, kann es zu einem "Internal Server Error" kommen. In diesem Fall bitte die Originaldateien nochmals prüfen.__
3. Verwenden Sie zur Auswahl der entsprechenden Dateien einfach den "Choose file" Button oder ziehen die Datei direkt auf den Button.
4. Nachdem alle drei Dateien ausgewählt wurden, können Sie über den Button "Erstelle Liste" die Vorschlagsliste für Umlagerungen generieren. Bitte haben Sie einen Moment Geduld, während der Prozess im Hintergrund durchgeführt wird. Je nach System sollte dies aber nicht länger als 5 Minuten dauern.
5. Sobald die Liste erstellt wurde, öffnet sich eine neue Seite mit zusätzlichen Visualisierungen zur Übersicht sowie einem Button, um die fertige Vorschlagsliste herunterzuladen. Die Liste ist im .xslx Format und ist problemlos mit der aktuellen Version von Excel zu nutzen.