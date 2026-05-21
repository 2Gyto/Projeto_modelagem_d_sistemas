import enum


class TipoEntradaConsumo(str, enum.Enum):
    KWH = "KWH"
    REAIS = "REAIS"


class OrientacaoTelhado(str, enum.Enum):
    NORTE = "NORTE"
    SUL = "SUL"
    LESTE = "LESTE"
    OESTE = "OESTE"


class TipoConexao(str, enum.Enum):
    MONOFASICA = "MONOFASICA"
    BIFASICA = "BIFASICA"
    TRIFASICA = "TRIFASICA"


class StatusSimulacao(str, enum.Enum):
    INICIADA = "INICIADA"
    VALIDANDO_DADOS = "VALIDANDO_DADOS"
    BUSCANDO_IRRADIACAO = "BUSCANDO_IRRADIACAO"
    CALCULANDO = "CALCULANDO"
    CONCLUIDA = "CONCLUIDA"
    ERRO = "ERRO"
