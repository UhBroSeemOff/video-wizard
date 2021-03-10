from wizards.Storyboard_Wizard import Storyboard_Wizard
from wizards.File_Wizard import File_Wizard
from queue import Queue

class Wizard_manager:
    def __init__(self):
        self.__storyboard_wizard = Storyboard_Wizard()
        self.__file_wizard = File_Wizard()
        self.__files = []
        self.__selected_file = ""
        self.__extension = ""
        self.__request_queue = Queue()
        self.__command_map = {
            "help": self.__help__,
            "look_for": self.__look_for__,
            "select": self.__select__,
            "cast": self.__cast__
        }
        self.__spell_map = {
            "storyboard": self.__cast_storyboard_spell__
        }

    def make_wise_request(self, input_queue):
        self.__store_queue__(input_queue)
        if self.__request_queue.empty():
            return
        self.__process_queue__()

    def __help__(self):
        [ print("   {}".format(command)) for command in self.__command_map.keys() if command != "help"]

    def __look_for__(self):
        if self.__request_queue.empty() == True:
            self.__extension = input("Specify file extension you are looking for\n")
        else:
            self.__extension = self.__request_queue.get()
        self.__files = self.__file_wizard.look_around(self.__extension)
        print("File_Wizard: I found {} files!".format(len(self.__files)))

    def __select__(self):
        if self.__request_queue.empty() == True:
            print("Choose file's index")
            self.__look_around__()
            number_of_selection = int(input())
        else:
            parameter = self.__request_queue.get()
            number_of_selection = self.__convert_parameter_to_file_index__(parameter)
        if number_of_selection > 0 & number_of_selection <= len(self.__files):
            self.__selected_file = self.__files[number_of_selection-1]
        else:
            print("Wrong index\n")

    def __cast__(self):
        if self.__request_queue.empty() == True:
            spell = input("Choose your spell\n")
        else:
            spell = self.__request_queue.get()
        if spell in self.__spell_map:
            self.__spell_map[spell]()
        else:
            print("Try another spell\n")

    def __cast_storyboard_spell__(self):
        self.__storyboard_wizard.open(self.__selected_file)
        print("Framerate: {} FPS".format(self.__storyboard_wizard.get_framerate()))
        self.__storyboard_wizard.get_storyboard()
        self.__storyboard_wizard.close()

    def __look_around__(self):
            self.__files = self.__file_wizard.look_around(self.__extension)
            file_number = 1
            for file in self.__files:
                print(" {} {}".format(str(file_number), str(file)))
                file_number += 1

    def __store_queue__(self, queue):
        while queue.empty() == False:
            self.__request_queue.put(queue.get())

    def __process_queue__(self):
        while self.__request_queue.empty() == False:
            command = self.__request_queue.get()
            if command in self.__command_map.keys():
                self.__command_map[command]()
            else:
                print("Try another spell \n")
                self.__request_queue = Queue()

    def __convert_parameter_to_file_index__(self, parameter):
        if parameter == "last":
            return len(self.__files)
        if parameter == "first":
            return 1
        return int(parameter)

if __name__ == "__main__":
    manager = Wizard_manager()  
    print("Type 'help' for commands list\n") 
    while True:
        input_array = input().split(' ')
        input_queue = Queue()
        [input_queue.put(element) for element in input_array]
        manager.make_wise_request(input_queue)