import urllib3
import xmltodict
import os.path


class AfishaParser:
    """
    Usage:
    parser = AfishaParser('pathTo.Xml')
    data = parser.parse()
    """

    AFISHA_API = 'http://img.afisha.net/export-vk/'

    def __init__(self, path):

        if os.path.isfile(path):
            f = open(path, 'r')
            data = f.read()
            f.close()

            self.data = data
        else:
            http = urllib3.PoolManager()
            response = http.request('GET', path)
            self.data = response.data

    def parse(self):
        return xmltodict.parse(self.data)


class Companies(AfishaParser):
    """
    Usage:
    parser = Companies(Companies.MAPPING['museum'], 'samara')
    data = parser.parse()
    """

    MAPPING = {
        'concert_hall': 29,
        'sport_building': 30,
        'cinema': 31,
        'museum': 32,
        'theatre': 33,
        'fitness_center': 46,
        'hotel': 47,
        'beauty_shop': 48,
        'shop': 49,
        'club': 50,
        'park': 51,
        'gallery': 52,
        'show_room': 53,
        'educational_center': 60,
        'other': 71
    }

    def __init__(self, cathegory, city='spb'):
        path = self.AFISHA_API + 'companies_' + city + '_' + str(cathegory) + '.xml'
        super().__init__(path)