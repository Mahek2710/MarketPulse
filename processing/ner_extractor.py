import spacy
import logging

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load('en_core_web_sm')
    logger.info('spaCy model loaded successfully')
except OSError:
    raise RuntimeError(
        'spaCy model not found. Run: python -m spacy download en_core_web_sm'
    )


def extract_companies(headline: str, summary: str = '') -> list:
    text = f'{headline}. {summary}' if summary else headline
    doc = nlp(text)

    companies = []
    seen = set()
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            name = ent.text.strip()
            if name and name not in seen and len(name) > 2:
                companies.append(name)
                seen.add(name)

    logger.debug(f'NER extracted {len(companies)} entities from: {headline[:60]}')
    return companies