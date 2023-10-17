#!/usr/bin/env python3

import random
import time
import math
import multiprocessing as mp
import argparse

class MatrixMultiplier:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def seq_matrix_multiply(self):
        A, B = self.A, self.B
        num_rows_A = len(A)
        num_cols_A = len(A[0])
        num_rows_B = len(B)
        num_cols_B = len(B[0])
        if num_cols_A != num_rows_B:
            raise ArithmeticError('Invalid dimensions; Cannot multiply {}x{}*{}x{}'.format(num_rows_A, num_cols_A, num_rows_B, num_cols_B))
        C = [[0] * num_cols_B for i in range(num_rows_A)]
        for i in range(num_rows_A):
            for j in range(num_cols_B):
                for k in range(num_cols_A):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def par_matrix_multiply(self):
        A, B = self.A, self.B
        num_rows_A = len(A)
        num_cols_A = len(A[0])
        num_rows_B = len(B)
        num_cols_B = len(B[0])
        if num_cols_A != num_rows_B:
            raise ArithmeticError('Invalid dimensions; Cannot multiply {}x{}*{}x{}'.format(num_rows_A, num_cols_A, num_rows_B, num_cols_B))
        if num_rows_A * num_cols_B < 25_000:
            return self.seq_matrix_multiply()
        num_workers = mp.cpu_count()
        chunk_size = math.ceil(num_rows_A/num_workers)
        C_1D = mp.RawArray('d', num_rows_A * num_cols_B)
        workers = []
        for w in range(num_workers):
            row_start_C = min(w * chunk_size, num_rows_A)
            row_end_C = min((w + 1) * chunk_size, num_rows_A)
            workers.append(mp.Process(target=self._par_worker, args=(A, B, C_1D, row_start_C, row_end_C)))
        for w in workers:
            w.start()
        for w in workers:
            w.join()
        C_2D = [[0] * num_cols_B for i in range(num_rows_A)]
        for i in range(num_rows_A):
            for j in range(num_cols_B):
                C_2D[i][j] = C_1D[i*num_cols_B + j]
        return C_2D

    @staticmethod
    def _par_worker(A, B, C_1D, row_start_C, row_end_C):
        for i in range(row_start_C, row_end_C):
            for j in range(len(B[0])):
                for k in range(len(A[0])):
                    C_1D[i*len(B[0]) + j] += A[i][k] * B[k][j]

def generate_random_matrix(rows, cols):
    return [[random.random() for _ in range(cols)] for _ in range(rows)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=200)
    parser.add_argument('--cols', type=int, default=200)
    parser.add_argument('--eval-runs', type=int, default=1)
    args = parser.parse_args()

    A = generate_random_matrix(args.rows, args.cols)
    B = generate_random_matrix(args.cols, args.rows)

    multiplier = MatrixMultiplier(A, B)

    sequential_result = multiplier.seq_matrix_multiply()
    sequential_time = sum(time.perf_counter() - start for _ in range(args.eval_runs) for start in [time.perf_counter()] if multiplier.seq_matrix_multiply()) / args.eval_runs

    parallel_result = multiplier.par_matrix_multiply()
    parallel_time = sum(time.perf_counter() - start for _ in range(args.eval_runs) for start in [time.perf_counter()] if multiplier.par_matrix_multiply()) / args.eval_runs

    if sequential_result != parallel_result:
        raise Exception('Results do not match.')

    print(f'Average Sequential Time: {sequential_time*1000:.2f} ms')
    print(f'Average Parallel Time: {parallel_time*1000:.2f} ms')
    print(f'Speedup: {sequential_time/parallel_time:.2f}')
    print(f'Efficiency: {100*(sequential_time/parallel_time)/mp.cpu_count():.2f}%')

