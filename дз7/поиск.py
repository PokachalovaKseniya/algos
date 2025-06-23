def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def backtrack(board, col):
        if col >= n:
            solutions.append([row[:] for row in board])
            return
        for row in range(n):
            if is_safe(board, row, col):
                board[row][col] = 1
                backtrack(board, col + 1)
                board[row][col] = 0

    solutions = []
    board = [[0 for _ in range(n)] for _ in range(n)]
    backtrack(board, 0)
    return solutions

n = int(input())
solutions = solve_n_queens(n)
for solution in solutions:
    for row in solution:
        print(' '.join('Q' if cell == 1 else '.' for cell in row))
    print()