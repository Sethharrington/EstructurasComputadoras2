#include <iostream>
#include <vector> // Para usar std::vector
#include <cmath>  // Para usar sqrt

using namespace std;

int main()
{
    double start = clock(); // Tiempo inicial

    int size = 100;                       // Rango máximo de números
    vector<bool> esPrimo(size + 1, true); // Vector para marcar números primos
    esPrimo[0] = esPrimo[1] = false;      // 0 y 1 no son primos

    int limite = sqrt(size);
    cout << "Limite: " << limite << endl; // Imprime el límite

    // Criba de Eratóstenes
    for (int p = 2; p <= limite; p++)
    {
        if (esPrimo[p])
        {
            // Marcar los múltiplos de p como no primos
            for (int i = p * p; i <= size; i += p)
            {
                esPrimo[i] = false;
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

    double end = clock(); // Tiempo final

    // Imprimir los números primos
    cout << "Números primos entre 1 y " << size << ":\n";
    for (int primo : numerosPrimos)
    {
        cout << primo << " ";
    }
    cout << endl;

    // Tiempo de ejecución
    cout << "Tiempo de ejecución: " << (end - start) / CLOCKS_PER_SEC << " segundos" << endl;
    return 0;
}