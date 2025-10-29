from pydantic import BaseModel, Field


class ArchivoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool = True


class ArchivoCreate(ArchivoBase):
    pass


class ArchivoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None


class ArchivoOut(ArchivoBase):
    id_archivo: int

    class Config:
        from_attributes = True


class ArchivoLinkOut(BaseModel):
    """Respuesta al vincular un archivo con una incapacidad."""
    incapacidad_id: int
    archivo_id: int


class ArchivoLinkOutWithUrl(ArchivoLinkOut):
    url_documento: str