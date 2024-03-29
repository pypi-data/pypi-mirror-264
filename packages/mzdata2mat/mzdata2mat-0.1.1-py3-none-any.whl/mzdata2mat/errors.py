class mzDataError(Exception):
    """Class used by mzDataXML package to throw errors"""

    def __init__(self, errorMsg : str, errorCode : int):
        self.errorMsg = errorMsg
        self.errorCode = errorCode
        super().__init__(f"An error occured : Error {self.errorCode} - {self.errorMsg}")