
def test_scanner():
    from IPScanner import Scan_Tools
    s = Scan_Tools.Scanner()

    assert s is not None, "Scan_Tools did not instantiate"


def test_start():
    from IPScanner import Scan_Tools
    s = Scan_Tools.Scanner()
    result = s.build_results(ips=['google.com'])

    assert result is not None, "build_result() returned None, Expected Value"


def test_listable():
    from IPScanner import Scan_Tools
    s = Scan_Tools.Scanner()
    result = s.is_listable(url="http://159.89.34.233/list/")

    assert result is True, "is_listable() returned False"
