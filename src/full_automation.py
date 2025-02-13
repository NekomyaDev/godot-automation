import os
import time
import random
import subprocess
import shutil
from ollama_integration import process_command_with_ollama

# ----------------- AI Yanıtlarını Özelleştirme -----------------
def extract_command_from_response(response: str) -> str:
    """
    AI modelinden gelen ham yanıtı, normalize edilmiş komuta dönüştürür.
    Örnek: Yanıt içinde "open godot" veya "godot'u aç" varsa "open_godot",
    "create game" veya "oyun yarat" varsa "create_game" döndürür.
    """
    lower_resp = response.lower()
    if "open godot" in lower_resp or "godot'u aç" in lower_resp:
        return "open_godot"
    elif "create game" in lower_resp or "oyun yarat" in lower_resp:
        return "create_game"
    else:
        return "unknown"

# ----------------- Otomatik Kurulum Fonksiyonu -----------------
def install_godot(preferred_command="godot") -> bool:
    """
    Eğer belirtilen 'godot' komutu sistemde bulunamazsa, otomatik olarak
    'sudo apt install -y godot3' komutunu çalıştırır.
    Kurulum sonrası önce "godot" komutunu, eğer bulunamazsa "godot3" komutunu kontrol eder.
    Eğer uygun komut tespit edilirse True, aksi halde False döndürür.
    """
    if shutil.which(preferred_command) is None:
        print(f"Hata: '{preferred_command}' komutu bulunamadı. Otomatik kurulum deneniyor...")
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "godot3"], check=True)
        except Exception as e:
            print("Otomatik kurulum başarısız oldu:", e)
            return False
        # Kurulum sonrası kontrol: önce "godot", sonra "godot3"
        if shutil.which("godot") is not None:
            print("'godot' komutu tespit edildi.")
            return True
        elif shutil.which("godot3") is not None:
            print("'godot3' komutu tespit edildi.")
            return True
        else:
            print("Otomatik kurulum sonrası da Godot bulunamadı. Lütfen manuel kurulum yapın.")
            return False
    return True

# ----------------- Otomasyon Fonksiyonları -----------------
def perform_action_open_godot():
    """
    Godot'u açar; eğer bulunamazsa otomatik kurulum denemesi yapar.
    """
    godot_command = "godot"  # Tercih edilen komut
    if not install_godot(godot_command):
        return
    # Eğer "godot" hala bulunamıyorsa, "godot3" kontrol edelim.
    if shutil.which(godot_command) is None:
        if shutil.which("godot3") is not None:
            godot_command = "godot3"
        else:
            print("Godot komutu bulunamadı.")
            return
    try:
        subprocess.Popen([godot_command])
        print("Godot açıldı.")
    except Exception as e:
        print("Godot açılamadı, hata:", e)

def search_images(keyword, folder="images"):
    """
    Belirtilen klasörde, anahtar kelimeyi içeren resim dosyalarını arar.
    Desteklenen uzantılar: .png, .jpg, .jpeg
    """
    matching_files = []
    if not os.path.exists(folder):
        print(f"Klasör '{folder}' bulunamadı!")
        return matching_files
    for filename in os.listdir(folder):
        if keyword.lower() in filename.lower() and filename.lower().endswith((".png", ".jpg", ".jpeg")):
            matching_files.append(os.path.join(folder, filename))
    return matching_files

def generate_game_code(command_text, images):
    """
    Komut metni ve bulunan resimler temelinde, Godot için tam işlevsel bir GDScript (Node2D tabanlı) üretir.
    Her resim için sahneye Sprite eklenir.
    """
    code = "# Otomatik Üretilmiş Godot Scripti\n"
    code += "extends Node2D\n\n"
    code += "func _ready():\n"
    code += "\tprint('Otomatik oluşturulmuş oyun sahnesi oluşturuldu.')\n"
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
        code += "\tprint('Resim bulunamadı, lütfen images klasörünü kontrol edin.')\n"
    return code

def save_code_to_file(code, filename="generated_game.gd"):
    """Oluşturulan GDScript kodunu belirtilen dosyaya kaydeder."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Oyun kodu '{filename}' dosyasına kaydedildi.")

def perform_action_create_game(command_text):
    """
    "Oyun yarat" komutu için:
      - Komut metninden anahtar kelime çıkarılır.
      - Belirtilen klasörden resimler aranır.
      - Resimler ve komut metni temelinde otomatik Godot scripti üretilir ve kaydedilir.
      - (İsteğe bağlı) Godot, projenin mevcut diziniyle açılır.
    """
    keywords = ["action", "platform", "rpg", "puzzle", "adventure", "aksiyon", "platform", "rpg", "puzzle", "macera"]
    found_keyword = None
    for word in keywords:
        if word.lower() in command_text.lower():
            found_keyword = word
            break
    if not found_keyword:
        found_keyword = "default"
    print("Kullanılacak anahtar kelime:", found_keyword)

    images = search_images(found_keyword)
    print("Bulunan resimler:", images)

    code = generate_game_code(command_text, images)
    save_code_to_file(code)

    try:
        subprocess.Popen(["godot", "--path", os.getcwd()])
        print("Godot açıldı, lütfen sahneyi kontrol edin.")
    except Exception as e:
        print("Godot açılırken hata oluştu:", e)

def self_improve_system():
    """
    (Placeholder) – Sistem, loglama veya geribildirimlere dayalı olarak kendini geliştirebilir.
    İlerleyen aşamalarda bu fonksiyon, AI modelinden geri bildirim alarak dinamik düzenlemeler yapacak şekilde genişletilebilir.
    """
    print("Kendini geliştirme rutini çalıştırılıyor...")
    # Gelecekte AI yanıtlarına göre sistemin kendini iyileştirme kodları eklenebilir.

def main():
    print("Sistem başlatıldı. Çıkmak için 'çık' veya 'exit' yazabilirsiniz.")
    while True:
        print("\nKomut bekleniyor. Örnek: \"Godot'u aç ve bana aksiyon oyunu yarat.\"")
        command_text = input("Komut girin: ").strip()
        if command_text.lower() in ["çık", "exit"]:
            print("Sistem kapatılıyor...")
            break
        if not command_text:
            print("Komut boş bırakıldı. Lütfen geçerli bir komut girin.")
            continue

        # Ollama üzerinden modelden yanıt alıyoruz.
        ai_response = process_command_with_ollama(command_text)
        print("AI model çıktısı:", ai_response)

        normalized_command = extract_command_from_response(ai_response)
        if normalized_command == "open_godot":
            perform_action_open_godot()
        elif normalized_command == "create_game":
            perform_action_create_game(command_text)
        else:
            print("Bilinmeyen komut. Lütfen komutu gözden geçirin.")

        self_improve_system()

if __name__ == "__main__":
    main()
