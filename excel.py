import pandas as pd
from account import Account


def create_excel(transactions, name_file):
    """
    Create an Excel file using transactions

    This function is responsible  for creating an Excel file using all the
    transactions we have until today.
    Creates a table order by date of transaction and highlights the positive
    and negative transactions.

    Args:
        name_file (string): name of the excel file.

    """

    df = pd.DataFrame({'Data': transactions.keys(),
                       'Montante': transactions.values()})

    df['Data'] = pd.to_datetime(df.Data, dayfirst = [True])
    df = df.sort_values(['Data', 'Montante'], ascending=[True,False])

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('{}.xlsx'.format(name_file), engine='xlsxwriter',
                            datetime_format='dd-mm-yyyy')
    df.to_excel(writer, sheet_name='Transactions', index=False)

    # Get the xlsxwriter objects from the dataframe writer object.
    workbook  = writer.book
    worksheet = writer.sheets['Transactions']

    format_mont = workbook.add_format({'num_format': u'#,##0.00 \u20ac'})
    format_red = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    format_green = workbook.add_format({'bg_color': '#C6EFCE',
                                        'font_color': '#006100'})

    worksheet.set_column('B:B', 10, format_mont)
    worksheet.set_column('A:A', 13, None)
    worksheet.conditional_format('B2:B{}'.format(len(df.index)+1), {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0,
                                         'format': format_green})
    worksheet.conditional_format('B1:B{}'.format(len(df.index)+1), {'type': 'cell',
                                         'criteria': '<',
                                         'value': 0,
                                         'format': format_red})

    writer.save()
