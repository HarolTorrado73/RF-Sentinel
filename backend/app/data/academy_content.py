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
            "Aprende los conceptos esenciales del espectro electromagnético, modulación y unidades de medida para comprender señales RF."
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
                    "## Espectro electromagnético\n\nLas ondas de radio son perturbaciones electromagnéticas que transportan información sin necesidad de un medio físico.\n\n### Conceptos clave\n- **Frecuencia (Hz)**: ciclos por segundo de la onda\n- **Longitud de onda**: distancia entre picos consecutivos\n- **Banda ISM**: frecuencias de uso industrial, científico y médico (2.4 GHz, 5.8 GHz)\n\n### Aplicaciones educativas\nObservar el espectro ayuda a identificar fuentes legítimas: Wi-Fi, Bluetooth, emisoras FM y satélites de investigación."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {"frequencies_mhz": [88, 100, 144, 433, 915, 2400, 5800], "amplitudes": [0.3, 0.9, 0.5, 0.4, 0.6, 0.8, 0.7], "labels": ["FM", "FM", "VHF", "UHF", "ISM", "Wi-Fi", "5 GHz"]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué mide la frecuencia?", "options": ["Ciclos por segundo de la onda", "Potencia en vatios", "Distancia entre antenas"], "correct_index": 0, "explanation": "La frecuencia se expresa en Hertz (Hz)."}, {"id": "q2", "question": "¿Qué es una banda ISM?", "options": ["Frecuencias de uso industrial, científico y médico", "Solo bandas militares", "Cualquier frecuencia > 1 GHz"], "correct_index": 0, "explanation": "ISM = Industrial, Scientific and Medical."}, {"id": "q3", "question": "¿Para qué sirve observar el espectro en educación?", "options": ["Identificar fuentes legítimas de señal", "Interferir transmisiones ajenas", "Jamming controlado"], "correct_index": 0, "explanation": "El análisis es pasivo y educativo."}],
                ),
                "order_index": 1,
                "duration_minutes": 15,
            },
            {
                "slug": "modulacion-am-fm",
                "title": "Modulación AM y FM",
                "content": (
                    "## Modulación\n\nLa modulación codifica información sobre una portadora.\n\n- **AM**: varía la amplitud de la señal\n- **FM**: varía la frecuencia instantánea\n\nEn investigación, reconocer el tipo de modulación permite clasificar emisoras y comprender protocolos de comunicación."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {"carrier_hz": 1000000, "modulation": "fm", "modulation_index": 0.5},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué parámetro varía en FM?", "options": ["La frecuencia instantánea", "La amplitud únicamente", "La polarización"], "correct_index": 0, "explanation": "FM modula la frecuencia de la portadora."}, {"id": "q2", "question": "¿Qué varía AM?", "options": ["La amplitud de la portadora", "Solo la polarización", "La longitud del cable"], "correct_index": 0, "explanation": "AM modula la amplitud."}, {"id": "q3", "question": "¿Para qué sirve reconocer la modulación?", "options": ["Clasificar emisoras y protocolos", "Aumentar potencia ilegalmente", "Bloquear canales vecinos"], "correct_index": 0, "explanation": "Ayuda a clasificar sin interferir."}],
                ),
                "order_index": 2,
                "duration_minutes": 20,
            },
            {
                "slug": "unidades-potencia",
                "title": "dBm, dBW y potencia",
                "content": (
                    "## Unidades logarítmicas\n\nEn RF se usa la escala decibel para comparar potencias:\n\n- **dBm**: potencia referida a 1 mW\n- **dBW**: potencia referida a 1 W\n- **dBi**: ganancia de antena respecto a isótropa\n\nComprender estas unidades es fundamental para uso responsable y seguro."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {"title": "Escala de potencia", "items": [{"label": "0 dBm", "value": "1 mW"}, {"label": "10 dBm", "value": "10 mW"}, {"label": "20 dBm", "value": "100 mW"}, {"label": "30 dBm", "value": "1 W"}]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿A qué equivale 0 dBm?", "options": ["1 mW", "1 W", "1 µW"], "correct_index": 0, "explanation": "0 dBm es la referencia de 1 milivatios."}, {"id": "q2", "question": "¿Qué es dBW?", "options": ["Potencia referida a 1 W", "Potencia referida a 1 mW", "Ganancia de antena"], "correct_index": 0, "explanation": "dBW usa 1 W como referencia."}, {"id": "q3", "question": "¿Qué representa dBi?", "options": ["Ganancia respecto a antena isótropa", "Potencia absoluta en vatios", "Frecuencia en GHz"], "correct_index": 0, "explanation": "dBi mide ganancia de antena."}],
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
            "Introducción a Software Defined Radio: arquitectura, muestreo digital y flujo de señal desde la antena hasta el software."
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
                    "## Software Defined Radio\n\nUn SDR digitaliza señales RF lo antes posible y procesa el espectro con software en lugar de circuitos analógicos fijos.\n\n### Componentes típicos\n1. Antena y front-end RF\n2. Conversor ADC (muestreo)\n3. FPGA o DSP para filtrado\n4. Software (GNU Radio, SDR#, etc.)\n\nVentaja educativa: puedes experimentar con filtros y demoduladores sin cambiar hardware."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {"title": "Flujo SDR", "items": [{"label": "Antena", "value": "Captura RF"}, {"label": "LNA/ADC", "value": "Digitaliza"}, {"label": "Software", "value": "Procesa"}]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué hace el ADC en un SDR?", "options": ["Convierte señal analógica a digital", "Amplifica la antena", "Transmite en FM"], "correct_index": 0, "explanation": "El ADC muestrea la señal para procesarla en software."}, {"id": "q2", "question": "¿Cuál es una ventaja educativa del SDR?", "options": ["Experimentar filtros sin cambiar hardware", "Transmitir sin restricciones", "Evitar normativa"], "correct_index": 0, "explanation": "El procesamiento flexible es ideal para aprender."}, {"id": "q3", "question": "¿Qué rol tiene el software en un SDR?", "options": ["Procesar y demodular la señal digitalizada", "Reemplazar la antena", "Generar interferencia"], "correct_index": 0, "explanation": "La demodulación y filtrado ocurren en software."}],
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "muestreo-nyquist",
                "title": "Muestreo y teorema de Nyquist",
                "content": (
                    "## Muestreo digital\n\nPara reconstruir una señal, el ADC debe muestrear al menos al doble de la frecuencia máxima (teorema de Nyquist).\n\n### Ejemplo\nSeñal de 1 MHz → mínimo 2 MSPS (mega-muestras por segundo).\n\nEn la práctica se usa sobremuestreo y filtros anti-aliasing."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {"carrier_hz": 500000, "modulation": "am", "modulation_index": 0.8},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Cuál es la tasa mínima según Nyquist?", "options": ["El doble de la frecuencia máxima", "La mitad de la frecuencia máxima", "Igual a la frecuencia portadora"], "correct_index": 0, "explanation": "Nyquist exige fs ≥ 2 × fmax."}, {"id": "q2", "question": "Si fmax = 1 MHz, ¿qué tasa mínima sugiere Nyquist?", "options": ["2 MSPS", "0.5 MSPS", "1 kSPS"], "correct_index": 0, "explanation": "fs ≥ 2 × fmax ⇒ 2 MSPS."}, {"id": "q3", "question": "¿Para qué sirve el filtro anti-aliasing?", "options": ["Evitar solapamiento espectral al muestrear", "Amplificar TX", "Hacer jamming"], "correct_index": 0, "explanation": "Reduce componentes fuera de banda antes del ADC."}],
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
            "Guía ética y legal para usar HackRF One en educación e investigación, con énfasis en recepción pasiva y límites de transmisión."
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
                    "## Uso responsable\n\nAntes de operar cualquier SDR transmisor:\n\n1. Consulta la normativa de tu país (FCC, CEPT, etc.)\n2. Obtén licencias si transmites\n3. Nunca interrumpas servicios críticos\n4. Prioriza recepción pasiva para aprendizaje\n\n**Prohibido en esta academia:** interferencia, jamming, escucha ilegal."
                ),
                "visual_type": "none",
                "visual_data": None,
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué actividad está prohibida en RF Sentinel?", "options": ["Interferencia y jamming", "Recepción pasiva educativa", "Análisis de espectro en laboratorio"], "correct_index": 0, "explanation": "La interferencia es ilegal y contraria a nuestra misión."}, {"id": "q2", "question": "¿Qué debes hacer antes de transmitir?", "options": ["Verificar normativa y licencias", "Aumentar potencia al máximo", "Transmitir en cualquier frecuencia"], "correct_index": 0, "explanation": "La legalidad depende de tu jurisdicción."}, {"id": "q3", "question": "¿Cuál es el enfoque preferido para aprender con SDR?", "options": ["Recepción pasiva", "Transmisión a máxima potencia", "Interferir señales desconocidas"], "correct_index": 0, "explanation": "La recepción pasiva es segura y educativa."}],
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "setup-hackrf",
                "title": "Configuración básica (solo recepción)",
                "content": (
                    "## Setup educativo HackRF\n\nPara aprendizaje seguro, configura solo recepción:\n\n```bash\nhackrf_info\nhackrf_transfer -r captura.raw -f 100000000 -s 2000000\n```\n\nParámetros clave:\n- `-f`: frecuencia central en Hz\n- `-s`: tasa de muestreo\n- `-r`: grabar a archivo (sin transmitir)\n\nAnaliza capturas offline con herramientas como inspectrum."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {"frequencies_mhz": [98, 100, 102, 104, 106], "amplitudes": [0.2, 0.95, 0.3, 0.7, 0.25], "labels": ["FM", "FM", "FM", "FM", "FM"]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué flag usa hackrf_transfer para grabar?", "options": ["-r", "-t", "-x"], "correct_index": 0, "explanation": "-r graba (receive) sin transmitir."}, {"id": "q2", "question": "¿Qué hace el parámetro -f?", "options": ["Frecuencia central en Hz", "Forzar transmisión", "Filtro FIR"], "correct_index": 0, "explanation": "-f fija la frecuencia central."}, {"id": "q3", "question": "¿Qué tipo de análisis es recomendado tras capturar?", "options": ["Offline con herramientas educativas", "Jamming en vivo", "TX sin licencia"], "correct_index": 0, "explanation": "Analizar capturas offline es seguro."}],
                ),
                "order_index": 2,
                "duration_minutes": 30,
            },
            {
                "slug": "limites-tx",
                "title": "Límites de transmisión",
                "content": (
                    "## Cuándo NO transmitir\n\nEvita transmitir si:\n- No tienes licencia amateur o autorización\n- La frecuencia está reservada (aviación, emergencias)\n- No conoces la potencia máxima permitida\n\nEn investigación universitaria, usa cámaras blindadas (Faraday) para pruebas de TX controladas."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {"title": "Zonas de riesgo", "items": [{"label": "Aviación", "value": "Prohibido sin licencia"}, {"label": "Emergencias", "value": "Nunca transmitir"}, {"label": "ISM 433 MHz", "value": "Verificar límites locales"}]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Dónde es seguro probar TX en laboratorio?", "options": ["Cámara Faraday con autorización", "En la calle sin licencia", "Cerca de un aeropuerto"], "correct_index": 0, "explanation": "Las cámaras blindadas contienen la señal."}, {"id": "q2", "question": "¿Qué bandas deben evitarse siempre?", "options": ["Aviación y emergencias sin autorización", "Solo Wi-Fi doméstico", "Ninguna banda"], "correct_index": 0, "explanation": "Servicios críticos están protegidos."}, {"id": "q3", "question": "Sin licencia, ¿qué debes priorizar?", "options": ["No transmitir / solo RX", "Transmitir a baja potencia en cualquier frecuencia", "Usar la máxima ganancia TX"], "correct_index": 0, "explanation": "Sin autorización no se transmite."}],
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
            "FFT, espectrogramas y técnicas para identificar modulaciones con datos simulados y capturas educativas."
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
                    "## FFT en SDR\n\nLa FFT descompone una señal temporal en componentes de frecuencia.\n\nEn un waterfall (espectrograma):\n- Eje X: tiempo\n- Eje Y: frecuencia\n- Color: intensidad\n\nÚtil para detectar patrones, saltos de frecuencia (FHSS) y portadoras."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {"frequencies_mhz": [2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409], "amplitudes": [0.1, 0.3, 0.9, 0.5, 0.2, 0.8, 0.4, 0.6, 0.3, 0.1], "labels": ["Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi", "Wi-Fi"]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué muestra un espectrograma en el eje Y?", "options": ["Frecuencia", "Tiempo", "Fase"], "correct_index": 0, "explanation": "El eje Y representa frecuencia en un waterfall."}, {"id": "q2", "question": "¿Qué representa el color en un waterfall típico?", "options": ["Intensidad de la señal", "Fase de la portadora", "Índice de licencia"], "correct_index": 0, "explanation": "El color suele mapear potencia/intensidad."}, {"id": "q3", "question": "¿Qué eje suele representar el tiempo en un espectrograma?", "options": ["Eje X", "Eje Y", "Ninguno"], "correct_index": 0, "explanation": "Comúnmente X=tiempo, Y=frecuencia."}],
                ),
                "order_index": 1,
                "duration_minutes": 25,
            },
            {
                "slug": "identificar-modulacion",
                "title": "Identificar modulaciones",
                "content": (
                    "## Patrones visuales\n\n| Modulación | Patrón en espectro |\n|------------|-------------------|\n| AM | Portadora central + bandas laterales |\n| FM | Banda ancha uniforme |\n| FSK | Picos discretos |\n| PSK | Constelación en I/Q |\n\nPractica con capturas de referencia antes de analizar señales reales."
                ),
                "visual_type": "waveform",
                "visual_data": _visual(
                    "waveform",
                    {"carrier_hz": 2000000, "modulation": "fm", "modulation_index": 1.2},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué modulación muestra picos discretos?", "options": ["FSK", "AM", "CW"], "correct_index": 0, "explanation": "FSK salta entre frecuencias discretas."}, {"id": "q2", "question": "¿Qué patrón se asocia a AM?", "options": ["Portadora central + bandas laterales", "Solo un tono único sin portadora", "Constelación QPSK"], "correct_index": 0, "explanation": "AM muestra portadora y bandas laterales."}, {"id": "q3", "question": "Antes de analizar señales reales, ¿qué recomienda el curso?", "options": ["Practicar con capturas de referencia", "Transmitir en aviación", "Aplicar jamming de prueba"], "correct_index": 0, "explanation": "Primero práctica con datos de referencia."}],
                ),
                "order_index": 2,
                "duration_minutes": 30,
            },
            {
                "slug": "iq-datos",
                "title": "Datos I/Q y constelaciones",
                "content": (
                    "## Representación I/Q\n\nLas señales complejas se representan como I (in-phase) + jQ (quadrature).\n\nLa constelación I/Q visualiza modulaciones digitales (QPSK, QAM).\n\nEn esta plataforma usamos **datos simulados** para practicar sin hardware."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {"title": "Constelación QPSK (simulada)", "items": [{"label": "00", "value": "Cuadrante I+, Q+"}, {"label": "01", "value": "Cuadrante I-, Q+"}, {"label": "10", "value": "Cuadrante I+, Q-"}, {"label": "11", "value": "Cuadrante I-, Q-"}]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué representan I y Q?", "options": ["Componentes en fase y cuadratura", "Intensidad y calidad", "Entrada y salida"], "correct_index": 0, "explanation": "I/Q es la representación compleja de la señal."}, {"id": "q2", "question": "¿Qué visualiza una constelación I/Q?", "options": ["Modulaciones digitales como QPSK/QAM", "Solo potencia en dBm", "La longitud de onda física"], "correct_index": 0, "explanation": "I/Q representa símbolos digitales."}, {"id": "q3", "question": "¿Qué tipo de datos usa esta plataforma para practicar?", "options": ["Datos simulados educativos", "Capturas de jamming", "TX ilícito"], "correct_index": 0, "explanation": "Se usan datos simulados sin hardware obligatorio."}],
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
            "Comparativa RTL-SDR vs HackRF, conexiones, calibración y buenas prácticas de laboratorio."
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
                    "## Comparativa educativa\n\n| Característica | RTL-SDR | HackRF One |\n|----------------|---------|------------|\n| Rango | ~24 MHz - 1.7 GHz | 1 MHz - 6 GHz |\n| TX | No | Sí (con precaución) |\n| Precio | Bajo | Medio |\n| Uso ideal | Recepción, aprendizaje | Investigación full-duplex |\n\nPara principiantes: empieza con RTL-SDR en recepción."
                ),
                "visual_type": "diagram",
                "visual_data": _visual(
                    "diagram",
                    {"title": "Rangos de frecuencia", "items": [{"label": "RTL-SDR", "value": "24 MHz – 1.7 GHz (RX)"}, {"label": "HackRF", "value": "1 MHz – 6 GHz (RX/TX)"}]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Qué dispositivo es solo recepción?", "options": ["RTL-SDR", "HackRF One", "Ambos transmiten"], "correct_index": 0, "explanation": "RTL-SDR típicamente no transmite."}, {"id": "q2", "question": "¿Qué dispositivo suele abarcar hasta ~6 GHz?", "options": ["HackRF One", "Solo RTL-SDR", "Ninguno"], "correct_index": 0, "explanation": "HackRF cubre aproximadamente 1 MHz–6 GHz."}, {"id": "q3", "question": "¿Por qué empezar con RTL-SDR?", "options": ["Es económico y solo recepción (más seguro)", "Permite TX ilegal fácil", "No requiere antena"], "correct_index": 0, "explanation": "Ideal para aprender con RX."}],
                ),
                "order_index": 1,
                "duration_minutes": 20,
            },
            {
                "slug": "conexiones-calibracion",
                "title": "Conexiones y calibración",
                "content": (
                    "## Buenas prácticas de laboratorio\n\n1. Usa cables y conectores de calidad (SMA)\n2. Evita sobrecargar entradas RF\n3. Calibra offset de frecuencia con referencia conocida\n4. Mantén antenas lejos de fuentes de interferencia artificial\n\nRegistra siempre offset y ganancia en tus notas de investigación."
                ),
                "visual_type": "spectrum",
                "visual_data": _visual(
                    "spectrum",
                    {"frequencies_mhz": [999, 1000, 1001], "amplitudes": [0.2, 1.0, 0.2], "labels": ["Ref", "1 GHz Ref", "Ref"]},
                ),
                "quiz": _quiz(
                    [{"id": "q1", "question": "¿Por qué calibrar el offset?", "options": ["El oscilador local puede desviarse", "Para aumentar la potencia TX", "No es necesario en SDR"], "correct_index": 0, "explanation": "Los TCXO/osciladores tienen error de frecuencia."}, {"id": "q2", "question": "¿Qué conector es habitual en SDR de laboratorio?", "options": ["SMA", "RJ45 como RF", "HDMI"], "correct_index": 0, "explanation": "SMA es común en RF de laboratorio."}, {"id": "q3", "question": "¿Qué debe registrarse en notas de investigación?", "options": ["Offset y ganancia", "Claves de cifrado ajenas", "Códigos de jamming"], "correct_index": 0, "explanation": "La trazabilidad incluye offset y ganancia."}],
                ),
                "order_index": 2,
                "duration_minutes": 25,
            },
        ],
    },
]
