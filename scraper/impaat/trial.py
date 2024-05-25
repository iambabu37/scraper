import scrapy

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['6https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY00741']

    def parse(self, response):
        # Extracting the dynamic values from the HTML

        # Extracting values from the Summary section
        summary_values = response.css('.chem h5 strong::text').get()

        # Extracting values from the Chemical structure information section
        smiles = response.css('.chem strong:contains("SMILES") + text::text').get()
        inchi = response.css('.chem strong:contains("InChI") + text::text').get()
        inchi_key = response.css('.chem strong:contains("InChIKey") + text::text').get()
        deep_smiles = response.css('.chem strong:contains("DeepSMILES") + text::text').get()
        functional_groups = response.css('.chem strong:contains("Functional groups") + text::text').get()

        # Extracting values from the Molecular scaffolds section
        scaffold_graph_node_bond = response.css('.chem strong:contains("Scaffold Graph/Node/Bond level") + text::text').get()
        scaffold_graph_node = response.css('.chem strong:contains("Scaffold Graph/Node level") + text::text').get()
        scaffold_graph = response.css('.chem strong:contains("Scaffold Graph level") + text::text').get()

        # Extracting values from the Chemical classification section
        classyfire_kingdom = response.css('.chem strong:contains("ClassyFire Kingdom") + text::text').get()
        classyfire_superclass = response.css('.chem strong:contains("ClassyFire Superclass") + text::text').get()
        classyfire_class = response.css('.chem strong:contains("ClassyFire Class") + text::text').get()
        classyfire_subclass = response.css('.chem strong:contains("ClassyFire Subclass") + text::text').get()
        np_classifier_biosynthetic_pathway = response.css('.chem strong:contains("NP Classifier Biosynthetic pathway") + text::text').get()
        np_classifier_superclass = response.css('.chem strong:contains("NP Classifier Superclass") + text::text').get()
        np_classifier_class = response.css('.chem strong:contains("NP Classifier Class") + text::text').get()
        np_likeness_score = response.css('.chem strong:contains("NP-Likeness score") + text::text').get()

        # Now you can use or print these values as needed
        print("Summary Values:", summary_values)
        print("SMILES:", smiles)
        print("InChI:", inchi)
        print("InChIKey:", inchi_key)
        print("DeepSMILES:", deep_smiles)
        print("Functional Groups:", functional_groups)
        print("Scaffold Graph/Node/Bond Level:", scaffold_graph_node_bond)
        print("Scaffold Graph/Node Level:", scaffold_graph_node)
        print("Scaffold Graph Level:", scaffold_graph)
        print("ClassyFire Kingdom:", classyfire_kingdom)
        print("ClassyFire Superclass:", classyfire_superclass)
        print("ClassyFire Class:", classyfire_class)
        print("ClassyFire Subclass:", classyfire_subclass)
        print("NP Classifier Biosynthetic pathway:", np_classifier_biosynthetic_pathway)
        print("NP Classifier Superclass:", np_classifier_superclass)
        print("NP Classifier Class:", np_classifier_class)
        print("NP Likeness Score:", np_likeness_score)


spider = MySpider()

spider.parse()