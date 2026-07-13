import json

ACADEMY_DISCLAIMER = (
    "La Academia RF Sentinel promueve educación, investigación y aprendizaje responsable. "
    "No se enseña interferencia ni actividades ilegales. Cumple siempre la normativa "
    "de tu país antes de transmitir o analizar señales."
)

HACKRF_DISCLAIMER = (
    "HackRF y dispositivos SDR son herramientas de investigación. La transmisión sin "
    "autorización es ilegal. Usa solo frecuencias y potencias permitidas por ley."
)


def _quiz(questions: list[dict], passing_score: int = 70) -> str:
    return json.dumps({"questions": questions, "passing_score": passing_score})


def _visual(visual_type: str, data: dict) -> str:
    return json.dumps({"type": visual_type, **data})


ACADEMY_COURSES = [
    {
        "slug": "rf-fundamentos",
        "title": "Fundamentos de Radiofrecuencia",
        "description": (
            "Aprende los conceptos esenciales del espectro electromagnético, modulación "
            "y unidades de medida para comprender señales RF."
        ),
        "category": "rf",
        "difficulty": "beginner",
        "estimated_hours": 2.0,
        "disclaimer": ACADEMY_DISCLAIMER,
        "order_index": 1,
        "lessons": [
            {
                "slug": "espectro-electromagnetico",
                "title": "El espectro electromagnético",
                "content": (
                    "## Espectro electromagnético\n\n"
                    "Las ondas de radio son perturbaciones electromagnéticas que transportan "
                    "información sin necesidad de un medio físico.\n\n"
                    "### Conceptos clave\n"
                    "- **Frecuencia (Hz)**: ciclos por segundo de la onda\n"
                    "- **Longitud de onda**: distancia entre picos consecutivos\n"
                    "- **Banda ISM**: frecuencias de uso industrial, científico y médico (2.4 GHz, 5.8 GHz)\n\n"
                    "### Aplicaciones educativas\n"
                    "Observar el espectro ayuda a identificar fuentes legítimas: Wi-Fi, Bluetooth, "
                    "emisoras FM y satélites de investigación."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {
                        "frequencies_mhz": [88, 100, 144, 433, 915, 2400, 5800],
                        "amplitudes": [0.3, 0.9, 0.5, 0.4, 0.6, 0.8, 0.7],
                        "labels": ["FM", "FM", "VHF", "UHF", "ISM", "Wi-Fi", "5 GHz"],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué mide la frecuencia?",
                            "options": [
                                "Ciclos por segundo de la onda",
                                "Potencia en vatios",
                                "Distancia entre antenas",
                            ],
                            "correct_index": 0,
                            "explanation": "La frecuencia se expresa en Hertz (Hz).",
                        }
                    ]
                ),
                "order_index": 1,
                "duration_minutes": 15,
            },
            {
                "slug": "modulacion-am-fm",
                "title": "Modulación AM y FM",
                "content": (
                    "## Modulación\n\n"
                    "La modulación codifica información sobre una portadora.\n\n"
                    "- **AM**: varía la amplitud de la señal\n"
                    "- **FM**: varía la frecuencia instantánea\n\n"
                    "En investigación, reconocer el tipo de modulación permite clasificar "
                    "emisoras y comprender protocolos de comunicación."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {
                        "carrier_hz": 1000000,
                        "modulation": "fm",
                        "modulation_index": 0.5,
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué parámetro varía en FM?",
                            "options": [
                                "La frecuencia instantánea",
                                "La amplitud únicamente",
                                "La polarización",
                            ],
                            "correct_index": 0,
                            "explanation": "FM modula la frecuencia de la portadora.",
                        }
                    ]
                ),
                "order_index": 2,
                "duration_minutes": 20,
            },
            {
                "slug": "unidades-potencia",
                "title": "dBm, dBW y potencia",
                "content": (
                    "## Unidades logarítmicas\n\n"
                    "En RF se usa la escala decibel para comparar potencias:\n\n"
                    "- **dBm**: potencia referida a 1 mW\n"
                    "- **dBW**: potencia referida a 1 W\n"
                    "- **dBi**: ganancia de antena respecto a isótropa\n\n"
                    "Comprender estas unidades es fundamental para uso responsable y seguro."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {
                        "title": "Escala de potencia",
                        "items": [
                            {"label": "0 dBm", "value": "1 mW"},
                            {"label": "10 dBm", "value": "10 mW"},
                            {"label": "20 dBm", "value": "100 mW"},
                            {"label": "30 dBm", "value": "1 W"},
                        ],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿A qué equivale 0 dBm?",
                            "options": ["1 mW", "1 W", "1 µW"],
                            "correct_index": 0,
                            "explanation": "0 dBm es la referencia de 1 milivatios.",
                        }
                    ]
                ),
                "order_index": 3,
                "duration_minutes": 15,
            },
        ],
    },
    {
        "slug": "sdr-conceptos",
        "title": "Conceptos de SDR",
        "description": (
            "Introducción a Software Defined Radio: arquitectura, muestreo digital "
            "y flujo de señal desde la antena hasta el software."
        ),
        "category": "sdr",
        "difficulty": "beginner",
        "estimated_hours": 1.5,
        "disclaimer": ACADEMY_DISCLAIMER,
        "order_index": 2,
        "lessons": [
            {
                "slug": "que-es-sdr",
                "title": "¿Qué es un SDR?",
                "content": (
                    "## Software Defined Radio\n\n"
                    "Un SDR digitaliza señales RF lo antes posible y procesa el espectro "
                    "con software en lugar de circuitos analógicos fijos.\n\n"
                    "### Componentes típicos\n"
                    "1. Antena y front-end RF\n"
                    "2. Conversor ADC (muestreo)\n"
                    "3. FPGA o DSP para filtrado\n"
                    "4. Software (GNU Radio, SDR#, etc.)\n\n"
                    "Ventaja educativa: puedes experimentar con filtros y demoduladores "
                    "sin cambiar hardware."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {
                        "title": "Flujo SDR",
                        "items": [
                            {"label": "Antena", "value": "Captura RF"},
                            {"label": "LNA/ADC", "value": "Digitaliza"},
                            {"label": "Software", "value": "Procesa"},
                        ],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué hace el ADC en un SDR?",
                            "options": [
                                "Convierte señal analógica a digital",
                                "Amplifica la antena",
                                "Transmite en FM",
                            ],
                            "correct_index": 0,
                            "explanation": "El ADC muestrea la señal para procesarla en software.",
                        }
                    ]
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "muestreo-nyquist",
                "title": "Muestreo y teorema de Nyquist",
                "content": (
                    "## Muestreo digital\n\n"
                    "Para reconstruir una señal, el ADC debe muestrear al menos al doble "
                    "de la frecuencia máxima (teorema de Nyquist).\n\n"
                    "### Ejemplo\n"
                    "Señal de 1 MHz → mínimo 2 MSPS (mega-muestras por segundo).\n\n"
                    "En la práctica se usa sobremuestreo y filtros anti-aliasing."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {
                        "carrier_hz": 500000,
                        "modulation": "am",
                        "modulation_index": 0.8,
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Cuál es la tasa mínima según Nyquist?",
                            "options": [
                                "El doble de la frecuencia máxima",
                                "La mitad de la frecuencia máxima",
                                "Igual a la frecuencia portadora",
                            ],
                            "correct_index": 0,
                            "explanation": "Nyquist exige fs ≥ 2 × fmax.",
                        }
                    ]
                ),
                "order_index": 2,
                "duration_minutes": 25,
            },
        ],
    },
    {
        "slug": "hackrf-responsable",
        "title": "HackRF: Uso Responsable",
        "description": (
            "Guía ética y legal para usar HackRF One en educación e investigación, "
            "con énfasis en recepción pasiva y límites de transmisión."
        ),
        "category": "hackrf",
        "difficulty": "intermediate",
        "estimated_hours": 2.0,
        "disclaimer": HACKRF_DISCLAIMER,
        "order_index": 3,
        "lessons": [
            {
                "slug": "marco-legal",
                "title": "Marco legal y ético",
                "content": (
                    "## Uso responsable\n\n"
                    "Antes de operar cualquier SDR transmisor:\n\n"
                    "1. Consulta la normativa de tu país (FCC, CEPT, etc.)\n"
                    "2. Obtén licencias si transmites\n"
                    "3. Nunca interrumpas servicios críticos\n"
                    "4. Prioriza recepción pasiva para aprendizaje\n\n"
                    "**Prohibido en esta academia:** interferencia, jamming, escucha ilegal."
                ),
                "visual_type": "none",
                "visual_data": None,
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué actividad está prohibida en RF Sentinel?",
                            "options": [
                                "Interferencia y jamming",
                                "Recepción pasiva educativa",
                                "Análisis de espectro en laboratorio",
                            ],
                            "correct_index": 0,
                            "explanation": "La interferencia es ilegal y contraria a nuestra misión.",
                        },
                        {
                            "id": "q2",
                            "question": "¿Qué debes hacer antes de transmitir?",
                            "options": [
                                "Verificar normativa y licencias",
                                "Aumentar potencia al máximo",
                                "Transmitir en cualquier frecuencia",
                            ],
                            "correct_index": 0,
                            "explanation": "La legalidad depende de tu jurisdicción.",
                        },
                    ]
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "setup-hackrf",
                "title": "Configuración básica (solo recepción)",
                "content": (
                    "## Setup educativo HackRF\n\n"
                    "Para aprendizaje seguro, configura solo recepción:\n\n"
                    "```bash\n"
                    "hackrf_info\n"
                    "hackrf_transfer -r captura.raw -f 100000000 -s 2000000\n"
                    "```\n\n"
                    "Parámetros clave:\n"
                    "- `-f`: frecuencia central en Hz\n"
                    "- `-s`: tasa de muestreo\n"
                    "- `-r`: grabar a archivo (sin transmitir)\n\n"
                    "Analiza capturas offline con herramientas como inspectrum."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {
                        "frequencies_mhz": [98, 100, 102, 104, 106],
                        "amplitudes": [0.2, 0.95, 0.3, 0.7, 0.25],
                        "labels": ["FM", "FM", "FM", "FM", "FM"],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué flag usa hackrf_transfer para grabar?",
                            "options": ["-r", "-t", "-x"],
                            "correct_index": 0,
                            "explanation": "-r graba (receive) sin transmitir.",
                        }
                    ]
                ),
                "order_index": 2,
                "duration_minutes": 30,
            },
            {
                "slug": "limites-tx",
                "title": "Límites de transmisión",
                "content": (
                    "## Cuándo NO transmitir\n\n"
                    "Evita transmitir si:\n"
                    "- No tienes licencia amateur o autorización\n"
                    "- La frecuencia está reservada (aviación, emergencias)\n"
                    "- No conoces la potencia máxima permitida\n\n"
                    "En investigación universitaria, usa cámaras blindadas (Faraday) "
                    "para pruebas de TX controladas."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {
                        "title": "Zonas de riesgo",
                        "items": [
                            {"label": "Aviación", "value": "Prohibido sin licencia"},
                            {"label": "Emergencias", "value": "Nunca transmitir"},
                            {"label": "ISM 433 MHz", "value": "Verificar límites locales"},
                        ],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Dónde es seguro probar TX en laboratorio?",
                            "options": [
                                "Cámara Faraday con autorización",
                                "En la calle sin licencia",
                                "Cerca de un aeropuerto",
                            ],
                            "correct_index": 0,
                            "explanation": "Las cámaras blindadas contienen la señal.",
                        }
                    ]
                ),
                "order_index": 3,
                "duration_minutes": 20,
            },
        ],
    },
    {
        "slug": "senal-analisis",
        "title": "Análisis de Señales",
        "description": (
            "FFT, espectrogramas y técnicas para identificar modulaciones "
            "con datos simulados y capturas educativas."
        ),
        "category": "signals",
        "difficulty": "intermediate",
        "estimated_hours": 2.5,
        "disclaimer": ACADEMY_DISCLAIMER,
        "order_index": 4,
        "lessons": [
            {
                "slug": "fft-fundamentos",
                "title": "Transformada de Fourier (FFT)",
                "content": (
                    "## FFT en SDR\n\n"
                    "La FFT descompone una señal temporal en componentes de frecuencia.\n\n"
                    "En un waterfall (espectrograma):\n"
                    "- Eje X: tiempo\n"
                    "- Eje Y: frecuencia\n"
                    "- Color: intensidad\n\n"
                    "Útil para detectar patrones, saltos de frecuencia (FHSS) y portadoras."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {
                        "frequencies_mhz": list(range(2400, 2410)),
                        "amplitudes": [0.1, 0.3, 0.9, 0.5, 0.2, 0.8, 0.4, 0.6, 0.3, 0.1],
                        "labels": ["Wi-Fi"] * 10,
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué muestra un espectrograma en el eje Y?",
                            "options": ["Frecuencia", "Tiempo", "Fase"],
                            "correct_index": 0,
                            "explanation": "El eje Y representa frecuencia en un waterfall.",
                        }
                    ]
                ),
                "order_index": 1,
                "duration_minutes": 25,
            },
            {
                "slug": "identificar-modulacion",
                "title": "Identificar modulaciones",
                "content": (
                    "## Patrones visuales\n\n"
                    "| Modulación | Patrón en espectro |\n"
                    "|------------|-------------------|\n"
                    "| AM | Portadora central + bandas laterales |\n"
                    "| FM | Banda ancha uniforme |\n"
                    "| FSK | Picos discretos |\n"
                    "| PSK | Constelación en I/Q |\n\n"
                    "Practica con capturas de referencia antes de analizar señales reales."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {
                        "carrier_hz": 2000000,
                        "modulation": "fm",
                        "modulation_index": 1.2,
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué modulación muestra picos discretos?",
                            "options": ["FSK", "AM", "CW"],
                            "correct_index": 0,
                            "explanation": "FSK salta entre frecuencias discretas.",
                        }
                    ]
                ),
                "order_index": 2,
                "duration_minutes": 30,
            },
            {
                "slug": "iq-datos",
                "title": "Datos I/Q y constelaciones",
                "content": (
                    "## Representación I/Q\n\n"
                    "Las señales complejas se representan como I (in-phase) + jQ (quadrature).\n\n"
                    "La constelación I/Q visualiza modulaciones digitales (QPSK, QAM).\n\n"
                    "En esta plataforma usamos **datos simulados** para practicar sin hardware."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {
                        "title": "Constelación QPSK (simulada)",
                        "items": [
                            {"label": "00", "value": "Cuadrante I+, Q+"},
                            {"label": "01", "value": "Cuadrante I-, Q+"},
                            {"label": "10", "value": "Cuadrante I+, Q-"},
                            {"label": "11", "value": "Cuadrante I-, Q-"},
                        ],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué representan I y Q?",
                            "options": [
                                "Componentes en fase y cuadratura",
                                "Intensidad y calidad",
                                "Entrada y salida",
                            ],
                            "correct_index": 0,
                            "explanation": "I/Q es la representación compleja de la señal.",
                        }
                    ]
                ),
                "order_index": 3,
                "duration_minutes": 25,
            },
        ],
    },
    {
        "slug": "hardware-integracion",
        "title": "Integración de Hardware",
        "description": (
            "Comparativa RTL-SDR vs HackRF, conexiones, calibración y buenas "
            "prácticas de laboratorio."
        ),
        "category": "hardware",
        "difficulty": "intermediate",
        "estimated_hours": 1.5,
        "disclaimer": ACADEMY_DISCLAIMER,
        "order_index": 5,
        "lessons": [
            {
                "slug": "comparativa-sdr",
                "title": "RTL-SDR vs HackRF",
                "content": (
                    "## Comparativa educativa\n\n"
                    "| Característica | RTL-SDR | HackRF One |\n"
                    "|----------------|---------|------------|\n"
                    "| Rango | ~24 MHz - 1.7 GHz | 1 MHz - 6 GHz |\n"
                    "| TX | No | Sí (con precaución) |\n"
                    "| Precio | Bajo | Medio |\n"
                    "| Uso ideal | Recepción, aprendizaje | Investigación full-duplex |\n\n"
                    "Para principiantes: empieza con RTL-SDR en recepción."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {
                        "title": "Rangos de frecuencia",
                        "items": [
                            {"label": "RTL-SDR", "value": "24 MHz – 1.7 GHz (RX)"},
                            {"label": "HackRF", "value": "1 MHz – 6 GHz (RX/TX)"},
                        ],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Qué dispositivo es solo recepción?",
                            "options": ["RTL-SDR", "HackRF One", "Ambos transmiten"],
                            "correct_index": 0,
                            "explanation": "RTL-SDR típicamente no transmite.",
                        }
                    ]
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "conexiones-calibracion",
                "title": "Conexiones y calibración",
                "content": (
                    "## Buenas prácticas de laboratorio\n\n"
                    "1. Usa cables y conectores de calidad (SMA)\n"
                    "2. Evita sobrecargar entradas RF\n"
                    "3. Calibra offset de frecuencia con referencia conocida\n"
                    "4. Mantén antenas lejos de fuentes de interferencia artificial\n\n"
                    "Registra siempre offset y ganancia en tus notas de investigación."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {
                        "frequencies_mhz": [999, 1000, 1001],
                        "amplitudes": [0.2, 1.0, 0.2],
                        "labels": ["Ref", "1 GHz Ref", "Ref"],
                    },
                ),
                "quiz": _quiz(
                    [
                        {
                            "id": "q1",
                            "question": "¿Por qué calibrar el offset?",
                            "options": [
                                "El oscilador local puede desviarse",
                                "Para aumentar la potencia TX",
                                "No es necesario en SDR",
                            ],
                            "correct_index": 0,
                            "explanation": "Los TCXO/osciladores tienen error de frecuencia.",
                        }
                    ]
                ),
                "order_index": 2,
                "duration_minutes": 25,
            },
        ],
    },
]
