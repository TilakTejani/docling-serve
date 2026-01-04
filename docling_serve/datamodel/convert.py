# Define the input options for the API
from typing import Annotated

from pydantic import Field

from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
)
from docling.models.factories import get_ocr_factory
from docling_jobkit.datamodel.convert import ConvertDocumentsOptions

from docling_serve.settings import docling_serve_settings

ocr_factory = get_ocr_factory(
    allow_external_plugins=docling_serve_settings.allow_external_plugins
)
ocr_engines_enum = ocr_factory.get_enum()


class ConvertDocumentsRequestOptions(ConvertDocumentsOptions):
    ocr_engine: Annotated[  # type: ignore
        ocr_engines_enum,
        Field(
            description=(
                "The OCR engine to use. String. "
                f"Allowed values: {', '.join([v.value for v in ocr_engines_enum])}. "
                "Optional, defaults to easyocr."
            ),
            examples=[EasyOcrOptions.kind],
        ),
    ] = ocr_engines_enum(EasyOcrOptions.kind)  # type: ignore

    ocr_lang: Annotated[
        list[str] | None,
        Field(
            description=(
                "List of languages used by the OCR engine. Note that each OCR engine has different values "
                "for the language names. String or list of strings. Optional, defaults to empty. "
                "EasyOCR supported languages: af, az, bs, cs, cy, da, de, en, es, et, fr, ga, hr, hu, id, "
                "is, it, ku, la, lt, lv, mi, ms, mt, nl, no, oc, pi, pl, pt, ro, rs_latin, sk, sl, sq, "
                "sv, sw, tl, tr, uz, vi, ar, fa, ug, ur, ru, rs_cyrillic, be, bg, uk, mn, abq, ady, kbd, "
                "ava, dar, inh, che, lbe, lez, tab, tjk, hi, mr, ne, bh, mai, ang, bho, mah, sck, new, "
                "gom, sa, bgc, bn, as, mni, th, ch_sim, ch_tra, ja, ko, ta, te, kn"
            ),
            examples=[["en", "fr", "de", "es"]],
        ),
    ] = None

    document_timeout: Annotated[
        float,
        Field(
            description="The timeout for processing each document, in seconds.",
            gt=0,
            le=docling_serve_settings.max_document_timeout,
        ),
    ] = docling_serve_settings.max_document_timeout
