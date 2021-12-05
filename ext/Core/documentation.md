# operations.py:

**_render_text_**: function(text, pos, color, size) => None

**_render_image_**: function(image_name: str, pos: tuple, size: tuple) => None

**_render_rectangle_**: function(color: tuple, size: tuple, pos: tuple) => None

**_render_circle_**: function(color: tuple,radius: int,pos: tuple) => None

**_check_interaction_**: function(clickpos: tuple, wanted_area: tuple, wanted_pages: list, page: str) => Booléen

**_render_time_**: function() => None

# variables.py:

  **_BASE_COLOR_**: tuple(3);
    Couleur de base du theme en rvb

  **_BLACK_**: tuple(3);
    Couleur en rvb
    
  **_GREY_**: tuple(3);
    Couleur en rvb

  **_BLUE_GREY_**: tuple(3);
    Couleur en rvb

  **_WHITE_**: tuple(3);
    Couleur en rvb

  **_GREEN_**: tuple(3);
    Couleur en rvb

  **_BLUE_**: tuple(3);
    Couleur en rvb

  **_LIGHT_BLUE_**: tuple(3);
    Couleur en rvb

  **_RED_**: tuple(3);
    Couleur en rvb

  **_YELLOW_**: tuple(3);
    Couleur en rvb

  **_resolution_**: tuple(2);
    Résolution de l'ecran pygame

  **_mid_screen_**: tuple(2);
    Coordonées du milieu de l'écran

  **_Login_Background_**: str;

  **_RUN_plat_**: bool;
    Booléen qui permet de savoir si le platformer marche ou pas

  **_unlocked_**: list(∞);
    Liste de tous les éléments qui ont été découverts/ouverts par le joueur

  **_recovered_drive_**: dict(dict-list);

  **_messages_**: dict(list);

  **_unlockable_messages_**: dict(list);

  **_sound_**: str;