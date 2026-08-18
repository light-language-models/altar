"""Portable Altar core."""

from .contracts import MODE_COUNTS, MomentRequest, Symbol, SymbolPack, SymbolSystem
from .field import FieldEnvelope, compile_field
from .packs import load_pack
from .process import ThinkingDepthReceipt, choose_thinking_depth
from .selector import DrawReceipt, select

__all__ = [
    "MODE_COUNTS",
    "MomentRequest",
    "DrawReceipt",
    "FieldEnvelope",
    "ThinkingDepthReceipt",
    "Symbol",
    "SymbolPack",
    "SymbolSystem",
    "load_pack",
    "select",
    "compile_field",
    "choose_thinking_depth",
]

__version__ = "0.2.0"
