# This program simply loads all images/sound as pygame objects and returns them as a dictionary for use in the program.


import os, pygame

PATH_TO_RESOURCES = "assets"

# normally assets are loaded directly into the resources dictionary
# each exception is a directory
# each file in the directory are instead loaded into their own lists in the resources dictionary
# the key is the directory path and the value is the name of the list that will hold the directory's assets
exceptions = {
  "assets/images/golem/Idle": "golem_idle",
  "assets/images/golem/Hurt": "golem_hurt",
  "assets/images/golem/Walking": "golem_walk",
  "assets/images/golem/Dying": "golem_death",
  "assets/images/golem/Attacking": "golem_attack",
  "assets/images/woodcutter/Idle": "woodcutter_idle",
  "assets/images/woodcutter/Run": "woodcutter_run",
  "assets/images/woodcutter/Attack": "woodcutter_attack",
  "assets/images/woodcutter/Hurt": "woodcutter_hurt",
  "assets/images/woodcutter/Death": "woodcutter_death",
  "assets/images/woodcutter/Jump": "woodcutter_jump",
  "assets/images/woodcutter/Fall": "woodcutter_fall"
}

# normalize all paths for cross-compatibility
# different OS have different path conventions (e.g., using / or \ for path delimiters)
new_exceptions = {}
for key in exceptions.keys():
  new_exceptions[os.path.normpath(key)] = exceptions[key]
exceptions = new_exceptions


# loads resources and returns resources dictionary
def load_resources():
  resources = {}

  path_len = len(PATH_TO_RESOURCES) + 1
  # use os.walk to search through all directories in assets/ directory
  for root, dirs, files in os.walk(PATH_TO_RESOURCES):
    # split path into parts
    bits = root.split(os.sep)
    # if the directory is images, then load the images
    if "images" in bits:
      # account for exceptions
      if root in exceptions.keys():
        sprite_list = []
        sprite_list_reverse = [] # horizontally flipped version of sprites
        for file in files:
          image = pygame.image.load(os.path.join(root, file))
          image_reverse = pygame.transform.flip(image, True, False)
          sprite_list.append(image)
          sprite_list_reverse.append(image_reverse)
        resources[exceptions[root]] = sprite_list
        resources[exceptions[root]+"_reverse"] = sprite_list_reverse
      # if not exception, load directly into dict
      else:
        for file in files:
          image = pygame.image.load(os.path.join(root, file))
          resources[file] = image
    # same as images, except for sounds
    if "sounds" in bits:
      for file in files:
        sound = pygame.mixer.Sound(os.path.join(root, file))
        resources[file] = sound
    # same as images, except for music
    if "music" in bits:
      for file in files:
        pygame.mixer.music.load(os.path.join(root, file))
    

  return resources
