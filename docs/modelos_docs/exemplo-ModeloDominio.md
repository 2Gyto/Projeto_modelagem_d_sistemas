# Exemplo de Modelo Conceitual de Domínio

## Sistema: Biblioteca Universitária

O modelo conceitual de domínio abaixo representa os principais conceitos do sistema e os relacionamentos entre eles.

```mermaid
classDiagram
    class Aluno {
        +matricula
        +nome
        +email
    }

    class Livro {
        +isbn
        +titulo
        +anoPublicacao
    }

    class Autor {
        +nome
        +nacionalidade
    }

    class Exemplar {
        +codigo
        +status
    }

    class Emprestimo {
        +dataEmprestimo
        +dataPrevistaDevolucao
        +dataDevolucao
    }

    class Reserva {
        +dataReserva
        +status
    }

    class Categoria {
        +nome
        +descricao
    }

    Aluno "1" --> "0..*" Emprestimo : realiza
    Aluno "1" --> "0..*" Reserva : faz
    Livro "1" --> "1..*" Exemplar : possui
    Livro "1..*" --> "1..*" Autor : escrito por
    Livro "1" --> "1" Categoria : pertence a
    Exemplar "1" --> "0..*" Emprestimo : participa de
    Livro "1" --> "0..*" Reserva : associado a