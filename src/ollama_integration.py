import subprocess

def process_command_with_ollama(prompt: str) -> str:
    """
    Runs Ollama in interactive mode and sends the prompt via STDIN.

    The command line runs:
        ollama run llama2:latest
    which opens an interactive session. The provided prompt is then sent through STDIN,
    and the function waits to read and return the output.

    Parameters:
        prompt (str): The input command or prompt to be processed by the AI model.

    Returns:
        str: The stripped output from the AI model, or "unknown" if an error occurs.
    """
    if not prompt.strip():
        print("Empty prompt provided!")
        return ""
    try:
        # Start Ollama in interactive mode.
        proc = subprocess.Popen(
            ["ollama", "run", "llama2:latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Run in text mode.
        )

        # Send the prompt and read the output.
        output, error = proc.communicate(prompt, timeout=30)

        if error:
            print("Ollama stderr:", error)
        return output.strip()
    except subprocess.TimeoutExpired as e:
        print("Ollama timed out waiting for a response:", e)
        proc.kill()
        return "unknown"
    except Exception as e:
        print("An error occurred while running Ollama:", e)
        return "unknown"

if __name__ == "__main__":
    test_prompt = "Godot'u aç ve bana aksiyon oyunu yarat."
    response = process_command_with_ollama(test_prompt)
    print("Ollama model output:", response)
