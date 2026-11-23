PRÁCTICA SEMANA 10 - PROCESAMIENTO DE LENGUAJE NATURAL (TITO)
Tema: Reconocimiento Automático del Habla (ASR)

1. INSTALACIÓN
   .venv\Scripts\python.exe -m pip install SpeechRecognition pyttsx3

2. ORDEN DE EJECUCIÓN
   Paso 1: .venv\Scripts\python.exe generar_audios.py
   Paso 2: .venv\Scripts\python.exe transcribir_archivo.py
   Paso 3: .venv\Scripts\python.exe pipeline_tito_voz.py

3. ESTRUCTURA
   - audios/                -> 9 archivos WAV de prueba.
   - resultados/            -> Tablas CSV y reporte final con diagrama.
   - transcribir_archivo.py -> Prueba individual (Clase 1).
   - pipeline_tito_voz.py   -> Integración Voz -> PLN (Clase 2).