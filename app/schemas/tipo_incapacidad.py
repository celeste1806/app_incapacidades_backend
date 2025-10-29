from pydantic import BaseModel, Field


class TipoIncapacidadBase(BaseModel):
   
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool = True


class TipoIncapacidadCreate(TipoIncapacidadBase):
    pass

# Alias/versión explícita para evitar cualquier caché de clases antiguas en Swagger
class TipoIncapacidadCreateV2(TipoIncapacidadBase):
    pass


class TipoIncapacidadUpdate(BaseModel):
    
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None


class TipoIncapacidadOut(TipoIncapacidadBase):
    id_tipo_incapacidad: int

    class Config:
        from_attributes = True
