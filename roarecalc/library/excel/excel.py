import openpyxl
import string

alphabet = string.ascii_uppercase

class Exproc :

    """
    later.
    """

    def __init__(self, path : str) -> None :

        """
        later.
        """

        self.path = path
        self.row = 1

    def prepare(self, headers : list, sheet_title = "Sheet") -> None :

        """
        later.
        """

        if len(headers) > 26 :
            error = "It only supports 26 letters of the alphabet! Sorry!"
            raise ValueError(error)
        
        self.headers = headers
        self.sheet_title = sheet_title

        wb = openpyxl.Workbook()
        sheet = wb[sheet_title]

        for ind, header in enumerate(headers) :
            cell = alphabet[ind] + "1"
            sheet[cell] = header

        self.wb = wb
        self.sheet = sheet
        self.row += 1

    def insert(self, values : list) -> None :

        """
        later.
        """

        try :
            self.sheet_title
        except :
            error = "The workbook has not yet been created; use the 'prepare' method."
            raise ValueError(error)

        if len(values) != len(self.headers) :
            error = "The number of values does not match the number of headers."
            raise ValueError(error)
        
        for ind, value in enumerate(values) :
            cell = alphabet[ind] + str(self.row)
            self.sheet[cell] = value
        
        self.row += 1
    
    def write(self, cell : str, message : str) -> None :

        """
        later.
        """

        self.sheet[cell] = message

    def finish(self) -> None :

        """
        later.
        """

        self.wb.save(self.path)