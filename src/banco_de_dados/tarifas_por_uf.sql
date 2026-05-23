-- Tarifas médias de referência por UF (R$/kWh) — valores educacionais.
-- Atualizar mensalmente conforme ANEEL (RB07).
CREATE TABLE IF NOT EXISTS tarifas_uf (
    uf TEXT PRIMARY KEY,
    tarifa_kwh REAL NOT NULL,
    atualizado_em TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR REPLACE INTO tarifas_uf (uf, tarifa_kwh) VALUES
    ('AC', 0.7921),
    ('AL', 0.8456),
    ('AP', 0.8102),
    ('AM', 0.7988),
    ('BA', 0.8312),
    ('CE', 0.8523),
    ('DF', 0.7890),
    ('ES', 0.8124),
    ('GO', 0.7654),
    ('MA', 0.8389),
    ('MT', 0.7712),
    ('MS', 0.7589),
    ('MG', 0.8234),
    ('PA', 0.8156),
    ('PB', 0.8401),
    ('PR', 0.7489),
    ('PE', 0.8590),
    ('PI', 0.8278),
    ('RJ', 0.8912),
    ('RN', 0.8467),
    ('RS', 0.7623),
    ('RO', 0.7834),
    ('RR', 0.8012),
    ('SC', 0.7345),
    ('SP', 0.8234),
    ('SE', 0.8512),
    ('TO', 0.7698);
