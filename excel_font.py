import openpyxl
from openpyxl.cell.rich_text import TextBlock, CellRichText
from openpyxl.cell.text import InlineFont

wb = openpyxl.Workbook()
ws = wb.active

size_10 = InlineFont(sz=10, color="FF0000")
size_20 = InlineFont(sz=20)

ws["A1"] = CellRichText([TextBlock(font=size_10, text="Apple"), TextBlock(font=size_20, text="Banana")])

wb.save("output.xlsx")