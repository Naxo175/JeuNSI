## 📒 Cahier des charges

L’objectif de ce projet est de créer un jeu en Python avec PyGame, une librairie conçue pour développer des jeux. Le thème du jeu que nous devons créer est “Nature”, alors nous avons imaginé un jeu qui correspond à ce thème. Pour cela, nous avons dû programmer plusieurs systèmes et fonctionnalités fondamentales.

On ne verra dans le cahier des charges que les programmes principaux.

**Le joueur**

Le code du joueur se trouve dans les scripts player.py, qui crée la classe Player, et main.py, qui gère ses mouvements. Pour créer le joueur, nous avons besoin de définir plusieurs paramètres dans sa classe :
- la position : où est-ce que le joueur se trouve actuellement ?
- la boîte de collision : sur quelle surface le joueur peut-il entrer en collision avec son environnement ?
- la direction : vers où est-ce que le joueur se déplace ?
- les sprites : un dictionnaire d’images du joueur en fonction de la direction dans laquelle il va
- l’inventaire : quels sont les objets que le joueur a récupérés durant son exploration ?

Avant de manipuler le joueur dans le script principal, on doit créer une instance. Cette instance représente le joueur existant dans le monde, qui possède tous les paramètres cités précédemment, et que l’on peut modifier. On met en paramètres la position X,Y initiale du joueur, définie par des valeurs constantes.

    START_X = 5 * TILE_SIZE # 5 cases vers la droite
    
    START_Y = 6 * TILE_SIZE # 6 cases vers le bas
    
    player = Player(START_X, START_Y)

Pour permettre au joueur de se déplacer, on récupère d’abord la liste des touches du clavier pressées par le joueur sur cette frame, puis on calcule la direction X,Y à lui appliquer en fonction des touches pressées (flèches gauche, droite, haut, bas).

    keys = pygame.key.get_pressed()
    
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

Puis, on appelle la fonction move() du joueur avec les paramètres dx et dy.

    player.move(dx, dy, walls)

**Le monde du jeu**

La carte (ou map) du jeu est composée de 12 scènes reliées entre elles ; ainsi le joueur peut se balader entre les différentes scènes en s’approchant d’un côté de la map.
Les maps font partie d’un dictionnaire MAPS_DATA, où les clés sont la position de la map sur une grille de 4x3, et les valeurs sont un Array des Tiles (ou images) présentes sur cette map.
Voici un exemple d’une map écrite dans le code du jeu :

    (0, 0) : [
    
    [["water"],["water"],["water"],["water"],["water"]], # Ligne 1
    
    [["water"],["grass"],["grass"],["grass"],["water"]], # Ligne 2
    
    ]

Maintenant, imaginons que nous avons besoin de placer un buisson sur l’herbe. On pourrait essayer de remplacer “grass” par “bush”, mais le buisson apparaîtrait seul, sans herbe en-dessous de lui. C’est pour cela que chaque case est elle-même représentée par un Array, où le premier élément est celui affiché dessous, et le dernier est affiché au-dessus.
Exemple :

    (0, 0) : [
    
    [["water"],["water"],["water"],["water"],["water"]], # Ligne 1
    
    [["w"],["grass"],["grass", “bush”],["grass"],["w"]], # Ligne 2
    
    ]

Enfin, certains éléments de décors ont besoin d’apparaître au-dessus du joueur. C’est pour cela que nous avons rajouté une règle d’affichage du jeu : les Tiles en dessous du joueur (couches 0 et 1) sont ajoutées à une liste tiles_below_player, et les autres Tiles (couches 2 à 10) sont ajoutées à la liste tiles_above_player. À l’affichage du jeu, on dessine d’abord les Tiles en dessous du joueur, puis le joueur lui-même, enfin les Tiles au-dessus.

    for img, pos in tiles_below_player: # Tiles en dessous
    
    screen.blit(img, pos)
    
    if(player): # Joueur
    
    player.draw(screen)
    
    for img, pos in tiles_above_player: # Tiles au-dessus
    
    screen.blit(img, pos)

Après avoir développé toutes ces fonctionnalités pour la map du jeu, nous nous sommes rendu compte de la complexité de devoir créer une map : il faudrait, à la main, écrire l’identifiant des Tiles dans des Arrays, pour les 336 cases de chaque map (car une map fait 14 cases de long et 24 de haut). Ce serait un travail trop fastidieux. C’est pour cela que nous avons développé une application Web permettant de placer des Tiles dans des cases, et avec la couche souhaitée.

**Les objets (interactables)**

Les interactables (comme appelés dans le code) sont des objets avec lesquels le joueur peut interagir. Ils sont, le plus souvent, utilisés comme animaux ou végétaux que le joueur peut ramasser afin de compléter sa collection. Ils ont leur propre classe dans le script interactable.py, et possèdent ces propriétés :

- l’image de l’objet
- l’identifiant (doit être unique)
- le nom
- la description (valable seulement pour les objets pouvant être récupérés)

Le joueur peut interagir avec eux en appuyant sur E : cela va appeler la fonction check_interaction() de la classe Player. Cette fonction a pour rôle de savoir quoi faire en fonction de l’objet avec lequel le joueur a interagi. Si c’est un objet à collecter, alors l’objet en question va être ajouté à l’inventaire du joueur :

    self.inventory.append(obj)

D’autres actions sont effectuées en fonction de l’objet.

Les Interactables à faire apparaître dans le jeu sont déterminés et configurés dans un dictionnaire INTERACTABLES_DATA, un peu semblable à celui des Maps. En effet, la clé est la position de la map sur une grille de 4x3, et la valeur est un Array des objets que l’on veut disposer sur cette map.

    INTERACTABLES_DATA = {
    
    # Format : (map_x, map_y): [(x, y, "id", "sprite.png", "name", "description")]
    
    (0, 0): [
    
    [500, 500, "ours_brun", "bear.png", "Bear", "It's a bear"],
    
    [500, 500, "mesange_nonnette", "bird1.png", "Bird1", "A bird"],
    
    ],
    
    (1, 0): [
    
    [500, 500, "mesange_charbonniere", "bird2.png", "Another bird"],
    
    [500, 500, "loup_gris", "wolf.png", "Wolf", "It's a wolf"],
    
    ]
    
    }

**🤖 Algorithmes**

Dans cette partie sur les algorithmes, nous allons observer et expliquer deux morceaux de programme de notre jeu. Le premier est la fonction load_map(), qui permet de charger la map (ses Tiles et Interactables) dans laquelle se trouve le joueur. Le système de transition dans la boucle “while” principale qui permet de transitionner entre deux maps.

*La fonction load_map()*

On commence par créer 3 listes vides : walls, tiles_below_player et tiles_above_player. Puis, on assigne à la variable data les données de la map actuelle : on cherche dans le dictionnaire MAPS_DATA, les données correspondantes aux coordonnées de la map dans laquelle le joueur se trouve (map_coords). Ensuite, on entre dans une première boucle for, qui parcourt la liste énumérée data. Ici, enumerate() permet d’obtenir un compteur à la liste et d’attribuer un index à chaque élément. Cela permet de savoir quelle ligne de la map le code est en train d’utiliser. Puis, on entre dans une autre boucle for, qui cette fois-ci parcourt la ligne actuelle. Grâce à ces deux boucles, on obtient les coordonnées X,Y, en pixels, de la case que le code est en train de traiter. On entre dans une dernière boucle for, qui parcourt toutes les Tiles placées sur cette case (car il peut y avoir autant de Tiles sur une case qu’il n’y a de couches). On attribue ensuite à tile_info, les informations de la Tile qu’on regarde dans la boucle for. Si la couche (obtenue à partir de l’index d’énumération) est inférieur à 2, on l’ajoute à tiles_below_player. Sinon, on l’ajoute à tiles_above_player. La dernière chose à faire pour nos Tiles est d’assigner la Tile la plus haute de la case à highest_tile_info. Enfin, si cette Tile possède de la collision, on l’ajoute à walls.

On passe maintenant au chargement des Interactables, qui lui est plus facile à comprendre. D’abord, on crée une liste interactables. On obtient tous les interactables de la map en les mettant dans la liste objs, puis on parcourt cette liste avec la boucle for, ce qui nous permet de récupérer la position, l’identifiant, le sprite, le nom et la description de chaque objet. Enfin, on ajoute l’objet à la liste interactables, et on retourne nos 4 listes.

*Le système de transition*

On commence par créer une variable booléenne transition. Ensuite, on crée 4 blocs if, qui ont tous le même rôle, mais ne fonctionnent pas avec les mêmes variables. Le premier s’exécute si le joueur sort de la map par la droite, le deuxième par la gauche, le troisième par le bas, et le quatrième par le haut. En fonction de là où le joueur sort, on le fait réapparaître à l’opposé de la map, et on met transition à True. Un autre bloc if exécuté seulement quand transition est à True continue le script. À l’intérieur, on y trouve deux actions à effectuer : la première est une mesure de sécurité qui empêche le joueur de sortir de la map. Par exemple, si le joueur sort de la map 2,3 par la droite, il ne se retrouvera pas dans le vide, mais réapparaîtra juste de l’autre côté de la map dans laquelle il se trouve déjà.

La deuxième action est la même qui est réalisée au lancement du jeu : elle permet de remplir les 4 listes tiles_below_player, tiles_above_player, walls et interactables.