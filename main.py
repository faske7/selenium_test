from check_website  import SauceDemo
from config import *



if __name__ == '__main__':
    test = SauceDemo(
        login=login,
        password=password,
        item=item,
        first_name=first_name,
        last_name=last_name,
        zip_code=zip_code
    )
    test.start()