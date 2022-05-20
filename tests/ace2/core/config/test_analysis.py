from ace2.core.config.analysis import AnalysisConfig, AnalysisConfigs
from pytest import raises

def test_analysis_config():
    class MyAnalysisConfig(AnalysisConfig):
        foo: str = 'bar'

    # test default
    analysis = AnalysisConfigs()
    assert analysis.my_analysis.foo == 'bar'

    # test specified
    d = {
        'my_analysis': {
            'foo': 'hello',
        },
    }
    analysis = AnalysisConfigs(**d)
    assert analysis.my_analysis.foo == 'hello'

    # test required analysis config
    class MyRequiredAnalysisConfig(AnalysisConfig):
        hello: str
    with raises(Exception):
        AnalysisConfigs()
