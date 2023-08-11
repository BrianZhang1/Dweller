# About
Dweller is a work-in-progress PyGame level-based rpg. This was made for a school project.  
Planned future features include:  
* Player Level-Up/Stat Point System
* Various Enemy Types/Bosses
* Auto-Generated Endless Mode
* Different Classes/Weapons
* Enemies Drop Items/Equipment upon Death

# How to play

1. Clone repository.
2. Install dependencies: `pip install -r requirements.txt` (create a venv if needed)
3. Run the dweller.py file: `python dweller.py`  

Enjoy!

# Project Structure
/resources: All resources (image files, audio files, etc.)  
/src: All source code.  

src/main.py: controls the entire program.  
src/states: contains a class for each state.  
src/components: contains the objects needed for the game.  
src/data_handler: loads all the data from data.json.  
src/resource_handler: loads all the resources.  