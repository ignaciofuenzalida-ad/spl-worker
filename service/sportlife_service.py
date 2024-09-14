import requests
from requests.cookies import RequestsCookieJar
from datetime import datetime

from bs4 import BeautifulSoup
from utils.utility import clean_dict


spanish_months = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


class SportlifeService:
    def __init__(self, config: dict[str, str]):
        self._base_url: str = config["SPORTLIFE_BASE_URL"]
        self._cookies: RequestsCookieJar = None

    def logout(self):
        self._cookies = None

    def login(self, run: str) -> bool:
        form_data = {
            "checkRUT": "1",
            "RUT": run,
            "PASS": "",
        }
        headers = {"user-agent": ""}

        response = requests.post(
            f"{self._base_url}/index.php", data=form_data, headers=headers
        )

        if response.status_code != 200:
            response.raise_for_status()

        user_exist = True if response.json()["status"] == 1 else False
        if user_exist:
            self._cookies = response.cookies

        return user_exist

    def get_profile(self) -> dict[str, str]:
        headers = {"user-agent": ""}
        response = requests.get(
            f"{self._base_url}/editProfile.php",
            cookies=self._cookies,
            headers=headers,
        )

        if response.status_code != 200:
            response.raise_for_status()

        profile_data = {}

        soup = BeautifulSoup(response.content, "html.parser")

        # firstName
        first_name_input = soup.find("input", {"name": "CONTACTOCAMPO2"})
        profile_data["firstName"] = (
            first_name_input["value"] if first_name_input else None
        )

        # lastName
        last_name_input = soup.find("input", {"name": "CONTACTOCAMPO1"})
        profile_data["lastName"] = last_name_input["value"] if last_name_input else None

        # phoneNumber
        phone_number = soup.find("input", {"name": "CONTACTOCAMPO10"})
        profile_data["phoneNumber"] = phone_number["value"] if phone_number else None

        # email
        email_input = soup.find("input", {"type": "email"})
        profile_data["email"] = email_input["value"] if email_input else None

        # gender
        checked_gender = soup.find("input", {"name": "CONTACTOCAMPO3", "checked": True})
        if checked_gender:
            profile_data["gender"] = (
                "MALE" if checked_gender["value"] == "Masculino" else "FEMALE"
            )

        # maritalStatus
        maritial_status_input = soup.find(
            "input", {"name": "CONTACTOCAMPO6", "checked": True}
        )
        profile_data["maritalStatus"] = (
            maritial_status_input["value"] if maritial_status_input else "NO REFIERE"
        )

        # birthDate
        bird_date_input = soup.find("input", {"name": "CONTACTOCAMPO4"})
        bird_date = bird_date_input["value"] if bird_date_input else None
        if bird_date:
            try:
                parsed_date = datetime.strptime(bird_date, "%Y-%m-%d")
                profile_data["birthDate"] = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                None

        # homeAddress
        address_input = soup.find("input", {"name": "CONTACTOCAMPO13"})
        profile_data["homeAddress"] = address_input["value"] if address_input else None

        # city
        city_selection = soup.find("select", {"name": "CONTACTOCAMPO18"})
        selected_city = city_selection.find("option", {"selected": True})
        profile_data["city"] = selected_city["value"] if selected_city else None

        # emergencyName
        emergency_name_input = soup.find("input", {"name": "CONTACTOCAMPO21"})
        profile_data["emergencyName"] = (
            emergency_name_input["value"] if emergency_name_input else None
        )

        # emergencyNumber
        emergency_number_input = soup.find("input", {"name": "CONTACTOCAMPO15"})
        profile_data["emergencyNumber"] = (
            emergency_number_input["value"] if emergency_number_input else None
        )

        return clean_dict(profile_data)

    def get_main_data(self) -> dict[str, str]:
        headers = {"user-agent": ""}
        response = requests.get(
            f"{self._base_url}/index.php",
            cookies=self._cookies,
            headers=headers,
        )

        if response.status_code != 200:
            response.raise_for_status()

        main_data = {}

        soup = BeautifulSoup(response.content, "html.parser")

        elements = soup.find_all("h5", class_="card-subtitle mb-2 text-muted")
        values = [element.text.strip() for element in elements]

        # plantType
        plan_exist = values[1] != "Sin plan"
        main_data["plantType"] = values[1] if plan_exist else None

        # expirationDate
        if plan_exist:
            date_string = values[2]
            parts = date_string.split()
            day = parts[3]
            spanish_month = parts[5]
            year = parts[7]

            month = spanish_months.get(spanish_month.lower())
            date_str = f"{year}-{month:02d}-{day}"
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                main_data["expirationDate"] = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                main_data["expirationDate"] = None

        return clean_dict(main_data)

    def get_agenda_data(self) -> dict[str, str]:
        headers = {"user-agent": ""}
        response = requests.get(
            f"{self._base_url}/agendar.php",
            cookies=self._cookies,
            headers=headers,
        )

        if response.status_code != 200:
            response.raise_for_status()

        agenda_data = {}
        soup = BeautifulSoup(response.content, "html.parser")

        select_element = soup.find("select", {"id": "SEDE"})

        options = select_element.find_all("option")
        locations = []
        for option in options:
            if option.text != "Seleccione...":  # Exclude "Seleccione..."
                first_value = option.text.split("\t")[0].strip()
                locations.append(first_value)

        agenda_data["locations"] = locations

        return clean_dict(agenda_data)
