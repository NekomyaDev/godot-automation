import subprocess

def process_command_with_ollama(prompt: str) -> str:
    """
    Ollama'yı interaktif modda çalıştırır ve STDIN üzerinden prompt'u gönderir.
    Komut satırında:
        ollama run llama2:latest
    açılır, ardından prompt STDIN üzerinden iletilir ve çıktı okunur.
    """
    if not prompt.strip():
        print("Boş prompt gönderildi!")
        return ""
    try:
        # Ollama'yı interaktif modda başlatıyoruz.
        proc = subprocess.Popen(
            ["ollama", "run", "llama2:latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # metin modunda çalıştırıyoruz
        )

        # Prompt'u gönderip çıktıyı alıyoruz.
        output, error = proc.communicate(prompt, timeout=30)

        if error:
            print("Ollama stderr:", error)
        return output.strip()
    except subprocess.TimeoutExpired as e:
        print("Ollama yanıt vermede zaman aşımına uğradı:", e)
        proc.kill()
        return "unknown"
    except Exception as e:
        print("Ollama çalıştırılırken hata oluştu:", e)
        return "unknown"

if __name__ == "__main__":
    test_prompt = "Godot'u aç ve bana aksiyon oyunu yarat."
    response = process_command_with_ollama(test_prompt)
    print("Ollama model çıktısı:", response)
