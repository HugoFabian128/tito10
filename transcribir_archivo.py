import os
import speech_recognition as sr


def transcribir_un_audio(ruta_audio):
  if not os.path.exists(ruta_audio):
    print(
        f"Error: No existe el archivo '{ruta_audio}'. Ejecuta primero"
        " generar_audios.py"
    )
    return

  r = sr.Recognizer()

  try:
    with sr.AudioFile(ruta_audio) as source:
      print(f"Procesando: {ruta_audio}...")
      audio = r.record(source)

    texto = r.recognize_google(audio, language="es-MX")
    print("Transcripción exitosa:", texto)
    return texto

  except sr.UnknownValueError:
    print("No se pudo entender el audio (demasiado ruido o volumen muy bajo).")
    return "[INAUDIBLE]"
  except sr.RequestError as error:
    print(f"Error de conexión con Google ASR: {error}")
    return "[ERROR_SERVICIO]"
  except Exception as e:
    print(f"Error inesperado al leer el archivo: {e}")
    return "[ERROR_ARCHIVO]"


if __name__ == "__main__":
  transcribir_un_audio("audios/voz_01_beca.wav")