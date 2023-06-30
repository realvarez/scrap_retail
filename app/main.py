from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from datetime import date
from pages.scrapping_note_ripley import ScrappingNotebookRipley

def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def get_pages_items_from_ripley(driver):
    last_page = 0
    links = []
    driver.get("https://simple.ripley.cl/tecno/computacion/notebooks")
    while last_page == 0:
        page = driver.find_element_by_class_name("catalog-page")
        catalogs = page.find_element_by_class_name("catalog-container")\
            .find_elements_by_class_name("catalog-product-item")
        for catalog in catalogs:
            containers_agotado = catalog.find_elements_by_class_name("catalog-product-details__tags-container")
            if len(containers_agotado) == 0:
                links.append(catalog.get_attribute('href'))
        next_page = page\
            .find_element_by_class_name("catalog-page__footer-pagination")\
            .find_elements_by_xpath("nav/ul/li")[-1]\
            .find_element_by_xpath("a")
        if 'is-disabled' in next_page.get_attribute('class').split():
            last_page = 1
        else:
            next_page.click()
    return links

def get_products_info_from_notebook_ripley(driver, links):
    products = []
    for link in links:
        product = {
            'product_name':'',
            'normal_value':'',
            'discount_value':'',
            'card_discount_value':''
        }
        driver.get(link)
        print('Enlace de datos: {}'.format(link))
        product['product_name'] = driver.find_element_by_xpath("//div[@id='row']/div[2]/section/h1").text
        print(product['product_name'])
        try:
            product['normal_value'] = driver.find_element_by_class_name("product-normal-price").find_element_by_xpath("span[2]").text
        except:
            pass
        try:
            product['discount_value'] = driver.find_element_by_class_name("product-internet-price-not-best").find_element_by_xpath("span[2]").text
        except:
            pass
        try:
            product['discount_value'] = driver.find_element_by_class_name("product-internet-price").find_element_by_xpath("span[2]").text
        except:
            pass
        try:
            product['card_discount_value'] = driver.find_element_by_class_name("product-internet-price-not-best").find_element_by_xpath("span[2]").text
        except:
            pass
        products.append(product)
    return products


def get_data_notebooks_from_ripley(driver):
    links = get_pages_items_from_ripley(driver)
    products = get_products_info_from_notebook_ripley(driver, links)
    df = pd.DataFrame(products)
    today = date.today()
    df.to_csv('/output/note_ripley_{}.csv'.format(today), sep=";", index=False)


def get_pages_items_from_paris(driver):
    last_page = 0
    links = []
    base_path = 'https://www.paris.cl/tecnologia/computadores/notebooks/'
    driver.get(base_path)
    page = 1
    while last_page == 0:
        catalogs = driver.find_element_by_class_name("list-products").find_element_by_xpath("ul").find_elements_by_xpath("li")
        for catalog in catalogs:
            product = catalog.find_element_by_class_name("onecolumn").find_element_by_xpath("div")
            product_data = product.get_attribute('data_product')
            link = product.find_element_by_xpath("div/div[2]/div[3]/div/a").get_attribute('href')
            links.append(link)
            print(link)
        try:
            next_page = driver.find_element_by_link_text("{}".format(page))
            next_page.click()
            page = page +1 
        except:
            break
    return links

def get_products_info_from_notebook_paris(driver, links):
    products = []
    for link in links:
        product = {
            'brand':'',
            'product_name':'',
            'normal_value':'',
            'discount_value':'',
            'card_discount_value':''
        }
        driver.get(link)
        product_div = driver.find_element_by_class_name('row-info-product')        
        product['product_name'] = product_div.find_element_by_xpath('div/h1').text.split('\n')[1]
        print('prod_name', product['product_name'])
        try:
            product['brand'] = product_div.find_element_by_xpath('div/h1/span/a').text
            print('brand', product['brand'])
        except:
            pass
        try:
            product['normal_value'] = product_div.find_element_by_xpath('div[4]/div/div[2]/div/div[2]/span/s').text
            print('normal_value', product['normal_value'])
        except:
            pass
        try:
            product['discount_value'] = product_div.find_element_by_xpath('div[4]/div/div[2]/div/div/div/span').text
            print('discount_value', product['discount_value'])
        except:
            pass
        try:
            product['card_discount_value'] = product_div.find_element_by_xpath('div[4]/div/div').text.split('\n')[0]
            print('card_discount_value', product['card_discount_value'])
        except:
            pass
        products.append(product)
    return products



def get_data_notebooks_from_paris(driver):
    links = get_pages_items_from_paris(driver)
    products = get_products_info_from_notebook_paris(driver, links)
    df = pd.DataFrame(products)
    today = date.today()
    df.to_csv('/output/note_paris_{}.csv'.format(today), sep=";", index=False)


if __name__ == "__main__":
    driver = webdriver.Chrome(options=set_chrome_options())
    ScrappingNotebookRipley(driver).get_data_notebooks_from_ripley()
    #get_data_notebooks_from_ripley(driver)
    #get_data_notebooks_from_paris(driver)
    driver.close()