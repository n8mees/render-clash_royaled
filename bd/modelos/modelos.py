from pydantic import BaseModel
from typing import Optional

class Carta(BaseModel):
    nombre: str
    elixir: int
    rareza: str
    arena: int
    tipo: str
    año_lanzamiento: int
    imagen: str

class UpdateCarta(BaseModel):
    nombre: Optional[str] = None
    elixir: Optional[int] = None
    rareza: Optional[str] = None
    arena: Optional[int] = None
    tipo: Optional[str] = None
    año_lanzamiento: Optional[int] = None
    imagen: Optional[str] = None