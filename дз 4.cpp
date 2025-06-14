#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <iomanip>
#include <cstdlib>
#include <ctime>

std::vector<int> create_random_vector(size_t size) {
    std::vector<int> vec(size);
    for (size_t i = 0; i < size; ++i) {
        vec[i] = rand() % 100000;
    }
    return vec;
}

int partition(std::vector<int>& vec, int left, int right) {
    int random_pivot_index = left + rand() % (right - left + 1);
    std::swap(vec[random_pivot_index], vec[right]);

    int pivot_value = vec[right];
    int i = (left - 1);

    for (int j = left; j < right; j++) {
        if (vec[j] <= pivot_value) {
            i++;
            std::swap(vec[i], vec[j]);
        }
    }
    std::swap(vec[i + 1], vec[right]);
    return (i + 1);
}

void sequential_qsort(std::vector<int>& vec, int left, int right) {
    if (left < right) {
        int pivot_index = partition(vec, left, right);
        sequential_qsort(vec, left, pivot_index - 1);
        sequential_qsort(vec, pivot_index + 1, right);
    }
}

const int PARALLEL_THRESHOLD = 2048;

void parallel_qsort_recursive(std::vector<int>& vec, int left, int right) {
    if (left < right) {
        if ((right - left) < PARALLEL_THRESHOLD) {
            sequential_qsort(vec, left, right);
        }
        else {
            int pivot_index = partition(vec, left, right);

#pragma omp task
            {
                parallel_qsort_recursive(vec, left, pivot_index - 1);
            }

#pragma omp task
            {
                parallel_qsort_recursive(vec, pivot_index + 1, right);
            }
        }
    }
}

void run_parallel_qsort(std::vector<int>& vec, int thread_count) {
#pragma omp parallel num_threads(thread_count)
    {
#pragma omp single
        {
            parallel_qsort_recursive(vec, 0, vec.size() - 1);
        }
    }
}

int main() {
    srand(time(0));
    setlocale(LC_ALL, "Russian");

    std::vector<int> sizes_to_test = { 100, 1000, 10000, 20000, 30000, 40000, 50000 };
    std::vector<int> thread_counts = { 2, 4, 8 };

    std::cout << std::left << std::setw(18) << "Размер массива"
        << std::setw(18) << "БС (сек)"
        << std::setw(24) << "БС_П 2 потока (сек)"
        << std::setw(24) << "БС_П 4 потока (сек)"
        << std::setw(24) << "БС_П 8 потока (сек)" << std::endl;
    std::cout << std::fixed << std::setprecision(8);

    for (int size : sizes_to_test) {
        std::cout << std::left << std::setw(18) << size;

        std::vector<int> base_vec = create_random_vector(size);
        std::vector<int> seq_vec = base_vec;

        auto start_time = std::chrono::high_resolution_clock::now();
        sequential_qsort(seq_vec, 0, seq_vec.size() - 1);
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> seq_duration = end_time - start_time;

        std::cout << std::setw(18) << seq_duration.count();

        for (int threads : thread_counts) {
            std::vector<int> par_vec = base_vec;

            start_time = std::chrono::high_resolution_clock::now();
            run_parallel_qsort(par_vec, threads);
            end_time = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> par_duration = end_time - start_time;

            std::cout << std::setw(24) << par_duration.count();
        }
        std::cout << std::endl;
    }

    return 0;
}