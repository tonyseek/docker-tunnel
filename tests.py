from subprocess import check_output


def test_installed():
    output = check_output(['docker-tunnel', '--help'])
    assert output.startswith(b'Usage: docker-tunnel')
