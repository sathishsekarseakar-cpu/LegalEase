from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import sqlite3
from datetime import datetime

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("documents.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            document_type TEXT,
            purpose TEXT,
            document TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def generate_document(name, document_type, purpose):

    if document_type == "Leave Letter":
        return f"""LEAVE LETTER

Date: __________________

To
The Concerned Authority

Subject: Request for Leave

Respected Sir/Madam,

I, {name}, am writing to request leave for the following reason:

{purpose}

I kindly request you to consider my request and grant me leave.

Thank you.

Yours faithfully,
{name}

Signature: __________________
"""

    elif document_type == "Rental Agreement":
        return f"""RENTAL AGREEMENT

Date: __________________

Tenant Name: {name}

Purpose:
{purpose}

This is a general rental document template.
Please verify all terms before signing.

Tenant Signature: __________________

Owner Signature: __________________
"""

    elif document_type == "Complaint Letter":
        return f"""COMPLAINT LETTER

Date: __________________

Complainant Name: {name}

Subject: Complaint Regarding the Following Matter

Details:

{purpose}

I request that the concerned authority review the above matter
and take appropriate action according to applicable procedures.

Name: {name}

Signature: __________________
"""

    elif document_type == "Legal Notice":
        return f"""LEGAL NOTICE - GENERAL TEMPLATE

Date: __________________

Name: {name}

Subject: Notice Regarding the Following Matter

Details:

{purpose}

This is a general template. It should be reviewed by a qualified
legal professional before official use.

Name: {name}

Signature: __________________
"""

    elif document_type == "Affidavit":
        return f"""AFFIDAVIT - GENERAL TEMPLATE

Date: __________________

I, {name}, state that the following information is provided by me:

{purpose}

I declare that the information stated above is true to the best
of my knowledge and belief.

Name: {name}

Signature: __________________

Place: __________________
"""

    else:
        return "Please select a valid document type."


@app.route("/", methods=["GET", "POST"])
def home():

    document = ""

    if request.method == "POST":

        name = request.form.get("name")
        document_type = request.form.get("document_type")
        purpose = request.form.get("purpose")

        document = generate_document(
            name,
            document_type,
            purpose
        )

    return render_template(
        "index.html",
        document=document
    )


@app.route("/download-pdf", methods=["POST"])
def download_pdf():

    name = request.form.get("name")
    document_type = request.form.get("document_type")
    purpose = request.form.get("purpose")

    document = generate_document(
        name,
        document_type,
        purpose
    )

    pdf_buffer = io.BytesIO()

    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

    width, height = A4

    x = 50
    y = height - 60

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, y, "AI Legal Document Creator")

    y -= 35

    pdf.setFont("Helvetica", 11)

    for line in document.split("\n"):

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50

        pdf.drawString(x, y, line[:100])
        y -= 18

    pdf.save()

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="legal_document.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)