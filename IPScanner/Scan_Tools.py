import sys
import json
import argparse
# https://docs.python.org/3/library/argparse.html
import requests
# http://docs.python-requests.org/en/latest/user/quickstart/#redirection-and-history
from bs4 import BeautifulSoup


class Scanner(object):
    """Scanner class - optionally accepts argsparse object"""
    def __init__(self, args=None):
        super(Scanner, self).__init__()
        if args is not None:
            self.args = args

        if args:
            self.verbose = args.verbose
            self.json = args.json
            self.all = args.all
            self.server_types = args.servers
        else:
            self.verbose = False
            self.json = False
            self.all = False
            self.server_types = ['nginx/1.2', 'IIS/7.0']

        if self.verbose:
            print(args)

    def build_results(self, ips=None):
        results = []
        server_types = self.server_types
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
            if self.verbose:
                print(response.headers)

            response.raise_for_status()

            return response, None

        except requests.exceptions.Timeout as err:
            if self.verbose:
                print("Connection Attempt Timed out for " + err.request.url)
            return None, err

        except requests.ConnectionError as err:
            if self.verbose:
                print("A Connection Error occured for " + err.request.url)
                print(err)

            return None, err
        except requests.exceptions.HTTPError as err:
            if self.verbose:
                print("A HTTP Error occured for " + err.request.url)
                print(err)

            return None, err

        except Exception as err:
            print("A General Error has occured:")
            raise(err)

    def is_listable(self, url):
        # Tests URL title for the word "Index"
        # TODO: Test with other methods, wget --spider?
        if self.verbose:
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


def start(ips=None):

    # https://stackoverflow.com/questions/12151306
    parser = argparse.ArgumentParser(description="Webserver Scanning Tool",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ip_group = parser.add_mutually_exclusive_group()
    ip_group.add_argument('--ips', nargs='*', help='''ips to be scanned,''' +
                          '''as comma separated list without protocol(http/s)''')
    ip_group.add_argument('--csv', nargs='?', help='string of path to local CSV file of ips to be scanned')

    server_group = parser.add_mutually_exclusive_group()
    server_group.add_argument('--servers', nargs='*', default=['nginx/1.2', 'IIS/7.0'],
                              help='Define Server types in comma separated list ' + 'Ex: --servers nginx, nginx/1, IIS')
    server_group.add_argument('--all', action='store_true', help='Show results for all server types.')

    parser.add_argument('--json', action='store_true', help='Output results as Json')
    parser.add_argument('--verbose', action='store_true', help='Verbose output for debugging')

    args = parser.parse_args()
    ips = args.ips

    if args.csv:  # overides --ips
        with open(args.csv, 'r') as csvfile:
            data = csvfile.read()

        args.ips = data.split(',')

    # https://stackoverflow.com/questions/4042452/
    if len(sys.argv) == 1:
        parser.print_help()

    if ips is None and args.ips is None:
        exit()  # prevents build results without provided ips during testing

    s = Scanner(args=args)
    results = s.build_results()

    if args.json:
        results = json.dumps(results)
        print(results)
    else:
        for result in results:
            print("URL: %s ServerType: %s Listable: %s" % (result['url'], result['server'], result['listable']))

if __name__ == "__main__":
    start()
