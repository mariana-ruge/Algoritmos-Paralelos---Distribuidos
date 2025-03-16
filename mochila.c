#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>
#include <time.h>

#define MAX_N 100
#define MAX_W 1000
#define NUM_ITEMS 20
#define MAX_VALUE 1000
#define MAX_WEIGHT 50

#define FILE_NAME "execution_times.txt" // Definir correctamente el nombre del archivo

int K[MAX_N + 1][MAX_W + 1];
int val[NUM_ITEMS];
int wt[NUM_ITEMS];

void generate_random_data() {
    srand(time(NULL));
    for (int i = 0; i < NUM_ITEMS; i++) {
        val[i] = rand() % MAX_VALUE + 1;
        wt[i] = rand() % MAX_WEIGHT + 1;
    }
}

void knapsack(int W, int wt[], int val[], int n, int rank, int size, double *exec_time, int *workload) {
    int rows_per_proc = n / size;
    int start = rank * rows_per_proc + 1;
    int end = (rank == size - 1) ? n : start + rows_per_proc;
    *workload = end - start + 1;
    
    double start_time = MPI_Wtime();
    for (int i = start; i <= end; i++) {
        for (int w = 0; w <= W; w++) {
            if (wt[i - 1] <= w)
                K[i][w] = (val[i - 1] + K[i - 1][w - wt[i - 1]] > K[i - 1][w]) ? val[i - 1] + K[i - 1][w - wt[i - 1]] : K[i - 1][w];
            else
                K[i][w] = K[i - 1][w];
        }
    }
    double end_time = MPI_Wtime();
    *exec_time = end_time - start_time;
    
    if (rank != 0)
        MPI_Send(&K[end][0], W + 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    else {
        for (int p = 1; p < size; p++) {
            int proc_start = p * rows_per_proc + 1;
            int proc_end = (p == size - 1) ? n : proc_start + rows_per_proc;
            MPI_Recv(&K[proc_end][0], W + 1, MPI_INT, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    }
}

int main(int argc, char *argv[]) {
    generate_random_data();
    int W = 50;
    int n = NUM_ITEMS;
    
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    double exec_time;
    int workload;
    knapsack(W, wt, val, n, rank, size, &exec_time, &workload);
    
    double exec_times[size];
    MPI_Gather(&exec_time, 1, MPI_DOUBLE, exec_times, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        FILE *file = fopen(FILE_NAME, "w");
        for (int i = 0; i < size; i++) {
            fprintf(file, "%d %f\n", i + 1, exec_times[i]);
        }
        fclose(file);
        
        // Visualización con gnuplot
        FILE *gnuplot = popen("gnuplot -persistent", "w");
        fprintf(gnuplot, "set terminal qt size 800,600\n");
        fprintf(gnuplot, "set title 'Eficiencia del paralelismo'\n");
        fprintf(gnuplot, "set xlabel 'Número de procesos'\n");
        fprintf(gnuplot, "set ylabel 'Tiempo de ejecución (s)'\n");
        fprintf(gnuplot, "set grid\n");
        fprintf(gnuplot, "plot '%s' using 1:2 with linespoints title 'Tiempo de ejecución'\n", FILE_NAME);
        pclose(gnuplot);
    }
    
    MPI_Finalize();
    return 0;
}
