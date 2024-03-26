# -*- coding: utf-8 -*-
"""Contains patterns used for identifying properties of widgets."""

from pypdf.generic import (DictionaryObject, NameObject, NumberObject,
                           TextStringObject)

from .constants import (AP, AS, CA, DA, FT, MK, READ_ONLY, Btn, Ch, Ff, Opt,
                        Parent, Q, Sig, Subtype, T, Tx, V, Widget, Yes)
from .middleware.checkbox import Checkbox
from .middleware.dropdown import Dropdown
from .middleware.radio import Radio
from .middleware.signature import Signature
from .middleware.text import Text

WIDGET_TYPE_PATTERNS = [
    (
        ({FT: Sig},),
        Signature,
    ),
    (
        ({FT: Tx},),
        Text,
    ),
    (
        ({FT: Btn},),
        Checkbox,
    ),
    (
        ({FT: Ch},),
        Dropdown,
    ),
    (
        ({Parent: {FT: Ch}},),
        Dropdown,
    ),
    (
        ({Parent: {FT: Tx}},),
        Text,
    ),
    (
        (
            {Parent: {FT: Btn}},
            {Parent: {Subtype: Widget}},
        ),
        Checkbox,
    ),
    (
        ({Parent: {FT: Btn}},),
        Radio,
    ),
]

WIDGET_KEY_PATTERNS = [
    {T: True},
    {Parent: {T: True}},
]

DROPDOWN_CHOICE_PATTERNS = [
    {Opt: True},
    {Parent: {Opt: True}},
]

WIDGET_ALIGNMENT_PATTERNS = [
    {Q: True},
    {Parent: {Q: True}},
]

TEXT_FIELD_FLAG_PATTERNS = [
    {Ff: True},
    {Parent: {Ff: True}},
]

TEXT_FIELD_APPEARANCE_PATTERNS = [
    {DA: True},
    {Parent: {DA: True}},
]

BUTTON_STYLE_PATTERNS = [
    {MK: {CA: True}},
]


def simple_update_checkbox_value(annot: DictionaryObject) -> None:
    """Patterns to update values for checkbox annotations."""

    annot[NameObject(AS)] = NameObject(Yes)


def simple_update_radio_value(annot: DictionaryObject, widget: Radio) -> None:
    """Patterns to update values for radio annotations."""

    annot[NameObject(AS)] = NameObject(f"/{widget.value}")


def simple_update_dropdown_value(annot: DictionaryObject, widget: Dropdown) -> None:
    """Patterns to update values for dropdown annotations."""

    annot[NameObject(V)] = TextStringObject(widget.choices[widget.value])
    annot[NameObject(AP)] = TextStringObject(widget.choices[widget.value])


def simple_update_text_value(annot: DictionaryObject, widget: Text) -> None:
    """Patterns to update values for text annotations."""

    annot[NameObject(V)] = TextStringObject(widget.value)
    annot[NameObject(AP)] = TextStringObject(widget.value)


def simple_flatten_radio(annot: DictionaryObject) -> None:
    """Patterns to flatten checkbox annotations."""

    annot[NameObject(Parent)][NameObject(Ff)] = NumberObject(  # noqa
        int(annot[NameObject(Parent)].get(NameObject(Ff), 0)) | READ_ONLY  # noqa
    )


def simple_flatten_generic(annot: DictionaryObject) -> None:
    """Patterns to flatten generic annotations."""

    annot[NameObject(Ff)] = NumberObject(
        int(annot.get(NameObject(Ff), 0)) | READ_ONLY  # noqa
    )
