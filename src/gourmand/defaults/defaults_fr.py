# -*- coding: utf-8 -*-
# we set up default information for our locale.
# Translators should use this file as the basis of their translation.
# Copy this file and rename it for you locale.
#
# For example, Spanish uses:
# defaults_es.py
#
# British English uses:
# defaults_en_GB.py
#
# Please fill in the below fields:

# Language: Français (French)
# Translator: Luc Charest.
# Last-updated: 2005-07-18 (07/18/05)

from typing import Collection, Mapping

from .abstractLang import AbstractLanguage


class Language(AbstractLanguage):

    CREDITS = "Luc Charest"

    # TRANSLATOR WARNING: DO NOT TRANSLATE THE FIELD NAMES: ONLY THE VALUES!!!

    # only translate the items in the list [..] (and feel free to create
    # categories that make sense for your locale -- no need to translate
    # these ones). DO NOT translate 'cuisine','rating','source' or
    # 'category'

    # The below are Gourmet's standard fields and the default categories for them.
    # Do not translate the field names ('cuisine','rating','source,'category').
    # Instead, fill in the list with categories that make sense for your locale.
    # Feel free to change the number or content of categories to be consistent
    # with what users in your locale are likely to be familiar with.

    fields = {'cuisine': ['Américaine', 'Italienne', 'Mexicaine',
                          'Américaine/sud-ouest', 'Asiatique/thaïlandaise', 'Asiatique/vietnamienne',
                          'Asiatique/chinoise', 'Asiatique/japonaise', 'Asiatique/indienne', 'Canadienne',
                          'Canadienne/québécoise', 'Grecque', 'Française'],
              'rating': ['5 - Excellent', '4 - Très bon', '3 - Bon', '2 - Moyen', '1 - Mauvais', '(non-testé)'],
              'source': [],
              'category': ['Dessert', 'Entrée', 'Salade', 'Soupe',
                           'Petit-déjeuner'],
              }

    # In English, there are a heck of a lot of synonyms. This is a list
    # for those synonyms.  ["preferred word","alternate word","alternate word"]
    # If there are none of these that you can think of in your language, just
    # set this to:
    # SYNONYMS=[]

    # note from translator: some terms are not standard but used in common langugage, some are used in a fautive manner,
    # I decided to put them in different sections so it is still clear what is a synonym and what should not be a synonym.
    SYNONYMS = [
        # the first item of each list is the default
        ["anis", "anis vert"],
        ["doliques à œil noir", "haricot à œil noir"],
        ["gourganes", "fèves des marais"],
        ["haricots de Lima", "haricot de Siéva", "haricot du Cap",
            "haricot du Tchad", "haricot de Madagascar"],
        ["soya", "soja"],
        ["fruit à pain", "fruit de l'arbre à pain"],
        ["chou pommé", "chou cabus"],
        ["bette à carde", "bette", "poirée", "carde", "bette poirée", "bette à côtes",
         "blète", "blette", "carde poirée", "bette à cardes"],
        ["coriandre", "persil chinois", "persil arabe"],
        ["mâche commune", "mâche", "doucette"],
        ["endive", "chicorée de Bruxelles", "chicon", "witloof", "chicorée witloof"],
        ["crosses de fougère", "crosses de fougère-à-l'autruche", "tête-de-violon"],
        ["chou vert frisé", "chou frisé"],
        ["maïs", "blé d'Inde", "blé d'Espagne", "blé de Turquie"],
        ["tétragone", "épinard de la Nouvelle-Zélande",
            "épinard d'été", "tétragone cornue", "tétragone étalée"],
        ["gombo", "okra", "ketmie comestible", "ketmie-gombo", "gombaud"],
        ["ciboulette", "civette"],
        ["poivron", "piment doux"],
        ["chile", "chili", "chilli"],
        ["chicorée de Vérone", "chicorée rouge de Vérone"],
        ["betterave", "betterave potagère"],
        ["carotte", "carotte potagère"],
        ["céleri-rave", "céleri tubéreux", "céleri rave"],
        ["daïkon", "radis oriental", "radis blanc", "radis blanc chinois", "radis de Satzouma",
         "radis de Satsuma", "radis du Japon", "daikon", "radis japonais"],
        ["navet", "rabiole"],
        ["courge poivrée", "courgeron", "courge gland"],
        ["courgette", "zucchini"],
        ["pâtisson", "bonnet d'électeur", "bonnet-d'électeur", "bonnet-de-prêtre",
         "bonnet de prêtre", "patisson", "pastisson"],
        ["dolique bulbeux", "dolique tubéreux"],
        ["topinambour", "artichaut de Jérusalem", "poire de terre", "artichaut du Canada",
         "artichaut d'hiver", "artichaut des neiges", "soleil vivace", "topine", "topinambourg"],
        ["patate douce", "patate sucrée"],
        ["taro", "colocase", "colocasie"],
        ["cenelle", "senelle"],
        ["amélanche", "Saskatoon"],
        ["nèfle du Japon", "bibace", "bibasse ", "loquat"],
        ["fruit du rosier", "fruit d'églantier", "cynorhodon", "cynorrhodon"],
        ["cerise de terre", "alkékenge"],
        ["mûre", "mûre sauvage", "mûron", "mûre des haies"],
        ["chicouté", "plaquebière", "mûre des marais", "chicoutai", "chicoutée"],
        ["bearberry", "raisin d'ours", "cerise d'ours"],
        ["myrtille", "airelle noire", "brimbelle",
            "raisin des bois", "teint-vin", "airelle"],
        ["canneberge", "atoca", "ataca", "mocauque", "airelle canneberge"],
        ["airelle", "airelle rouge", "airelle ponctuée",
            "pomme de terre", "graine rouge", "berri"],
        ["groseille rouge à grappes", "gadelle rouge"],
        ["cassis", "groseille noire", "gadelle noire"],
        ["groseille blanche à grappes", "gadelle blanche"],
        ["baie de sureau", "sureau"],
        ["groseille à maquereau", "groseille"],
        ["symphorine occidentale", "graine de loup", "symphorine du Nord-Ouest"],
        ["kaki", "plaquemine", "fruit de Sharon"],
        ["Shepherdie du Canada", "Shépherdie du Canada", "Shéferdie du Canada",
         "Shéferdie argentée", "graines de bœuf"],
        ["pitahaya", "pitaya"],
        ["melon d'eau", "pastèque"],
        ["raisin vert", "raisin blanc"],
        ["jujube", "datte chinoise"],
        ["cédrat", "poncire", "pomme du paradis"],
        ["pomélo", "pomelo"],
        ["lime", "citron vert", "lime acide", "limette acide",
            "lime mexicaine", "limette mexicaine"],
        ["longane", "œil-de-dragon"],
        ["litchi", "letchi"],
        ["fruit de la Passion", "passiflore", "fruit de la passion"],
        ["akée", "akee", "aki"],
        ["banane à cuire", "banane plantain", "plantain"],
        ["carambole", "fruit étoile", "pomme de Goa"],
        ["anone cœur de bœuf", "cachiman cœur de bœuf", "cœurde bœuf"],
        ["durion", "dourian"],
        ["jaque", "jacque"],
        ["mangoustan", "mangouste"],
        ["langsat", "duku"],
        ["ramboutan", "litchi chevelu"],
        ["pomme-rose", "pomme de rose", "jamerose"],
        ["sapodilla", "nèfle d'Amérique"],
        ["corossol épineux", "corossol", "anone", "anone muriquée",
         "cachiman épineux", "sapadille", "Guanabana"],
        ["pomme cannelle", "anone écailleuse", "pomme-cannelle"],
        ["bar d'Amérique", "loup de mer", "bar rayé", "bar de mer"],
        ["flet", "flondre"],
        ["églefin", "aiglefin"],
        ["flétan de l'Atlantique", "flétan", "flétan atlantique", "flétan blanc"],
        ["grand brochet", "brochet du Nord",
            "grand brochet du Nord", "brochet commun"],
        ["goberge", "lieu noir"],
        ["plie canadienne", "plie du Canada", "balai de l'Atlantique", "balai"],
        ["tilapia", "perche d'Afrique"],
        ["tile", "achigan", "achigan de mer", "doré de mer", "tile de mer"],
        ["truite", "ombles"],
        ["caviar", "caviar noir"],
        ["calmar", "encornet"],
        ["bifteck", "biftèque"],
        ["hamburger", "hambourgeois", "burger"],
        ["dinde", "dindon"],
        ["cerf de Virginie", "chevreuil", "cerf à queue blanche"],
        ["levure chimique", "levure artificielle",
            "poudre levante", "poudre à lever"],
        ["hydrogénocarbonate de sodium", "carbonate acide de sodium"],
        ["cassonade", "sucre roux"],
        ["beurre d'arachide", "pâte de cacahuète", "pâte d'arachide", "beurre de cacahouètes",
         "beurre de cacahuètes", "pâte de cacahuètes", "beurre d'arachides"],
        ["mozzarella", "mozzarelle"],
        ["féta", "feta"],
        ["yogourt", "yaourt", "yoghourt"],
        ["linguines", "languettes"],
        ["tomate cerise", "tomate cocktail"],
        ["tomate en grappe", "tomate grappe"],
        ["nappa", "chou nappa", "chou napa", "napa"],
        ["plumes rayées", "penne rigate"],
        ["plumes", "penne"],
        ["pâtes alimentaires", "pâtes"],
        ["sauce de soja", "sauce soja", "sauce soya", "sauce de soya"],
        ["poivre de Cayenne", "piment de Cayenne", "cayenne"],
        ["cari", "curry"],
        ["garam masala", "masala", "massala", "garam massala"],

        # non-standard usage
        ["morue charbonnière", "morue noire"],
        ["barbue de rivière", "barbue d'Amérique", "barbue du Nord", "barbue"],
        ["barbotte", "barbotte brune"],
        ["morue", "cabillaud"],
        ["lamproie", "grande lamproie marine"],
        ["morue-lingue", "abadèche lingue"],
        ["coryphène", "dauphin", "dorade tropicale"],
        ["baudroie", "crapaud de mer"],
        ["hoplostète orange", "hoplostète rouge", "perche de mer néo-zélandaise"],
        ["goberge", "colin", "colin noir"],
        ["goberge de l'Alaska", "morue du Pacifique occidental",
            "morue des neiges", "lieu de l'Alaska"],
        ["turbot de sable", "turbot"],
        ["plie canadienne", "plie blanche",
            "faux flétan", "flétan nain", "carrelet"],
        ["sprat", "esprot"],
        ["bar commun", "corvine", "loubine"],
        ["vivaneau", "lutian"],
        ["scorpène", "rascasse"],
        ["vivaneau rouge", "vivaneau campèche"],
        ["merlu blanc", "merlu du Sud"],
        ["crabe royal", "crabe d'Alaska"],
        ["crabe des neiges", "crabe araignée"],
        ["ormeau", "abalone", "oreille de mer"],
        ["mye", "coque", "palourde", "quahog"],
        ["hydrogénocarbonate de sodium", "bicarbonate de sodium",
            "bicarbonate de soude", "sel de Vichy"],
        ["grains de chocolat", "brisures de chocolat",
            "larmes de chocolat", "pépites de chocolats"],
        ["crème 10% M.G.", "crème à café"],
        ["crème 15% M.G.", "crème de table"],
        ["crème 35% M.G.", "crème à fouetter"],
        ["vermicelle", "vermicelli", "capellini"],

        # fautive/discouraged usages
        #["oignon vert","échalote"],
        #["chile","piment du Chili"],
        # ["poivron","piment"],
        ["germes de haricot", "fèves germées", "haricots germés",
            "pousses de soja", "pousse de soya"],
        ["navet", "navet blanc"],
        ["pommette", "pomme sauvage"],
        ["amélanche", "petite poire"],
        ["figue de Barbarie", "poire cactus"],
        ["melon à cornes", "Kiwano"],
        ["litchi", "cerise de Chine"],
        ["barbue de rivière", "poisson-chat"],
        ["églefin", "haddeck"],
        ["baudroie", "lotte"],
        #["turbot de sable","sole","plie"],
        #["plie canadienne","sole"],
        ["vivaneau", "dorade"],
        ["espadon", "poisson sabre", "poisson épée"],
        ["mye", "clam"],
        ["poulpe", "pieuvre"],
        ["levure chimique", "poudre à pâte"],
        ["hydrogénocarbonate de sodium", "soda à pâte"],
        ["beurre d'arachide", "beurre de peanut", "beurre de peanuts"],
        ["tomate en grappe", "tomate sur vigne", "tomate sur la vigne", "tomate en vigne",
         "tomate en branches", "tomate sur tige", "tomate à tiges"],
    ]

    # a dictionary for ambiguous words.
    # key=ambiguous word, value=list of possible non-ambiguous terms
    #
    # Translators: if you have a word that has more than one food meaning
    # in your language, you can add an entry as follow

    # AMBIGUOUS = {
    #              'word':['meaning1','meaning2','meaning3'],
    #             }

    AMBIGUOUS = {
        'chou-navet': ['chou-navet blanc', 'rutabaga'],
        'chou navet': ['chou-navet blanc', 'rutabaga'],
        'patate': ['pomme de terre', 'patate douce']
    }

    # triplicates ITEM, KEY, SHOPPING CATEGORY
    # These will be defaults.

    # They should include whatever foods might be standard for your
    # locale, with whatever sensible default categories you can think of
    # (again, thinking of your locale, not simply translating what I've
    # done).

    # Items provided here will automatically be recognized and go onto the
    # given category in a user's shopping list by default.

    # Don't feel obligated to translate every item -- especially since not
    # all items will be common for all locales. However, the more items
    # you can put here, the more the user will get the sense that gourmet
    # "knows" about foods that they enter.

    # I generated the below list using the wikipedia entry on foods as my
    # starting point. You may want to do something similar for your
    # locale.  Also, if the syntax of the below is too complicated, you
    # can send me a list of category headings and ingredients for your
    # locale and I'll do the necessary formatting <Thomas_Hinkle@alumni.brown.edu>

    INGREDIENT_DATA = [  # l é g u m e s
        # alfalfa sprouts
        ("luzerne", "luzerne", "fruits et légumes"),
        # anise
        ("anis", "anis", "fruits et légumes"),
        # artichoke
        ("artichaut", "artichaut", "fruits et légumes"),
        # arugula
        ("roquette", "roquette", "fruits et légumes"),
        # asparagus
        ("asperges", "asperges", "fruits et légumes"),
        ("aubergine", "aubergine", "fruits et légumes"),                        # (same)
        # avocado
        ("avocat", "avocat", "fruits et légumes"),
        ("haricots verts", "haricots verts",
         "fruits et légumes"),              # green beans
        ("haricots azuki", "haricots azuki",
         "fruits et légumes"),              # azuki beans
        ("germes de haricot", "germes de haricot",
         "fruits et légumes"),        # bean sprouts
        ("haricots noirs", "haricots noirs",
         "fruits et légumes"),              # black beans
        ("doliques à œil noir", "doliques à œil noir",
         "fruits et légumes"),    # black-eyed peas
        ("haricots borlotti", "haricots borlotti",
         "fruits et légumes"),        # borlotti beans (not sure)
        # broad beans
        ("gourganes", "gourganes", "fruits et légumes"),
        ("pois chiche ou garbanzos", "pois chiche ou garbanzos",
         "fruits et légumes"),  # chickpeas, garbanzos, or ceci beans
        # ("green beans","green beans","fruits et légumes"),                      # (already in the list !)
        ("haricots rouges", "haricots rouges",
         "fruits et légumes"),            # kidney beans
        # lentils
        ("lentilles", "lentilles", "fruits et légumes"),
        ("haricots de Lima ou haricots jaunes", "haricots de Lima ou haricots jaunes",
         "fruits et légumes"),  # lima bean or butter bean
        ("haricots mungo", "haricots mungo",
         "fruits et légumes"),              # mung beans
        ("petits haricots blancs", "petits haricots blancs",
         "fruits et légumes"),  # navy beans
        ("haricots d'Espagne", "haricots d'Espagne",
         "fruits et légumes"),      # runner beans
        # soybeans
        ("soya", "soya", "fruits et légumes"),
        ("pois", "pois", "fruits et légumes"),                                  # peas
        # ("snap peas","snap peas","fruits et légumes"),                          # (unknown)
        # bok choy
        ("pak-choï", "pak-choï", "fruits et légumes"),
        ("fruit à pain", "fruit à pain",
         "fruits et légumes"),                  # breadfruit
        # broccoflower
        ("brocofleur", "brocofleur", "fruits et légumes"),
        # broccoli
        ("brocoli", "brocoli", "fruits et légumes"),
        ("chou de Bruxelles", "chou de Bruxelles",
         "fruits et légumes"),        # brussels sprouts
        # cabbage
        ("chou pommé", "chou pommé", "fruits et légumes"),
        # ("calabrese","calabrese","fruits et légumes"),                          # (unknown)
        # cauliflower
        ("chou-fleur", "chou-fleur", "fruits et légumes"),
        # celery
        ("céleri", "céleri", "fruits et légumes"),
        ("bette à carde", "bette à carde",
         "fruits et légumes"),                # chard
        # cilantro
        ("coriandre", "coriandre", "fruits et légumes"),
        ("feuilles de chou", "feuilles de chou",
         "fruits et légumes"),          # collard greens
        ("mâche commune", "mâche commune",
         "fruits et légumes"),                # corn salad
        # (same)
        ("endive", "endive", "fruits et légumes"),
        # fennel
        ("fenouil", "fenouil", "fruits et légumes"),
        ("crosses de fougère", "crosses de fougère",
         "fruits et légumes"),      # fiddleheads
        ("chicorée frisée", "chicorée frisée",
         "fruits et légumes"),            # frisee
        ("chou vert frisé", "chou vert frisé",
         "fruits et légumes"),            # kale
        # kohlrabi
        ("chou-rave", "chou-rave", "fruits et légumes"),
        # lemon grass
        ("citronnelle", "citronnelle", "fruits et légumes"),
        # lettuce lactuca sativa
        ("laitue", "laitue", "fruits et légumes"),
        ("maïs", "maïs", "fruits et légumes"),                                  # corn
        # mushrooms
        ("champignons", "champignons", "fruits et légumes"),
        ("feuilles de moutarde", "feuilles de moutarde",
         "fruits et légumes"),  # mustard greens
        # nettles
        ("orties", "orties", "fruits et légumes"),
        # new zealand spinach
        ("tétragone", "tétragone", "fruits et légumes"),
        ("gombo", "gombo", "fruits et légumes"),                                # okra
        # ("onion family","onion family","fruits et légumes"),                    # (title?)
        ("ciboulette", "ciboulette", "fruits et légumes"),                      # chives
        # garlic
        ("ail", "ail", "fruits et légumes"),
        # leek allium porrum
        ("poireau", "poireau", "fruits et légumes"),
        # onion
        ("oignon", "oignon", "fruits et légumes"),
        # shallot
        ("échalote", "échalote", "fruits et légumes"),
        # scallion
        ("oignon vert", "oignon vert", "fruits et légumes"),
        # parsley
        ("persil", "persil", "fruits et légumes"),
        # pepper
        ("piment", "piment", "fruits et légumes"),
        # red bell pepper
        ("poivron rouge", "poivron rouge", "fruits et légumes"),
        ("poivron vert", "poivron vert",
         "fruits et légumes"),                  # (added)
        ("poivron jaune", "poivron jaune",
         "fruits et légumes"),                # (added)
        # chilli pepper
        ("chile", "chile", "fruits et légumes"),
        ("piment Jalapeño", "piment Jalapeño",
         "fruits et légumes"),            # jalapeño pepper
        ("piment habanero", "piment habanero",
         "fruits et légumes"),            # habanero pepper
        ("chicorée de Vérone", "chicorée de Vérone",
         "fruits et légumes"),      # radicchio
        # (same)
        ("rapini", "rapini", "fruits et légumes"),
        # rhubarb
        ("rhubarbe", "rhubarbe", "fruits et légumes"),
        # ("root vegetables","root vegetables","fruits et légumes"),              # (title?)
        ("betterave", "betterave", "fruits et légumes"),                        # beet
        # carrot
        ("carotte", "carotte", "fruits et légumes"),
        # cassava (manioc)
        ("manioc", "manioc", "fruits et légumes"),
        # celeriac
        ("céleri-rave", "céleri-rave", "fruits et légumes"),
        # daikon
        ("daïkon", "daïkon", "fruits et légumes"),
        # ("fennel","fennel","fruits et légumes"),                              # (already in the list !)
        ("gingembre", "gingembre", "fruits et légumes"),                        # ginger
        # parsnip
        ("panais", "panais", "fruits et légumes"),
        # radish
        ("radis", "radis", "fruits et légumes"),
        # (same)
        ("rutabaga", "rutabaga", "fruits et légumes"),
        ("chou-navet blanc", "chou-navet blanc",
         "fruits et légumes"),          # (added)
        # turnip
        ("navet", "navet", "fruits et légumes"),
        # (same)
        ("wasabi", "wasabi", "fruits et légumes"),
        # ("white radish","white radish","fruits et légumes"),                    # (daikon synonym)
        # skirret
        ("chervis", "chervis", "fruits et légumes"),
        # spinach
        ("épinard", "épinard", "fruits et légumes"),
        ("courge poivrée", "courge poivrée",
         "fruits et légumes"),              # acorn squash
        ("courge musquée", "courge musquée",
         "fruits et légumes"),              # butternut squash
        # zucchini
        ("courgette", "courgette", "fruits et légumes"),
        # cucumber
        ("concombre", "concombre", "fruits et légumes"),
        # ("gem squash","squash, gem","fruits et légumes"),                       # (unknown)
        # patty pans
        ("pâtisson", "pâtisson", "fruits et légumes"),
        # pumpkin
        ("citrouille", "citrouille", "fruits et légumes"),
        ("courge spaghetti", "courge spaghetti",
         "fruits et légumes"),          # spaghetti squash
        # ("tat soi","tat soi","fruits et légumes"),                              # (unknown)
        # tomato
        ("tomate", "tomate", "fruits et légumes"),
        ("dolique bulbeux", "dolique bulbeux",
         "fruits et légumes"),            # jicama
        # jerusalem artichoke
        ("topinambour", "topinambour", "fruits et légumes"),
        ("pomme de terre", "pomme de terre",
         "fruits et légumes"),              # potato
        # sweet potato
        ("patate douce", "patate douce", "fruits et légumes"),
        # (same)
        ("taro", "taro", "fruits et légumes"),
        ("igname", "igname", "fruits et légumes"),                              # yam
        ("châtaigne d'eau", "châtaigne d'eau",
         "fruits et légumes"),            # water chestnut
        ("cresson de fontaine", "cresson de fontaine",
         "fruits et légumes"),    # watercress
        # f r u i t s
        # apple
        ("pomme", "pomme", "fruits et légumes"),
        ("pomme cortland", "pomme cortland",
         "fruits et légumes"),              # (added)
        ("pomme délicieuse rouge", "pomme délicieuse rouge",
         "fruits et légumes"),  # (added)
        ("pomme golden", "pomme golden",
         "fruits et légumes"),                  # (added)
        ("pomme granny smith", "pomme granny smith",
         "fruits et légumes"),      # (added)
        ("pomme mcIntosh", "pomme mcIntosh",
         "fruits et légumes"),              # (added)
        # (added)
        ("pomme lobo", "pomme lobo", "fruits et légumes"),
        ("pomme spartan", "pomme spartan",
         "fruits et légumes"),                # (added)
        ("pomme melba", "pomme melba",
         "fruits et légumes"),                    # (added)
        ("pomme jerseymac", "pomme jerseymac",
         "fruits et légumes"),            # (added)
        # (added)
        ("pomme fuji", "pomme fuji", "fruits et légumes"),
        # green apple
        ("pomme verte", "pomme verte", "fruits et légumes"),
        # crabapple
        ("pommette", "pommette", "fruits et légumes"),
        # ("chokeberry","chokeberry","fruits et légumes"),                        # (unknown)
        # hawthorn
        ("cenelle", "cenelle", "fruits et légumes"),
        # juneberry
        ("amélanche", "amélanche", "fruits et légumes"),
        ("nèfle du Japon", "nèfle du Japon",
         "fruits et légumes"),              # loquat
        # medlar
        ("nèfle", "nèfle", "fruits et légumes"),
        # pomegranate
        ("grenade", "grenade", "fruits et légumes"),
        # quince
        ("coing", "coing", "fruits et légumes"),
        # rowan
        ("sorbe", "sorbe", "fruits et légumes"),
        ("fruit du rosier", "fruit du rosier",
         "fruits et légumes"),            # rose hip
        # apricot
        ("abricot", "abricot", "fruits et légumes"),
        # cherry
        ("cerise", "cerise", "fruits et légumes"),
        ("cerise de terre", "cerise de terre",
         "fruits et légumes"),            # (added)
        # (added)
        ("griotte", "griotte", "fruits et légumes"),
        ("cerise montmorency", "cerise montmorency",
         "fruits et légumes"),      # (added)
        ("prune", "prune", "fruits et légumes"),                                # plum
        ("prune reine-claude", "prune reine-claude",
         "fruits et légumes"),      # (added)
        ("prune mirabelle", "prune mirabelle",
         "fruits et légumes"),            # (added)
        ("prune quetsche", "prune quetsche",
         "fruits et légumes"),              # (added)
        ("prune black beaut", "prune black beaut",
         "fruits et légumes"),        # (added)
        ("prune friard", "prune friard",
         "fruits et légumes"),                  # (added)
        ("prune laroda", "prune laroda",
         "fruits et légumes"),                  # (added)
        ("prune santa rosa", "prune santa rosa",
         "fruits et légumes"),          # (added)
        ("prune simka", "prune simka",
         "fruits et légumes"),                    # (added)
        # peach
        ("pêche", "pêche", "fruits et légumes"),
        ("nectarine", "nectarine", "fruits et légumes"),                        # (same)
        # blackberry
        ("mûres", "mûres", "fruits et légumes"),
        ("mûre de Boysen", "mûre de Boysen",
         "fruits et légumes"),              # boysenberry
        # raspberry
        ("framboise", "framboise", "fruits et légumes"),
        ("framboise blanche", "framboise blanche",
         "fruits et légumes"),        # (added)
        ("framboise pourpre", "framboise pourpre",
         "fruits et légumes"),        # (added)
        ("framboise orange", "framboise orange",
         "fruits et légumes"),          # (added)
        ("framboise jaune", "framboise jaune",
         "fruits et légumes"),            # (added)
        # cloudberry
        ("chicouté", "chicouté", "fruits et légumes"),
        # ("wineberry","wineberry","fruits et légumes"),                          # (unknown)
        # bearberry
        ("busserole", "busserole", "fruits et légumes"),
        # bilberry
        ("myrtille", "myrtille", "fruits et légumes"),
        # blueberry
        ("bleuet", "bleuet", "fruits et légumes"),
        # cranberry
        ("canneberge", "canneberge", "fruits et légumes"),
        # ("huckleberry","huckleberry","fruits et légumes"),                      # (myrtille synonym)
        # lingonberry
        ("airelle", "airelle", "fruits et légumes"),
        # ("barberry ","barberry ","fruits et légumes"),                          # (unknown)
        ("groseille rouge à grappes", "groseille rouge à grappes",
         "fruits et légumes"),  # red currant
        # black currant
        ("cassis", "cassis", "fruits et légumes"),
        ("groseille blanche à grappes", "groseille blanche à grappes",
         "fruits et légumes"),  # white currant
        ("baie de sureau", "baie de sureau",
         "fruits et légumes"),              # elderberry
        ("groseille à maquereau", "groseille à maquereau",
         "fruits et légumes"),  # gooseberry
        # ("nannyberry","nannyberry","fruits et légumes"),                        # (unknown)
        # sea-buckthorn
        ("argouse", "argouse", "fruits et légumes"),
        ("symphorine occidentale", " symphorine occidentale",
         "fruits et légumes"),  # wolfberry
        # crowberry
        ("camarine", "camarine", "fruits et légumes"),
        # ("mulberry","mulberry","fruits et légumes"),                            # (blackberry synonym)
        # ("goumi","goumi","fruits et légumes"),                                  # (unknown)
        # kiwi fruit
        ("kiwi", "kiwi", "fruits et légumes"),
        # persimmon
        ("kaki", "kaki", "fruits et légumes"),
        ("Shepherdie du Canada", "Shepherdie du Canada",
         "fruits et légumes"),  # buffaloberry
        # pawpaw
        ("asimine", "asimine", "fruits et légumes"),
        # ("american persimmon","american persimmon","fruits et légumes"),        # (unknown)
        ("figue de Barbarie", "figue de Barbarie",
         "fruits et légumes"),        # prickly pear
        # ("saguaro","saguaro ","fruits et légumes"),                             # (unknown)
        # pitaya
        ("pitahaya", "pitahaya", "fruits et légumes"),
        # cantaloupe
        ("cantaloup", "cantaloup", "fruits et légumes"),
        ("melon miel Honeydew", "melon miel Honeydew",
         "fruits et légumes"),    # honeydew
        ("melon brodé", "melon brodé",
         "fruits et légumes"),                    # (added)
        ("melon à cornes", "melon à cornes",
         "fruits et légumes"),              # (added)
        ("melon Casaba", "melon Casaba",
         "fruits et légumes"),                  # (added)
        ("melon Santa Claus", "melon Santa Claus",
         "fruits et légumes"),        # (added)
        # ("sunberry","sunberry","fruits et légumes"),                            # (unknown)
        # watermelon
        ("melon d'eau", "", "fruits et légumes"),
        # strawberry
        ("fraise", "fraise", "fruits et légumes"),
        # angelica
        ("angélique", "angélique", "fruits et légumes"),
        # ("rhubarb","rhubarb","fruits et légumes"),                              # (already in the list !)
        ("figue", "figue", "fruits et légumes"),                                # fig
        # grape
        ("raisin", "raisin", "fruits et légumes"),
        ("raisin vert", "raisin vert",
         "fruits et légumes"),                    # (added)
        ("raisin rouge", "raisin rouge",
         "fruits et légumes"),                  # (added)
        # (same)
        ("jujube", "jujube", "fruits et légumes"),
        # black mulberry
        ("mûre noir", "mûre noir", "fruits et légumes"),
        # ("pomegranate","pomegranate","fruits et légumes"),                      # (already in the list !)
        ("datte", "datte", "fruits et légumes"),                                # date
        # citron
        ("cédrat", "cédrat", "fruits et légumes"),
        ("pamplemousse", "pamplemousse",
         "fruits et légumes"),                  # grapefruit
        # pommelo
        ("pomélo", "pomélo", "fruits et légumes"),
        # key lime
        ("lime", "lime", "fruits et légumes"),
        # (same)
        ("kumquat", "kumquat", "fruits et légumes"),
        # lemon
        ("citron", "citron", "fruits et légumes"),
        # (key lime synonym)
        ("lime", "lime", "fruits et légumes"),
        # mandarin
        ("mandarine", "mandarine", "fruits et légumes"),
        # clementine
        ("clémentine", "clémentine", "fruits et légumes"),
        # (same)
        ("tangelo", "tangelo", "fruits et légumes"),
        ("tangerine", "tangerine", "fruits et légumes"),                        # (same)
        # (same)
        ("orange", "orange", "fruits et légumes"),
        # ugli fruit
        ("ugli", "ugli", "fruits et légumes"),
        # guava
        ("goyave", "goyave", "fruits et légumes"),
        # longane
        ("longane", "longane", "fruits et légumes"),
        # lychee
        ("litchi", "litchi", "fruits et légumes"),
        ("fruit de la Passion", "fruit de la Passion",
         "fruits et légumes"),    # passion fruit
        # (same)
        ("feijoa", "feijoa", "fruits et légumes"),
        ("akée", "akée", "fruits et légumes"),                                  # akee
        # banana
        ("banane", "banane", "fruits et légumes"),
        ("banane cavendish", "banane cavendish",
         "fruits et légumes"),          # (added)
        ("banane gros michel", "banane gros michel",
         "fruits et légumes"),      # (added)
        ("banane à cuire", " banane à cuire",
         "fruits et légumes"),             # plantain
        # ("breadfruit","breadfruit","fruits et légumes"),                        # (already in the list !)
        # ("camucamu","camucamu","fruits et légumes"),                            # (unknown)
        # star fruit
        ("carambole", "carambole", "fruits et légumes"),
        # ("cempedak","cempedak","fruits et légumes"),                          # (unknown)
        # cherimoya
        ("chérimole", "chérimole", "fruits et légumes"),
        ("noix de coco", "noix de coco",
         "fruits et légumes"),                  # coconut
        ("anone cœur de bœuf", "anone cœur de bœuf",
         "fruits et légumes"),      # custard apple
        # ("dragonfruit","dragonfruit","fruits et légumes"),                      # (unknown)
        # durian
        ("durion", "durion", "fruits et légumes"),
        # ("guarana","guarana","fruits et légumes"),                              # (unknown)
        # jackfruit
        ("jaque", "jaque", "fruits et légumes"),
        # ("keppel fruit","keppel fruit","fruits et légumes"),                    # (unknown)
        # (same)
        ("langsat", "langsat", "fruits et légumes"),
        # ("velvet persimmon","velvet persimmon","fruits et légumes"),            # (unknown)
        ("abricot de Saint-Domingue", "abricot de Saint-Domingue",
         "fruits et légumes"),  # mamey sapote(apple)?
        # mamey sapote(apple)?
        ("sapote", "sapote", "fruits et légumes"),
        # ("mamoncillo","mamoncillo","fruits et légumes"),                        # (unknown)
        # mango
        ("mangue", "mangue", "fruits et légumes"),
        # mangosteen
        ("mangoustan", "mangoustan", "fruits et légumes"),
        # ("marang","marang","fruits et légumes"),                                # (unknown)
        # papaya
        ("papaye", "papaye", "fruits et légumes"),
        # ("peanut butter fruit","peanut butter fruit","fruits et légumes"),      # (unknown)
        # pineapple
        ("ananas", "ananas", "fruits et légumes"),
        # ("poha","poha","fruits et légumes"),                                    # (unknown)
        # rambutan
        ("ramboutan", "ramboutan", "fruits et légumes"),
        # rose apple
        ("pomme-rose", "pomme-rose", "fruits et légumes"),
        # (same)
        ("salak", "salak", "fruits et légumes"),
        # sapodilla
        ("sapotille", "sapotille", "fruits et légumes"),
        ("corossol épineux", "corossol épineux",
         "fruits et légumes"),          # soursop
        ("pomme cannelle", "pomme cannelle",
         "fruits et légumes"),              # sugar apple
        # tamarind
        ("tamarin", "tamarin", "fruits et légumes"),
        # ("acorn squash","squash, acorn","fruits et légumes"),                   # (already in the list !)
        # ("apple","apple","fruits et légumes"),                                  # (already in the list !)
        # ("arugula","arugula","fruits et légumes"),                              # (already in the list !)
        # ("avocado","avocado","fruits et légumes"),                              # (already in the list !)
        # ("basil, thai fresh","basil, fresh, thai","fruits et légumes"),         # (modifier?)
        # ("bean sprouts","bean sprouts","fruits et légumes"),                    # (already in the list !)
        # ("broccoli","broccoli","fruits et légumes"),                            # (already in the list !)
        # ("carrot","carrot","fruits et légumes"),                                # (already in the list !)
        # ("celery","celery","fruits et légumes"),                                # (already in the list !)
        ("tomate cerise", "tomate cerise",
         "fruits et légumes"),                # cherry tomato
        # ("chiles, dried red","chiles, red, dried","fruits et légumes"),         # (modifier?)
        # ("cilantro stems","cilantro stems","fruits et légumes"),                # (modifier?)
        # ("cucumber","cucumber","fruits et légumes"),                            # (already in the list !)
        # ("curly endive","endive, curly","fruits et légumes"),                   # (same as frisee?)
        # ("curly lettuce leaf","lettuce, curly leaf","fruits et légumes"),       # (unknown)
        # ("fresh basil","basil, fresh","fruits et légumes"),                     # (modifier?)
        # ("fresh cilantro","cilantro, fresh","fruits et légumes"),               # (modifier?)
        # ("fresh ginger","ginger, fresh","fruits et légumes"),                   # (modifier?)
        # (same)
        ("galanga", "galanga", "fruits et légumes"),
        # ("garlic","garlic","fruits et légumes"),                                 # (already in the list !)
        ("tomate en grappe", "tomate en grappe",
         "fruits et légumes"),          # grape tomato
        # ("leek","leek","fruits et légumes"),                                     # (already in the list !)
        # ("lemon grass","lemon grass","fruits et légumes"),                       # (already in the list !)
        ("jus de citron", "jus de citron",
         "fruits et légumes"),                # lemon juice
        # lime juice
        ("jus de lime", "jus de lime", "fruits et légumes"),
        # ("lime leaves","lime leaves","fruits et légumes"),                       # (modifier)
        # ("lime","lime","fruits et légumes"),                                     # (already in the list !)
        # nappa cabbage
        ("nappa", "nappa", "fruits et légumes"),
        # (same)
        ("olives", "olives", "fruits et légumes"),
        ("olives vertes", "olives vertes",
         "fruits et légumes"),                # (added)
        ("olives noirs", "olives noirs",
         "fruits et légumes"),                  # (added)
        # orange juice
        ("jus d'orange", "jus d'orange", "fruits et légumes"),
        # ("parsley","parsley","fruits et légumes"),                              # (already in the list !)
        # ("portobello mushroom","mushroom, portobello","fruits et légumes"),     # (unknown)
        # ("potato","potato","fruits et légumes"),                                # (already in the list !)
        # ("radicchio","radicchio","fruits et légumes"),                          # (already in the list !)
        ("oignon rouge", "oignon rouge",
         "fruits et légumes"),                  # red onion
        # ("red potato-skinned","potato, red-skinned","fruits et légumes"),       # (unknown)
        # ("roasted peanuts","peanuts, roasted","fruits et légumes"),             # (modifier?)
        # ("russet potato","potato, russet","fruits et légumes"),                 # (unknown)
        # ("salad greens","salad greens","fruits et légumes"),                    # (unknown)
        # ("scallion","scallion","fruits et légumes"),                            # (already in the list !)
        # ("spinach","spinach","fruits et légumes"),                              # (already in the list !)
        # squash
        ("courge", "courge", "fruits et légumes"),
        # ("tahitian squash","squash, tahitian","fruits et légumes"),             # (unknown)
        # ("tomato","tomato","fruits et légumes"),                                # (already in the list !)
        # white onion
        ("oignon blanc", "oignon blanc", "fruits et légumes"),
        # yellow onion
        ("oignon jaune", "oignon jaune", "fruits et légumes"),
        # ("zucchini","zucchini","fruits et légumes"),                            # (already in the list !)
        # ("zuchini","zuchini","fruits et légumes"),                              # (already in the list !)
        # ("mushroom","mushroom","fruits et légumes"),                            # (already in the list !)
        # ("shallot","shallot","fruits et légumes"),                              # (already in the list !)
        # ("bell red pepper","bell pepper, red","fruits et légumes"),             # (already in the list !)
        # f r u i t s   d e   m e r
        # anchovy
        ("anchois", "anchois", "fruits de mer"),
        ("achigan", "achigan", "fruits de mer"),                                # bass
        ("bar d'Amérique", "bar d'Amérique",
         "fruits de mer"),                  # striped bass
        ("morue charbonnière", "morue charbonnière",
         "fruits de mer"),          # black cod
        ("poisson globe", "poisson globe",
         "fruits de mer"),                    # blowfish
        ("barbue de rivière", "barbue de rivière",
         "fruits de mer"),            # catfish
        # (added)
        ("barbotte", "barbotte", "fruits de mer"),
        ("morue", "morue", "fruits de mer"),                                    # cod
        ("lamproie", "lamproie", "fruits de mer"),                              # eel
        # flounder
        ("flet", "flet", "fruits de mer"),
        # haddock
        ("églefin", "églefin", "fruits de mer"),
        ("flétan de l'Atlantique", "flétan de l'Atlantique",
         "fruits de mer"),  # halibut
        ("morue-lingue", "morue-lingue",
         "fruits de mer"),                      # lingcod
        # mahi mahi
        ("coryphène", "coryphène", "fruits de mer"),
        # monkfish
        ("baudroie", "baudroie", "fruits de mer"),
        ("hoplostète orange", "hoplostète orange",
         "fruits de mer"),            # orange roughy
        # ("chilean sea bass","chilean sea bass","fruits de mer"),                # (unknown)
        ("brochet", "brochet", "fruits de mer"),                                # pike
        ("grand brochet", "grand brochet",
         "fruits de mer"),                    # (added)
        # pollock
        ("goberge", "goberge", "fruits de mer"),
        ("goberge de l'Alaska", "goberge de l'Alaska",
         "fruits de mer"),        # (added)
        ("turbot de sable", "turbot de sable",
         "fruits de mer"),                # sanddab
        ("plie canadienne", "plie canadienne",
         "fruits de mer"),                # (added)
        # (same)
        ("sardine", "sardine", "fruits de mer"),
        # (added)
        ("sprat", "sprat", "fruits de mer"),
        # salmon
        ("saumon", "saumon", "fruits de mer"),
        # sea bass
        ("bar commun", "bar commun", "fruits de mer"),
        # shark
        ("requin", "requin", "fruits de mer"),
        # snapper
        ("vivaneau", "vivaneau", "fruits de mer"),
        # rockfish
        ("scorpène", "scorpène", "fruits de mer"),
        # ("rock cod","rock cod","fruits de mer"),                                # (rockfish synonym?)
        ("sébaste aux yeux jaunes", "sébaste aux yeux jaunes",
         "fruits de mer"),  # pacific snapper
        ("vivaneau rouge", "vivaneau rouge",
         "fruits de mer"),                  # red snapper
        # (same)
        ("sole", "sole", "fruits de mer"),
        # sturgeon
        ("esturgeon", "esturgeon", "fruits de mer"),
        # (same)
        ("surimi", "surimi", "fruits de mer"),
        # swordfish
        ("espadon", "espadon", "fruits de mer"),
        # (same)
        ("tilapia", "tilapia", "fruits de mer"),
        # tilefish
        ("tile", "tile", "fruits de mer"),
        # trout
        ("truite", "truite", "fruits de mer"),
        # tuna
        ("thon", "thon", "fruits de mer"),
        ("poisson maigre", "poisson maigre",
         "fruits de mer"),                  # whitefish
        # whiting
        ("merlu blanc", "merlu blanc", "fruits de mer"),
        # ("roe","roe","fruits de mer"),                                          # (title?)
        # (same)
        ("caviar", "caviar", "fruits de mer"),
        ("œufs de saumon", "œufs de saumon",
         "fruits de mer"),                  # salmon roe
        # crab
        ("crabe", "crabe", "fruits de mer"),
        # dungeness crab
        ("crabe dormeur", "crabe dormeur", "fruits de mer"),
        # king crab
        ("crabe royal", "crabe royale", "fruits de mer"),
        ("crabe des neiges", "crabe des neiges",
         "fruits de mer"),              # snow crab
        # écrevisse
        ("écrevisse", "écrevisse", "fruits de mer"),
        # lobster
        ("homard", "homard", "fruits de mer"),
        # shrimp
        ("crevette", "crevette", "fruits de mer"),
        ("crevettes roses", "crevettes roses",
         "fruits de mer"),                # prawns
        # abalone
        ("ormeau", "ormeau", "fruits de mer"),
        # clam
        ("mye", "mye", "fruits de mer"),
        # mussel
        ("moules", "moules", "fruits de mer"),
        # octopus
        ("poulpe", "poulpe", "fruits de mer"),
        # oyster
        ("huître", "huître", "fruits de mer"),
        # snail
        ("escargot", "escargot", "fruits de mer"),
        # squid
        ("calmar", "calmar", "fruits de mer"),
        # scallop
        ("pétoncle", "pétoncle", "fruits de mer"),
        # v i a n d e s
        # (same)
        ("bacon", "bacon", "viandes"),
        # (same)
        ("chorizo", "chorizo", "viandes"),
        # ("fuet","fuet","viandes"),                                              # (unknown)
        # (same)
        ("salami", "salami", "viandes"),
        # ham
        ("jambon", "jambon", "viandes"),
        # mutton
        ("mouton", "mouton", "viandes"),
        # lamb
        ("agneau", "agneau", "viandes"),
        # veal
        ("veau", "veau", "viandes"),
        # steak
        ("bifteck", "bifteck", "viandes"),
        # (same)
        ("hamburger", "hamburger", "viandes"),
        # roast beef
        ("rôti de bœuf", "rôti de bœuf", "viandes"),
        # chicken
        ("poulet", "poulet", "viandes"),
        # turkey
        ("dinde", "dinde", "viandes"),
        # duck
        ("canard", "canard", "viandes"),
        # goose
        ("oie", "oie", "viandes"),
        # (added)
        ("sanglier", "sanglier", "viandes"),
        # beef
        ("bœuf", "bœuf", "viandes"),
        # ground beef
        ("bœuf haché", "bœuf, haché", "viandes"),
        # (added)
        ("cerf", "cerf", "viandes"),
        # (added)
        ("lapin", "lapin", "viandes"),
        ("poitrine de poulet", "poulet, poitrine",
         "viandes"),                  # chicken breast
        # whole chicken
        ("poulet entier", "poulet, entier", "viandes"),
        ("patte de poulet", "poulet, patte",
         "viandes"),                        # chicken leg
        # pork
        ("porc", "porc", "viandes"),
        # Q u é b e c ' s   l o c a l e
        ("beurre d'érable", "beurre d'érable",
         "épicerie sucrée"),              # (added)
        ("sirop d'érable", "sirop d'érable",
         "épicerie sucrée"),                # (added)
        ("tire d'érable", "tire d'érable",
         "épicerie sucrée"),                  # (added)
        ("tire à l'érable", "tire à l'érable",
         "épicerie sucrée"),              # (added)
        # (added)
        ("caribou", "caribou", "viandes"),
        ("cerf de Virginie", "cerf de Virginie",
         "viandes"),                    # (added)
        # (added)
        ("relish", "relish", "condiments"),
        # é p i c e r i e
        ("farine tout usage", "farine tout usage",
         "épicerie"),                 # all flour purpose
        ("levure chimique", "levure chimique",
         "épicerie"),                     # baking powder
        ("hydrogénocarbonate de sodium",
         "hydrogénocarbonate de sodium", "épicerie"),  # baking soda
        # brown sugar
        ("cassonade", "cassonade", "épicerie"),
        ("grains de chocolat", "grains de chocolat",
         "épicerie"),               # chocolate chips
        # ("dark sugar brown","sugar, dark brown","épicerie"),                    # (unknown)
        # honey
        ("miel", "miel", "épicerie"),
        # ("light sugar brown","sugar, light brown","épicerie"),                  # (unknown)
        # salt
        ("sel", "sel", "épicerie"),
        # (added)
        ("gros sel", "sel, gros", "épicerie"),
        # (added)
        ("sel de mer", "sel de mer", "épicerie"),
        # ("shredded coconut","coconut, shredded","épicerie"),                    # (modifier?)
        ("extrait de vanille", "vanille, extrait de",
         "épicerie"),              # vanilla extract
        # walnut
        ("noix", "noix", "épicerie"),
        # white sugar
        ("sucre blanc", "sucre blanc", "épicerie"),
        ("farine de maïs jaune", "farine de maïs jaune",
         "épicerie"),           # yellow cornmeal
        ("flocons d'avoine", "flocons d'avoine",
         "épicerie"),                   # rolled oats
        # rice
        ("riz", "riz", "épicerie"),
        # p a i n
        # croutons
        ("croûtons", "croûtons", "pain"),
        # sourdough bread
        ("pain au levain", "pain au levain", "pain"),
        # c o n d i m e n t s
        ("moutarde de Dijon", "moutarde de Dijon",
         "condiments"),               # dijon mustard
        # (added)
        ("ketchup", "ketchup", "condiments"),
        # (same)
        ("mayonnaise", "mayonnaise", "condiments"),
        # t a r t i n a d e s
        ("beurre d'arachide", "beurre d'arachide",
         "tartinades"),               # peanut butter
        # é p i c e s
        # ("black ground pepper","black pepper, ground","épices"),                # (modifier?)
        ("poivre de cayenne", "poivre de cayenne",
         "épices"),                   # cayenne
        # ("chili powder","chili powder","épices"),                               # (modifier?)
        # ("coriander seeds","coriander, seeds","épices"),                        # (modifier?)
        # curry powder
        ("cari", "cari", "épices"),
        # (same)
        ("garam masala", "garam masala", "épices"),
        # ("ground cinnamon","cinnamon, ground","épices"),                        # (modifier?)
        # ("ground coriander","coriander, ground","épices"),                      # (modifier?)
        # ("ground cumin","cumin, ground","épices"),                              # (modifier?)
        # ("nutmeg","nutmeg","épices"),                                           # (modifier?)
        # (same)
        ("paprika", "paprika", "épices"),
        # ("powdered ginger","ginger, powdered","épices"),                        # (modifier?)
        # ("seeds ajowan","ajowan, seeds","épices"),                              # (modifier?)
        # ("seeds cumin","cumin, seeds","épices"),                                # (modifier?)
        # ("seeds mustard","mustard, seeds","épices"),                            # (modifier?)
        # ("star anise","star anise","épices"),                                   # (modifier?)
        # ("stick cinnamon","cinnamon, stick","épices"),                          # (modifier?)
        # turmeric
        ("curcuma", "curcuma", "épices"),
        # ("monkfish","monkfish","fruits de mer"),                                # (already in the list !)
        # ("salmon","salmon","fruits de mer"),                                    # (already in the list !)
        # ("whole rock cod or snapper","whole rock cod or snapper","fruits de mer"),  # (unknown)
        # i n t e r n a t i o n a l
        # coconut milk
        ("lait de coco", "lait de coco", "international"),
        # ("dried shrimp","shrimp, dried","international"),                       # (modifier?)
        # ("fish sauce","fish sauce","international"),                            # (unknown)
        # ("flat rice flour noodles","flat rice flour noodles","international"),  # (unknown)
        # ("green canned chiles","green chiles, canned","international"),         # (unknown)
        # ("green curry paste","green curry paste","international"),              # (unknown)
        ("vinaigre de riz", "vinaigre de riz",
         "international"),                # rice vinegar
        # ("roasted chili paste","roasted chili paste","international"),          # (unknown)
        # (same)
        ("salsa", "salsa", "international"),
        ("graine de sésame", "graine de sésame",
         "international"),              # sesame seeds
        ("pâte de crevettes", "pâte de crevettes",
         "international"),            # shrimp paste
        ("sauce de soja", "sauce de soja",
         "international"),                    # soy sauce
        # ("tamarind juice","tamarind juice","international"),                    # (unknown)
        # ("tamarind water","tamarind water","international"),                    # (unknown)
        # (same)
        ("couscous", "couscous", "international"),
        # p â t e s
        # lasagna pasta noodles
        ("pâtes à lasagne", "pâtes à lasagne", "pâtes"),
        # linguine pasta
        ("linguines", "linguines", "pâtes"),
        ("pâtes alimentaires", "pâtes alimentaires",
         "pâtes"),                  # pasta
        # penne pasta
        ("plumes rayées", "plumes rayées", "pâtes"),
        # (added)
        ("plumes", "plumes", "pâtes"),
        # ("peppered linguini","linguini, peppered","pâtes"),                     # (modifier?)
        # shells pasta
        ("coquilles", "coquilles", "pâtes"),
        ("coquilles petites", "coquilles petites",
         "pâtes"),                    # (added)
        ("coquilles géantes", "coquilles géantes",
         "pâtes"),                    # (added)
        # (same)
        ("spaghettis", "spaghettis", "pâtes"),
        # (added)
        ("vermicelles", "vermicelles", "pâtes"),
        # p r o d u i t s   l a i t i e r s
        # butter
        ("beurre", "beurre", "produits laitiers"),
        # (added)
        ("margarine", "margarine", "produits laitiers"),
        ("œuf", "œuf", "produits laitiers"),                                    # egg
        ("œufs", "œufs", "produits laitiers"),                                  # eggs
        # ("flour tortillas","tortillas, flour","produits laitiers"),             # (unknown)
        ("lait", "lait", "produits laitiers"),                                  # milk
        # sour cream
        ("crème sure", "crème sure", "produits laitiers"),
        # (added)
        ("crème", "crème", "produits laitiers"),
        ("crème 10% M.G.", "crème, 10% M.G.",
         "produits laitiers"),             # (added)
        ("crème 15% M.G.", "crème, 15% M.G.",
         "produits laitiers"),             # (added)
        ("crème 35% M.G.", "crème, 35% M.G.",
         "produits laitiers"),             # (added)
        # yogurt
        ("yogourt", "yogourt", "produits laitiers"),
        # f r o m a g e s
        # cheddar cheese
        ("cheddar", "fromage, cheddar", "fromages"),
        # cottage cheese
        ("cottage", "fromage, cottage", "fromages"),
        # feta cheese
        ("féta", "fromage, féta", "fromages"),
        ("fromage de chèvre blanc", "fromage de chèvre blanc",
         "fromages"),     # fresh cheese white goat
        # jack cheese
        ("jack", "fromage, jack", "fromages"),
        # mozzarella cheese
        ("mozzarella", "fromage, mozzarella", "fromages"),
        # parmesan cheese
        ("parmesan", "fromage, parmesan", "fromages"),
        # provolone cheese
        ("provolone", "fromage, provolone", "fromages"),
        # ricotta cheese
        ("ricotta", "fromage, ricotta", "fromages"),
        # smoked cheese Gouda
        ("Gouda fumé", "fromage, Gouda fumé", "fromages"),
        # s o u p e s   &   s a u c e s
        ("soupe de tomates", "soupe, tomate",
         "soupes & sauces"),               # tomato sauce
        ("bouillon de légumes", "bouillon, légumes",
         "soupes & sauces"),        # vegetable broth
        # h u i l e s   &   v i n a i g r e s
        ("vinaigre balsamique", "vinaigre balsamique",
         "huiles & vinaigres"),   # balsamic vinegar
        ("huile de maïs", "huile de maïs",
         "huiles & vinaigres"),               # corn oil
        ("huile d'olive", "huile d'olive",
         "huiles & vinaigres"),               # olive oil
        ("huile de sésame", "huile de sésame",
         "huiles & vinaigres"),           # sesame oil
        ("huile végétale", "huile végétale",
         "huiles & vinaigres"),             # vegetable oil
        ("huile de soja", "huile de soja",
         "huiles & vinaigres"),               # (added)
        # v i n   &   s p i r i t u e u x
        # white wine
        ("vin blanc", "vin, blanc", "vin & spiritueux"),
        # (added)
        ("vin rouge", "vin, rouge", "vin & spiritueux"),
        # t h i n g   y o u   s h o u l d   h a v e   a t   h o m e
        # water
        ("eau", "eau", "")
    ]

    # THESE ARE STANDARD UNIT CONVERSIONS. You can simply translate unit names where
    # you know them. Eliminate entries that are untranslatable or don't exist in your
    # locale. And please add any additional units that you know of.
    # Each unit is of the following format:
    # ("unit1","unit2"):conversion_factor, where unit1 contains conversion_factor X unit2
    # For example: 1 cup has 16 tablespoons.
    CONVERTER_TABLE = {
        ("c.", "tbs."): 16,
        ("lb.", "oz."): 16,
        ("tbs.", "tsp."): 3,
        ("pt.", "c."): 2,
        ("qt.", "c."): 4,
        ("gallon", "qt."): 4,
        ("l", "qt."): 1.057,
        ("l", "ml"): 1000,
        ("l", "cl"): 100,
        ("l", "dl"): 10,
        ("oz.", "g"): 28.35,
        ("kg", "g"): 1000,
        ("g", "mg"): 1000,
        ("tsp.", "drop"): 76,
        ("oz.", "dram"): 16,
        ("dram", "grains"): 27.34375,
        ("peck", "gallon"): 2,
        ("bucket", "peck"): 2,
        ("bushel", "bucket"): 2,
        ("lb.", "grains"): 7000}

    # from translator : see note further...

    # # THESE ARE STANDARD UNIT CONVERSIONS. You can simply translate unit names where
    # # you know them. Eliminate entries that are untranslatable or don"t exist in your
    # # locale. And please add any additional units that you know of.
    # # Each unit is of the following format:
    # # ("unit1","unit2"):conversion_factor, where unit1 contains conversion_factor X unit2
    # # For example: 1 cup has 16 tablespoons.
    # CONVERTER_TABLE = {
    #     ("tasse","c. à table"):16,
    #     ("lb","oz"):16,
    #     ("c. à table","c. à thé"):3,
    #     ("chop","tasse"):2,
    #     ("pte","tasse"):4,
    #     ("gallon","pte"):4,
    #     ("l","pte"):1.057,
    #     ("l","ml"):1000,
    #     ("l","cl"):100,
    #     ("l","dl"):10,
    #     ("oz","g"):28.35,
    #     ("kg","g"):1000,
    #     ("g","mg"):1000,
    #     ("c. à thé","goutte"):76,
    #     ("oz","dram"):16
    #    }

    # DENSITIES of common foods. This allows us to convert between mass and volume.
    # Translators: You may be best off translating the food names below, since lists
    # of food densities can be hard to come by!
    DENSITY_TABLE = {
        "eau": 1,                        # water
        "jus de raisins": 1.03,          # juice, grape
        "bouillon de légumes": 1,        # vegetable broth
        "bouillon de poulet": 1,         # broth, chicken
        "lait": 1.029,                   # milk
        "lait entier": 1.029,            # milk, whole
        "lait écrémé": 1.033,            # milk, skim
        "lait 2%": 1.031,                # milk, 2%
        "lait 1%": 1.03,                 # milk, 1%
        "lait de noix de coco": 0.875,   # coconut milk
        "babeurre": 1.03,                # buttermilk
        "crème riche": 0.994,            # heavy cream
        "crème légère": 1.012,           # light cream
        "crème 11,5%": 1.025,            # half-and-half
        "miel": 1.420,                   # honey
        "sucre blanc": 1.550,            # sugar, white
        "sel": 2.165,                    # salt
        "beurre": 0.911,                 # butter
        "huile végétale": 0.88,          # oil, vegetable
        "huile d'olive": 0.88,           # oil, olive
        "huile de maïs": 0.88,           # oil, corn
        "huile de sésame": 0.88,         # oil, sesame
        "farine tout usage": 0.6,       # flour, all purpose
        "farine de blé entier": 0.6,    # flour, whole wheat
        "fécule de maïs": 0.6,          # corn starch
        "sucre en poudre": 0.6,         # sugar, powdered
        "sucre glace": 0.6              # sugar, confectioners
    }

    # Standard unit names and alternate unit names that might appear.  For
    # example: "c." is our standard abbreviation for cup.  "cup","c." or
    # "cups" might appear in a recipe we are importing.  Each item of this
    # list looks like this:
    #
    # ["standard", ["alternate1","alternate2","alternate3",...]]
    #
    # The first item should be the preferred abbreviation
    # The second item should be the full name of the unit
    # e.g. ["c.", ["cup",...]]
    #
    UNITS = [("bucket", ["bucket", "buckets", "bckt."]),
             ("peck", ["peck", "pecks"]),
             ("bushel", ["bushel", "bushels", "bsh.",
              "bu.", "bu", "bsh", "bshl", "bshl."]),
             ("grains", ["grain", "grains"]),
             ("dram", ["dram", "drams"]),
             ("drop", ["drop"]),
             ("tsp.", ["teaspoon", "tsp", "tsp.", "tea spoon", "tsps.", "teaspoons",
              "tea spoons", "Teaspoon", "Teaspoons", "t", "Ts.", "Tsp.", "Tsp"]),
             ("tbs.", ["tablespoon", "tbs", "tbsp", "tbs.", "tbsp.", "table spoon",
              "tbsps.", "tablespoons", "Tablespoon", "T", "Tbs.", "Tbsp", "Tbsp."]),
             ("lb.", ["pound", "lb", "lb.", "lbs.", "pounds"]),
             ("oz.", ["ounce", "oz", "ounces", "oz."]),
             ("c.", ["cup", "c.", "cups"]),
             ("qt.", ["quart", "qt.", "quarts"]),
             ("pt.", ["pint", "pt.", "pints"]),
             ("gallon", ["gallon", "gallons", "gal."]),
             ("ml", ["mililiter", "ml", "ml.", "mililiters"]),
             ("cl", ["centiliter", "cl", "cl.", "centiliters"]),
             ("dl", ["deciliter", "dl", "dl.", "deciliters"]),
             ("l", ["liter", "l.", "lit.", "liters"]),
             ("g", ["grams", "gram", "g."]),
             ("mg", ["miligram", "mg.", "mg", "miligrams"]),
             ("kg", ["kilogram", "kg.", "kg",  "kilograms"]),
             ]

    METRIC_RANGE = (1, 999)

    # The following sets up unit groups. Users will be able to turn
    # these on or off (American users, for example, would likely turn
    # off metric units, since we don't use them).
    # (User choice not implemented yet)
    UNIT_GROUPS = {
        'metric mass': [('mg', METRIC_RANGE),
                        ('g', METRIC_RANGE),
                        ('kg', (1, None))],
        'metric volume': [('ml', METRIC_RANGE),
                          ('cl', (1, 99)),
                          ('dl', (1, 9)),
                          ('l', (1, None)), ],
        'imperial weight': [('grains', (0, 27)),
                            ('dram', (0.5, 15)),
                            ('oz.', (0.25, 32)),
                            ('lb.', (0.25, None)),
                            ],
        'imperial volume': [('drop', (0, 3)),
                            ('tsp.', (0.125, 3)),
                            ('tbs.', (1, 4)),
                            ('c.', (0.25, 6)),
                            ('pt.', (1, 1)),
                            ('qt.', (1, 3)),
                            ('gallon', (1, None)),
                            ('peck', (1, 2)),
                            ('bucket', (1, 2)),
                            ('bushel', (1, None))]
    }

    # The units here need to correspond to the standard unit names defined
    # above in UNITS
    CROSS_UNIT_TABLE = {
        # This if for units that require an additional
        # bit of information -- i.e. to convert between
        # volume and mass you need the density of an
        # item.  In these cases, the additional factor
        # will be provided as an 'item' that is then looked
        # up in the dictionary referenced here (i.e. the density_table)
        # currently, 'density' is the only keyword used
        ("pt.", "lb."): ('density', 1),
        ("tbs.", "oz."): ('density', 0.5),
        ("c.", "oz."): ('density', 8),
        ("pt.", "oz."): ('density', 16),
        ("ml", "g"): ('density', 1)}

    # The units here need to correspond to the standard unit names defined
    # in UNITS.  These are some core conversions from mass-to-volume,
    # assuming a density of 1 (i.e. the density of water).
    VOL_TO_MASS_TABLE = {
        ("pt.", "lb."): 1,
        ("tbs.", "oz."): 0.5,
        ("c.", "oz."): 8,
        ("pt.", "oz."): 16,
        ("ml", "g"): 1,
        ("ml", "mg"): 1000,
        ("ml", "kg"): 0.001,
        ("cl", "kg"): 0.01,
        ("cl", "g"): 10,
        ("dl", "kg"): 0.1,
        ("dl", "g"): 100,
        ("l", "kg"): 1}

    # From translator :
    # FRENCH PART TO BE REVISED !!! US units != UK units != Canadian units !!!
    # I will work on these later...

    # # Stand unit names and alternate unit names that might appear.  For
    # # example: "c." is our standard abbreviation for cup.  "cup","c." or
    # # "cups" might appear in a recipe we are importing.  Each item of this
    # # list looks like this:
    # #
    # # ["standard", ["alternate1","alternate2","alternate3",...]]

    # UNITS = [
    #         #["bucket" , ["bucket","buckets","bckt."]],
    #          ["picotin", ["peck","pecks","picotin"]],                            #peck
    #          ["boisseau", ["bushel","bushels","bsh.","bu.","bu","bsh","bshl","bshl.","boisseau","minot"]],    #bushel
    #          #["grains", ["grain","grains"]],
    #          ["dram", ["dram","drams"]],                                    #(same)
    #          ["goutte", ["drop","goutte","gouttes"]],                            #drop
    #          ["c. à thé", ["teaspoon","tsp","tsp.","tea spoon","tsps.","teaspoons","tea spoons","Teaspoon",
    #                    "cuiller à thé","cuillers à thé","cuiller a the","cuillers a the","cuiller à th.",
    #                "cuillers a th.", "c. à th.","c. a th."]],                    #tsp.
    #      ["c. à table", ["tablespoon","tbs","tbsp","tbs.","tbsp.","table spoon","tbsps.","tablespoons",
    #                  "Tablespoon", "cuillère à table","cuillères à table","cuillere a table","cuilleres a table",
    #                  "cuillerée à soupe","cuillerées à soupe","cuilleree a soupe","cuillerees a soupe"]],    #tbs.
    #          ["lb", [ "pound","lb","lb.","lbs.","pounds","livre","livres"]],                #lb.
    #          ["oz", [ "ounce","oz","ounces","oz.","once","onces"]],                        #oz.
    #          ["tasse", ["cup","c.","cups","tasse","tasses","t"]],                        #c.
    #          ["pte", ["quart","qt.","quarts","pte","pinte","pintes"]],                    #qt.
    #          ["chop", ["pint","pt.","pints","chop","chopine","chopines","chopine liquide"]],        #pt.
    #          ["gallon", ["gallon","gallons","gal."]],
    #          ["gallon US", ["gallon US","gallon amériacain"]],
    #          ["ml", ["mililiter","ml","ml.","mililiters","millilitre","millilitres"]],            #ml.
    #          ["cl", ["centiliter","cl","cl.","centiliters","centilitre","centilitres"]],            #cl.
    #          ["dl", ["deciliter","dl","dl.","deciliters","décilitre","decilitre","décilitres","décilitres"]],#dl.
    #          ["l", ["liter","l.","lit.","liters","litre","litres"]],                    #l.
    #          ["g", ["grams","gram","g","gramme","grammes"]],                        #g.
    #          ["mg", ["miligram","mg.","mg","miligrams","milligramme","milligrammes"]],            #mg.
    #          ["kg", ["kilogram","kg.","kg","kilograms","kilogramme","kilogrammes"]]                #kg.
    #          ]

    # METRIC_RANGE = (1,999)

    # # The following sets up unit groups. Users will be able to turn
    # # these on or off (American users, for example, would likely turn
    # # off metric units, since we don"t use them).
    # # (User choice not implemented yet)
    # UNIT_GROUPS = {
    #     "metric mass":[("mg",METRIC_RANGE),
    #                    ("g",METRIC_RANGE),
    #                    ("kg",(1,None))],
    #     "metric volume":[("ml",METRIC_RANGE),
    #                      ("cl",(1,99)),
    #                      ("dl",(1,9)),
    #                      ("l",(1,None))],
    #     "imperial weight":[#("grains",(0,27)),
    #                        ("dram",(0.5,15)),
    #                        ("oz",(0.25,32)),
    #                        ("lb",(0.25,None))
    #                        ],
    #     "imperial volume":[("goutte",(0,3)),
    #                        ("c. à thé",(0.125,3)),
    #                        ("c. à table",(1,4)),
    #                        ("tasse",(0.25,6)),
    #                        ("chop",(1,1)),
    #                        ("pte",(1,3)),
    #                        ("gallon US",(1,None)),
    #                        ("picotin",(1,2)),
    #                        #("bucket",(1,2)),
    #                        ("boisseau",(1,None))]
    #     }

    # # The units here need to correspond to the standard unit names defined
    # # above in UNITS
    # CROSS_UNIT_TABLE = {
    #     ## This if for units that require an additional
    #     ## bit of information -- i.e. to convert between
    #     ## volume and mass you need the density of an
    #     ## item.  In these cases, the additional factor
    #     ## will be provided as an "item" that is then looked
    #     ## up in the dictionary referenced here (i.e. the density_table)
    #     ## currently, "density" is the only keyword used
    #     ("chop","lb"):["density",1],
    #     ("c. à table","oz"):["density",0.5],
    #     ("tasse","oz"):["density",8],
    #     ("chop","oz"):["density",16],
    #     ("ml","g"):["density",1]}

    # # The units here need to correspond to the standard unit names defined
    # # in UNITS.  These are some core conversions from mass-to-volume,
    # # assuming a density of 1 (i.e. the density of water).
    # VOL_TO_MASS_TABLE = {
    #     ("chop","lb") : 1,                    #(warning, might not be accurate, see below)
    #     ("c. à table","oz") : 0.5,
    #     ("tasse","oz") : 8,
    #     ("chop","oz") : 20,                    #(warning, modified, see "chopine" in granddictionnaire)
    #     ("ml","g") : 1,
    #     ("ml","mg") : 1000,
    #     ("ml","kg"): 0.001,
    #     ("cl","kg"): 0.01,
    #     ("cl","g") : 10,
    #     ("dl","kg") : 0.1,
    #     ("dl","g") : 100,
    #     ("l","kg") : 1}

    # These functions are rather important! Our goal is simply to
    # facilitate look ups -- if the user types in "tomatoes", we want to
    # find "tomato." Note that the strings these functions produce will
    # _never_ be shown to the user, so it's fine to generate nonsense
    # words as well as correct answers -- our goal is to generate a list
    # of possible hits rather than to get the plural/singular form "right".

    @staticmethod
    def guess_singulars(s):
        """I don't really know French, but I'm going to guess it's
        like English and Spanish with regard to plurals and try some basic
        rules here.
        """
        if len(s) < 3:
            return []
        ret = []
        if s[-1] == 's':
            ret.append(s[0:-1])  # try chopping off the s
            if s[-2] == 'e':
                ret.append(s[0:-2])  # try chopping off 'es'
        return ret

    @staticmethod
    def guess_plurals(s):
        return [s+'s', s+'es']

    IGNORE = ["et", "avec", "de", "des", "d'", "pour", "froid", "froide", "froids", "froides",
              "chaud", "chaude", "chauds", "chaudes", "finement", "mince", "minces",
              "approximativement", "grosso modo", "vulgairement"]

    NUMBERS: Mapping[float, Collection[str]] = {
    }
