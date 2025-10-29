from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    correo_electronico: str = Field(alias="email")
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    correo_electronico: str
    rol: int | None = None
    nombre: str
    id_usuario: int


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id_usuario: int
    nombre: str
    numero_identificacion: str | None = None
    correo_electronico: str
    telefono: str | None = None
    tipo_identificacion: str | None = None
    tipo_empleador: str | None = None
    cargo_interno: str | None = None
    rol: str | None = None


class LogoutResponse(BaseModel):
    message: str = "Logged out successfully"


class ForgotPasswordRequest(BaseModel):
    correo_electronico: str = Field(alias="email")


class ForgotPasswordResponse(BaseModel):
    message: str = "Si el correo existe, se enviará un enlace para restablecer la contraseña"


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class ResetPasswordResponse(BaseModel):
    message: str = "Contraseña restablecida exitosamente"


# Mantener compatibilidad con el esquema anterior
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    correo_electronico: str
    rol: int | None = None
    nombre: str


