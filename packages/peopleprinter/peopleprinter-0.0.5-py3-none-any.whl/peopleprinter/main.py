from .sub_main import InitPrinter
from .manufacturers.KYOCERA.major_kyocera import KyoceraMajor
from .manufacturers.HP.major_hp import HPMajor
from .manufacturers.PANTUM.major_pantum import PantumMajor
from .manufacturers.Xerox.major_xerox import XeroxMajor


class PeoplePrinter(InitPrinter):
    def __init__(self, ip_address):
        super().__init__(ip_address)

    def info(self):
        if self.prod == 'KYOCERA':
            x = KyoceraMajor
        elif self.prod == 'HP':
            x = HPMajor
        elif self.prod == 'PANTUM':
            x = PantumMajor
        elif self.prod == 'XEROX':
            x = XeroxMajor
        else:
            return 'Производитель неизвестен'
        return self.work(x(self.ip_address))


    # Принимает определенный класс производителя принтера
    def work(self, printer):
        return {
                'ip_address': self.ip_address,
                'mac_address': printer.mac(),
                'host_name': printer.host_name(),
                'prod': self.prod,
                'model': printer.model(),
                'locate': self.locate,
                'toner_lvl': printer.toner(),
                'prints_count': printer.prints_count()
                }


if __name__ == "__main__":
    ip = '192.168.2.184'
    printer = PeoplePrinter(ip)
    print(printer.info())


# Возвращает словарь со всей инфой
# {'ip_address': '192.168.1.39', 'mac_address': '00:17:C8:A0:4D:89', 'host_name': 'NetPRN1-AMBRA', 'prod': 'KYOCERA', 'model': 'ECOSYS M2735dn', 'locate': 'Olimp', 'toner_lvl': 75, 'prints_count': 24109}
# получаем данные по ключу printer.full_info()['mac_address']