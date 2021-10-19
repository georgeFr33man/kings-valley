from ai_algorithms.AiAlgorithmInterface import AiAlgorithmInterface


class MinMax(AiAlgorithmInterface):
    def __init__(self, depth: int):
        super().__init__()
        self.depth = depth
