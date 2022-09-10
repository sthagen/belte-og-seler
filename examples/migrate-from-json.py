import datetime as dti
import json
import sys

EMPTY_SHA512 = (
    'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce'
    '47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
)

OLE_TS_FORMAT_A = '%Y%m%dT%H%M%SZ'
OLE_TS_FORMAT_B = '%Y-%m-%dT%H:%M:%SZ'
NEW_TS_FORMAT = '%Y-%m-%d %H:%M:%S.%f +00:00'

product_example = {'example': {'family': 'things', 'name': 'thing', 'description': 'The simple thing.'}}
build_example = {
    'example': {
        'description': 'the precious build',
        'source': 'https://example.com/vcs/branch/xyz/',
        'version': '2022.9.4',
        'timestamp': '2022-09-04 19:20:21.123456 +00:00.',
        'target': 'https://example.com/brm/family/product/version/',
        'sha512': EMPTY_SHA512,
    }
}

if len(sys.argv) != 2:
    print('usage: migrate-from-json datafile.json')
    sys.exit(2)

with open(sys.argv[1], 'rt', encoding='utf-8') as handle:
    ole = json.load(handle)

products = {}
for entry in ole:
    key = entry['id']
    name = entry['topic']
    if name not in products:
        products[name] = {'family': 'ABCD', 'name': name, 'description': 'Explain me later.', 'builds': []}
    try:
        ts = dti.datetime.strptime(entry['time_ref'], OLE_TS_FORMAT_A).strftime(NEW_TS_FORMAT)
    except Exception:
        ts = dti.datetime.strptime(entry['time_ref'], OLE_TS_FORMAT_B).strftime(NEW_TS_FORMAT)
    products[name]['builds'].append(
        {
            key: {
                'description': entry['summary'],
                'source': entry['source_url'],
                'version': entry['tag'],
                'timestamp': ts,
                'target': entry['target_url'],
                'sha512': EMPTY_SHA512,
            }
        }
    )

print(json.dumps(products, indent=2))
