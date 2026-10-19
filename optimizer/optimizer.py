from optimizer.constant_folding import fold_constants
from optimizer.constant_propagation import propagate_constants
from optimizer.algebraic_simplification import simplify_algebraic
from optimizer.dead_code_elimination import eliminate_dead_code


class Optimizer:

    def optimize(self, tac):
        # 1. Constant propagation
        tac = propagate_constants(tac)

        # 2. Constant folding
        tac = fold_constants(tac)

        # 3. Algebraic simplification
        tac = simplify_algebraic(tac)

        # 4. Dead code elimination
        tac = eliminate_dead_code(tac)

        return tac