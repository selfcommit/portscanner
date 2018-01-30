# import urllib2
import requests
# http://docs.python-requests.org/en/latest/user/quickstart/#redirection-and-history
# https://github.com/riramar/hsecscan/blob/master/hsecscan.py

ips = ['less.fail/derp', '217.70.184.38']


def start():
    print("Welcome to IP scanner")


def scan_ip(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=0.5)
        print(response.headers)
        response.raise_for_status()
        r.raise_for_status()
        return response

    # https://stackoverflow.com/questions/6095717
    #except requests.exceptions.Timeout:
    #    print("Timout")
    #except requests.ConnectionError:
    #    print("problem with local connection")
    except requests.exceptions.HTTPError as err:
        print(err)
    except Exception as e:
        print("request errored: " + str(e.message))


#for ip in ips:
#    url = 'http://' + ip
#    scan_ip(url)
#    url = 'https://' + ip
#    scan_ip(url)

#print("complete")