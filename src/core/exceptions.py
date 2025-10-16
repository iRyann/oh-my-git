class ModuleNotFoundException(Exception):
    pass

class ModuleEntryPointNotFoundException(Exception):
    pass

class RepositoryAlreadyExistsException(Exception):
    pass

class InvalidRepositoryDataStructureException(Exception):
    pass

class RepositoryDoesNotExistsException(Exception):
    pass

class SystemCallErrorException(Exception):
    pass