# Matrix Multiplication

A Python program that performs matrix multiplication both sequentially and in parallel, leveraging multiple processors when available.

## Features

- **Sequential Matrix Multiplication**: A standard implementation for multiplying matrices.
- **Parallel Matrix Multiplication**: Uses Python's `multiprocessing` to divide the work across available CPUs.
- **Performance Evaluation**: Compares the time taken for both sequential and parallel methods.

## Prerequisites

Make sure you have Python 3.x installed.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/mbm6448/parallel_matmul.git
cd matmul
```

2. Run the program:

```bash
python matmul.py --rows 200 --cols 200 --eval-runs 1
```

### Command Line Arguments

- `--rows`: Number of rows in Matrix A. Default is `200`.
- `--cols`: Number of columns in Matrix A (also rows in Matrix B). Default is `200`.
- `--eval-runs`: Number of evaluation runs for averaging the performance. Default is `1`.

## Results

The program outputs:

- Average time taken by the sequential method.
- Average time taken by the parallel method.
- Speedup achieved with the parallel method.
- Efficiency of the parallel method.

## Contribute

Feel free to raise issues, send PRs, or suggest improvements.

## License

MIT License. See `LICENSE` for more information.
