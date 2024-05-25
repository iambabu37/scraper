import scrapy


class ImpactSpider(scrapy.Spider):
    name = "impact"
    allowed_domains = ["cb.imsc.res.in"]
    #start_urls = ["https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY007417"]
    
    def start_requests(self):

        for number in range(1, 17968):
            formatted_number = f'{number:06d}'
            url = f"https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY{formatted_number}"
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        yield{

        "Phytochemical name"   : response.xpath('//strong[text()="Phytochemical name:"]/following-sibling::text()').get(),
        "Phytochemical id "   : response.xpath('//strong[text()="IMPPAT Phytochemical identifier:"]/following-sibling::text()').get(),
        "Synonymous chemical names" : response.xpath('//strong[text()="Synonymous chemical names:"]/following-sibling::text()').get(),
        "Pubchem" : response.xpath('//a[contains(text(), "CID")]/@href').get(),
        "Chembl" :response.xpath('//a[contains(text(), "ChEMBL")]/@href').get(),
        "Zinc" :  response.xpath('//a[contains(text(), "ZINC")]/@href').get(),
        "Fdars" : response.xpath('//a[contains(text(), "FDARS")]/@href').get(),  
        "Surechembl" :response.xpath('//a[contains(text(), "SCHEMBL")]/@href').get(),   
        "Molprot" : response.xpath('//a[contains(text(), "MolPort")]/@href').get(),   
        "smiles" : response.css('.chem strong:contains("SMILES") + br + text::text').get(),
        "inchi" : response.css('.chem strong:contains("InChI") + br + text::text').get(),

        "inchi_key" : response.xpath('//strong[contains(text(), "InChIKey")]/following-sibling::br/following-sibling::text()').get(),
        "deep_smiles" : response.xpath('//strong[contains(text(), "DeepSMILES")]/following-sibling::br/following-sibling::text()').get(),
        "functional_groups" : response.xpath('//strong[contains(text(), "Functional groups")]/following-sibling::br/following-sibling::text()').get(),

        # Extracting values from the Molecular scaffolds section
        "scaffold_graph_node_bond" : response.xpath('//strong[contains(text(), "Scaffold Graph/Node/Bond level")]/following-sibling::br/following-sibling::text()').get(),
        "scaffold_graph_node" : response.xpath('//strong[contains(text(), "Scaffold Graph/Node level")]/following-sibling::br/following-sibling::text()').get(),
        "scaffold_graph" : response.xpath('//strong[contains(text(), "Scaffold Graph level")]/following-sibling::br/following-sibling::text()').get(),

        # Extracting values from the Chemical classification section
        "classyfire_kingdom" : response.xpath('//strong[contains(text(), "ClassyFire Kingdom")]/following-sibling::text()').get(),
        "classyfire_superclass" : response.xpath('//strong[contains(text(), "ClassyFire Superclass:")]/following::a[1]/text()').get(),
        "classyfire_class" : response.xpath('//strong[contains(text(), "ClassyFire Class")]/following-sibling::text()').get(),
        "classyfire_subclass" : response.xpath('//strong[contains(text(), "ClassyFire Subclass")]/following-sibling::text()').get(),
        "np_classifier_biosynthetic_pathway" : response.xpath('//strong[contains(text(), "ClassyFire Kingdom")]/following-sibling::text()').get(),
        "np_classifier_superclass" : response.xpath('//strong[contains(text(), "NP Classifier Biosynthetic pathway")]/following-sibling::text()').get(),
        "np_classifier_class" : response.xpath('//strong[contains(text(), "NP Classifier Class")]/following-sibling::text()').get(),
        "np_likeness_score" : response.xpath('//strong[contains(text(), "NP-Likeness score")]/following-sibling::text()').get(),
        
        }
        