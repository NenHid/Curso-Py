"""Muestra una notificación de escritorio de prueba usando Plyer.

Ejecutar desde la raíz del proyecto:
    uv run python Automatizacion/Modulo_3/probar_notificacion.py
"""

from plyer import notification


def main() -> None:
    notification.notify(
        title="Prueba de Plyer",
        message="Si ves este aviso, Plyer pudo solicitar una notificación al sistema.",
        timeout=10,
    )
    print("Solicitud de notificación enviada al sistema operativo.")


if __name__ == "__main__":
    main()
