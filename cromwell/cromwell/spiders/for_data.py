import scrapy
import json
# from ..utils import translate_new
# from ..utils import clean
from scrapy_selenium import SeleniumRequest 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import codecs
class ForDataSpider(scrapy.Spider):
    name = "for_data"
    crawled_urls = []
    def start_requests(self):
        with codecs.open('./cromwell_uk_21august2023.json', 'r' , encoding='utf-8') as f:
            crawled_data = json.load(f)
        
        for c_data in crawled_data:
            c_url = c_data['Product_url']
            self.crawled_urls.append(c_url)

        with open('./final_cromwell_links2_uk.json' , 'r') as f:
            urls = json.load(f)
        for url in urls:
            if url["link"] not in self.crawled_urls:
                self.crawled_urls.append(url)
                yield SeleniumRequest(
                    url=url['link'] ,
                    callback=self.parse_item ,
                    wait_time=10,
                    # script="document.querySelector('h6[data-testid='productSpecificationTitle']').closest('div.MuiButtonBase-root.MuiAccordionSummary-root').click()",
                    # script='window.scrollTo(0, document.body.scrollHeight);'
                    script="""
                        const elementToClick = document.querySelector('h6[data-testid="productSpecificationTitle"]')
                            .closest('div.MuiButtonBase-root.MuiAccordionSummary-root');
                        if (elementToClick) {
                            elementToClick.click();
                        }
                        try {
                            // Click the second element
                            const elementToClick2 = document.querySelector('h6[data-testid="productDocumentsTitle"]')
                                .closest('div.MuiButtonBase-root.MuiAccordionSummary-root');
                            if (elementToClick2) {
                                elementToClick2.click();
                            }
                        } catch (error) {
                            console.error("Error occurred while clicking the second element:", error);
                        }
                        
                    """ ,
                    # wait_until=EC.element_to_be_clickable((By.XPATH, '//h3[contains(text() , "Similar Products")]/ancestor::div[@class="MuiPaper-root MuiPaper-elevation0 MuiPaper-rounded"]'))
    
                    )
            else:
                print('Already Crawled')
   
    def parse_item(self , response):
        # buttons = response.xpath('//div[@class="MuiButtonBase-root MuiAccordionSummary-root"]').getall()
        # for button in buttons:
        #     button.click()
        time.sleep(5)
        item = {}
        # self.scroll_to_bottom(response)
        item['Product_url'] = response.url
        item['part_number'] = self.parse_partno(response) #check
        item['add_part_number'] = self.parse_addPartno(response) #check
        item['Product_name'] = self.parse_product_name(response) #check
        item['Product_price'] = self.parse_product_price(response)
        item['product_specifications'] = self.parse_product_specifications(response)
        item['downloads'] = self.parse_downloads(response)
        # item['Related_products'] = self.parse_Related_products(response)
        item['Bread_Crumbs'] = self.parse_bread_crumbs(response) #check
        item['web_Series_link'] = self.parse_web_series_links(response) #check
        item['Primary_image'] = self.parse_primary_image(response) #check
        item['Secondary_images'] = self.parse_secondary_images(response) #check
        item['Product_Brand_Name'] = self.parse_brand_name(response) #check
        item['Product_description'] = self.parse_product_description(response) #check
        item['Product_meta_data'] = self.parse_meta_data(response) #check
        yield item
    def parse_product_price(self , response):
        item = response.xpath('//section[contains(@class , "MuiGrid-root MuiGrid-item")]//p[@data-testid="priceLabel"]/text()').get()
        return item
    def parse_product_name(self , response):
        item = response.xpath('//h1[@data-testid="productTitle"]/text()').get()
        return item
    def parse_bread_crumbs(self , response):
        item = response.xpath('//ol[@class="MuiBreadcrumbs-ol"]//li[not(contains(@class , "MuiBreadcrumbs-separator"))]//text()').getall()
        return item
    def parse_web_series_links(self , response):
        item_key = response.xpath('//ol[@class="MuiBreadcrumbs-ol"]//li[not(contains(@class , "MuiBreadcrumbs-separator"))]//text()').getall()
        item_value = response.xpath('//ol[@class="MuiBreadcrumbs-ol"]//li[not(contains(@class , "MuiBreadcrumbs-separator"))]//@href').getall()
        return dict(zip(item_key , item_value))
    def parse_meta_data(self , response):
        item = {
            'description' : response.xpath('//meta[@name="description"]/@content').get(),
            'title' : response.xpath('//meta[@name="twitter:title"]/@content').get()
        }
        return item
    def parse_product_description(self , response):
        item = response.xpath('//meta[@name="description"]/@content').get()
        return item
    def parse_primary_image(self , response):
        item = response.xpath('(//div[@class="image-gallery-slides"]//img/@src)[1]').get()
        return item
    def parse_secondary_images(self , response):
        item = response.xpath('//div[@class="image-gallery-slides"]//img/@src').getall()
        return item
    def parse_brand_name(self , response):
        item = response.xpath('//h3[@data-testid="productBrand"]/text()').get()
        return item
    def parse_addPartno(self , response):
        item = response.xpath('//p[@data-testid="productMpn"]/text()').get()
        return item
    def parse_partno(self , response):
        item = response.xpath('//p[@data-testid="productSku"]/text()').get()
        return item
    def parse_product_specifications(self , response):
        key = response.xpath('//table[@class="MuiTable-root"]//tr/td/h6/text()').getall()
        value = response.xpath('//table[@class="MuiTable-root"]//tr/td/text()').getall()
        item = dict(zip(key , value))
        return item
    def parse_downloads(self , response):
        key = response.xpath('//div[@class="MuiAccordionDetails-root"]//ul[@class="MuiList-root MuiList-padding MuiList-subheader"]//a//div[@class="MuiListItemText-root"]/span/text()').getall()
        value = response.xpath('//div[@class="MuiAccordionDetails-root"]//ul[@class="MuiList-root MuiList-padding MuiList-subheader"]//a/@href').getall()
        item = dict(zip(key , value))
        return item
    # def parse_Related_products(self , response):
    #     time.sleep(5)
    #     temps = response.xpath('//h3[contains(text() , "Similar Products")]/ancestor::div[@class="MuiPaper-root MuiPaper-elevation0 MuiPaper-rounded"]//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineHover jss338 MuiTypography-colorPrimary"]')
    #     f_item = []
    #     for temp in temps:
    #         url = temp.xpath('./@href').get()
    #         a = url.split('/p/')
    #         partno = a[1]
    #         item = {
    #             'url' : url,
    #             'name' : temp.xpath('./text()').get(),
    #             'partno' : partno
    #         }
    #         f_item.append(item)
    #     return f_item