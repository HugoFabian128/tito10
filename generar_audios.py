import io
import os
from gtts import gTTS
import numpy as np
import soundfile as sf

os.makedirs("audios", exist_ok=True)

AUDIOS_A_GENERAR = [
    # (nombre_archivo, frase, velocidad_lenta, factor_volumen, nivel_ruido)
    ("voz_01_beca.wav", "Quiero información sobre becas", False, 1.0, 0.0),
    ("voz_02_biblioteca.wav", "A qué hora abre la biblioteca", False, 1.0, 0.0),
    (
        "voz_03_inscripciones.wav",
        "Cuándo empiezan las inscripciones",
        False,
        1.0,
        0.0,
    ),
    (
        "voz_04_horarios.wav",
        "Dónde puedo consultar mis horarios",
        False,
        1.0,
        0.0,
    ),
    (
        "voz_05_kardex.wav",
        "Necesito tramitar mi kárdex oficial",
        False,
        0.2,
        0.01,
    ),  # Volumen bajo
    (
        "voz_06_servicio_social.wav",
        "Requisitos para liberar el servicio social",
        False,
        1.0,
        0.0,
    ),
    # 3 condiciones de prueba
    (
        "cond_01_silencio.wav",
        "Cómo solicito una beca",
        False,
        1.0,
        0.0,
    ),  # Silencio
    (
        "cond_02_ruido.wav",
        "Cómo solicito una beca",
        False,
        0.8,
        0.15,
    ),  # Ruido moderado real
    (
        "cond_03_distancia.wav",
        "Cómo solicito una beca",
        False,
        0.03,
        0.02,
    ),  # Mayor distancia (muy bajo)
]


def crear_audios():
  print("Generando archivos WAV PCM de 16 bits...")
  for nombre, texto, lento, volumen, ruido in AUDIOS_A_GENERAR:
    ruta_final = os.path.join("audios", nombre)

    # 1. Generar voz en memoria
    tts = gTTS(text=texto, lang="es", tld="com.mx", slow=lento)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # 2. Leer audio y aplicar condiciones (volumen y ruido real)
    datos, frecuencia = sf.read(mp3_fp)
    datos = datos * volumen

    if ruido > 0:
      estatica = np.random.normal(0, ruido, datos.shape)
      datos = datos + estatica

    # Recortar picos para evitar distorsión
    datos = np.clip(datos, -1.0, 1.0)

    # 3. Guardar garantizado como WAV PCM 16-bit
    sf.write(ruta_final, datos, frecuencia, subtype="PCM_16")
    print(f"OK -> {ruta_final}")

  print("\n¡Listo! Los 9 audios WAV se generaron sin errores.")


if __name__ == "__main__":
  crear_audios()