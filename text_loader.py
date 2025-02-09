################################################################################ # 
#     Author:      Lorenzo D. Moon
#     Instructor:  Karla Fant
#     Course:      CS-302
#     Assignment:  Program 4/5
#     Description: TextToDict: 
#                  Loads a file and converts it to a list of dictionaries.
#                  The file is expected to be in the format:
#                  key_0: value
#                  ...
#                  key_n: value
#                  -- Blank Line --
#                  key_0: value
#                  ...
#                  key_n: value
#             
#                  TextToList:
#                  Loads a file and converts it to a list of strings.
#                  The file is expected to be in the format:
#                  string_0
#                  ...
#                  string_n
#
################################################################################

class TextToDict:
    '''
    __init__ requires no parameters.
    Data Members:
        __data: list of dictionaries. Each dictionary contains the data to hold
                the information to instantiate another class.
    
    Methods:
        load_file(file_name: str) -> None
    '''

    def __init__(self) -> None:
        self.__data = [] 
        pass
        
    def load_file(self, file_name: str) -> None:
        self.__data = [] # Clear the data
        temp_dict = {} # Temporary dictionary to hold the data

        # Check if this file exists
        try:
            open(file_name, 'r')
        except FileNotFoundError:
            # The game must exit, this is a critical error.
            # This helps pinpoint where the error is.
            raise FileNotFoundError(f"File {file_name} not found.")

        # Open the file and read it line by line
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip() # Remove leading and trailing whitespace

                # If the line starts with a comment, skip it.
                if line.startswith('#'):
                    continue
                # If it's a blank line, we're at the end of the load for that
                # dictionary. Append it to the list and reset the temp_dict.
                elif line == "": 
                    self.__data.append(temp_dict)
                    temp_dict = {}
                else:
                    key, value = line.split(": ")
                    temp_dict[key] = self.auto_type(value)

        self.__data.append(temp_dict) # Append the last dictionary
        return

    @property
    def data(self):
        return self.__data
    
    @property
    def data_length(self):
        return len(self.__data)
    
    def auto_type(self, value: str) -> any:
        # Formats the incoming data to the correct type 
        # Converts to int, float, or boolean. Supports negative numbers.

        # Convert to int
        if value.isdigit():
            value = int(value)
        # Convert to float
        elif value.replace('.', '', 1).isdigit():
            value = float(value)
        # Convert to negative int
        elif value[0] == '-' and value[1:].isdigit():
            value = int(value)
        # Convert to negative float
        elif value[0] == '-' and value[1:].replace('.', '', 1).isdigit():
            value = float(value)
        # Convert to booleans
        elif value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.lower() == "none":
            value = None
        return value 

class TextToList:
    def __init__(self):
        self.__data = []
        pass

    def load_file(self, file_name: str) -> None:
        self.__data = []

        try:
            open(file_name, 'r')
        except FileNotFoundError:
            # Same as above, this is a critical error.
            # This helps pinpoint where the error is.
            raise FileNotFoundError(f"File {file_name} not found.")
        
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#'):
                    continue
                elif line != "":
                    self.__data.append(line) 
    
    @property
    def data(self):
        return self.__data