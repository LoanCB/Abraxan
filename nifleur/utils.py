import csv

import xlwt as xlwt
from django.http import HttpResponse
from django.utils.formats import date_format


def export_csv(filename: str, data: list, excel: bool = False):
    """
        Return a response to send data into a CSV or XLS file

        :params str filename
        :params list (2 dimensional) data
        :params bool excel : return XLS instead of CSV file
    """
    if excel:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xls'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Data')

        # Add font style
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for row_num in range(len(data)):
            if row_num != 0:
                font_style = xlwt.XFStyle()
            for col_num in range(len(data[row_num])):
                ws.write(row_num, col_num, data[row_num][col_num], font_style)

        wb.save(response)
        return response
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        writer = csv.writer(response)
        writer.writerows(data)

        return response


def short_datetime(date):
    return date_format(date, "SHORT_DATETIME_FORMAT")
