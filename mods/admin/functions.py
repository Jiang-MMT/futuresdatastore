import os
from datetime import datetime
import csv
import boto3


month_codes_dict = dict(zip(list('FGHJKMNQUVXZ'), range(1, 13)))


def _parse_contract_date(filename):
    keys = filename.split('.')[0].split('_')[-1]
    symbol = keys[:2]
    year_str = str(keys[-2:])
    month_str = str(month_codes_dict[keys[-3]])
    contract_date_str = year_str + '-' + month_str + '-' + str(1)
    contract_date = datetime.strptime(contract_date_str, '%y-%m-%d')
    if contract_date.year > 2030:
        contract_date = contract_date.replace(year=contract_date.year-100)
    return symbol, contract_date


def _load_csv_to_db(f, db, model):
    cr = csv.DictReader(f)
    for row in cr:
        entry = model(symbol=row['symbol'],
                    description=row['description'],
                    exchange=row['exchange'],
                    category=row['category'])
        db.session.add(entry)
    db.session.commit()
    f.close()


def _init_s3():
    return boto3.client('s3',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

