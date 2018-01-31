import argparse
# https://docs.python.org/3/library/argparse.html
import requests
# http://docs.python-requests.org/en/latest/user/quickstart/#redirection-and-history
from bs4 import BeautifulSoup
# https://github.com/riramar/hsecscan/blob/master/hsecscan.py


class Scanner(object):
    """Scanner class - accepts dict of args"""
    def __init__(self, arg=None):
        super(Scanner, self).__init__()
        if arg is not None:
            self.arg = arg

        self.verbose = False

    def scan_url(self, url):
        try:
            response = requests.get(url, allow_redirects=True, timeout=0.5)
            # print(response.headers)
            response.raise_for_status()

            return response, None

    # https://stackoverflow.com/questions/6095717
    #   except requests.exceptions.Timeout:
    #    print("Timout")
    # except requests.ConnectionError:
    #    print("problem with local connection")
        except requests.exceptions.HTTPError as err:
            # print(err)
            return None, err
        except Exception as err:
            # print("request errored: " + str(err.message))
            return None, err

    def dir_listing(self, url):
        print('checking ' + url)
        response, error = self.scan_url(url)
        if response:
            if self.verbose is True:
                print(response.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            for node in soup.find_all('title'):
                if "Index" in node.text:
                    print("Listable")
                    return True
                else:
                    return False


def start():
    ips = ['159.89.34.233', '159.89.34.233/list/', '159.89.34.233/nolist/',
           'www.ebay.com', 'stackoverflow.com' 'less.fail/derp', '217.70.184.38']
    listing_ips = ['159.89.34.233/list/', '159.89.34.233/nolist/']

    parser = argparse.ArgumentParser(description="Webserver Scanning Tool")
    parser.add_argument('-i', '--ips', action='store_true', help='''ips to be scanned,''' +
                                                                 '''as comma separated list without protocol(http/s)''')
    print("Welcome to IP scanner 3")
    s = Scanner()
    for ip in ips:
        url = 'http://' + ip
        response, error = s.scan_url(url)
        if response:
            headers = response.headers.get('Server', None)
            if headers:
                print(headers)

        url = 'https://' + ip
        response, error = s.scan_url(url)
        if response:
            headers = response.headers.get('Server', None)
            if headers:
                print(headers)
    for ip in listing_ips:
        url = 'http://' + ip
        listable = s.dir_listing(url)

    print("complete")


if __name__ == "__main__":
    start()
