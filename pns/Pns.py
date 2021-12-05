from game import Move
from game import Board
from time import time_ns
from pns.Node import Node


class Pns:
    VAL_INF = float(10000)

    startTime: float = None

    def __init__(self, resources):
        self.resources = resources

    def run(self, root: 'Move', startingBoard: 'Board', startingPlayer: str) -> dict:
        # Start counting time
        self.startTime = time_ns()

        rootNode = Node(root, startingBoard, startingPlayer)
        self.evaluate(rootNode)
        self.setProofAndDisproofNumbers(rootNode)
        current = rootNode
        while rootNode.proof != 0 and rootNode.disproof != 0 and self.resourcesAvailable():
            mostProving = self.selectMostProvingNode(current)
            self.expandNode(mostProving)
            current = self.updateAncestors(mostProving, rootNode)

        return {'proof': rootNode.proof, 'disproof': rootNode.disproof}

    def evaluate(self, root: 'Node') -> None:
        root.evalGoal()

    def setProofAndDisproofNumbers(self, node: 'Node'):
        if node.isExpanded():
            if node.isOrPlayer is False:
                node.proof = 0
                node.disproof = self.VAL_INF
                for child in node.getChildren():
                    if child.disproof is None or child.proof is None:
                        break
                    node.proof += child.proof
                    node.disproof = min(node.disproof, child.disproof)
            else:
                node.proof = self.VAL_INF
                node.disproof = 0
                for child in node.getChildren():
                    if child.disproof is None or child.proof is None:
                        break
                    node.disproof += child.disproof
                    node.proof = min(node.proof, child.proof)
        else:
            if node.value == node.NODE_WIN:
                node.proof = 0
                node.disproof = self.VAL_INF
            elif node.value == node.NODE_LOSE:
                node.proof = self.VAL_INF
                node.disproof = 0
            else:
                node.proof = 1
                node.disproof = 1

    def selectMostProvingNode(self, node: 'Node') -> 'Node':
        best = node
        while node.isExpanded():
            value = self.VAL_INF
            if node.isOrPlayer is False:
                for child in node.getChildren():
                    if value > child.disproof:
                        best = child
                        value = child.disproof
            else:
                for child in node.getChildren():
                    if value > child.proof:
                        best = child
                        value = child.proof
            node = best

        return node

    def expandNode(self, node: 'Node') -> None:
        node.expandNode()
        for child in node.getChildren():
            self.evaluate(child)
            self.setProofAndDisproofNumbers(child)
            if node.isOrPlayer is False:
                if child.disproof == 0:
                    break
            else:
                if child.proof == 0:
                    break

    def updateAncestors(self, node: 'Node', root: 'Node'):
        while node.isRoot() is False:
            oldProof = node.proof
            oldDisproof = node.disproof
            self.setProofAndDisproofNumbers(node)
            if node.proof == oldProof and node.disproof == oldDisproof:
                return node
            node = node.getParent()
        self.setProofAndDisproofNumbers(root)

        return root

    def resourcesAvailable(self) -> bool:
        return time_ns() - self.startTime <= self.resources
