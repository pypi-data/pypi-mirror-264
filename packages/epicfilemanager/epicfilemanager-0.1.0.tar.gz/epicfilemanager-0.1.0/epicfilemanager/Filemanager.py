#Einfachen zugang zu Dateien, un später einfaches Speichern von Nutzerdaten zu ermöglichen
import os, json

class File:
    def __init__(self, path : str, create : bool = False):
        """
        neues File Objekt erstellen. 


        :param path: Pfad zur angegebenen Datei
        :param create: Soll eine neue Datei erstellt werden.       
        """
        self.path : str = path
        if not os.path.isfile(path):
            if not create:
                raise FileNotFoundError("The specified File does not exist.")
            else:
                with open(path, "x") as file:
                    pass
    @property
    def exists(self):
        #überprüfen, ob Datei existiert
        return os.path.isfile(self.path)
    def clear(self) -> bool:
        """
        Löschen der Inhalte der Datei
        """
        if not self.exists: return False
        #Schreiben der Datei mit Angabe eines Leeren Textes um Inhalt zu löschen
        return self.write("")
    def write(self, text : str) -> bool:
        """
        Schreiben der Datei, vorherige Inhalte werden Überschrieben

        :param text: Text, welcher in die Datei geschrieben wird
        """
        if not self.exists:
            return False
        #Schreiben der Datei mit auffangen möglicher Fehler
        try:
            with open(self.path, "w") as file:
                file.write(text)

        except Exception as error:
            print(error)
            return False
        return True # Alle Funktionen geben einen Kontroll Bool zurück 
    def writeJSON(self, data : any) -> bool:
        """
        Erweiterte Write Funktion, welche das schreiben von JSON Objekten ermöglicht
        
        :param data: Daten, welche in die Datei geschrieben werden sollen.
        """
        if not self.exists:
            return False
        try: 
            text_data = json.dumps(data)
            return self.write(text_data)
        except Exception as error:
            #Fehler beim konvertieren des Objekt zu einem JSON String.
            print(error)
            return False
    def read(self) -> str:
        """
        Lesen der Datei
        """
        if not self.exists:
            return False
        try:
            with open(self.path, "r") as file:
                return file.read() 
        except Exception as error:
            print(error)
            return False       
    def readJSON(self) -> any:
        """
        Erweiterte Read Funktion welche den Inhalt der Datei in ein Python Objekt umwandelt
        """
        if not self.exists:
            return False
        try:
            text_data = self.read()
            if text_data == False:
                return False
            data = json.loads(text_data)
            return data
        
        except Exception as error:
            print(error)
            return False