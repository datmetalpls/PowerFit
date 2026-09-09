"""Control de existencias de un producto."""

from datetime import date


class Inventario:
    """Registra niveles de stock y la fecha de su última actualización."""

    def __init__(self, fechaActualizacion: date, stockMinimo: int, stockActual: int):
        # Función: conservar el estado operativo de las existencias.
        # Razón: permite anticipar faltantes y coordinar reposiciones.
        if stockMinimo < 0 or stockActual < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.fechaActualizacion = fechaActualizacion
        self.stockMinimo = stockMinimo
        self.stockActual = stockActual

    def reponerStock(self, cant: int) -> None:
        # Función: aumentar el stock y actualizar la fecha de control.
        # Razón: registra la reposición de mercadería recibida.
        if cant < 0:
            raise ValueError("La cantidad de reposición no puede ser negativa.")
        self.stockActual += cant
        self.fechaActualizacion = date.today()

    def alertaStock(self) -> bool:
        # Función: detectar stock igual o inferior al mínimo configurado.
        # Razón: permite actuar antes de que un producto se agote.
        return self.stockActual <= self.stockMinimo
