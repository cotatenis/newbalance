from data_loader import load_newbalance_data
from scrapy.utils.project import get_project_settings
import os
from scrapy.crawler import CrawlerRunner
from newbalance.spiders import NewBalanceSpider
from scrapy.utils.log import configure_logging
from config import settings
from typer import Typer
from twisted.internet import reactor
import os

app = Typer()

@app.command()
def start_crawl():
    nb_data = load_newbalance_data()
    if nb_data:
        crawl_settings = get_project_settings()
        settings_module_path = os.environ.get("SCRAPY_ENV", "newbalance.settings")
        crawl_settings.setmodule(settings_module_path)
        configure_logging(crawl_settings)
        runner = CrawlerRunner(crawl_settings)
        d = runner.crawl(NewBalanceSpider, mpn=nb_data.get("mpn"), urls=nb_data.get("urls"))
        d.addBoth(lambda _: reactor.stop())
        reactor.run() 
    else:
        print("Não foi possível carregar os dados.")


if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.get("store.GOOGLE_APPLICATION_CREDENTIALS", "./credentials/credentials.json")
    app()
