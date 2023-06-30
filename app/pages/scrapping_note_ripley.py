from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from datetime import date



class ScrappingNotebookRipley:
    def __init__(self, driver):
        self.driver = driver
        self.base_page = "https://simple.ripley.cl/tecno/computacion/notebooks"
        self.links = []
        self.products = []
    
    def get_links_in_page(self, page):
        catalogs = page.find_element_by_class_name("catalog-container")\
                       .find_elements_by_class_name("catalog-product-item")
        for catalog in catalogs:
            containers_agotado = catalog.find_elements_by_class_name(
                "catalog-product-details__tags-container")
            if len(containers_agotado) == 0:
                self.links.append(catalog.get_attribute('href'))

    def get_pages_items_from_ripley(self):
        last_page = 0
        self.driver.get(self.base_page)
        while last_page == 0:
            page = self.driver.find_element_by_class_name("catalog-page")
            self.get_links_in_page(page)
            next_page = page\
                .find_element_by_class_name("catalog-page__footer-pagination")\
                .find_elements_by_xpath("nav/ul/li")[-1]\
                .find_element_by_xpath("a")
            if 'is-disabled' in next_page.get_attribute('class').split():
                last_page = 1
            else:
                next_page.click()

    def get_products_info_from_notebook_ripley(self):
        for link in self.links:
            product = {
                'product_name':'',
                'normal_value':'',
                'discount_value':'',
                'card_discount_value':''
            }
            self.driver.get(link)
            product['product_name'] = self.driver.find_element_by_xpath("//div[@id='row']/div[2]/section/h1").text
            try:
                product['normal_value'] = self.driver.find_element_by_class_name("product-normal-price")\
                                                     .find_element_by_xpath("span[2]").text
            except:
                pass
            try:
                product['discount_value'] = self.driver.find_element_by_class_name("product-internet-price-not-best")\
                                                       .find_element_by_xpath("span[2]").text
            except:
                pass
            try:
                product['discount_value'] = self.driver.find_element_by_class_name("product-internet-price")\
                                                       .find_element_by_xpath("span[2]").text
            except:
                pass
            try:
                product['card_discount_value'] = self.driver.find_element_by_class_name("product-internet-price-not-best")\
                                                            .find_element_by_xpath("span[2]").text
            except:
                pass
            self.products.append(product)

    def get_data_notebooks_from_ripley(self):
        self.get_pages_items_from_ripley()
        self.get_products_info_from_notebook_ripley()
        df = pd.DataFrame(self.products)
        today = date.today()
        df.to_csv('/output/note_ripley_{}.csv'.format(today), sep=";", index=False)
