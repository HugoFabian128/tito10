import csv
import os
import re
import unicodedata
import speech_recognition as sr

PRUEBAS_CORPUS = [
    ("voz_01_beca.wav", "quiero informacion sobre becas", "becas"),
    ("voz_02_biblioteca.wav", "a que hora abre la biblioteca", "biblioteca"),
    (
        "voz_03_inscripciones.wav",
        "cuando empiezan las inscripciones",
        "inscripciones",
    ),
    ("voz_04_horarios.wav", "donde puedo consultar mis horarios", "horarios"),
    ("voz_05_kardex.wav", "necesito tramitar mi kardex oficial", "tramites"),
    (
        "voz_06_servicio_social.wav",
        "requisitos para liberar el servicio social",
        "servicio_social",
    ),
]

PRUEBAS_CONDICIONES = [
    ("Silencio", "cond_01_silencio.wav", "como solicito una beca"),
    ("Ruido moderado", "cond_02_ruido.wav", "como solicito una beca"),
    ("Mayor distancia", "cond_03_distancia.wav", "como solicito una beca"),
]


def normalizar_texto(texto):
  texto = texto.lower().strip()
  texto = "".join(
      c
      for c in unicodedata.normalize("NFD", texto)
      if unicodedata.category(c) != "Mn"
  )
  texto = re.sub(r"[^\w\s]", "", texto)
  return texto


def clasificar_intencion_tito(texto_limpio):
  if any(p in texto_limpio for p in ["beca", "becas", "apoyo"]):
    return "becas"
  elif any(p in texto_limpio for p in ["biblioteca", "libro", "abre"]):
    return "biblioteca"
  elif any(p in texto_limpio for p in ["inscripcion", "inscripciones"]):
    return "inscripciones"
  elif any(p in texto_limpio for p in ["horario", "horarios", "clase"]):
    return "horarios"
  elif any(p in texto_limpio for p in ["kardex", "constancia", "tramitar"]):
    return "tramites"
  elif any(p in texto_limpio for p in ["servicio", "social", "liberar"]):
    return "servicio_social"
  return "desconocida"


def reconocer_audio(ruta_completa):
  r = sr.Recognizer()
  if not os.path.exists(ruta_completa):
    return "[ARCHIVO_NO_ENCONTRADO]"

  try:
    with sr.AudioFile(ruta_completa) as source:
      audio = r.record(source)
    return r.recognize_google(audio, language="es-MX")
  except sr.UnknownValueError:
    return "[NO_ENTENDIDO]"
  except sr.RequestError:
    return "[ERROR_CONEXION]"
  except Exception as e:
    return f"[ERROR: {e}]"


def ejecutar_practica():
  os.makedirs("resultados", exist_ok=True)

  ruta_csv_principal = "resultados/registro_transcripciones.csv"
  with open(
      ruta_csv_principal, mode="w", newline="", encoding="utf-8"
  ) as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow([
        "archivo",
        "texto_esperado",
        "texto_reconocido",
        "texto_limpio_pln",
        "intencion_esperada",
        "intencion_detectada",
        "correcto",
    ])

    print("\n--- 1. EVALUANDO PIPELINE VOZ -> PLN ---")
    for archivo, esperado, intencion_esp in PRUEBAS_CORPUS:
      ruta = os.path.join("audios", archivo)
      reconocido_raw = reconocer_audio(ruta)

      if reconocido_raw.startswith("["):
        limpio = ""
        intencion_det = "error"
        es_correcto = "No"
      else:
        limpio = normalizar_texto(reconocido_raw)
        intencion_det = clasificar_intencion_tito(limpio)
        es_correcto = "Sí" if intencion_esp == intencion_det else "No"

      escritor.writerow([
          archivo,
          esperado,
          reconocido_raw,
          limpio,
          intencion_esp,
          intencion_det,
          es_correcto,
      ])
      print(
          f"{archivo} -> '{reconocido_raw}' | Intención: {intencion_det}"
          f" ({es_correcto})"
      )

  ruta_csv_condiciones = "resultados/comparacion_condiciones.csv"
  with open(
      ruta_csv_condiciones, mode="w", newline="", encoding="utf-8"
  ) as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(
        ["condicion", "archivo", "texto_esperado", "texto_reconocido", "observacion"]
    )

    print("\n--- 2. EVALUANDO CONDICIONES DE GRABACIÓN ---")
    for condicion, archivo, esperado in PRUEBAS_CONDICIONES:
      ruta = os.path.join("audios", archivo)
      reconocido_raw = reconocer_audio(ruta)

      if reconocido_raw.startswith("["):
        obs = "Fallo de reconocimiento por ruido/distancia"
      elif normalizar_texto(reconocido_raw) == esperado:
        obs = "Transcripción limpia"
      else:
        obs = "Degradación parcial por entorno"

      escritor.writerow([condicion, archivo, esperado, reconocido_raw, obs])
      print(f"[{condicion}] -> '{reconocido_raw}' ({obs})")

  print(
      "\n¡PROCESO TERMINADO! Revisa los CSV dentro de la carpeta 'resultados/'."
  )


if __name__ == "__main__":
  ejecutar_practica()