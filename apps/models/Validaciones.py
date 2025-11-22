"""
Utilities de validación portadas desde JS a Python.

Funciones devuelven `None` si la validación pasa, o un mensaje de error (string) si falla.
"""

from datetime import datetime, date
import calendar
import re
from typing import Optional, List


class Validaciones:
    @staticmethod
    def esNumeroPositivo(valor, nombreCampo: str) -> Optional[str]:
        try:
            num = float(valor)
        except Exception:
            raise ValueError(f"{nombreCampo} debe ser un número positivo")
        if num <= 0:
            raise ValueError(f"{nombreCampo} debe ser un número positivo")
        return num

    @staticmethod
    def esEnteroPositivo(valor, nombreCampo: str, max_value=None) -> Optional[str]:
        try:
            f = float(valor)
        except Exception:
            raise ValueError(f"{nombreCampo} debe ser un número entero positivo")
        if f <= 0 or not float(f).is_integer():
            raise ValueError(f"{nombreCampo} debe ser un número entero positivo")
        if max_value is not None and f > max_value:
            raise ValueError(f"{nombreCampo} no puede ser mayor que {max_value}")
        return f

    @staticmethod
    def esDNIValido(dni) -> Optional[str]:
        if dni is None or (isinstance(dni, str) and dni.strip() == ""):
            raise ValueError("El DNI es obligatorio")

        dni_s = str(dni).strip().replace('.', '')

        if not re.fullmatch(r"\d+", dni_s):
            raise ValueError("El DNI debe contener solo números")

        if len(dni_s) < 7 or len(dni_s) > 8:
            raise ValueError("El DNI debe tener entre 7 y 8 dígitos")

        if re.fullmatch(r"0+", dni_s):
            raise ValueError("El DNI no puede ser un número inválido")
        
        if int(dni_s) < 0:
            raise ValueError("El DNI debe ser positivo")

        return int(dni_s)

    @staticmethod
    def esTelefonoValido(telefono) -> Optional[str]:
        if telefono is None:
            raise ValueError('El teléfono debe contener entre 7 y 15 dígitos')
        cleaned = re.sub(r"[\s-]", '', str(telefono))
        if not re.fullmatch(r"\d{7,15}", cleaned):
            raise ValueError('El teléfono debe contener entre 7 y 15 dígitos')
        return cleaned

    @staticmethod
    def esTextoValido(texto, nombreCampo: str, minLength: int = 2, maxLength: int = 100) -> Optional[str]:
        if texto is None:
            raise ValueError(f"{nombreCampo} debe tener al menos {minLength} caracteres")
        trimmed = str(texto).strip()
        if len(trimmed) < minLength:
            raise ValueError(f"{nombreCampo} debe tener al menos {minLength} caracteres")
        if len(trimmed) > maxLength:
            raise ValueError(f"{nombreCampo} no puede exceder {maxLength} caracteres")
        if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", trimmed):
            raise ValueError(f"{nombreCampo} solo puede contener letras y espacios")
        return trimmed

    @staticmethod
    def _parse_datetime(fecha) -> Optional[datetime]:
        if isinstance(fecha, datetime) or isinstance(fecha, date):
            return fecha
        if fecha is None or (isinstance(fecha, str) and fecha.strip() == ""):
            return None
        try:
            # soportar formato ISO local como 'YYYY-MM-DDTHH:MM'
            return datetime.fromisoformat(str(fecha))
        except Exception:
            try:
                # intentar parseo flexible
                return datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S")
            except Exception:
                try:
                    # aceptar formatos comunes con solo fecha 'YYYY-MM-DD'
                    return datetime.strptime(str(fecha), "%Y-%m-%d")
                except Exception:
                    try:
                        # aceptar formato DD/MM/YYYY que viene del frontend
                        return datetime.strptime(str(fecha), "%d/%m/%Y")
                    except Exception:
                        try:
                            return datetime.strptime(str(fecha), "%d/%m/%Y %H:%M:%S")
                        except Exception:
                            raise ValueError(f"{fecha} no es una fecha válida")
    @staticmethod
    def esFechaValida(fecha, nombreCampo: str) -> Optional[str]:
        if fecha is None or (isinstance(fecha, str) and fecha.strip() == ""):
            raise ValueError(f"{nombreCampo} es requerida")
        fechaObj = Validaciones._parse_datetime(fecha)
        if fechaObj is None:
            raise ValueError(f"{nombreCampo} no es válida")
        if fechaObj.minute != 0:
            raise ValueError(f"{nombreCampo} debe tener los minutos en 00")
        return fechaObj

    @staticmethod
    def esFechaFutura(fecha, nombreCampo: str) -> Optional[str]:
        # esFechaValida devuelve un objeto datetime o lanza ValueError
        fechaObj = Validaciones.esFechaValida(fecha, nombreCampo)
        ahora = datetime.now()
        if fechaObj < ahora:
            raise ValueError(f"{nombreCampo} debe ser una fecha futura")
        return fechaObj

    @staticmethod
    def esFechaDentroDeRango(fecha, nombreCampo: str, mesesMaximos: int) -> Optional[str]:
        # esFechaFutura devolverá un datetime válido o lanzará ValueError
        fechaObj = Validaciones.esFechaFutura(fecha, nombreCampo)
        ahora = datetime.now()
        # sumar meses de forma segura
        month = ahora.month - 1 + mesesMaximos
        year = ahora.year + month // 12
        month = month % 12 + 1
        day = min(ahora.day, calendar.monthrange(year, month)[1])
        fechaMaxima = datetime(year, month, day, ahora.hour, ahora.minute, ahora.second, ahora.microsecond)
        if fechaObj > fechaMaxima:
            raise ValueError(f"{nombreCampo} no puede ser superior a {mesesMaximos} meses desde hoy")
        return fechaObj

    @staticmethod
    def esFechaPosterior(fechaInicio, fechaFin) -> Optional[str]:
        inicio = Validaciones._parse_datetime(fechaInicio)
        fin = Validaciones._parse_datetime(fechaFin)
        if inicio is None or fin is None:
            raise ValueError('Formato de fecha inválido')
        if fin <= inicio:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        # devolver el objeto datetime válido (consistente con otras validaciones)
        return fin

    @staticmethod
    def mostrarErrores(errores: List[str]) -> Optional[str]:
        if errores and len(errores) > 0:
            return "\n".join(errores)
        return None
