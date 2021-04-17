from unittest import TestCase
from input_layer.azure_input import AzureInput


class TestAzureInput(TestCase):
    def test_get_data_via_dl(self):
        source = AzureInput(
            SourceCategory='Core Report',
            SourceName='31_5-7 Eos/02.Drilling_and_Completion/CORING_2020-01-14_REPORT_1.PDF',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl'
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_data_via_bytes(self):
        source = AzureInput(
            SourceCategory='Core Report',
            SourceName='31_5-7 Eos/02.Drilling_and_Completion/CORING_2020-01-14_REPORT_1.PDF',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')
