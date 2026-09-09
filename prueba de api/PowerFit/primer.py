# Importa funciones para escribir texto y controlar la salida.
import sys
# Importa pausas para producir el efecto de animación.
import time
# Importa Protocol para definir interfaces simples.
from typing import Protocol
# Importa dataclass para guardar dependencias del servicio.
from dataclasses import dataclass
    
# 1. Definición de Protocolos (Interfaces)
class MessageFormatter(Protocol):
    def format(self, target: str) -> str:
        ...


class ConsolePrinter(Protocol):
    def render(self, message: str) -> None:
        ...


# 2. Implementaciones Concretas
class StandardFormatter:
    def __init__(self, prefix: str = "🚀", suffix: str = "⚡"):
        self.prefix = prefix
        self.suffix = suffix

    def format(self, target: str) -> str:
        return f"{self.prefix} ¡Hola, {target}! {self.suffix}"


class AnimatedConsolePrinter:
    def __init__(self, delay: float = 0.03):
        self.delay = delay

    def render(self, message: str) -> None:
        print("\n" + "=" * 45)
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.delay)
        print("\n" + "=" * 45 + "\n")


# 3. Servicio Principal con Inyección de Dependencias
@dataclass
class GreeterService:
    formatter: MessageFormatter
    printer: ConsolePrinter

    def greet(self, target: str = "Mundo PRO") -> None:
        formatted_msg = self.formatter.format(target)
        self.printer.render(formatted_msg)


# 4. Punto de Entrada
def main() -> None:
    formatter = StandardFormatter(prefix="🔥", suffix="✨")
    printer = AnimatedConsolePrinter(delay=0.03)

    greeter = GreeterService(formatter=formatter, printer=printer)
    greeter.greet("Mundo PRO - PowerFit System")


if __name__ == "__main__":
    main()