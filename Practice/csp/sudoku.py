from ortools.sat.python import cp_model

model = cp_model.CpModel()
grid = [[model.NewIntVar(1, 9, f"cell_{r}_{c}") for c in range(9)] for r in range(9)]

for i in range(9):
    model.AddAllDifferent([grid[i][j] for j in range(9)])  # rows
    model.AddAllDifferent([grid[j][i] for j in range(9)])  # columns

for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        model.AddAllDifferent([grid[r][c] for r in range(i, i+3) for c in range(j, j+3)])

# Add a few example clues
clues = [(0, 1, 3), (0, 4, 2), (1, 0, 6), (1, 3, 5), (2, 2, 1)]
for r, c, v in clues:
    model.Add(grid[r][c] == v)

solver = cp_model.CpSolver()
if solver.Solve(model) == cp_model.FEASIBLE:
    for row in grid:
        print([solver.Value(cell) for cell in row])
