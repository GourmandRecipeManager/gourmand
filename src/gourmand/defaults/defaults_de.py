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

# Language: Deutsch (German)
# Translator:
# Last-updated: 2005-01-15 (07/18/05)

from typing import Any, Collection, Mapping

from .abstractLang import AbstractLanguage


class Language(AbstractLanguage):

    CREDITS = ""

    # The next line can be used to determine some things about how to handle this language
    LANG_PROPERTIES = {'hasAccents': True,
                       'capitalisedNouns': True, 'useFractions': False}

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

    fields = {'cuisine': ['deutsch', 'amerikanisch', 'italienisch', 'französisch',
                          'mexikanisch', 'asiatisch', 'indisch', 'griechisch', 'vegetarisch'],

              'rating': ['5 - ausgezeichnet', '4 - lecker',
                         '3 - OK', '2 - mittelmäßig', '1 - vergiss es!',
                         '(nicht geprüft)'],

              'source': [],

              'category': [
        'Nachspeise', 'Vorspeise', 'Hauptgericht',
        'Beilage', 'Salat', 'Suppe', 'Frühstück',
        'Picknick', 'Andere', 'Plan'],
    }

    # In English, there are a heck of a lot of synonyms. This is a list
    # for those synonyms.  [u"preferred word","alternate word","alternate word"]
    # If there are none of these that you can think of in your language, just
    # set this to:
    # SYNONYMS=[]

    # note from translator: some terms are not standard but used in common langugage, some are used in a fautive manner,
    # I decided to put them in different sections so it is still clear what is a synonym and what should not be a synonym.
    SYNONYMS = [
        # the first item of each list is the default
        ["Cocktailtomaten", "Tomaten, cherry"],
        ["Alfaalfa", "Alfapha", "Luzerne"],
        ["Porree", "Lauch"],
        ["Frühlingszwiebel", "Lauch-Zwiebeln"],
        ["Zuckermelone", "Gartenmelone"],
        ["Bleichsellerie", "Stangensellerie", "Straudensellerie"],
        ["Hammelfleisch", "Hammel"],
        ["Kalbfleisch", "Kalb"],
        ["Truthahn", "Puter", "Pute"],
        ["Rindfleisch", "Rind"],
        ["Rotbusch", "Rooibos", "Rooibosch"],
        ["Seelachs", "Köhler"],
        ["Anschovis", "Anchovis", "Sardelle"],
        ["Kabeljau", "Dorsch"],
        ["Nutella", "Nusspli"],
        ["Tomatenmark", "Tomatenkonzentrat"],
        ["Weizenmehl", "Mehl, weiß"],
        ["Soja-Milch", "Sojamilch", "Soya-Milch", "Soja Milch"],
        ["Soja-Sauce", "sauce soja", "sauce soya",
            "Soya-Sauce", "Sojasoße", "Sojasosse"],
        ["Soja", "Soya"],
        ["Sojabohnen", "Soyabohnen"],
        ["Püree", "Kartoffelpüree"],
        ["Müsli", "Muesli"],
        ["Nudeln", "Pasta"],
        ["Chile", "Chili", "Chilli"],
        ["Zucchini", "Zuchini", "Courgette"],
        ["Tafeltrauben", "Trauben, weiß", "Trauben, grün"],
        ["Garam Masala", "Masala", "Massala", "Garam Massala"],
        ["Gemüsebouillon", "Gemüsebrühe"],
        ["Hühnerbouillon", "Hühnerbrühe"],
        ["Muskat", "Muskatnuss", "Muscat", "Muscatnuss"],
        ["Sesammus", "Tahin"],
        ["Brokkoli", "Broccoli"],
        ["Kräuter", "gemischte Kräuter"],
        ["Langkornreis", "Reis"],
        ["Eierschwammerl", "Pfifferlinge"],
        ["Herrenpilze", "Steinpilze"],
        ["Paradeiser", "Tomaten"],

        # Irregular plurals
        ["Äpfel", "Apfel"],
        ["Pfirsiche", "Pfirsich"],
        ["Nüsse", "Nuss"],
        ["Eier", "Ei"]

        # non-standard usage

        # fautive/discouraged usages
    ]

    # A DICTIONARY CONTAINING INGREDIENT KEYS AND NDBNO for the USDA
    # nutritional database. For these items, we will have nutritional
    # information by default.

    NUTRITIONAL_INFO: Mapping[str, Any] = {}

    # a dictionary for ambiguous words.
    # key=ambiguous word, value=list of possible non-ambiguous terms
    #
    # Translators: if you have a word that has more than one food meaning
    # in your language, you can add an entry as follow

    # AMBIGUOUS = {
    #              'word':['meaning1','meaning2','meaning3'],
    #             }

    AMBIGUOUS = {
        'Sellerie': ['Sellerie', 'Staudensellerie'],
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
    # u"knows" about foods that they enter.

    # I generated the below list using the wikipedia entry on foods as my
    # starting point. You may want to do something similar for your
    # locale.  Also, if the syntax of the below is too complicated, you
    # can send me a list of category headings and ingredients for your
    # locale and I'll do the necessary formatting <Thomas_Hinkle@alumni.brown.edu>

    INGREDIENT_DATA = [  # G e m ü s e
        # alfalfa sprouts
        ("Alfaalfa", "Alfalfa", "Gemüse"),
        # anise
        ("Anis", "Anis", "Gemüse"),
        # artichoke
        ("Artischocke", "Artischocke", "Gemüse"),
        # rocket
        ("Ölranke", "Ölranke", "Gemüse"),
        # asparagus (white)
        ("Spargel", "Spargel", "Gemüse"),
        # asparagus - white
        ("weißer Spargel", "Spargel, weißer", "Gemüse"),
        # asparagus - green
        ("grüner Spargel", "Spargel, grüner", "Gemüse"),
        # aubergine
        ("Aubergine", "Aubergine", "Gemüse"),
        # avocado
        ("Avocado", "Avocado", "Gemüse"),
        # broccoli
        ("Brokkoli", "Brokkoli", "Gemüse"),
        # spinach
        ("Spinat", "Spinat", "Gemüse"),
        # brussels sprouts
        ("Rosenkohl", "Kohl, Rosenkohl", "Gemüse"),
        # cabbage
        ("Kohl", "Kohl", "Gemüse"),
        # white cabbage
        ("Weißkohl", "Kohl, Weißkohl", "Gemüse"),
        # red cabbage
        ("Rotkohl", "Kohl, Rotkohl", "Gemüse"),
        # cauliflower
        ("Blumenkohl", "Kohl, Blumenkohl", "Gemüse"),
        # china cabbage
        ("Chinakohl", "Kohl, Chinakohl", "Gemüse"),
        # kohlrabi
        ("Kohlrabi", "Kohl, Kohlrabi", "Gemüse"),
        ("Grünkohl", "Kohl, Grünkohl", "Gemüse"),                            # kale

        ("Bleichsellerie", "Bleichsellerie",
         "Gemüse"),                      # celery
        # lemon grass
        ("Zitronengras", "Zitronengras", "Gemüse"),
        ("Mais", "Mais", "Gemüse"),                                          # corn

        # button mushrooms
        ("Champignons", "Champignons", "Gemüse"),
        # large mushrooms
        ("Pilze", "Pilze", "Gemüse"),
        # mushrooms
        ("Steinpilz", "Steinpilze", "Gemüse"),
        # other woodland fungus
        ("Pfifferlinge", "Pfifferlinge", "Gemüse"),

        # mustard greens
        ("Senfkeimlinge", "Senfkeimlinge", "Gemüse"),
        # nettles
        ("Brennessel", "Brennessel", "Gemüse"),
        ("Okra", "Okra", "Gemüse"),                                          # okra
        ("Schnittlauch", "Schnittlauch", "Gemüse"),                          # chives

        ("Zwiebeln", "Zwiebeln", "Gemüse"),                                  # onion
        # shallot
        ("Schalotte", "Schalotte", "Gemüse"),
        # spring onion, scallion
        ("Frühlingszwiebel", "Frühlingszwiebel", "Gemüse"),
        # red (spanish) onion
        ("rote Zwiebeln, rot", "Zwiebeln, rote", "Gemüse"),
        ("weiße Zwiebeln", "Zwiebeln, weiße",
         "Gemüse"),                     # white onion
        ("gelbe Zwiebeln", "Zwiebeln, gelbe",
         "Gemüse"),                     # yellow onion
        ("Metzgerzwiebeln", "Zwiebeln, Metzger-",
         "Gemüse"),                 # large onion (salad)
        # standard cooking onion
        ("Speisezwiebeln", "Zwiebeln, Speise-", "Gemüse"),
        ("Knoblauch", "Knoblauch", "Gemüse"),                                # garlic
        ("Porree", "Porree", "Gemüse"),                                      # leek

        # pepper
        ("Paprika", "Paprika", "Gemüse"),
        # red bell pepper
        ("rote Paprika", "Paprika, rote", "Gemüse"),
        ("grüne Paprika", "Paprika, grüne", "Gemüse"),                       #
        ("gelbe Paprika", "Paprika, gelbe", "Gemüse"),                       #
        # chilli pepper
        ("Chile", "Chile", "Gemüse"),
        # jalapeño pepper
        ("Jalapeño-Chile", "Chile, Jalapeño", "Gemüse"),
        # habanero pepper
        ("Habanero-Chile", "Chile, Habanero", "Gemüse"),

        ("Radieschen", "Radieschen", "Gemüse"),                              # radish
        # beetroot
        ("Rote Beet", "Rote Beet", "Gemüse"),
        # carrot
        ("Möhren", "Möhren", "Gemüse"),
        # horse radish
        ("Rettich", "Rettich", "Gemüse"),
        # japanese horseraddish
        ("Wasabi", "Wasabi", "Gemüse"),
        # celeriac
        ("Sellerie", "Sellerie", "Gemüse"),
        # parsnip
        ("Pastinake", "Pastinake", "Gemüse"),
        # turnip
        ("Kohlrübe", "Kohlrübe", "Gemüse"),
        # fennel
        ("Fenchel", "Fenchel", "Gemüse"),

        # lettuce
        ("Kopfsalat", "Kopfsalat", "Gemüse"),
        ("Rucolasalat", "Rucolasalat", "Gemüse"),                            # rucola
        # open lettuce
        ("Friseesalat", "Friseesalat", "Gemüse"),
        # lettuce
        ("Feldsalat", "Feldesalat", "Gemüse"),

        # broad beans
        ("Saubohnen", "Saubohnen", "Gemüse"),
        # small green beans
        ("Bobby Bohnen", "Bobby Bohnen", "Gemüse"),
        # haricot beans
        ("Haricots", "Haricots", "Gemüse"),
        # runner beans
        ("Carbasc", "Carbasc", "Gemüse"),
        ("Erbsen", "Erbsen", "Gemüse"),                                      # peas
        # mange tous
        ("Zuckererbsen", "Zuckererbsen", "Gemüse"),

        # zucchini
        ("Zucchini", "Zucchini", "Gemüse"),
        ("Gurke (Salat-)", "Gurke (Salat-)",
         "Gemüse"),                      # cucumber

        # pumpkin
        ("Kürbis", "Kürbis", "Gemüse"),

        # cocktail (cherry) tomato
        ("Cocktailtomaten", "Tomaten, Cocktail-", "Gemüse"),
        # cherry tomato
        ("Tomaten", "Tomaten", "Gemüse"),
        # tomato on stems
        ("Rispentomaten", "Tomaten, Rispen-", "Gemüse"),

        ("Kartoffel", "Kartoffel", "Gemüse"),                                # potato
        # standard cooking potatoes
        ("Speisekartoffeln", "Kartoffeln, Speise-", "Gemüse"),
        # sweet potato
        ("Süßkartoffel", "Süßkartoffel", "Gemüse"),

        ("Jamswurzel", "Jamswurzel", "Gemüse"),                              # yam
        # water chestnut
        ("Wasserkastanie", "Wasserkastanie", "Gemüse"),
        # watercress
        ("Brunnenkresse", "Brunnenkresse", "Gemüse"),

        ("Oliven", "Oliven", "Gemüse"),                                      #
        ("grüne Oliven", "Oliven, grüne", "Gemüse"),                         #
        ("schwarze Oliven", "Oliven, schwarze", "Gemüse"),                   #

        # H ü l s e n f r u c h t e
        # green beans
        ("grüne Bohnen", "Bohnen, grüne", "Gemüse"),
        ("weiße Bohnen", "Bohnen, weiße",
         "Hülsenfrüchte"),                  # green beans
        ("Azuki Bohnen", "Bohnen, Azuki",
         "Hülsenfrüchte"),                  # azuki beans
        ("schwarze Bohnen", "Bohnen, schwarze",
         "Hülsenfrüchte"),            # black beans
        # borlotti beans (not sure)
        ("Borlottibohnen", "Bohnen, Borlotti-", "Hülsenfrüchte"),
        # chickpeas, garbanzos, or ceci beans
        ("Kichererbsen", "Kichererbsen", "Hülsenfrüchte"),
        ("Kidneybohnen", "Bohnen, Kidney-",
         "Hülsenfrüchte"),                # kidney beans
        ("Teller-Linsen", "Linsen, Teller-",
         "Hülsenfrüchte"),               # standard lentils
        # red lentils
        ("rote Linsen", "Linsen, rote", "Hülsenfrüchte"),
        # green lentils
        ("grüne Linsen", "Linsen, grüne", "Hülsenfrüchte"),
        ("schwarze Linsen", "Linsen, schwarze",
         "Hülsenfrüchte"),            # black lentils
        # lima bean or butter bean
        ("Gartenbohnen", "Gartenbohnen", "Gemüse"),
        # mung beans
        ("Mungbohnen", "Bohnen, Mung-", "Hülsenfrüchte"),
        ("Sojabohnen", "Bohnen, Soja-", "Hülsenfrüchte"),                    # soybeans
        # green dried peas
        ("grüne Erbsen", "Erbsen, grüne", "Hülsenfrüchte"),
        # yellow dried peas
        ("gelbe Erbsen", "Erbsen, gelbe", "Hülsenfrüchte"),
        ("Schälerbsen", "Erbsen, Schälerbsen", "Hülsenfrüchte"),             #

        # F r u c h t e
        # general fruit
        ("Obst", "Obst", "Obst"),
        # apple
        ("Äpfel", "Äpfel", "Obst"),
        ("rote Äpfel", "Äpfel, rote", "Obst"),                               #
        ("goldene Äpfel", "Äpfel, goldene", "Obst"),                         #
        ("Granny Smith Äpfel", "Äpfel, Granny Smith", "Obst"),               #
        ("Fuji Äpfel", "Äpfel, Fuji-", "Obst"),                              #
        # green apple
        ("grüne Äpfel", "Äpfel, grüne", "Obst"),
        # pomegranate
        ("Granatäpfel", "Granatäpfel", "Obst"),
        # quince
        ("Quitte", "Quitte", "Obst"),
        # rose hip
        ("Hagebutten", "Hagebutten", "Obst"),
        # apricot
        ("Aprikosen", "Aprikosen", "Obst"),
        ("Birnen", "Birnen", "Obst"),                                        # pear
        ("Conference Birnen", "Birnen, Conference",
         "Obst"),                 # pear, large conference
        # pear, standard william
        ("William Birnen", "Birnen, William", "Obst"),
        # cherry
        ("Kirschen", "Kirschen", "Obst"),
        ("Pflaumen", "Pflaumen", "Obst"),                                    # plum
        ("Pfirsiche", "Pfirsiche", "Obst"),                                  # peach
        # nectarine
        ("Nektarinen", "Nektarinen", "Obst"),
        ("Brombeeren", "Beeren, Brombeeren",
         "Obst"),                        # blackberry
        # raspberry
        ("Himbeeren", "Beeren, Himbeeren", "Obst"),
        # raspberry
        ("Erdbeeren", "Beeren, Erdbeeren", "Obst"),
        ("Heidelbeeren", "Beeren, Heidelbeeren",
         "Obst"),                    # bilberry
        ("Blaubeeren", "Beeren, Blaubeeren",
         "Obst"),                        # blueberry
        ("Preiselbeeren", "Beeren, Preiselbeeren",
         "Obst"),                  # cranberry
        ("Johannisbeeren", "Beeren, Johannisbeeren",
         "Obst"),                # red currant
        ("schwarze Johannisbeeren",
         "Beeren, schwarze Johannisbeeren", "Obst"),  # black currant
        ("Holunderbeeren", "Beeren, Holunderbeeren",
         "Obst"),                # elderberry
        # gooseberry
        ("Stachelbeeren", "Stachelbeeren", "Obst"),
        # kiwi fruit
        ("Kiwi", "Kiwi", "Obst"),
        # pawpaw
        ("Papaya", "Papaya", "Obst"),
        # cantaloupe
        ("Zuckermelonen", "Zucker-", "Obst"),
        # honeydew melon
        ("Honigmelonen", "Melonen, Honig-", "Obst"),
        # galia melon
        ("Galiamelonen", "Melonen, Galia-", "Obst"),
        # net melon
        ("Netzmelonen", "Melonen, Netz-", "Obst"),
        ("Wassermelonen", "Melonen, Wasser-",
         "Obst"),                       # watermelon
        ("Feigen", "Feigen", "Obst"),                                        # fig
        ("Weintrauben", "Weintrauben", "Obst"),                              # grape
        ("Tafeltrauben", "Weintrauben, Tafel",
         "Obst"),                      # green grapes
        ("blaue Weintrauben", "Weintrauben, blau",
         "Obst"),                  # black grapes
        ("Datteln", "Datteln", "Obst"),                                      # date
        # grapefruit
        ("Grapefruit", "Grapefruit", "Obst"),
        ("Limetten", "Limetten", "Obst"),                                    # lime
        # kumquat
        ("Kumquat", "Kumquat", "Obst"),
        ("Zitronen", "Zitronen", "Obst"),                                    # lemon
        # mandarin
        ("Mandarinen", "Mandarinen", "Obst"),
        # clementine
        ("Klementinen", "Klementinen", "Obst"),
        # tangerine
        ("Tangerinen", "Tangerinen", "Obst"),
        # orange
        ("Orangen", "Orangen", "Obst"),
        # ugli fruit
        ("Ugli", "Ugli", "Obst"),
        # guava
        ("Guave", "Guave", "Obst"),
        # lychee
        ("Litschi", "Litschi", "Obst"),
        # passion fruit
        ("Passionsfrucht", "Passionsfrucht", "Obst"),
        # banana
        ("Banane", "Banane", "Obst"),
        # plantain
        ("Wegerich", "Wegerich", "Obst"),
        # coconut
        ("Kokosnuss", "Kokosnuss", "Obst"),
        # durian
        ("Durion", "Durion", "Obst"),
        # mango
        ("Mango", "Mangue", "Obst"),
        # papaya
        ("Papaya", "Papaya", "Obst"),
        # pineapple
        ("Ananas", "Ananas", "Obst"),
        # tamarind
        ("Tamarinde", "Tamarinde", "Obst"),
        # rhubarb
        ("Rhabarber", "Rhabarber", "Obst"),

        # M e e r e s f r ü c h t e
        ("Anchovis", "Anchovis", "Meeresfrüchte"),                           # anchovy
        ("Barsch", "Barsch", "Meeresfrüchte"),                               # bass
        ("Kugelfisch", "Kugelfisch", "Meeresfrüchte"),                       # blowfish
        # catfish
        ("Wels", "Wels", "Meeresfrüchte"),
        ("Dorsch", "Dorsch", "Meeresfrüchte"),                               # cod
        ("Aal", "Aal", "Meeresfrüchte"),                                     # eel
        # flounder
        ("Flunder", "Flunder", "Meeresfrüchte"),
        ("Schellfisch", "Schellfisch", "Meeresfrüchte"),                     # haddock
        # smoked haddock
        ("Haddock", "Haddock", "Meeresfrüchte"),
        ("Heilbutt", "Heilbutt", "Meeresfrüchte"),                           # halibut
        ("Zander", "Zander", "Meeresfrüchte"),                               # pike
        ("Seelachs", "Seelachs", "Meeresfrüchte"),                           # pollock
        # sardine
        ("Sardine", "Sardine", "Meeresfrüchte"),
        ("Sprotte", "Sprotte", "Meeresfrüchte"),                             # sprat
        ("Lachs", "Lachs", "Meeresfrüchte"),                                 # salmon
        ("Sägebarsch", "Sägebarsch", "Meeresfrüchte"),                       # sea bass
        ("Hai", "Hai", "Meeresfrüchte"),                                     # shark
        ("Seezunge", "Seezunge", "Meeresfrüchte"),                           # sole
        # sturgeon
        ("Stör", "Stör", "Meeresfrüchte"),
        ("Schwertfisch", "Schwertfisch",
         "Meeresfrüchte"),                   # swordfish
        ("Forelle", "Forelle", "Meeresfrüchte"),                             # trout
        ("Thunfisch", "Thunfisch", "Meeresfrüchte"),                         # tuna
        # whitefish
        ("Weißfisch", "Weißfisch", "Meeresfrüchte"),
        ("Wittling", "Wittling", "Meeresfrüchte"),                           # whiting
        # roe of fish
        ("Rogen", "Rogen", "Meeresfrüchte"),
        ("Kaviar", "Kaviar", "Meeresfrüchte"),                               # caviar
        ("Krebs", "Krebs", "Meeresfrüchte"),                                 # crab
        # lobster
        ("Hummer", "Hummer", "Meeresfrüchte"),
        ("Garnele", "Garnele", "Meeresfrüchte"),                             # prawns
        ("Krabbe", "Krabbe", "Meeresfrüchte"),                               # shrimp
        ("Klaffmuschel", "Klaffmuschel", "Meeresfrüchte"),                   # clam
        ("Muschel", "Muschel", "Meeresfrüchte"),                             # mussel
        ("Tintenfisch", "Tintenfisch", "Meeresfrüchte"),                     # octopus
        ("Auster", "Auster", "Meeresfrüchte"),                               # oyster
        ("Schnecke", "Schnecke", "Meeresfrüchte"),                           # snail
        ("Kalmar", "Kalmar", "Meeresfrüchte"),                               # squid
        ("Kammuschel", "Kammuschel", "Meeresfrüchte"),                       # scallop

        # F l e i s c h
        # chopped bacon
        ("Speck", "Speck", "Fleisch"),
        # bacon
        ("Bacon", "Bacon", "Fleisch"),
        ("Schinken", "Schinken", "Fleisch"),                                 # ham
        # mutton
        ("Hammel", "Hammel", "Fleisch"),
        ("Lamm", "Lamm", "Fleisch"),                                         # lamb
        ("Kalb", "Kalb", "Fleisch"),                                         # veal
        # steak
        ("Steak", "Steak", "Fleisch"),
        # hamburger
        ("Hamburger", "Hamburger", "Fleisch"),
        # roast beef
        ("Roastbeef", "Roastbeef", "Fleisch"),
        # chicken
        ("Hähnchen", "Hähnchen", "Fleisch"),
        # turkey
        ("Pute", "Pute", "Fleisch"),
        ("Ente", "Ente", "Fleisch"),                                         # duck
        # goose
        ("Gans", "Gans", "Fleisch"),
        ("Rind", "Rind", "Fleisch"),                                         # beef
        # mince beef
        ("Hackfleisch", "Hackfleisch", "Fleisch"),
        ("Hase", "Hase", "Fleisch"),                                         # hare
        ("Kaninchen", "Kaninchen", "Fleisch"),                               # rabbit
        ("Hirsch", "Hirsch", "Fleisch"),                                     # deer
        # chicken breast
        ("Hühnerbrust", "Hühnerbrust", "Fleisch"),
        ("Schweinefleisch", "Schweinefleisch", "Fleisch"),                   # pork
        # chorizo
        ("Chorizo", "Chorizo", "Fleisch"),
        # salami
        ("Salami", "Salami", "Fleisch"),
        # sausage
        ("Wurst", "Wurst", "Fleisch"),
        # sausage
        ("Bratwurst", "Bratwurst", "Fleisch"),
        # sausage
        ("Weißwurst", "Weißwurst", "Fleisch"),
        # sausage
        ("Currywurst", "Currywurst", "Fleisch"),

        # L e b e n s m i t t e l
        # all purpose flour
        ("Weizenmehl", "Mehl, Weizen-", "Lebensmittel"),
        ("Vollkorn Weizenmehl", "Mehl, Vollkorn Weizen-",
         "Lebensmittel"),   # wholemeal flour
        ("Hirsemehl", "Mehl, Hirse-", "Lebensmittel"),                       # flour
        ("Roggenmischung", "Mehl, Roggenmischung",
         "Lebensmittel"),          # rye flour
        # baking powder
        ("Backpulver", "Backpulver", "Lebensmittel"),
        # baking soda
        ("Natron", "Natron", "Lebensmittel"),
        # chocolate
        ("Schokolade", "Schokolade", "Lebensmittel"),
        # chocolate chips
        ("Schokotröpfen", "Schokotröpfen", "Lebensmittel"),
        ("Zucker", "Zucker", "Lebensmittel"),                                # suger
        # artificial sweetner
        ("Süßstoff", "Süßstoff", "Lebensmittel"),
        ("brauner Zucker", " Zucker, braun",
         "Lebensmittel"),                # brown suger
        ("weißer Zucker", "Zucker, weiß",
         "Lebensmittel"),                   # white sugar
        ("Raffinade", "Zucker, Raffinade",
         "Lebensmittel"),                  # castor sugar
        ("Salz", "Salz", "Lebensmittel"),                                    # salt
        # sea salt
        ("Meersalz", "Salz, Meer-", "Lebensmittel"),
        # currents
        ("Rosinen", "Rosinen", "Lebensmittel"),
        ("Sultanienen", "Sultanienen", "Lebensmittel"),                      # sultanas
        ("geraspelte Kokosnuss", "Kokosnuss, geraspelt",
         "Lebensmittel"),    # (modifier?)
        # vanilla
        ("Vanille", "Vanille", "Lebensmittel"),
        # vanilla extract
        ("Vanilleessenz", "Vanilleessenz", "Lebensmittel"),
        ("Walnusskerne", "Walnusskerne", "Lebensmittel"),                    # walnut
        # cashew nut
        ("Cashewnüsse", "Cashewnüsse", "Lebensmittel"),
        # almonds
        ("Mandeln", "Mandeln", "Lebensmittel"),
        ("Erdnüsse", "Erdnüsse", "Lebensmittel"),                            # peanut
        ("Kartoffelpüree", "Kartoffelpüree",
         "Lebensmittel"),                # potato mash
        # potato dumplings
        ("Klöße", "Klöße", "Lebensmittel"),
        # yellow cornmeal
        ("Polenta", "Polenta", "Lebensmittel"),
        ("kernige Haferflocken", "Haferflocken, kernig",
         "Lebensmittel"),    # rolled oats
        ("zarte Haferflocken", "Haferflocken, zart",
         "Lebensmittel"),        # fine rolled oats
        # ketchup
        ("Ketchup", "Ketchup", "Lebensmittel"),
        # mayonnaise
        ("Mayonnaise", "Mayonnaise", "Lebensmittel"),
        # ryebread wafers
        ("Knäckebrot", "Knäckebrot", "Lebensmittel"),
        # canned tomatoes
        ("Dosentomaten", "Tomaten, Dosen-", "Lebensmittel"),
        # canned sweetcorn
        ("Dosenmais", "Mais, Dosen-", "Lebensmittel"),

        ("Sonnenblumenkerne", "Sonnenblumenkerne",
         "Lebensmittel"),          # sunflower seeds
        # sesame seeds
        ("Sesammus", "Sesammus", "Lebensmittel"),

        # lemon juice
        ("Zitronensaft", "Zitronensaft", "Lebensmittel"),
        ("Zitronenkonzentrat", "Zitronenkonzentrat",
         "Lebensmittel"),        # lemon concentrate
        ("Limettensaft", "Saft, Limetten-",
         "Lebensmittel"),                 # lime juice
        # whole orange juice
        ("Orangensaft", "Saft, Orangen", "Lebensmittel"),
        ("Orangennektar", "Saft, Orangennektar",
         "Lebensmittel"),            # orange juice

        # tomato sauce
        ("Tomatensuppe", "Tomatensuppe", "Lebensmittel"),
        ("Bouillon", "Bouillon", "Lebensmittel"),                            # broth
        ("Gemüsebouillon", "Bouillon, Gemüse-",
         "Lebensmittel"),             # vegetable broth
        ("Hühnerbouillon", "Bouillon, Hühner-",
         "Lebensmittel"),             # broth, chicken
        # hollandais sauce
        ("Hollandaise", "Hollandaise", "Lebensmittel"),

        ("gehackte Tomaten", "Tomaten, gehackt",
         "Lebensmittel"),            # chopped tomato
        ("geschälte Tomaten", "Tomaten, geschält",
         "Lebensmittel"),          # peeled tomato
        ("passierte Tomaten", "Tomaten, passiert",
         "Lebensmittel"),          # mashed tomato
        # pureed tomato
        ("Tomatenmark", "Tomatenmark", "Lebensmittel"),

        # biscuits
        ("Kekse", "Kekse", "Lebensmittel"),
        # muesli
        ("Müsli", "Müsli", "Lebensmittel"),
        # instant custard pudding
        ("Pudding", "Pudding", "Lebensmittel"),
        # corn starch
        ("Stärke", "Stärke", "Lebensmittel"),

        # R e i s   u n d   T e i g w a r e n
        ("Nudeln", "Nudeln", "Reis & Teigwaren"),                            # pasta
        # spaghetti
        ("Spaghetti", "Spagghetti", "Reis & Teigwaren"),
        # pasta tubes
        ("Penne", "Penne", "Reis & Teigwaren"),
        ("Canelonni", "Canelonni", "Reis & Teigwaren"),                      #
        # pasta twirls
        ("Fusilli", "Fusilli", "Reis & Teigwaren"),
        # pasta twirls
        ("Riccioli", "Riccioli", "Reis & Teigwaren"),
        # pasta sheets
        ("Lasagna", "Lasagna", "Reis & Teigwaren"),
        # vermicelli
        ("Vermicelli", "Vermicelli", "Reis & Teigwaren"),

        ("Teig", "Teig", "Reis & Teigwaren"),                                # dough
        # pastry dough
        ("Hefeteig", "Teig, Hefe-", "Reis & Teigwaren"),
        # pizza dough
        ("Pizzateig", "Teig, Pizza-", "Reis & Teigwaren"),

        ("Langkornreis", "Reis, Langkorn-",
         "Reis & Teigwaren"),             # rice longcorn
        ("Basmatireis", "Reis, Basmati-",
         "Reis & Teigwaren"),               # basmati rice
        # pudding rice
        ("Milchreis", "Reis, Milch-", "Reis & Teigwaren"),
        # whole rice
        ("Naturreis", "Reis, Natur-", "Reis & Teigwaren"),
        # wild (black) rice
        ("Wildreis", "Reis, Wild-", "Reis & Teigwaren"),
        ("Spitzenlangkornreis", "Reis, Spitzenlangkorn-",
         "Reis & Teigwaren"),  # rice longcorn cook

        # B r o t
        # bread, any
        ("Brot", "Brot, allgemeines", "Brot"),
        # white bread
        ("Weißbrot", "Brot, weiß", "Brot"),
        # sliced white toasting bread
        ("Toastbrot", "Brot, Toast-", "Brot"),
        # wholemeal bread
        ("Vollkornbrot", "Brot, Vollkorn-", "Brot"),
        ("Sonnenblumenkernbrot", "Brot, Sonnenblumenkern-",
         "Brot"),         # sunflower seed wholmeal
        # pupkin seed wholemeal
        ("Kürbiskernbrot", "Brot, Kürbiskern-", "Brot"),
        # sesame seed wholemeal
        ("Sesambrot", "Brot, Sesam-", "Brot"),
        # 3 corn wholemeal bread
        ("Dreikornbrot", "Brot, Dreikorn-", "Brot"),
        # Crusty wholemeal bread
        ("Krustenbrot", "Brot, Krusten-", "Brot"),
        # wholemeal bread
        ("Landbrot", "Brot, Land-", "Brot"),
        # turkish round bread
        ("Fladenbrot", "Brot, Fladen-", "Brot"),
        # pumpernickel bread
        ("Pumpernickel", "Pumpernickel", "Brot"),

        # K r ä u t e r   u n d   G e w ü r z e
        # mixed herbs
        ("Kräuter", "Kräuter, gemischt", "Gemüse"),
        # parsley
        ("Petersilie", "Petersilie", "Gemüse"),
        ("schwarze Pfeffer", "Pfeffer schwarz",
         "Kräuter u Gewürze"),        # black pepper
        ("Cayennepfeffer", "Pfeffer, Cayenne",
         "Kräuter u Gewürze"),         # cayenne
        ("Kräuter de Provence", "Kräuter de Provence",
         "Kräuter u Gewürze"),  # Herbs de Provence
        # Herbed salt
        ("Kräutersalz", "Kräutersalz", "Kräuter u Gewürze"),
        ("Lorbeerblatt", "Lorbeerblatt",
         "Kräuter u Gewürze"),               # Bay leaf
        ("Gewürznelken", "Gewürznelken", "Kräuter u Gewürze"),                #
        # (modifier?)
        ("Chilipulver", "Chilipulver", "Kräuter u Gewürze"),
        # curry powder
        ("Curry", "Curry", "Kräuter u Gewürze"),
        # curry paste
        ("Currypaste", "Currypaste", "Kräuter u Gewürze"),
        # hotter curry powder
        ("Madras Curry", "Curry, madras", "Kräuter u Gewürze"),
        ("Garam Masala", "Garam Masala", "Kräuter u Gewürze"),                #
        ("Zimtschote", "Zimt, Zimtschote",
         "Kräuter u Gewürze"),             # (modifier?)
        ("gemahlener Zimt", "Zimt, gemahlener",
         "Kräuter u Gewürze"),        # (modifier?)
        ("Korianderkerne", "Korianderkerne",
         "Kräuter u Gewürze"),           # (modifier?)
        ("gemahlener Koriander", "Koriander, gemahlener",
         "Kräuter u Gewürze"),  # (modifier?)
        # (modifier?)
        ("Cuminkerne", "Cuminkerne", "Kräuter u Gewürze"),
        ("gemahlener Cumin", "Cumin, gemahlener",
         "Kräuter u Gewürze"),      # (modifier?)
        # (modifier?)
        ("Senfkerne", "Senfkerne", "Kräuter u Gewürze"),
        # (modifier?)
        ("Senf", "Senf", "Kräuter u Gewürze"),
        # (modifier?)
        ("Dijon-Senf", "Senf, Dijon", "Kräuter u Gewürze"),
        ("Muskatnuss", "Muskatnuss", "Kräuter u Gewürze"),                   # nutmeg
        ("Paprika, gemahlen", "Paprika, gemahlen", "Kräuter u Gewürze"),      #
        ("Ingwerpulver", "Ingwer, Ingwerpulver",
         "Kräuter u Gewürze"),       # ground ginger
        # turmeric, curcuma
        ("Kurkuma", "Kurkuma", "Kräuter u Gewürze"),
        # turmeric, curcuma
        ("Majoran", "Majoran", "Kräuter u Gewürze"),
        ("Oregano", "Oregano", "Kräuter u Gewürze"),                         # oregano
        ("Basilikum, gerebelt", "Basilikum, gerebelt",
         "Kräuter u Gewürze"),  # basil, crushed
        ("frisches Basilikum", "Basilikum, frisches",
         "Kräuter u Gewürze"),  # fresh basil leaves
        ("frischer Koriander", "Koriander, frischer",
         "Kräuter u Gewürze"),  # fresh coriander leaves
        ("frisches Schnittlauch", "Schnittlauch, frisches",
         "Kräuter u Gewürze"),  # fresh chives
        ("frischer Ingwer", "Ingwer, frischer",
         "Kräuter u Gewürze"),        # fresh ginger
        # ginger paste
        ("Ingwerpaste", "Ingwerpaste", "Kräuter u Gewürze"),

        # M a r m e l a d e
        ("Pflaumenmarmelade", "Marmelade, Pflaumen-",
         "Konfitüren"),         # plum jam
        ("Aprikosenmarmelade", "Marmelade, Aprikosen-",
         "Konfitüren"),       # apricot jam
        ("Orangenmamalade", "Marmalade, Orangen-",
         "Konfitüren"),            # orange jam
        # jam - general
        ("Marmelade", "Marmelade", "Konfitüren"),
        ("Erdbeermarmelade", "Marmelade, Erdbeer-",
         "Konfitüren"),           # strawberry jam
        ("Himbeermarmelade", "Marmelade, Himbeer-",
         "Konfitüren"),           # raspberry jam
        # peanut butter
        ("Erdnussbutter", "Erdnussbutter", "Konfitüren"),
        # nussply
        ("Nutella", "Nutella", "Konfitüren"),
        # tahini - sesame spread
        ("Sesammus", "Sesammus", "Konfitüren"),
        ("Honig", "Honig", "Konfitüren"),                                    # honey

        # I n t e r n a t i o n a l
        # tartex spread
        ("Tartex", "Tartex", "International"),
        # coconut milk
        ("Kokosmilch", "Kokusmilch", "International"),
        # coconut cream
        ("Kokoscreme", "Kokuscreme", "International"),
        ("grüne Currypaste", "Currypaste, grüne",
         "International"),          # green curry paste
        ("rote Currypaste", "Currypaste, rote",
         "International"),            # red curry paste
        # rice vinegar
        ("Reisessig", "Essig, Reis-", "International"),
        ("Salsa", "Salsa", "International"),                                 # salsam
        # sesame seeds
        ("Sesamkerne", "Sesamkerne", "International"),
        # soy sauce
        ("Soja-Sauce", "Soja-Sauce", "International"),
        # soya cream
        ("Sojacreme", "Sojacreme", "International"),
        ("Bulgur", "Bulgur", "International"),                               # bulgar
        # couscous
        ("Couscous", "Couscous", "International"),
        # felafel
        ("Falafel", "Falafel", "International"),
        ("Tofu", "Tofu", "International"),                                   # tofu
        # bok choy
        ("Pak-choï", "Pak-choï", "Gemüse"),

        # M i l c h p r o d u k t e
        # milk, unspecified
        ("Milch", "Milch", "Milchprodukte"),
        # cheese, any
        ("Käse", "Käse, allgemeiner", "Milchprodukte"),
        ("Butter", "Butter", "Milchprodukte"),                               # butter
        ("Margarine", "Margarine", "Milchprodukte"),                          #
        ("Eier", "Eier", "Milchprodukte"),                                   # egg
        ("frische Milch", "Milch, frische", "Milchprodukte"),                # milk
        ("fettarme Milch", "Milch, fettarme",
         "Milchprodukte"),              # skimmed milk
        # long-life milk
        ("H-Milch", "Milch, H-Milch", "Milchprodukte"),
        ("Sojamilch", "Milch, Sojamilch",
         "Milchprodukte"),                  # soya milk
        ("Buttermilch", "Milch, Buttermilch",
         "Milchprodukte"),              # buttermilk
        # sour cream
        ("Sauerrahm", "Sauerrahm", "Milchprodukte"),
        ("Sahne", "Sahne", "Milchprodukte"),                                 #
        ("Sahne 10% Fett", "Sahne, 10% Fett", "Milchprodukte"),              #
        ("Sahne 15% Fett", "Sahne, 15% Fett", "Milchprodukte"),              #
        ("Sahne 35% Fett", "Sahne, 35% Fett", "Milchprodukte"),              #
        ("Joghurt", "Joghurt", "Milchprodukte"),                             # yogurt
        ("Quark", "Quark", "Milchprodukte"),                                 #
        ("Speisequark Magerstufe", "Quark, Speise- Magerstufe", "Milchprodukte"),  #
        ("Kräuterquark", "Quark, Kräuter", "Milchprodukte"),                 #
        # cheddar cheese
        ("Cheddar-Käse", "Käse, Cheddar", "Milchprodukte"),
        # general hard cheese
        ("Hartkäse", "Käse, Hart-", "Milchprodukte"),
        # cottage cheese
        ("Hüttenkäse", "Käse, Hüttenkäse", "Milchprodukte"),
        ("Schnittkäse", "Käse, Schnittkäse",
         "Milchprodukte"),               # cottage cheese
        # feta cheese
        ("Fetakäse", "Käse, Fetakäse", "Milchprodukte"),
        # fresh cheese white goat
        ("Ziegenkäse", "Käse, Ziegenkäse", "Milchprodukte"),
        # sheeps cheese
        ("Schaffskäse", "Schaffskäse", "Milchprodukte"),
        ("Emmentaler", "Käse, Emmentalerkäse",
         "Milchprodukte"),             # emmental
        # mozzarella cheese
        ("Mozzarella", "Käse, Mozzarella", "Milchprodukte"),
        # parmesan cheese
        ("Parmesan", "Käse, Parmesan", "Milchprodukte"),
        # provolone cheese
        ("Provolone", "Käse, Provolone", "Milchprodukte"),
        # ricotta cheese
        ("Ricotta", "Käse, Ricotta", "Milchprodukte"),
        # cheese Gouda
        ("Gouda", "Käse, Gouda", "Milchprodukte"),
        # cheese Brie
        ("Brie", "Käse, Brie", "Milchprodukte"),
        # spreading cheese
        ("Streichkäse", "Käse, Steich", "Milchprodukte"),
        ("Philladelphia", "Käse, Philladelphia",
         "Milchprodukte"),           # philladelphia cheese

        # h e i ß e   G e t r ä n k e
        ("schwarzer Tee", "Tee, schwarzer",
         "Getränke, heiß"),               # black tea
        ("gemahlener Kaffee, ", "Kaffee, gemahlener",
         "Getränke, heiß"),     # ground coffee
        ("gemahler entkoffeinierter Kaffee", "Kaffee, gemahlener entkoffeinierter",
         "Getränke, heiß"),  # decaff ground coffee
        # coffee filters
        ("Kaffeefilter", "Kaffeefilter", "Getränke, heiß"),
        # drinking chocolate
        ("Kakao", "Kakao", "Getränke, heiß"),
        # caro coffee
        ("Carokaffee", "Carokaffee", "Getränke, heiß"),
        ("Früchtetee, ", "Tee, Früchtetee",
         "Getränke, heiß"),               # fruit tea
        ("Pfefferminztee", "Tee, Pfefferminztee",
         "Getränke, heiß"),         # peppermint tea
        ("Hagebuttentee", "Tee, Hagebuttentee",
         "Getränke, heiß"),           # rosehip tea
        ("Kamillentee", "Tee, Kamillentee",
         "Getränke, heiß"),               # camomile tea
        ("Fencheltee", "Tee, Fencheltee",
         "Getränke, heiß"),                 # fenchel tea
        ("Rotbuschtee", "Tee, Rotbuschtee",
         "Getränke, heiß"),               # roobusch tea
        ("Kräutertee", "Tee, Kräutertee",
         "Getränke, heiß"),                 # herb tea
        # green tea
        ("grüner Tee", "Tee, grüner", "Getränke, heiß"),
        # yogi (ayurvedic) tea
        ("Yogitee", "Tee, Yogitee", "Getränke, heiß"),

        # F l u ß i g k e i t e n
        # table vinegar
        ("Tafelessig", "Essig, Tafel-", "Flüssigkeiten"),
        # table vinegar
        ("Obstessig", "Essig, Obst-", "Flüssigkeiten"),
        ("Balsamico-Essig", "Essig, Balsamico-",
         "Flüssigkeiten"),           # balsamic vinegar
        ("Sonnenblumenöl", "Öl, Sonnenblumenöl",
         "Flüssigkeiten"),           # sunflower oil
        # olive oil
        ("Olivenöl", "Öl, Olivenöl", "Flüssigkeiten"),
        # sesame oil
        ("Sesamöl", "Öl, Sesamöl", "Flüssigkeiten"),
        # vegetable oil
        ("Pflanzenöl", "Öl, Pflanzenöl", "Flüssigkeiten"),
        # soya oil
        ("Sojaöl", "Öl, Sojaöl", "Flüssigkeiten"),
        # white wine
        ("Weißwein", "Wein, weiß", "Flüssigkeiten"),
        # red wine
        ("Rotwein", "Wein, rot", "Flüssigkeiten"),

        # t h i n g   y o u   s h o u l d   h a v e   a t   h o m e
        ("Wasser", "Wasser", "Flüssigkeiten")                                # water
    ]

    # THESE ARE STANDARD UNIT CONVERSIONS. You can simply translate unit names where
    # you know them. Eliminate entries that are untranslatable or don't exist in your
    # locale. And please add any additional units that you know of.
    # Each unit is of the following format:
    # (u"unit1",u"unit2"):conversion_factor, where unit1 contains conversion_factor X unit2
    # For example: 1 cup has 16 tablespoons.
    CONVERTER_TABLE = {
        ("Tasse", "EL"): 16,
        ("EL", "TL"): 3,
        ("pt.", "Tasse"): 2,
        ("qt.", "Tasse"): 4,
        ("l", "ml"): 1000,
        ("l", "cl"): 100,
        ("l", "dl"): 10,
        ("oz.", "g"): 28.35,
        ("kg", "g"): 1000,
        ("g", "mg"): 1000,
        ("TL", "Tröpchen"): 76,
        ("Dose, mittel", "g"): 400,
        ("Dose, groß",   "g"): 800,
        ("Dose, klein",  "g"): 200,
        ("lb.", "oz."): 16,
        ("l", "qt."): 1.057
    }

    # DENSITIES of common foods. This allows us to convert between mass and volume.
    # Translators: You may be best off translating the food names below, since lists
    # of food densities can be hard to come by!
    DENSITY_TABLE = {
        "Wasser": 1,               # water
        "Traubensaft": 1.03,       # juice, grape
        "Bouillon, gemüse": 1,     # vegetable broth
        "Bouillon, hühner": 1,     # broth, chicken
        "Milch": 1.029,            # milk
        "Milch entier": 1.029,     # milk, whole
        "Milch, fettarm": 1.033,   # milk, skim
        "Milch 2%": 1.031,         # milk, 2%
        "Milch 1%": 1.03,          # milk, 1%
        "Kokosmilch": 0.875,       # coconut milk
        "Buttermilch": 1.03,       # buttermilk
        "Sahne riche": 0.994,      # heavy cream
        "Sahne légère": 1.012,     # light cream
        "Sahne 11,5%": 1.025,      # half-and-half
        "Honig": 1.420,            # honey
        "Zucker": 1.550,           # sugar, white
        "Salz": 2.165,             # salt
        "Butter": 0.911,           # butter
        "Pflanzen Öl": 0.88,       # oil, vegetable
        "Oliven Öl": 0.88,         # oil, olive
        "Sonnenblumen Öl": 0.88,   # oil, corn
        "Sesam Öl": 0.88,          # oil, sesame
        "Mehl": 0.6,               # flour, all purpose
        "Vollkornmehl": 0.6,       # flour, whole wheat
        "Stärke": 0.6,             # corn starch
        "Zucker en poudre": 0.6,   # sugar, powdered
        "Zucker glace": 0.6        # sugar, confectioners
    }

    # ORIGINAL TABLES FROM ENGLISH

    # Standard unit names and alternate unit names that might appear.  For
    # example: u"c." is our standard abbreviation for cup.  u"cup",u"c." or
    # u"cups" might appear in a recipe we are importing.  Each item of this
    # list looks like this:
    #
    # [u"standard", [u"alternate1",u"alternate2",u"alternate3",...]]
    #
    # The first item should be the preferred abbreviation
    # The second item should be the full name of the unit
    # e.g. [u"c.", [u"cup",...]]
    #
    UNITS = [
        ("ml", ["Milliliter", "milliliter",
         "Milliliters", "milliliters", "ml", "ml."]),
        ("cl", ["Centiliter", "centiliter",
         "Centiliters", "centiliters", "cl", "cl."]),
        ("dl", ["Deciliter", "deciliter",
         "Deciliters", "deciliters", "dl", "dl."]),
        ("l", ["Liter", "Liters", "liter", "liters", "l.", "lit.", "l"]),

        ("g", ["Gramm", "Gramme", "gramm", "gramme", "g.", "g", "gram", "grams"]),
        ("mg", ["Milligramm", "milligramm", "Milligramme",
         "milligramme", "mg.", "mg", "milligram", "milligrams"]),
        ("kg", ["Kilogramm", "kilogramm", "Kilogramme",
         "kilogramme", "kg.", "kg", "kilogram", "kilograms"]),

        ("cm", ["Centimeter", "centimeter",
         "Centimeters", "centimeters", "cm", "cm."]),
        ("mm", ["Millimeter", "millimeter",
         "Millimeters", "millimeters", "mm", "mm."]),
        ("m", ["Meter", "meter", "Meters", "meters", "m", "m."]),

        ("Tröpfchen", ["Tröpfchen", "tröpfchen",
         "troepfchen", "Troepfchen", "drop", "drops"]),
        ("TL", ["Teelöffel", "Teelöffeln", "teelöffel", "teelöffeln",
         "tl", "TL", "tsp", "tsp.", "tea spoon", "teaspoon"]),
        ("EL", ["Esslöffel", "Esslöffeln", "esslöffel", "esslöffeln", "el",
         "EL", "tbs", "tbsp", "tbs.", "tbsp.", "table spoon", "tablespoon"]),
        ("Tasse", ["Tasse", "Tassen", "tasse", "tassen", "cup",
         "c.", "cups", "Glas", "glas", "Glass", "glass"]),
        ("Becher", ["Becher", "becher"]),

        ("St.", ["St.", "Stück", "Stücke", "Stueck", "Stuecke", "Mal", "stück",
         "stücke", "stueck", "stuecke", "mal", "piece", "pieces", "St", "st"]),
        ("Dose, mittel", ["Dose, mittel", "dose, mittel",
         "mittlere Dose", "mittlere dose"]),
        ("Dose, groß", ["Dose, groß", "dose, groß",
         "größe Dose", "größe dose"]),
        ("Dose, klein", ["Dose, klein", "dose, klein",
         "kleine Dose", "kleine dose"]),
        ("Zeh", ["Zeh", "Zehen", "zeh", "zehen"]),  # garlic
        ("Paket", ["Paket", "Pakete", "paket",
         "pakete", "Packung", "packung", "pack"]),
        ("Prise", ["Prise", "Prisen", "prise", "prisen"]),  # pinch
        ("Bund", ["Bund", "Bunde", "bund", "bunde"]),  # bunch

        ("lb.", ["Pfund", "pfund", "pound", "pounds", "lb", "lb.", "lbs."]),
        ("oz.", ["ounce", "ounces", "oz", "oz."]),
        ("qt.", ["quart", "qt.", "quarts"]),
        ("pt.", ["pint", "pt.", "pints"]),
        ("gallon", ["gallon", "gallons", "gal."]),

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
        'imperial weight': [('oz.', (0.25, 32)),
                            ('lb.', (0.25, None)),
                            ],
        'imperial volume': [('Tröpfchen', (0, 3)),
                            ('TL', (0.125, 3)),
                            ('EL', (1, 4)),
                            ('Tasse', (0.25, 6)),
                            ('pt.', (1, 1)),
                            ('qt.', (1, 3))]
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
        ("EL", "oz."): ('density', 0.5),
        ("Tasse", "oz."): ('density', 8),
        ("l", "kg"): ('density', 1),
        ("ml", "g"): ('density', 1),
    }

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
        ("l", "kg"): 1
    }

    # From translator :
    # FRENCH PART TO BE REVISED !!! US units != UK units != Canadian units !!!
    # I will work on these later...
    # VOL_TO_MASS_TABLE = {
    #     (u"chop",u"lb") : 1,                    #(warning, might not be accurate, see below)
    #     (u"c. à table",u"oz") : 0.5,
    #     (u"tasse",u"oz") : 8,
    #     (u"chop",u"oz") : 20,                    #(warning, modified, see u"chopine" in granddictionnaire)
    #     (u"ml",u"g") : 1,
    #     (u"ml",u"mg") : 1000,
    #     (u"ml",u"kg"): 0.001,
    #     (u"cl",u"kg"): 0.01,
    #     (u"cl",u"g") : 10,
    #     (u"dl",u"kg") : 0.1,
    #     (u"dl",u"g") : 100,
    #     (u"l",u"kg") : 1}

    # TIME ABBREVIATIONS (this is new!)
    TIME_ABBREVIATIONS = {
        'sec': 'Sek.',
        'min': 'Min.',
        'hr': 'Std.'
    }

    IGNORE = ["und", "mit", "von", "für",
              "kalt", "kalter", "kalte", "kaltes", "kalten",
              "warm", "warmer", "warme", "warmes", "warmen",
              "dünn", "dünner", "dünne", "dünnes", "dünnen",
              "dick", "dicker", "dicke", "dickes", "dicken"
              ]

    NUMBERS: Mapping[float, Collection[str]] = {
    }

    # These functions are rather important! Our goal is simply to
    # facilitate look ups -- if the user types in u"tomatoes", we want to
    # find "tomato." Note that the strings these functions produce will
    # _never_ be shown to the user, so it's fine to generate nonsense
    # words as well as correct answers -- our goal is to generate a list
    # of possible hits rather than to get the plural/singular form "right".

    @staticmethod
    def guess_singulars(s):
        # Note - German, here we're not only going to try to make nouns singular,
        # we could also get an adjective, so lets also take the adjectival endings off
        if len(s) < 3:
            return []
        ret = []
        if s[-1] == 'n':
            if s[-2] == 'e':
                ret.append(s[0:-2])  # try chopping off 'en'
            if (s[-2] != 'u') & (s[-2] != 'o') & (s[-2] != 'a') & (s[-2] != 'i'):
                ret.append(s[0:-1])  # try chopping off the n

        if s[-1] == 's':
            ret.append(s[0:-1])  # try chopping off the s
            if s[-2] == 'e':
                ret.append(s[0:-2])  # try chopping off 'es'

        if s[-1] == 'e':
            ret.append(s[0:-1])  # try chopping off the 'e'

        if (s[-1] == 'r') & (s[-2] == 'e'):
            ret.append(s[0:-2])  # try chopping off the 'er'

        return ret

    @staticmethod
    def guess_plurals(s):
        # Ditto above, assume this could also be an adjective, so try adding the common agreements
        return [s+'n', s+'en', s+'e', s+'er', s+'s', s+'es']
