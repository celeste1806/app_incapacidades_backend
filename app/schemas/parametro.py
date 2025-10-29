from pydantic import BaseModel, Field


class ParametroBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool = True


class ParametroCreate(ParametroBase):
    pass


class ParametroUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None


class ParametroOut(ParametroBase):
    id_parametro: int

    class Config:
        from_attributes = True
