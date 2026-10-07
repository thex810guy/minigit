class MinigitError(Exception):
    pass

class RepositoryError(MinigitError):
    pass

class RepositoryAlreadyExistsError(RepositoryError):
    pass

class RepositoryNotFound(RepositoryError):
    pass

class RepositoryCorrupted(RepositoryError):
    pass

class RepositoryInitilizationError(RepositoryError):
    pass

class PathNotFound(MinigitError):
    pass
