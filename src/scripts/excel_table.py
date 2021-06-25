from ..utils import ingredient_class, product_encoder, node_class, excel_utils
from openpyxl import *
from openpyxl.styles import *
from openpyxl.utils import get_column_letter

def outputBasicInfoExcel(factory_nodes, fname):
    "make excel table of basic information"
    wb = Workbook()
    ws = wb.active
    
    # for all nodes, make table