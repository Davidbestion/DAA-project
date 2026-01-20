from instances.predefined import INSTANCE_TINY
from solver.models.brute import BruteForceSolver


tiny_instance = INSTANCE_TINY
print("Instancia Pequeña:")
# print(tiny_instance.summary())
tiny_instance.display()


solver = BruteForceSolver()
solution = solver.solve(tiny_instance)
print("\nSolución encontrada por BruteForceSolver:")
print(solution)
