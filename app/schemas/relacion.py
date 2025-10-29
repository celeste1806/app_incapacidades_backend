from pydantic import BaseModel, Field, ConfigDict


class RelacionBase(BaseModel):
    tipo_incapacidad_id: int 
    archivo_id: int


class RelacionUpdate(BaseModel):
    pass
class RelacionCreate(RelacionBase):
    pass

class RelacionOut(RelacionBase):
    # Permite crear el esquema desde objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)


class RelacionWithNamesOut(BaseModel):
    tipo_incapacidad_id: int
    tipo_incapacidad_nombre: str | None = None
    archivo_id: int
    archivo_nombre: str | None = None

    