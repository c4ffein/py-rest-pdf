import io
from base64 import b64decode

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image
import bleach


def canvased_signature(canvas, b64, left, top):
    image = Image.open(io.BytesIO(b64decode(b64)))

    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image)
    # Should check width / height, but not needed for that use case
    # https://intellipaat.com/community/9926/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    canvas.drawImage(ImageReader(new_image), left, top, width=185, height=75)


def draw_paragraph(canvas, msg, x, y, max_width, max_height):
    message_style = ParagraphStyle("Normal")
    message = bleach.clean(msg)  # As Paragraph supports basic xml/markup syntax for styles etc
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)


def gen_pdf(template, data):
    template_io = io.BytesIO(template)
    out_io = io.BytesIO()
    template_pdf = PdfFileReader(template_io)

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    for s in data.get("strings", []):
        c.drawString(*s)
    for p in data.get("paragraphs", []):
        draw_paragraph(c, *p)  # max_height doesn't seem to work but who cares
    for s in data.get("signatures", []):
        canvased_signature(c, *s)

    c.showPage()
    c.save()
    packet.seek(0)
    layer = PdfFileReader(packet)

    output_pdf = PdfFileWriter()
    page = template_pdf.getPage(0)
    page.mergePage(layer.getPage(0))
    output_pdf.addPage(page)
    output_pdf.write(out_io)
    out_io.seek(0)
    return out_io.read()
