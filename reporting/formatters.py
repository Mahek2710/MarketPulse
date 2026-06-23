from tabulate import tabulate


def print_company_report(company: str, days: int, data: dict):
    rows = data.get('rows', [])

    print()
    print('=' * 60)
    print(f'  MARKETPULSE REPORT: {company.upper()}  |  Last {days} Days')
    print('=' * 60)

    if not rows:
        print(f'  No data found for "{company}" in the last {days} days.')
        print('=' * 60)
        return

    scores = [r[1] for r in rows]
    avg_score = round(sum(scores) / len(scores), 4)
    label = 'Positive' if avg_score >= 0.05 else ('Negative' if avg_score <= -0.05 else 'Neutral')
    best = max(rows, key=lambda r: r[1])
    worst = min(rows, key=lambda r: r[1])

    sources = {}
    for r in rows:
        src = r[4]
        sources[src] = sources.get(src, 0) + 1
    source_str = ', '.join(f'{k} ({v})' for k, v in sorted(sources.items()))

    print(f'  Articles Analyzed  : {len(rows)}')
    print(f'  Avg Sentiment      : {avg_score:+.4f}  ({label})')
    print(f'  Most Positive      : [{best[1]:+.4f}]  {best[0][:60]}')
    print(f'  Most Negative      : [{worst[1]:+.4f}]  {worst[0][:60]}')
    print(f'  Coverage Sources   : {source_str}')
    print()
    print('  RECENT HEADLINES (last 5):')
    for row in rows[:5]:
        headline, score, lbl, date, source = row
        print(f'  [{score:+.4f}] {headline[:65]}')
    print('=' * 60)
    print()


def print_sector_report(sector: str, days: int, data: dict):
    rows = data.get('rows', [])

    print()
    print('=' * 60)
    print(f'  MARKETPULSE SECTOR: {sector.upper()}  |  Last {days} Days')
    print('=' * 60)

    if not rows:
        print(f'  No data found for sector "{sector}".')
        print('=' * 60)
        return

    print(tabulate(
        rows,
        headers=['Company', 'Avg Score', 'Articles', 'Label'],
        floatfmt='+.4f',
        tablefmt='simple'
    ))
    print('=' * 60)
    print()


def print_anomalies_report(rows: list, threshold: float, days: int):
    print()
    print('=' * 60)
    print(f'  ANOMALY REPORT  |  Z-score < -2  |  Last {days} Days')
    print('=' * 60)

    if not rows:
        print('  No anomalies detected. Market sentiment is stable.')
        print('=' * 60)
        return

    print(tabulate(
        rows,
        headers=['Company', 'Headline', 'Date', 'Score', 'Z-Score'],
        floatfmt='.4f',
        tablefmt='simple'
    ))
    print('=' * 60)
    print()


def print_pipeline_report(rows: list, days: int):
    print()
    print('=' * 60)
    print(f'  PIPELINE HEALTH  |  Last {days} Days')
    print('=' * 60)

    if not rows:
        print('  No pipeline runs found.')
        print('=' * 60)
        return

    print(tabulate(
        rows,
        headers=['Day', 'Source', 'Fetched', 'Inserted', 'Failed', 'Rate%'],
        tablefmt='simple'
    ))
    print('=' * 60)
    print()