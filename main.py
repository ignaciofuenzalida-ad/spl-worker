import logging
from config.env import config
from flask import Flask, jsonify
from service.scrapper_service import ScrapperService
from threading import Thread

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


def start_flask():
    logging.info("Starting Flask server at port 8000")
    app.run(host="0.0.0.0", port=8000)


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    if config["EXPOSE_SERVER"]:
        # Start Flask in a separate thread
        flask_thread = Thread(target=start_flask)
        flask_thread.start()

    scrapper_service = ScrapperService(config)
    scrapper_service.start()


if __name__ == "__main__":
    main()
