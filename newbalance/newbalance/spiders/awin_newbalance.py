from scrapy import Spider
from scrapy.utils.project import get_project_settings
from newbalance.items import NewBalanceItem
import undetected_chromedriver as uc
from scrapy import signals
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from pyvirtualdisplay import Display

class NewBalanceSpider(Spider):
    name = 'awin_newbalance'
    allowed_domains = ['newbalance.com.br']
    start_urls = ["https://quotes.toscrape.com/"]
    settings = get_project_settings()
    version = settings.get("VERSION")

    def __init__(self, mpn=[""], urls=[""], *args, **kwargs):
        super(NewBalanceSpider, self).__init__(*args, **kwargs)
        self.urls = urls
        self.mpn = mpn

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(NewBalanceSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    def spider_opened(self, spider):
        display = Display(visible=True, size=(800, 600), backend="xvfb")
        display.start()
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        #options.add_argument('--headless')
        self.browser = uc.Chrome(options=options)
        self.browser.set_page_load_timeout(30)
        self.wdw = WebDriverWait(self.browser, 10)
        self.wdw_page_not_found = WebDriverWait(self.browser, 3)
        self.wdw_sizes = WebDriverWait(self.browser, 2)
    
    def spider_closed(self, spider):
        self.browser.close()

    def parse(self, response):
        for sku, url in zip(self.mpn, self.urls):
            sleep(.5)
            image_urls = []
            self.logger.debug(url)
            try:
                self.browser.get(url)
            except Exception:
                try:
                    self.browser.refresh()
                except Exception:
                    continue
            try:
                _ = self.wdw_page_not_found.until_not(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'vtex-rich-text-0-x-strong')]")))
            except Exception:
                self.logger.debug(f"Página sem conteúdo: {url}.")
                continue
            try:
                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'vtex-store-components-3-x-productImageTag')]")))
            except (NoSuchElementException, TimeoutException):
                continue            
            else:
                images = self.browser.find_elements(By.XPATH, "//img[contains(@class, 'vtex-store-components-3-x-productImageTag')]")
                try:
                    image_urls = [i.get_attribute("srcset").split(",")[0].split(" ")[0].replace("-600-", "-400-").replace("width=600", "width=400") for i in images]
                except Exception:
                    continue
                else:
                    image_uris = [
                        f"{self.settings.get('IMAGES_STORE')}{sku}_{filename.split('/')[-1].split('-')[0]}"
                        for filename in image_urls
                    ]
                    if len(image_uris) > 0:
                        img_search_page = image_uris[0]
                    else:
                        img_search_page = ""
            try:
                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'items-center')]//div[contains(@class, 'vtex-store-components-3-x-frameAround--mz-product__sku absolute')]/..//div[contains(@class, 'vtex-store-components-3-x-valueWrapper')]")))
            except (NoSuchElementException, TimeoutException):
                continue    
            else:
                container_of_sizes = []
                sizes = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'items-center')]//div[contains(@class, 'vtex-store-components-3-x-frameAround--mz-product__sku absolute')]/..//div[contains(@class, 'vtex-store-components-3-x-valueWrapper')]")
                for element_size in sizes:
                    in_stock = True
                    sleep(1)
                    element_size.click()
                    try:
                        _ = self.wdw_sizes.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'vtex-store-components-3-x-title')]")))
                    except (NoSuchElementException, TimeoutException):
                        in_stock = True
                    else:
                        in_stock = False
                    finally:
                        if in_stock:
                            try:
                                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'currencyInteger')]")))
                            except (NoSuchElementException, TimeoutException):
                                self.logger.debug(f"Não foi possível coletar os preços do tamanho: {element_size.text}")
                                continue  
                            else:
                                price_integer = self.browser.find_element(By.XPATH, "//span[contains(@class, 'currencyInteger')]").text
                            try:
                                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'currencyFraction')]")))
                            except (NoSuchElementException, TimeoutException):
                                self.logger.debug(f"Não foi possível coletar os preços do tamanho: {element_size.text}")
                                continue  
                            else:
                                price_fraction = self.browser.find_element(By.XPATH, "//span[contains(@class, 'currencyFraction')]").text
                            try:
                                container_of_sizes.append(
                                    {
                                        'size' : element_size.text,
                                        'in_stock' : in_stock,
                                        'price' : float(f"{price_integer}.{price_fraction}")

                                    }
                                )
                            except Exception:
                                continue
                        else:
                            container_of_sizes.append(
                                {
                                    'size' : element_size.text,
                                    'in_stock' : in_stock,
                                    'price' : -1

                                }
                            )

            try:
                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'product-identifier__value')]")))
            except (NoSuchElementException, TimeoutException):
                continue    
            else:
                site_sku = self.browser.find_element(By.XPATH, "//span[contains(@class, 'product-identifier__value')]").text
            try:
                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'vtex-breadcrumb-1')]")))
            except (NoSuchElementException, TimeoutException):
                continue      
            else:
                breadcrumbs = [e.text for e in self.browser.find_elements(By.XPATH, "//span[contains(@class, 'vtex-breadcrumb-1')]") if e.text != ""]
                genre = breadcrumbs[0]
            try:
                _ = self.wdw.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-specification-name, 'Cor')]")))
            except (NoSuchElementException, TimeoutException):
                continue   
            else:
                color = self.browser.find_element(By.XPATH, "//span[contains(@data-specification-name, 'Cor')]").get_attribute("data-specification-value")
            for info_sizes in container_of_sizes:
                payload = {
                        'url' : url,
                        'sku' : sku,
                        'site_sku' : site_sku,
                        'color' : color,
                        'genre' : genre,
                        'img_search_page' : img_search_page,
                        'image_urls' : image_urls,
                        'image_uris' : image_uris,
                        'price' : info_sizes.get('price', -1),
                        'size' : info_sizes.get('size', -1),
                        'in_stock' : info_sizes.get('in_stock', False),
                        'qty_stock' : "",
                        'spider' : self.name,
                        'spider_version' : self.version
                    }
                yield NewBalanceItem(**payload)
