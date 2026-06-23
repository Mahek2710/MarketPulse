COMPANY_MAP = {
    'Infosys':                    ('INFY',       'IT'),
    'Tata Consultancy Services':  ('TCS',        'IT'),
    'TCS':                        ('TCS',        'IT'),
    'Wipro':                      ('WIPRO',      'IT'),
    'HCL Technologies':           ('HCLTECH',    'IT'),
    'HCL':                        ('HCLTECH',    'IT'),
    'Tech Mahindra':              ('TECHM',      'IT'),
    'HDFC Bank':                  ('HDFCBANK',   'Banking'),
    'ICICI Bank':                 ('ICICIBANK',  'Banking'),
    'State Bank of India':        ('SBIN',       'Banking'),
    'SBI':                        ('SBIN',       'Banking'),
    'Axis Bank':                  ('AXISBANK',   'Banking'),
    'Kotak Mahindra Bank':        ('KOTAKBANK',  'Banking'),
    'Reliance Industries':        ('RELIANCE',   'Energy'),
    'Reliance':                   ('RELIANCE',   'Energy'),
    'ONGC':                       ('ONGC',       'Energy'),
    'Indian Oil':                 ('IOC',        'Energy'),
    'Hindustan Unilever':         ('HINDUNILVR', 'FMCG'),
    'HUL':                        ('HINDUNILVR', 'FMCG'),
    'ITC':                        ('ITC',        'FMCG'),
    'Nestle India':               ('NESTLEIND',  'FMCG'),
    'Sun Pharmaceutical':         ('SUNPHARMA',  'Pharma'),
    'Sun Pharma':                 ('SUNPHARMA',  'Pharma'),
    'Dr Reddys':                  ('DRREDDY',    'Pharma'),
    'Cipla':                      ('CIPLA',      'Pharma'),
    'Maruti Suzuki':              ('MARUTI',     'Auto'),
    'Tata Motors':                ('TATAMOTORS', 'Auto'),
    'Mahindra':                   ('M&M',        'Auto'),
}


def classify_companies(ner_entities: list) -> list:
    results = []
    for entity in ner_entities:
        if entity in COMPANY_MAP:
            ticker, sector = COMPANY_MAP[entity]
            results.append((entity, ticker, sector))
        else:
            results.append((entity, None, 'Uncategorized'))
    return results