import requests


class UserService:
    def __init__(self, config: dict[str, str]):
        self._base_url: str = config["SPL_USERS_BASE_URL"]
        self._token: str = config["SPL_USERS_TOKEN"]

    def get_random_users(self) -> list[str]:
        response = requests.get(
            f"{self._base_url}/users/random",
            headers={"X-Auth-Token": self._token},
        )

        if response.status_code == 200:
            return response.json()["data"]
        else:
            response.raise_for_status()

    def notify_user_not_found(self, run: str) -> None:
        response = requests.post(
            f"{self._base_url}/users/{run[:-2]}",
            headers={"X-Auth-Token": self._token},
            data={
                "fetchStatus": "COMPLETED",
                "status": "NOT_FOUND",
            },
        )

        if response.status_code == 200:
            return

        response.raise_for_status()

    def send_user(self, run: str, data: dict[str, str]) -> None:
        payload = {
            "fetchStatus": "COMPLETED",
            "status": "FOUND",
        }
        payload.update(data)

        response = requests.post(
            f"{self._base_url}/users/{run[:-2]}",
            headers={"X-Auth-Token": self._token},
            data=payload,
        )

        if response.status_code != 200:
            response.raise_for_status()
