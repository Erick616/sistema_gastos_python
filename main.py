import json
import os
from datetime import datetime


CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MOVIMIENTOS = os.path.join(
    CARPETA_PROYECTO,
    "movimientos.json"
)


def cargar_movimientos():
    if not os.path.exists(ARCHIVO_MOVIMIENTOS):
        return []

    try:
        with open(
            ARCHIVO_MOVIMIENTOS,
            "r",
            encoding="utf-8"
        ) as archivo:
            return json.load(archivo)

    except (json.JSONDecodeError, OSError):
        print("No se pudieron cargar los movimientos.")
        return []


movimientos = cargar_movimientos()


def guardar_movimientos():
    try:
        with open(
            ARCHIVO_MOVIMIENTOS,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                movimientos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    except OSError:
        print("No se pudieron guardar los movimientos.")


def mostrar_menu():
    print("\n=== SISTEMA DE GASTOS PERSONALES ===")
    print("1. Registrar ingreso")
    print("2. Registrar gasto")
    print("3. Ver movimientos")
    print("4. Ver saldo disponible")
    print("5. Ver gastos por categoría")
    print("6. Salir")


def pedir_monto():
    try:
        monto = float(input("Monto: "))

        if monto <= 0:
            print("El monto debe ser mayor que cero.")
            return None

        return monto

    except ValueError:
        print("Debes escribir un número válido.")
        return None


def registrar_ingreso():
    descripcion = input(
        "Descripción del ingreso: "
    ).strip()

    if descripcion == "":
        print("La descripción no puede estar vacía.")
        return

    monto = pedir_monto()

    if monto is None:
        return

    movimientos.append({
        "tipo": "ingreso",
        "descripcion": descripcion,
        "categoria": "Ingreso",
        "monto": monto,
        "fecha": datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    })

    guardar_movimientos()
    print("Ingreso registrado correctamente.")


def registrar_gasto():
    descripcion = input(
        "Descripción del gasto: "
    ).strip()

    categoria = input(
        "Categoría del gasto: "
    ).strip()

    if descripcion == "" or categoria == "":
        print(
            "La descripción y la categoría "
            "son obligatorias."
        )
        return

    monto = pedir_monto()

    if monto is None:
        return

    movimientos.append({
        "tipo": "gasto",
        "descripcion": descripcion,
        "categoria": categoria,
        "monto": monto,
        "fecha": datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    })

    guardar_movimientos()
    print("Gasto registrado correctamente.")


def ver_movimientos():
    if not movimientos:
        print("No hay movimientos registrados.")
        return

    print("\n=== MOVIMIENTOS REGISTRADOS ===")

    for numero, movimiento in enumerate(
        movimientos,
        start=1
    ):
        signo = "+" if movimiento["tipo"] == "ingreso" else "-"

        print(
            f"{numero}. "
            f"{movimiento['fecha']} | "
            f"{movimiento['tipo'].capitalize()} | "
            f"{movimiento['descripcion']} | "
            f"{movimiento['categoria']} | "
            f"{signo}${movimiento['monto']:.2f}"
        )


def calcular_totales():
    total_ingresos = 0
    total_gastos = 0

    for movimiento in movimientos:
        if movimiento["tipo"] == "ingreso":
            total_ingresos += movimiento["monto"]
        else:
            total_gastos += movimiento["monto"]

    return total_ingresos, total_gastos


def ver_saldo():
    if not movimientos:
        print("No hay movimientos registrados.")
        return

    total_ingresos, total_gastos = calcular_totales()
    saldo = total_ingresos - total_gastos

    print("\n=== RESUMEN FINANCIERO ===")
    print(f"Total de ingresos: ${total_ingresos:.2f}")
    print(f"Total de gastos: ${total_gastos:.2f}")
    print(f"Saldo disponible: ${saldo:.2f}")


def ver_gastos_por_categoria():
    gastos_por_categoria = {}

    for movimiento in movimientos:
        if movimiento["tipo"] == "gasto":
            categoria = movimiento["categoria"]
            monto = movimiento["monto"]

            if categoria not in gastos_por_categoria:
                gastos_por_categoria[categoria] = 0

            gastos_por_categoria[categoria] += monto

    if not gastos_por_categoria:
        print("No hay gastos registrados.")
        return

    print("\n=== GASTOS POR CATEGORÍA ===")

    for categoria, total in gastos_por_categoria.items():
        print(f"{categoria}: ${total:.2f}")


def main():
    while True:
        mostrar_menu()
        opcion = input(
            "Selecciona una opción: "
        ).strip()

        if opcion == "1":
            registrar_ingreso()

        elif opcion == "2":
            registrar_gasto()

        elif opcion == "3":
            ver_movimientos()

        elif opcion == "4":
            ver_saldo()

        elif opcion == "5":
            ver_gastos_por_categoria()

        elif opcion == "6":
            print("Hasta luego.")
            break

        else:
            print("Esa opción no es válida.")


if __name__ == "__main__":
    main()