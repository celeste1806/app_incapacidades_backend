from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):
    nombre_completo: str = Field(min_length=1, max_length=150)
    numero_identificacion: str = Field(min_length=1, max_length=150)
    tipo_identificacion_id: int = Field(default=None)
    tipo_empleador_id: int = Field(default=None)
    cargo_interno: int
    correo_electronico: str = Field(min_length=1, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    password: str = Field(min_length=1, max_length=150)
    rol_id: int = Field(default=None)
    estado: bool = True


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre_completo: str | None = Field(default=None, min_length=1, max_length=150)
    numero_identificacion: str | None = Field(default=None, min_length=1, max_length=150)
    tipo_identificacion_id: int | None = Field(default=None)
    tipo_empleador_id: int | None = Field(default=None)
    cargo_interno: int | None = Field(default=None)
    correo_electronico: str | None = Field(default=None, min_length=1, max_length=150)
    telefono: str | None = Field(default=None, max_length=30)
    password: str | None = Field(default=None, min_length=1, max_length=150)
    rol_id: int | None = Field(default=None)
    estado: bool | None = Field(default=None)   


class UsuarioOut(UsuarioBase):
    # Mapear atributo ORM cargo_interno_id al campo API cargo_interno
    cargo_interno: int = Field(validation_alias="cargo_interno_id")
    id_usuario: int

    class Config:
        from_attributes = True
