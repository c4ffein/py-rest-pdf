"""PyRestPdf URL Configuration"""

from base64 import b64decode, b64encode

from django.urls import path
from ninja import NinjaAPI, Schema
from ninja.errors import ValidationError
from ninja.orm.fields import AnyObject

from apps.pdf_template.models import PdfTemplate
from apps.generated_pdf.pdf_gen import gen_pdf


api = NinjaAPI()


class PdfTemplateS(Schema):
    file: str


@api.get("/pdf-template/{item_id}")
def get_pdf_template(request, item_id: int):
    if request.custom_rights not in ["r", "w"]:
        raise ValidationError
    pdf_template = PdfTemplate.objects.get(id=item_id)
    return {"id": pdf_template.id, "file": b64encode(pdf_template.file).decode()}


@api.post("/pdf-template")
def create(request, payload: PdfTemplateS):
    if request.custom_rights != "w":
        raise ValidationError
    pdf_template = PdfTemplate.objects.create(file=b64decode(payload.file))
    return {"id": pdf_template.id}


class PdfGeneratedS(Schema):
    template_id: int
    works: AnyObject


@api.post("/generated-pdf")
def get_generated_pdf(request, payload: PdfGeneratedS):
    if request.custom_rights not in ["r", "w"]:
        raise ValidationError
    generated_pdf = gen_pdf(PdfTemplate.objects.get(id=payload.template_id).file, payload.works)
    return {"file": b64encode(generated_pdf).decode(), "works": payload.works}


urlpatterns = [
    path("", api.urls),
]
