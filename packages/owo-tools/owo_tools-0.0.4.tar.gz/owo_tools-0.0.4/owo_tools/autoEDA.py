import pandas as pd
from dataprep.eda import create_report # 1-create report with dataprep
from pandas_profiling import ProfileReport # 2-create report with pandas_profiling
import sweetviz as sv # 3-create report with sweetviz


class AutoEDA:

    def __init__(self, df):
        self.df = df

    def dataprep_report(self, output_path="dataprep_report.html"):
        report = create_report(self.df)
        report.save(output_path)

    def pandas_profiling_report(self, output_path="pandas_profiling_report.html"):
        report = ProfileReport(self.df)
        report.to_file(output_path)

    def sweetviz_report(self, output_path="sweetviz_report.html"):
        report = sv.analyze(self.df)
        report.show_html(output_path)

