import pandas as pd
import requests


def import_SPM_data():
    """import System Performance Measures Data excel spreadsheet from HUD website"""

    spmd_url = "https://files.hudexchange.info/resources/documents/System-Performance-Measures-Data-Since-FY-2015.xlsx"
    req = requests.get(spmd_url)
    url_content = req.content

    return url_content


def SPM_data_to_DataFrame(content):
    """convert downloaded SPM data into Pandas DataFrame
    notes: options to select data years, or adjust column selection for other applications
    """
    df = pd.read_excel(content, sheet_name='2020', header=[1])

    cols = ['State', 'Continuum of Care (CoC)',
            'Total Persons Returns in 24 mths (should include both the 6- and 12-month cohort).5', 'Total HMIS Count',
            'ES-SH-TH-PH 1st Time Homeless', 'Total Persons Exiting ES, TH, SH, PH-RRH',
            'Total Persons Exiting ES, TH, SH, PH-RRH to Permanent Housing',
            ]
    new_cols = ['state', 'coc', 'return_from_PH', 'total_count', 'new_homeless', 'total_exiting', 'total_exiting_to_PH']

    selected_df = df[cols].copy()
    column_map_dict = dict(zip(cols, new_cols))
    coc = selected_df.rename(columns=column_map_dict)

    coc['existing'] = coc['total_count'] - coc['new_homeless'] - coc['return_from_PH']
    coc['exit_to_unknown'] = coc['total_exiting'] - coc['total_exiting_to_PH']
    coc['remain'] = coc['total_count'] - coc['total_exiting']
    coc['%_successful_exit'] = coc['total_exiting'] / coc['total_exiting_to_PH']

    col_order = ['state', 'coc', 'new_homeless', 'existing', 'return_from_PH',
                 'total_count', 'exit_to_unknown', 'total_exiting_to_PH', 'remain', 'total_exiting',
                 '%_successful_exit']
    coc = coc[col_order].copy()

    return coc


data = import_SPM_data()
coc = SPM_data_to_DataFrame(data)

print(coc.head(1))


