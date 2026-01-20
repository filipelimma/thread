import threading
from typing import List

SudokuGrid = List[List[int]]

def is_1_to_9(values: List[int]) -> bool:
    if len(values) != 9:
        return False
    s = set(values)
    return s == set(range(1, 10))

def validate_row(grid: SudokuGrid, row: int, results: dict, lock: threading.Lock):
    vals = grid[row]
    ok = is_1_to_9(vals)
    with lock:
        results[f"row-{row}"] = ok

def validate_col(grid: SudokuGrid, col: int, results: dict, lock: threading.Lock):
    vals = [grid[r][col] for r in range(9)]
    ok = is_1_to_9(vals)
    with lock:
        results[f"col-{col}"] = ok

def validate_subgrid(grid: SudokuGrid, box_row: int, box_col: int, results: dict, lock: threading.Lock):
    vals = []
    start_r = box_row * 3
    start_c = box_col * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            vals.append(grid[r][c])
    ok = is_1_to_9(vals)
    with lock:
        results[f"box-{box_row}-{box_col}"] = ok

def validate_sudoku_multithread(grid: SudokuGrid) -> bool:
    if not (isinstance(grid, list) and len(grid) == 9 and all(len(row) == 9 for row in grid)):
        raise ValueError("Grid deve ser uma lista 9x9 de inteiros.")
    
    threads = []
    results = {}
    lock = threading.Lock()

    for r in range(9):
        t = threading.Thread(target=validate_row, args=(grid, r, results, lock))
        threads.append(t)
        t.start()

    for c in range(9):
        t = threading.Thread(target=validate_col, args=(grid, c, results, lock))
        threads.append(t)
        t.start()

    for br in range(3):
        for bc in range(3):
            t = threading.Thread(target=validate_subgrid, args=(grid, br, bc, results, lock))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    return all(results.get(key, False) for key in results)

if __name__ == "__main__":

    valid_grid = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]

    invalid_grid = [
        [5,3,5,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]
    ]

    print("Valid grid is valid?", validate_sudoku_multithread(valid_grid))
    print("Invalid grid is valid?", validate_sudoku_multithread(invalid_grid))
