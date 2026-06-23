import argparse
import sys
from storage import repository as repo
from reporting.formatters import (
    print_company_report,
    print_sector_report,
    print_anomalies_report,
    print_pipeline_report,
)
from reporting.exporters import export_csv, export_json


def main():
    parser = argparse.ArgumentParser(
        prog='report.py',
        description='MarketPulse Report Generator'
    )
    parser.add_argument('--company',   type=str,   help='Company name for deep-dive report')
    parser.add_argument('--sector',    type=str,   help='Sector name for overview')
    parser.add_argument('--anomalies', action='store_true', help='Show sentiment anomalies')
    parser.add_argument('--pipeline',  action='store_true', help='Show pipeline health')
    parser.add_argument('--threshold', type=float, default=-0.5, help='Anomaly threshold')
    parser.add_argument('--days',      type=int,   default=30,   help='Look-back window in days')
    parser.add_argument('--export',    type=str,   choices=['csv', 'json'], help='Export format')
    parser.add_argument('--output',    type=str,   default='output.csv',   help='Export file path')

    args = parser.parse_args()

    if args.company:
        rows = repo.fetch_company_summary(args.company, args.days)
        data = {'rows': rows}
        print_company_report(args.company, args.days, data)
        if args.export == 'csv':
            export_csv(rows, args.output)
        elif args.export == 'json':
            export_json(rows, args.output)

    elif args.sector:
        rows = repo.fetch_sector_summary(args.sector, args.days)
        data = {'rows': rows}
        print_sector_report(args.sector, args.days, data)
        if args.export == 'csv':
            export_csv(rows, args.output)

    elif args.anomalies:
        rows = repo.fetch_anomalies(args.days)
        print_anomalies_report(rows, args.threshold, args.days)
        if args.export == 'csv':
            export_csv(rows, args.output)

    elif args.pipeline:
        rows = repo.fetch_pipeline_health(args.days)
        print_pipeline_report(rows, args.days)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()