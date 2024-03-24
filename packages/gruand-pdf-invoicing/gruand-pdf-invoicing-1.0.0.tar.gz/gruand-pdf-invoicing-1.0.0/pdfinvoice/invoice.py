import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import time


def generate(invoices_path, pdfs_path, image_path, product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files into pdf invoices.
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        filename = Path(filepath).stem
        invoice_number = filename.split("-")[0]

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=9, txt=f"Invoice #{invoice_number}", ln=1)

        pdf.set_font(family="Times", size=16)
        pdf.cell(w=50, h=9, txt=f"From {time.strftime("%b %d, %Y")}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        headers = df.columns
        headers = [item.replace("_", " ").title() for item in headers]

        # Header of the table
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=30, h=8, txt=headers[0], border=1)
        pdf.cell(w=70, h=8, txt=headers[1], border=1)
        pdf.cell(w=40, h=8, txt=headers[2], border=1)
        pdf.cell(w=30, h=8, txt=headers[3], border=1)
        pdf.cell(w=25, h=8, txt=headers[4], border=1, ln=1)

        # Generating the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=25, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df[total_price].sum()
        # Sum row of the table
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=40, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=25, h=8, txt=str(total_sum), border=1, ln=1)

        # Total amount
        pdf.set_font(family="Times", size=11, style="B")
        pdf.cell(w=30, h=8, txt=f"The total amount is {total_sum}", ln=1)

        disclaimer_text = """
        Why do we use it?
        It is a long established fact that a reader will be distracted by the readable content of a page when looking at its
        layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to 
        using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web 
        page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many 
        web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes 
        on purpose (injected humour and the like).
        """

        # Company info
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=28, h=11, txt=f"Gruand Ltd")
        pdf.image(image_path, w=12)
        pdf.set_font(family="Times", size=8)
        pdf.multi_cell(w=0, h=6, txt=disclaimer_text)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/invoice-{invoice_number}.pdf")
