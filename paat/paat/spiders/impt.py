import scrapy


class ImptSpider(scrapy.Spider):
    name = "impt"
    allowed_domains = ["cb.imsc.res.in"]
    #start_urls = ["https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY007416"]
    

    def start_requests(self):

        for number in range(1, 17968):
            formatted_number = f'{number:06d}'
            url = f"https://cb.imsc.res.in/imppat/phytochemical-detailedpage/IMPHY{formatted_number}"
            yield scrapy.Request(url, callback=self.parse,meta={'my_argument': formatted_number})
  
    
    def parse(self,response) :
         data= {}

         my_argument_value = response.meta.get('my_argument')
         print(my_argument_value)
         data["Phytochemical name"] = response.xpath('//strong[text()="Phytochemical name:"]/following-sibling::text()').get()
         data["Phytochemical id "]   = response.xpath('//strong[text()="IMPPAT Phytochemical identifier:"]/following-sibling::text()').get()
         data["Synonymous chemical names"] = response.xpath('//strong[text()="Synonymous chemical names:"]/following-sibling::text()').get()
        
         pubchem = response.xpath('//a[contains(text(), "CID")]/@href').get()
         
         if pubchem:
             data["pubchem"]=pubchem.split("/")[-1]      
         chembl = response.xpath('//a[contains(text(), "ChEMBL")]/@href').get()
         
         if chembl:
             data["chembl"]=chembl.split("/")[-1]
         zinc =  response.xpath('//a[contains(text(), "ZINC")]/@href').get()
         
         if zinc:
             data["zinc"]=zinc.split("/")[-2]

         fdars = response.xpath('//a[contains(text(), "FDARS")]/@href').get()  
         if fdars:
             data["fdras"] = fdars.split("/")[-1]

         surecheml = response.xpath('//a[contains(text(), "SCHEMBL")]/@href').get()  
         if surecheml:
            data["surecheml"] = surecheml.split("/")[-1] 
         
         molprot = response.xpath('//a[contains(text(), "MolPort")]/@href').get()
         if molprot:
            data["Molprot"] = molprot.split("/")[-1]   

         data["smiles"] = response.css('.chem strong:contains("SMILES") + br + text::text').get()
         data["inchi"] = response.css('.chem strong:contains("InChI") + br + text::text').get()

         data["inchi_key"] = response.xpath('//strong[contains(text(), "InChIKey")]/following-sibling::br/following-sibling::text()').get()
         data["deep_smiles"] = response.xpath('//strong[contains(text(), "DeepSMILES")]/following-sibling::br/following-sibling::text()').get()
         data["functional_groups"] = response.xpath('//strong[contains(text(), "Functional groups")]/following-sibling::br/following-sibling::text()').get()

        # Extracting values from the Molecular scaffolds section
        #  data["scaffold_graph_node_bond"] = response.xpath('//strong[contains(text(), "Scaffold Graph/Node/Bond level")]/following-sibling::br/following-sibling::text()').get(),
        # "scaffold_graph_node" : response.xpath('//strong[contains(text(), "Scaffold Graph/Node level")]/following-sibling::br/following-sibling::text()').get(),
        # "scaffold_graph" : response.xpath('//strong[contains(text(), "Scaffold Graph level")]/following-sibling::br/following-sibling::text()').get(),

        # Extracting values from the Chemical classification section
        # "classyfire_kingdom" : response.xpath('//strong[contains(text(), "ClassyFire Kingdom")]/following-sibling::text()').get()
        # "classyfire_superclass" : response.xpath('//strong[contains(text(), "ClassyFire Superclass:")]/following::a[1]/text()').get()
        # "classyfire_class" : response.xpath('//strong[contains(text(), "ClassyFire Class")]/following-sibling::text()').get()
        # "classyfire_subclass" : response.xpath('//strong[contains(text(), "ClassyFire Subclass")]/following-sibling::text()').get()
        # "np_classifier_biosynthetic_pathway" : response.xpath('//strong[contains(text(), "ClassyFire Kingdom")]/following-sibling::text()').get()
        # "np_classifier_superclass" : response.xpath('//strong[contains(text(), "NP Classifier Biosynthetic pathway")]/following-sibling::text()').get()
        # "np_classifier_class" : response.xpath('//strong[contains(text(), "NP Classifier Class")]/following-sibling::text()').get()
         data["np_likeness_score"] = response.xpath('//strong[contains(text(), "NP-Likeness score")]/following-sibling::text()').get()
         url = f"https://cb.imsc.res.in/imppat/physicochemicalproperties/IMPHY{my_argument_value}"
         yield scrapy.Request(url, callback=self.parsesecond,meta={"data":data})
           
       
    def parsesecond(self, response):
        print("second function")
        data = response.meta.get('data')


        properties = [
            'Molecular weight (g/mol)', 
            'Log P', 
            'Number of hydrogen bond acceptors',
            'Number of hydrogen bond donors',
            'Number of carbon atoms',
            'Number of heavy atoms', 
            'Number of heteroatoms',
            'Number of nitrogen atoms',
            'Number of sulfur atoms',
            'Number of chiral carbon atoms',
            'Stereochemical complexity',
            'Number of sp hybridized carbon atoms',  
            'Shape complexity',
            'Number of rotatable bonds', 
            'Number of aliphatic carbocycles',
            'Number of aliphatic heterocycles', 
            'Number of aliphatic rings',
            'Number of aromatic carbocycles', 
            'Number of aromatic heterocycles',
            'Number of aromatic rings', 
            'Total number of rings',
            'Number of saturated carbocycles', 
            'Number of saturated heterocycles',
            'Number of saturated rings', 
            'Number of Smallest Set of Smallest Rings (SSSR)',
            "Lipinski’s rule of 5 filter", 
            "Number of Lipinski",
            'Number of Ghose filter violations', 
            'Veber',
            'GSK', 
            'Pfizer', 
            'Weighted quantitative estimate of drug-likeness (QEDw) score',
            'Bioavailability score', 
            'Solubility class [ESOL]', 
            'Solubility class [Silicos-IT]',
            'Blood Brain Barrier permeation', 
            'Gastrointestinal absorption',
            'Log K', 
            'Number of PAINS structural alerts',
            'Number of Brenk structural alerts', 
            'CYP1A2 inhibitor', 
            'CYP2C19 inhibitor',
            'CYP2C9 inhibitor', 
            'CYP2D6 inhibitor', 
            'CYP3A4 inhibitor',
            'P-glycoprotein substrate'
        ]
       
        

        # Loop through each property and extract values
        for prop in properties:
          
        
            values = response.xpath(f'//td[contains(text(), "{prop}")]/following-sibling::td[2]//text()').get()
            
            # Add the values to the dictionary
            data[prop] = values
           
        data["sp2_atoms"]= response.xpath("//td[substring-before(substring-after(., 'Number of sp'), ' ') = '2']/following-sibling::td[2]/text()").get()
        data["sp3_atoms"]= response.xpath("//td[substring-before(substring-after(., 'Number of sp'), ' ') = '3']/following-sibling::td[2]/text()").get()
        data["Ghose_rule"]=response.xpath('//tr[td[1]=" Ghose filter "]/td[3]/text()').get()
        data['Topological polar surface area'] =response.xpath('//td[contains(text(), "Topological polar surface area")]/following-sibling::td[2]//text()').get()
            
        yield data
           