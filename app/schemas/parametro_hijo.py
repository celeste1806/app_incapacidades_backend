from pydantic import BaseModel, Field


class ParametroHijoBase(BaseModel):
    parametro_id: int
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool = True


class ParametroHijoCreate(ParametroHijoBase):
    pass


class ParametroHijoUpdate(BaseModel):
    parametro_id: int | None = Field(default=None)
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    estado: bool | None = None


class ParametroHijoOut(ParametroHijoBase):
    id_parametrohijo: int

    class Config:
        from_attributes = True
