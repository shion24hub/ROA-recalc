import openpyxl

from config import EXCEL_COLUMN
alphabet = EXCEL_COLUMN

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

    def prepare(self, headers : list, sheetTitle = "Sheet") -> None :

        """
        later.
        """

        if len(headers) > 702 :
            error = "It only supports 702 letters of the alphabet(a-zz)! Sorry!"
            raise ValueError(error)
        
        self.headers = headers
        self.sheet_title = sheetTitle

        wb = openpyxl.Workbook()
        sheet = wb[sheetTitle]

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
            print("POINT : {}".format(values[0]))
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