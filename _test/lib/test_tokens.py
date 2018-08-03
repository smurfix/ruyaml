from __future__ import absolute_import
from __future__ import print_function

import ruamel.yaml as yaml
import pprint
from ruamel.yaml.compat import PY3

# Tokens mnemonic:
# directive:            %
# document_start:       ---
# document_end:         ...
# alias:                *
# anchor:               &
# tag:                  !
# scalar                _
# block_sequence_start: [[
# block_mapping_start:  {{
# block_end:            ]}
# flow_sequence_start:  [
# flow_sequence_end:    ]
# flow_mapping_start:   {
# flow_mapping_end:     }
# entry:                ,
# key:                  ?
# value:                :

_replaces = {
    yaml.DirectiveToken: '%',
    yaml.DocumentStartToken: '---',
    yaml.DocumentEndToken: '...',
    yaml.AliasToken: '*',
    yaml.AnchorToken: '&',
    yaml.TagToken: '!',
    yaml.ScalarToken: '_',
    yaml.BlockSequenceStartToken: '[[',
    yaml.BlockMappingStartToken: '{{',
    yaml.BlockEndToken: ']}',
    yaml.FlowSequenceStartToken: '[',
    yaml.FlowSequenceEndToken: ']',
    yaml.FlowMappingStartToken: '{',
    yaml.FlowMappingEndToken: '}',
    yaml.BlockEntryToken: ',',
    yaml.FlowEntryToken: ',',
    yaml.KeyToken: '?',
    yaml.ValueToken: ':',
}


def test_tokens(data_filename, tokens_filename, verbose=False):
    tokens1 = []
    with open(tokens_filename, 'r' if PY3 else 'rb') as fp:
        tokens2 = fp.read().split()
    try:
        with open(data_filename, 'rb') as fp1:
            for token in yaml.scan(fp1):
                if not isinstance(token, (yaml.StreamStartToken, yaml.StreamEndToken)):
                    tokens1.append(_replaces[token.__class__])
    finally:
        if verbose:
            print('TOKENS1:', ' '.join(tokens1))
            print('TOKENS2:', ' '.join(tokens2))
    assert len(tokens1) == len(tokens2), (tokens1, tokens2)
    for token1, token2 in zip(tokens1, tokens2):
        assert token1 == token2, (token1, token2)


test_tokens.unittest = ['.data', '.tokens']


def test_scanner(data_filename, canonical_filename, verbose=False):
    for filename in [data_filename, canonical_filename]:
        tokens = []
        try:
            with open(filename, 'rb') as fp:
                for token in yaml.scan(fp):
                    tokens.append(token.__class__.__name__)
        finally:
            if verbose:
                pprint.pprint(tokens)


test_scanner.unittest = ['.data', '.canonical']

if __name__ == '__main__':
    import test_appliance

    test_appliance.run(globals())
