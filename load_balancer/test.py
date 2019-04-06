import unittest
import load_balancer.robin as robin

class BalancerServer( unittest.TestCase ):

    def setUp(self):
        self.lb = robin.RoundRobin()


    def test1(self):

        nodes = [ ('localhost', i) for i in range(5000, 5005)]

        self.lb.nodes = nodes

        self.assertTrue(self.lb.index == 0)

        for j in range(len(nodes)):
            self.assertTrue(self.lb.get() == nodes[j])