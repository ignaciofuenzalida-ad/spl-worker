import logging
import time

from requests import HTTPError
from service.sportlife_service import SportlifeService
from service.user_service import UserService


class ScrapperService:
    def __init__(self, config):
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user_service = UserService(config)
        self._sportlife_service = SportlifeService(config)

        self._user_data = []
        self._current_user = None

    def start(self):
        self._user_data = ["22141732-1"]  # test

        while True:
            try:
                if len(self._user_data) == 0:
                    self._logger.info("Empty user data, fetching from spl-users.")
                    self._user_data = self._user_service.get_random_users()
                if len(self._user_data) == 0:
                    self._logger.info(
                        "Empty user data from spl-users, waiting 5 seconds."
                    )
                    time.sleep(5)

                for run in self._user_data[:]:
                    self._current_user = run

                    user_exist = self._sportlife_service.login(run)
                    if not user_exist:
                        self._user_service.notify_user_not_found(run)
                        self._logger.info("[%s] User not found.", run)
                        self._user_data.remove(run)
                        continue

                    self._logger.info(
                        "[%s] New user found, extracting information.", run
                    )
                    user_information = self._build_information()

                    self._logger.info(
                        "[%s] Success extraction, sending to spl-users.", run
                    )
                    self._user_service.send_user(run, user_information)
                    self._user_data.remove(run)

            except Exception as error:
                self.handle_error(error, self._current_user)

    def _build_information(self) -> dict[str, str]:
        main_data = self._sportlife_service.get_main_data()
        profile_data = self._sportlife_service.get_profile()

        agenda_data = {}
        if "plantType" in main_data:
            agenda_data = self._sportlife_service.get_agenda_data()

        return {**main_data, **profile_data, **agenda_data}

    def handle_error(self, error: any, run: int):
        if error is HTTPError:
            self._logger.error("HTTP error occurred: %s", error)
        elif error is ConnectionError:
            self._logger.error("Connection error occurred: %s", error)
        else:
            self._logger.error("[%s] An error occurred: %s", run, error)

        self._logger.info("Waiting 10 seconds before continue")
        time.sleep(10)
