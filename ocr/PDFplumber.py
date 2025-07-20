import pdfplumber

with pdfplumber.open("acc.pdf") as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table:
                print(row)
