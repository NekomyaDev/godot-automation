import os
import time
import random
import subprocess
import shutil
from ollama_integration import process_command_with_ollama

# ----------------- AI Response Normalization -----------------
def extract_command_from_response(response: str) -> str:
    """
    Converts the raw AI model response into a normalized command.
    For example, if the response contains "open godot" or "godot'u aç",
    it returns "open_godot". If it contains "create game" or "oyun yarat",
    it returns "create_game". Otherwise, it returns "unknown".
    """
    lower_resp = response.lower()
    if "open godot" in lower_resp or "godot'u aç" in lower_resp:
        return "open_godot"
    elif "create game" in lower_resp or "oyun yarat" in lower_resp:
        return "create_game"
    else:
        return "unknown"

# ----------------- Automatic Installation Function -----------------
def install_godot(preferred_command="godot") -> bool:
    """
    Checks if the specified 'godot' command exists on the system.
    If not, it attempts to automatically install it using:
      sudo apt install -y godot3
    After installation, it checks first for the "godot" command,
    then for "godot3". Returns True if a valid command is found,
    and False otherwise.
    """
    if shutil.which(preferred_command) is None:
        print(f"Error: '{preferred_command}' command not found. Attempting automatic installation...")
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "godot3"], check=True)
        except Exception as e:
            print("Automatic installation failed:", e)
            return False
        # Check after installation: first "godot", then "godot3"
        if shutil.which("godot") is not None:
            print("'godot' command detected.")
            return True
        elif shutil.which("godot3") is not None:
            print("'godot3' command detected.")
            return True
        else:
            print("Godot not found even after automatic installation. Please install it manually.")
            return False
    return True

# ----------------- Automation Functions -----------------
def perform_action_open_godot():
    """
    Launches Godot. If Godot is not found, it attempts an automatic installation.
    """
    godot_command = "godot"  # Preferred command
    if not install_godot(godot_command):
        return
    # If "godot" is still not found, check for "godot3"
    if shutil.which(godot_command) is None:
        if shutil.which("godot3") is not None:
            godot_command = "godot3"
        else:
            print("Godot command not found.")
            return
    try:
        subprocess.Popen([godot_command])
        print("Godot has been launched.")
    except Exception as e:
        print("Failed to launch Godot, error:", e)

def search_images(keyword, folder="images"):
    """
    Searches the specified folder for image files containing the keyword.
    Supported file extensions are: .png, .jpg, .jpeg.
    """
    matching_files = []
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found!")
        return matching_files
    for filename in os.listdir(folder):
        if keyword.lower() in filename.lower() and filename.lower().endswith((".png", ".jpg", ".jpeg")):
            matching_files.append(os.path.join(folder, filename))
    return matching_files

def generate_game_code(command_text, images):
    """
    Generates a fully functional Godot GDScript (based on Node2D) using the provided command text and found images.
    For each image, a Sprite is created and added to the scene.
    """
    code = "# Automatically Generated Godot Script\n"
    code += "extends Node2D\n\n"
    code += "func _ready():\n"
    code += "\tprint('Automatically generated game scene created.')\n"
    if images:
        for i, img in enumerate(images):
            godot_path = img.replace(os.sep, '/')
            pos_x = random.randint(50, 400)
            pos_y = random.randint(50, 300)
            code += f"\tvar sprite{i} = Sprite.new()\n"
            code += f"\tsprite{i}.texture = load('res://{godot_path}')\n"
            code += f"\tsprite{i}.position = Vector2({pos_x}, {pos_y})\n"
            code += f"\tadd_child(sprite{i})\n\n"
    else:
        code += "\tprint('No images found, please check the images folder.')\n"
    return code

def save_code_to_file(code, filename="generated_game.gd"):
    """
    Saves the generated GDScript code to the specified file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Game code saved to '{filename}'.")

def perform_action_create_game(command_text):
    """
    For the "create game" command:
      - Extracts a keyword from the command text.
      - Searches for images in the specified folder.
      - Generates and saves a Godot GDScript based on the command text and found images.
      - Optionally launches Godot with the current directory as the project path.
    """
    keywords = ["action", "platform", "rpg", "puzzle", "adventure", "aksiyon", "platform", "rpg", "puzzle", "macera"]
    found_keyword = None
    for word in keywords:
        if word.lower() in command_text.lower():
            found_keyword = word
            break
    if not found_keyword:
        found_keyword = "default"
    print("Keyword to be used:", found_keyword)

    images = search_images(found_keyword)
    print("Images found:", images)

    code = generate_game_code(command_text, images)
    save_code_to_file(code)

    try:
        subprocess.Popen(["godot", "--path", os.getcwd()])
        print("Godot has been launched. Please check the scene.")
    except Exception as e:
        print("Failed to launch Godot, error:", e)

def self_improve_system():
    """
    (Placeholder) – This function can be expanded in the future to allow the system to self-improve based on logging or feedback.
    """
    print("Running self-improvement routine...")
    # Future improvements based on AI responses can be added here.

def main():
    print("System started. Type 'çık' or 'exit' to quit.")
    while True:
        print("\nAwaiting command. Example: \"Godot'u aç ve bana aksiyon oyunu yarat.\"")
        command_text = input("Enter command: ").strip()
        if command_text.lower() in ["çık", "exit"]:
            print("Shutting down the system...")
            break
        if not command_text:
            print("Empty command. Please enter a valid command.")
            continue

        # Get the AI model response via Ollama.
        ai_response = process_command_with_ollama(command_text)
        print("AI model response:", ai_response)

        normalized_command = extract_command_from_response(ai_response)
        if normalized_command == "open_godot":
            perform_action_open_godot()
        elif normalized_command == "create_game":
            perform_action_create_game(command_text)
        else:
            print("Unknown command. Please review the command.")

        self_improve_system()

if __name__ == "__main__":
    main()
