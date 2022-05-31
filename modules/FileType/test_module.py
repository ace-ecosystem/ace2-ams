from ace2.test import *
import module

def test_analysis():
    # create analysis to run
    analysis = {
        'id': 1,
        'type': 'FileType',
        'target': {
            'type': 'File',
            'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
            'metadata': [
                {
                    'type': 'DisplayValue',
                    'value': 'hello.txt',
                },
            ],
        },
    }

    # TODO: check module run_condition

    # run the analysis
    analysis = module.run(analysis, None)

    # verify analysis
    assert analysis == {
        'id': 1,
        'type': 'FileType',
        'target': {
            'type': 'File',
            'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
            'metadata': [
                {
                    'type': 'DisplayValue',
                    'value': 'hello.txt',
                },
            ],
        },
        'callback': None,
        'state': {},
        'summary': 'File Type Analysis: (ASCII text) (text/plain)',
        'details': {
            'file_type': 'ASCII text',
            'mime_type': 'text/plain',
        },
        'observables': [],
    }
