import numpy as np
import timeit
from exact_cover import get_all_solutions
from xcover import covers_bool

matrix = np.genfromtxt("test_problem.txt", dtype = np.int32)

def solve_exact_cover():
    sols = get_all_solutions(matrix)
    print("exact_cover nsols:", len(sols))

def solve_xcover():
    sols = list(covers_bool(matrix))
    print("xcover nsols:", len(sols))

time_exact_cover = timeit.timeit(solve_exact_cover, number=5)
time_xcover = timeit.timeit(solve_xcover, number=5)

print(f"exact_cover solve in {time_exact_cover} s")
print(f"xcover solve in {time_xcover} s")
print(f"xcover faster by factor of {time_exact_cover/time_xcover}")




