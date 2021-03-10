import os

class File_Wizard:
    def __init__(self):
        pass

    def look_around(self, extension):
        return [file for file in os.listdir() if str(file).find(extension, -len(str(extension))) != -1]

if __name__ == "__main__":
    file_wizard = File_Wizard()
    extension = input("Please enter extension (with '.')")
    print(file_wizard.look_around(extension))
    input()