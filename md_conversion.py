from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
# result = md.convert("/Users/fredrikjacobsen/Downloads/CV_Fredrik_Jacobsen.pdf")

result = md.convert("/Users/fredrikjacobsen/Downloads/Oilers Cup kontoinfo.xlsx")

print(result.text_content)