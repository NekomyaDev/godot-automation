# Godot Automation

## Overview

Godot Automation is an innovative project that leverages AI to automate game creation on the Godot engine. Imagine telling an AI, "Open Godot and create an action game," and watching as it not only launches Godot but also generates a complete game scene for you—all through natural language commands. This project harnesses advanced AI models (via Ollama) and combines them with automation techniques to streamline game development.

## Current State

The project currently includes:
- **AI Integration:**  
  Utilizes Ollama's interactive mode to process natural language commands using models like `llama2:latest`. The system receives commands and normalizes them (e.g., "open godot" or "create game").

- **Automation:**  
  Depending on the AI response, the system either:
  - Launches Godot (and even attempts automatic installation if Godot isn’t detected on the system), or
  - Generates a Godot GDScript that creates a game scene. This script instantiates Sprite nodes based on images found in the project’s assets folder.

- **Interactive Loop:**  
  The system runs in a continuous loop, allowing users to enter commands in real time without restarting the program.

## Future Goals

Our vision is to evolve Godot Automation into a comprehensive, AI-driven game creation platform. The ultimate goal is to develop a system where you simply describe your game idea in plain English, and the AI takes care of the rest—from launching the engine and generating game assets to creating complete levels and gameplay mechanics.

## Join the Development Team

We are actively seeking passionate developers and AI enthusiasts to join our team. If you’re excited about AI, game development, and automation, we’d love for you to contribute! This project is proudly powered by the NekoAI Assistant, and together, we’re pushing the boundaries of what’s possible in automated game creation.

## Getting Started

1. **Clone the Repository:**
   git clone https://github.com/NekomyaDev/godot-automation.git
   cd godot-automation
   python3 -m venv godot-automation
   source godot-automation-env/bin/activate
   read requirements.txt

Ensure Prerequisites:

Make sure that Ollama is installed and configured on your system.
Godot should be installed OR The system will attempt automatic installation if it’s not found (Ubuntu/Pop OS).

Run the Project:

python3 src/full_automation.py

Contact
For questions, suggestions, or further information, please reach out to
[dev.nekomya@gmail.com].


---

This README outlines the project's current capabilities, future vision, and invites collaboration, while clearly stating that NekoAI Assistant is an integral part of the project. Feel free to modify any section as needed before adding it to your repository.
