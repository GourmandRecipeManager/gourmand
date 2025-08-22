import unittest

from bs4 import BeautifulSoup

from gourmand.importers import interactive_importer


class TestGetImages(unittest.TestCase):

    def setUp(self):

        # img tag containing parts of:
        # https://www.webtenerifefr.com/propos-tenerife/gastronomie/produits/recettes/garbanzas-compuestas/
        self.html = """
<!DOCTYPE html>
<html dist-version="240" lang="fr">
<body class="">
<section class="item-page">
<a class="navbar-brand" href="https://www.webtenerifefr.com/">
        <img itemprop="logo" src="https://www.webtenerifefr.com/-/media/project/webtenerife/common/logos_tenerife/tene\
rife_logo_degradado_fra.svg" width="640" height="360" title="Turismo de Tenerife" alt="" />
    </a>
    <a class="navbar-brand-mobile" href="https://www.webtenerifefr.com/">
        <img class="img-mobile" itemprop="logo" src="/dist/images/logo-tenerife-responsive.png" width="640" height="360"\
 title="Turismo de Tenerife" alt="Turismo de Tenerife" />
    </a>
        <div class="container">
            <div class="row">
                <div class="col-xs-12 col-md-9">
                        <h1 class="heading heading__page">Garbanzas compuestas (Ragoût de pois chiche)</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-12 col-md-7 col-md-offset-1">
                                            <h2 class="subtitle__page">Recette traditionnelle de T&#233;n&#233;rife</h2>
                        <div class="rte">
Avant de vous offrir la recette de ce plat, qui peut encore se trouver dans presque tous les \
restaurants des Iles Canaries, faisons la différence entre «garbanzos» et «garbanzas», dénominations \
qui a tendance à confondre les étrangers. Le «Garbanzo» (pois chiche) est le légume cru qui se \
transforme en «garbanza», du moins dans le langage insulaire, une fois qu’il a été cuit.    \
<p>Préparation: les pois chiche, les côtelettes et les pieds de porc (s’ils sont salés) doivent être \
mis à tremper la veille dans des récipients différents. Dans celui des pois chiche, vous pouvez \
ajouter une pincée de bicarbonate pour qu’ils soient plus tendres. Placer ces trois ingrédients \
dans une cocotte, les couvrir d’eau et laisser cuire à feu lent. Au bout de vingt minutes de \
cuisson, ajouter le lard et le chorizo, coupés en morceaux.</p>  <p>Préparer dans une poêle \
avec un peu d’huile, une sauce avec l’ail, l’oignon, les tomates (pelées et sans pépins) et \
le poivron, le tout coupé en petits morceaux. Ajouter un peu de paprika, dans la poêle hors \
du feu. Ajouter ensuite, une feuille de laurier, quatre ou cinq grains de poivre noir, un peu \
de safran ou colorant et broyer le cumin au dessus de la vapeur. </p>  <p>Éplucher les pommes \
de terre, les couper en dés et les faire revenir dans l’huile. Les ajouter ensuite à la cocotte \
lorsque les pois chichs sont presque cuits. Goûter et rectifier le sel (faire attention car ce \
plat est composé d’une certaine quantité d’ingrédients salés).</p>
                        </div>
    <div class="rte-snippet__col">
        <article class="rte-snippet rte">
            <div class="row">
                <div class="col-sm-12 col-xs-12 rte-snippet__content-col">
                        <div class="rte-snippet__title-container">
                            <h6 class="rte-snippet__title heading">
                                Autres renseignements
                            </h6>
                        </div>
                    <div class="rte-snippet__description-container rte">
<p>INGRÉDIENTS:</p>  <p>½ kg de pois chiche</p>  <p>350 gr de pommes de terre</p>  <p>Un ou deux\
pieds de porc</p>  <p>150 gr de côtelettes de porc salées</p>  <p>Un joli morceau de lard blanc</p>\
  <p>Un morceau de chorizo</p>  <p>2 oignons</p>  <p>1 poivron rouge</p>  <p>3 tomates</p>  <p>4 \
  gousses d’ail</p>  <p>1 cuillérée de paprika</p>  <p>Laurier</p>  <p>Poivre noir</p>  <p>Cumin</p>  \
  <p>Safran ou colorant</p>
                    </div>
                </div>
            </div>
        </article>
    </div>
                </div>
                <div class="col-xs-12 col-md-3 col-md-offset-1">
                </div>
            </div>
        </div>
        <div class="footer__logo">
<img class="image--responsive" width="640" height="360" data-image-src="https://www.\
webtenerifefr.com/-/media/project/webtenerife/common/logos_tenerife/tenerife_logo_blanco_fra.png" \
alt="Turismo de Tenerife" />
                            </div>
    </section>
</body>
</html>
"""
        self.soup = BeautifulSoup(self.html, "html.parser")

    def test_get_images(self):
        # Passes if this call does not throw an error
        interactive_importer.get_images(self.soup)


class TestConvenientImporter(unittest.TestCase):

    def setUp(self):
        self.ci = interactive_importer.ConvenientImporter()

    def test_import(self):
        self.ci.start_rec()
        self.ci.add_attribute("title", "Test")
        self.ci.add_attribute("category", "foo")
        self.ci.add_attribute("category", "bar")
        self.ci.add_ings_from_text(
            """6 garlic cloves, peeled
  1/2 pound linguine
  1/4 cup plus 1 tablespoon olive oil
  2 to 2 1/2 pounds small fresh squid (about 10), cleaned and cut into 3/4-inch thick rings, tentacles cut in half*
  1 1/2 teaspoons Baby Bam or Emeril's Original Essence, to taste
  1/4 cup chopped green onions
  1 teaspoon crushed red pepper, or to taste
  1/4 teaspoon salt
  1/4 cup fish stock, shrimp stock, or water
  2 tablespoons fresh lemon juice
  1 tablespoon unsalted butter
  1/4 cup chopped fresh parsley leaves
  1/2 cup freshly grated Parmesan"""
        )
        self.ci.commit_rec()
        rec = self.ci.added_recs[-1]
        self.assertEqual(rec.title, "Test")
        cats = self.ci.rd.get_cats(rec)
        cats.sort()
        self.assertEqual(len(cats), 2)
        self.assertEqual(cats[0], "bar")
        self.assertEqual(cats[1], "foo")
        ings = self.ci.rd.get_ings(rec)
        self.assertEqual(len(ings), 13)
        self.assertEqual(ings[1].amount, 0.5)
        self.assertEqual(ings[1].unit, "pound")
        self.assertEqual(ings[1].item, "linguine")
