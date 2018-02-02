import sys
import argparse
import json
# https://docs.python.org/3/library/argparse.html
import requests
# http://docs.python-requests.org/en/latest/user/quickstart/#redirection-and-history
from bs4 import BeautifulSoup
# https://github.com/riramar/hsecscan/blob/master/hsecscan.py


class Scanner(object):
    """Scanner class - accepts dict of args"""
    def __init__(self, args=None):
        super(Scanner, self).__init__()
        if args is not None:
            self.args = args

        if args:
            self.verbose = args.verbose
            self.json = args.json
            self.all = args.all
        else:
            self.verbose = False
            self.json = False
            self.all = False

        if self.verbose:
            print(args)

    def build_results(self, ips=None):
        results = []
        server_types = ['nginx', 'IIS']
        if ips is None:
            ips = self.args.ips
        protocols = ['http://', 'https://']
        for ip in ips:
            for protocol in protocols:
                url = protocol + ip
                result = {}
                result['url'] = url
                response, error = self.scan_url(url)
                if response:
                    server = response.headers.get('Server', None)
                    if server:
                        for server_type in server_types:
                            if server_type in server or self.all:
                                result['server'] = server
                else:
                    if self.verbose:
                        print(error)
                if result.get('server', None):
                    listable = self.is_listable(url)
                    result['listable'] = listable
                    results.append(result)

        return results

    def scan_url(self, url):
        try:
            response = requests.get(url, allow_redirects=True, timeout=2.5)
            # print(response.headers)
            response.raise_for_status()

            return response, None

    # https://stackoverflow.com/questions/6095717
    #   except requests.exceptions.Timeout:
    #    print("Timout")
        except requests.ConnectionError as err:
            print("A Connection Error occured for " + err.request.url)
            if self.verbose:
                print(err)

            return None, err
        except requests.exceptions.HTTPError as err:
            print("A HTTP Error occured for " + err.request.url)
            if self.verbose:
                print(err)

            return None, err
        except Exception as err:
            print("A General Error has occured:")
            raise(err)

    def is_listable(self, url):
        # Tests URL title for the word "Index"
        # TODO: Test with other methods, wget --spider?
        print('checking ' + url)
        response, error = self.scan_url(url)
        if response:
            if self.verbose is True:
                print(response.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            for node in soup.find_all('title'):
                if "Index" in node.text:
                    return True
                else:
                    return False


def start(args=None):

    print("Welcome to IP scanner 3")
    parser = argparse.ArgumentParser(description="Webserver Scanning Tool")
    parser.add_argument('--ips', nargs='*', help='''ips to be scanned,''' +
                        '''as comma separated list without protocol(http/s)''')
    parser.add_argument('--json', action='store_true', help='Output results as Json')
    parser.add_argument('--all', action='store_true', help='Show results for all server types')
    parser.add_argument('--verbose', action='store_true', help='Verbose output for debugging')

    args = parser.parse_args()
    # https://stackoverflow.com/questions/4042452/
    if len(sys.argv) == 1:
        parser.print_help()
    if args.ips is None:
        args.ips = ['159.89.34.233', '159.89.34.233/list/', '159.89.34.233/nolist/',
                    'www.ebay.com', 'www.htps.us', 'helpdesk.htps.us',
                    'stackoverflow.com', 'less.fail', '217.70.184.38']
    s = Scanner(args=args)
    results = s.build_results()

    # results = dict((key, value) for key, value in results if 'IIS' in value)
    if args.json:
        results = json.dumps(results)
        print(results)
    else:
        for result in results:
            print("URL: %s ServerType: %s Listable: %s" % (result['url'], result['server'], result['listable']))

if __name__ == "__main__":
    start()
