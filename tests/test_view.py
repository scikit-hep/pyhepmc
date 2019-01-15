from test_basic import prepare_event
from pyhepmc_ng.view import to_dot

def test_dot():
    evt = prepare_event()
    d = to_dot(evt)
    print(d)
    d.render(view=True)

if __name__ == '__main__':
    test_dot()