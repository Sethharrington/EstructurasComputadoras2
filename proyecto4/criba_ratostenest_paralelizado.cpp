#include <iostream>
#include <vector> // Para usar std::vector
#include <cmath>  // Para usar sqrt
#include <omp.h>  // Para paralelización con OpenMP

using namespace std;

int main()
{

    omp_set_num_threads(2);         // Limitar a 4 núcleos
    double start = omp_get_wtime(); // Tiempo inicial

    int size = 100;                       // Rango máximo de números
    vector<bool> esPrimo(size + 1, true); // Vector para marcar números primos

    // 0 y 1 no son primos
    esPrimo[0] = false;
    esPrimo[1] = false;

    int limite = sqrt(size);
    cout << "Limite: " << limite << endl; // Imprime el límite

// Criba de Eratóstenes paralelizada
#pragma omp parallel for schedule(dynamic)
    for (int p = 2; p <= limite; p++)
    {
        if (esPrimo[p])
        {
// Marcar los múltiplos de p como no primos
#pragma omp parallel for schedule(dynamic)
            for (int i = p * p; i <= size; i += p)
            {
                if (i <= size)
                { // Asegúrate de que no se sale del rango
                    esPrimo[i] = false;
                }
            }
        }
    }

    // Extraer los números primos
    vector<int> numerosPrimos;
    for (int i = 2; i <= size; i++)
    {
        if (esPrimo[i])
        {
            numerosPrimos.push_back(i);
        }
    }

    double end = omp_get_wtime(); // Tiempo final

    // Imprimir los números primos
    cout << "Números primos entre 1 y " << size << ":\n";
    for (int primo : numerosPrimos)
    {
        cout << primo << " ";
    }
    cout << endl;

    // Tiempo de ejecución
    cout << "Tiempo de ejecución: " << (end - start) << " segundos" << endl;
    return 0;
}