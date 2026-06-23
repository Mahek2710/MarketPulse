from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)

_analyzer = SentimentIntensityAnalyzer()


def score_article(headline: str, summary: str = '') -> dict:
    text = headline
    if summary:
        text = f'{headline}. {summary[:500]}'

    scores = _analyzer.polarity_scores(text)
    compound = round(scores['compound'], 4)

    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    return {
        'score': compound,
        'magnitude': round(abs(compound), 4),
        'label': label,
        'model_used': 'vader',
    }