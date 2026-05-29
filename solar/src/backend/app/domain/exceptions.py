class DomainError(Exception):
    """Erro de regra de negócio."""


class EntityNotFoundError(DomainError):
    pass


class InvalidCredentialsError(DomainError):
    pass


class EmailAlreadyRegisteredError(DomainError):
    pass


class ExternalApiError(DomainError):
    """Falha em integração externa (ADR-03)."""

    def __init__(self, api_name: str, message: str) -> None:
        self.api_name = api_name
        super().__init__(message)
