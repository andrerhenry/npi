

class NiagaraSystemException(Exception):
    """ Exception for error in reading Niagara system or if user does not specify a directory."""
    def __init__(self):
        self.message = "Niagara System could not be detected. " \
        "Please use npi at the Niagara directory or specify the path a Niagara file system."
        super().__init__(self.message)