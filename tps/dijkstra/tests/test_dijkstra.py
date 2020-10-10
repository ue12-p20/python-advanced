from unittest import TestCase

from dijkstra import parse_graph1, parse_graph2
from dijkstra import number_vertices1, reachables1
from dijkstra import shortest_distance1, shortest_path1

def fetch_thrones():
    url = "https://raw.githubusercontent.com/pupimvictor/NetworkOfThrones/master/stormofswords.csv"
    cache = "data/thrones.csv"
    from pathlib import Path
    if not Path(cache).exists():
        get_request = requests.get(url)
        text_data = get_request.text
        with Path(cache).open('w') as output:
            for line in text_data.split("\n")[1:]:
                print(line, file=output)
    return cache


class Tests(TestCase):

    def test_parse(self):
        g1 = parse_graph1("data/graph.csv")
        g2 = parse_graph2("data/graph.csv")
        assert g1 == g2

    def test_number_vertices(self):
        g1 = parse_graph1("data/graph.csv")
        cache = fetch_thrones()
        thrones = parse_graph1(cache)

        self.assertEqual(number_vertices1(g1), 6)
        self.assertEqual(number_vertices1(thrones), 107)

    def test_reachables(self):
        reach = parse_graph1("data/reach.csv")

        all = {'a', 'b', 'c', 'd', 'e', 'f'}
        cycle = {'e', 'f'}

        assert reachables1(reach, 'a') == all
        assert reachables1(reach, 'b') == all
        assert reachables1(reach, 'c') == all
        assert reachables1(reach, 'd') == all
        assert reachables1(reach, 'e') == cycle
        assert reachables1(reach, 'f') == cycle

    def test_distance(self):
        G = parse_graph1("data/graph.csv")

        assert shortest_distance1(G, 'a', 'f') == 23
        assert shortest_distance1(G, 'a', 'e') == 20
        assert shortest_distance1(G, 'c', 'b') is None

        G2 = parse_graph1("data/graph2.csv")

        assert shortest_distance1(G2, 'v1', 'v6') == 5
        assert shortest_distance1(G2, 'v6', 'v1') is None

    def test_path(self):
        G = parse_graph1("data/graph.csv")

        assert shortest_path1(G, 'a', 'f') == (23, ['a', 'c', 'f'])
        assert shortest_path1(G, 'a', 'e') == (20, ['a', 'd', 'e'])

        G2 = parse_graph1("data/graph2.csv")

        assert shortest_distance1(G2, 'v1', 'v6') == 5
        assert shortest_distance1(G2, 'v6', 'v1') is None

    def test_thrones(self):
        cache = fetch_thrones()
        thrones = parse_graph1(cache)

        self.assertEqual(number_vertices1(thrones), 107)
        self.assertEqual(shortest_distance1(thrones, 'Daenerys', 'Karl'), 38)