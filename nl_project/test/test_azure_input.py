from unittest import TestCase
from nl_project.input_layer.azure_input import AzureInput


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

    def test_get_asc_data_via_bytes(self):
        source = AzureInput(
            SourceCategory='Directional Survey',
            SourceName='31_5-7 Eos/03.Directional_Surveys/WELLPATH_COMPUTED_1.ASC',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_asc_data_via_dl(self):
        source = AzureInput(
            SourceCategory='Directional Survey',
            SourceName='31_5-7 Eos/03.Directional_Surveys/WELLPATH_COMPUTED_1.ASC',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            # download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_tif_photo_data_via_dl(self):

        source = AzureInput(
            SourceCategory='Directional Survey',
            SourceName='31_5-7 Eos/11.Core_Data/Core_Photos/CORE_PHOTO_CV_M_TOP264900_1_007W1.TIF',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            # download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_tif_photo_data_via_bytes(self):
        source = AzureInput(
            SourceCategory='Directional Survey',
            SourceName='31_5-7 Eos/11.Core_Data/Core_Photos/CORE_PHOTO_CT_M_TOP259200_1.TIF',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            # download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_segy_data_via_dl(self):
        source = AzureInput(
            SourceCategory='Borehole Siesmic Raw',
            SourceName='31_5-7 Eos/07.Borehole_Seismic/VSPZO_RAW_2020-01-17_1.SEGY',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            # download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')

    def test_get_segy_data_via_bytes(self):
        source = AzureInput(
            SourceCategory='Borehole Siesmic Raw',
            SourceName='31_5-7 Eos/07.Borehole_Seismic/VSPZO_RAW_2020-01-17_1.SEGY',
            Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
            AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
            download=False
        )
        data = source.get_data()
        if data is None:
            raise Exception('No data loaded')
    # def test_get_las_via_dl(self):
    #     source = AzureInput(
    #         SourceCategory='Directional Survey',
    #         SourceName='31_5-7 Eos/13.Petrophysical_Data_Evaluations/CPI/WLC_PETRO_COMPUTED_OUTPUT_1.LAS',
    #         Endpoint='https://datavillagesa.blob.core.windows.net/northernlights',
    #         AdditionalConnectionInfo='sv=2018-03-28&sr=c&sig=ySdG6%2BRmccOC1Eg4H0UlVDyVQgAQ1QzQdxCh1dxcTXs%3D&se=2021-05-16T16%3A56%3A39Z&sp=rl',
    #         # download=False
    #     )
    #     data = source.get_data()
    #     if data is None:
    #         raise Exception('No data loaded')

