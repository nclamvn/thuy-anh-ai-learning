#!/usr/bin/env python3
"""Validate an inactive offline provider plan; deliberately cannot activate API calls."""
import argparse
import json
from pathlib import Path
import re
from build_resources import KitError, read_json, require

FIELDS = {'schemaVersion','dataKind','enabled','mode','provider','model','modelVersion','credentialsEnvName','dataClass','allowChildData','maxRequests','maxCostUSD','timeoutMs','retryCount','humanAuthorizationRef','rawEvidenceDirectory'}


def verify(path):
    config, _ = read_json(path)
    require(isinstance(config, dict) and set(config) == FIELDS, 'unexpected or missing provider fields; secrets are forbidden')
    require(config['schemaVersion'] == 1 and config['dataKind'] == 'inactive-provider-proposal', 'provider plan must remain a proposal')
    require(config['enabled'] is False and config['mode'] == 'offline-import', 'live activation is not implemented; use offline import')
    require(config['allowChildData'] is False and config['dataClass'] == 'public-synthetic-adult-only', 'child/private data not permitted by this plan')
    require(type(config['maxRequests']) is int and config['maxRequests'] == 0 and type(config['maxCostUSD']) in (int,float) and config['maxCostUSD'] == 0, 'no paid/request budget is enabled')
    require(type(config['timeoutMs']) is int and 1000 <= config['timeoutMs'] <= 120000 and type(config['retryCount']) is int and config['retryCount'] == 0, 'timeout/retry proposal invalid')
    require(isinstance(config['credentialsEnvName'], str) and re.fullmatch(r'AI_LEARNING_[A-Z0-9_]+', config['credentialsEnvName']), 'credential field is an environment variable name, not a key')
    for name in ('provider','model','modelVersion','humanAuthorizationRef','rawEvidenceDirectory'):
        require(config[name] is None or isinstance(config[name], str) and config[name].strip(), f'{name} must be null or a nonempty proposal')
    return {'status':'PASS','active':False,'requests':0,'scope':'Offline configuration structure only; no credentials read and no API calls'}


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('config', type=Path); args=parser.parse_args()
    try: result=verify(args.config)
    except (KitError,OSError,TypeError,KeyError) as error: result={'status':'FAIL','errors':[str(error)]}
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if result['status']=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
