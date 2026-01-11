from generator.random_gen import generate_small_instance
from instances.predefined import INSTANCE_TINY

tiny_instance = INSTANCE_TINY
print("Instancia Pequeña:")
# print(tiny_instance.summary())
tiny_instance.display()

from solver.models.brute import BruteForceSolver

solver = BruteForceSolver()
solution = solver.solve(tiny_instance)
print("\nSolución encontrada por BruteForceSolver:")
print(solution)