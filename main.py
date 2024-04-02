import random
import numpy as np
import multiprocessing as mp
import time

def multiply_elements(index, matrix_a, matrix_b):
    row, col = index
    element_sum = sum(matrix_a[row][k] * matrix_b[k][col] for k in range(len(matrix_b)))
    return (row, col), element_sum

def multiply_matrices_parallel(matrix_a, matrix_b, result_queue, stop_event):
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Number of columns in matrix A must be equal to number of rows in matrix B")

    indices = [(i, j) for i in range(len(matrix_a)) for j in range(len(matrix_b[0]))]

    try:
        with mp.Pool() as pool:
            results = [pool.apply_async(multiply_elements, args=(index, matrix_a, matrix_b)) for index in indices]
            for result in results:
                if stop_event.is_set():
                    break
                result_queue.put(result.get())
    except Exception as e:
        print(f"Error multiplying matrices: {e}")

def create_random_matrix(size):
    return np.random.randint(0, 10, size=(size, size))

if __name__ == '__main__':
    matrix_size = int(input("Enter the size of square matrices (one number): "))
    stop_event = mp.Event()
    result_queue = mp.Queue()

    matrix_a = create_random_matrix(matrix_size)
    matrix_b = create_random_matrix(matrix_size)

    try:
        multiply_matrices_parallel(matrix_a, matrix_b, result_queue, stop_event)

        time.sleep(2)
        stop_event.set()

        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        print("Matrix A:")
        print(matrix_a)
        print("\nMatrix B:")
        print(matrix_b)
        print("\nResult:")
        result_matrix = np.zeros((matrix_size, matrix_size))
        for index, result in results:
            i, j = index
            result_matrix[i][j] = result
        print(result_matrix)
    except ValueError as e:
        print(e)
