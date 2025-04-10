

class NiagaraSystemDectectionError(Exception):
    """ Exception for error in reading Niagara system cannot be found."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class GetPackageManifestError(Exception):
    """ Exception for error with packacke manifest from server."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"