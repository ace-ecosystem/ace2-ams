from analysis import FileType

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

    # make sure it is setup to run on files
    analysis = FileType(**analysis)
    assert analysis.requirements_met()

    # run the analysis
    analysis = analysis.run()

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
        'summary': None,
        'details': {
            'file_type': 'ASCII text',
            'mime_type': 'text/plain',
        },
        'observables': [],
    }
