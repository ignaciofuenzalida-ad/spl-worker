import logging
from config.env import config
from service.scrapper_service import ScrapperService


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    scrapper_service = ScrapperService(config)
    scrapper_service.start()


if __name__ == "__main__":
    main()
