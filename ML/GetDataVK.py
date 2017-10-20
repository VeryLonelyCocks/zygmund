import vk
from transliterate import translit
import time


class DataVKGroup:
    def __init__(self, token, group_id, count):
        self._need_fields_user = ['uid', 'first_name', 'last_name', 'interests', 'sex', 'city', 'country']
        self._need_field_user_personal = ['political', 'people_main', 'life_main', 'smoking', 'alcohol']

        self._session = vk.Session(token)

        self._api = vk.API(self._session, lang='en')

        self._users = []

        self._export_users_from_group(group_id, count)

        self._friends_for_users = self._get_friends()
        self._cities = self._get_cities()
        self._countries = self._get_countries()

    def _export_users_from_group(self, group_id, count):
        group_members = self._api.groups.getMembers(group_id=group_id, count=count)

        self._users = self._api.users.get(user_ids=group_members['users'],
                                          fields='city,country,sex,interests,personal')

        self._users = [user for user in self._users if 'deactivated' not in user]

        self._translit_user_interests()
        self._fill_none_field()

    def _check_user(self, user):

        if 'city' not in user or 'country' not in user:
            return False

        if not user['city'] or not user['country']:
            return False

        if 'university' not in user or 'university_name' not in user or user['university_name'] == '':
            return False

        return True

    def _get_user_data(self, user):
        return {
            'uid': user['uid'],
            'country': self._api.database.getCountriesById(country_ids=user['country']),
            'city': self._api.database.getCitiesById(city_ids=user['city']),
            'university': user['university_name']
        }

    def _get_cities(self):

        if len(self._users) == 0:
            print("Users aren't exist")
            return

        cities = set()

        for user in self._users:
            if 'city' in user:
                cities.add(user['city'])

        cities_data = self._api.database.getCitiesById(city_ids=cities)

        cities_list = {}
        for cityData in cities_data:
            cities_list[cityData['cid']] = cityData['name']

        print('Got cities')

        return cities_list

    def _get_countries(self):

        if len(self._users) == 0:
            print("Users aren't exist")
            return

        countries = set()

        for user in self._users:
            if 'country' in user:
                countries.add(user['country'])

        countries_data = self._api.database.getCountriesById(country_ids=countries)

        countries_list = {}
        for countryData in countries_data:
            countries_list[countryData['cid']] = countryData['name']

        print('Got countries')

        return countries_list

    def _translit_user_interests(self):
        for user in self._users:
            if 'interests' in user:
                user['interests'] = translit(user['interests'], 'ru', reversed=True)

    def _get_friends(self):

        if len(self._users) == 0:
            print("Users aren't exist")
            return

        friends_for_users = []

        for user in self._users:
            print(user)
            friends_for_users.append({'user': user['uid'], 'friends': self._api.friends.get(user_id=user['uid'])})
            time.sleep(0.4)

        return friends_for_users

    def _fill_none_field(self):

        fill_users = []

        for user in self._users:
            data = {}
            for field in self._need_fields_user:
                if field not in user:
                    data[field] = 'null'
                else:
                    if str(user[field]) == '':
                        data[field] = 'null'
                    else:
                        data[field] = user[field]

            if 'personal' in user:
                for field in self._need_field_user_personal:
                    if field not in user['personal']:
                        data[field] = 0
                    else:
                        data[field] = user['personal'][field]
            else:
                for field in self._need_field_user_personal:
                    data[field] = 0

            fill_users.append(data)

        self._users = fill_users

    def get_users(self):
        return self._users

    def get_friends(self):
        return self._friends_for_users

    def get_cities(self):
        return self._cities

    def get_countries(self):
        return self._countries
