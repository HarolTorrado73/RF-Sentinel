import argparse
import sys

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rf-sentinel", description="Plataforma de análisis de radiofrecuencia"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Comando API server
    api_parser = subparsers.add_parser("api", help="Iniciar servidor API")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host del servidor")
    api_parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor")

    # Comando UI
    subparsers.add_parser("ui", help="Iniciar interfaz gráfica")

    args = parser.parse_args()

    if args.command == "api":
        uvicorn.run("rf_sentinel.api.main:app", host=args.host, port=args.port, reload=True)
    elif args.command == "ui":
        from rf_sentinel.ui.main import main as ui_main

        ui_main()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
