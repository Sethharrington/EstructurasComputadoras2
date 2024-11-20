#include <iostream>
#include <string>
using namespace std;

int FindNumber(vector<int> arrayNumber, int numberToSearch)
{
    // To store the index of numberToSearch
    int Index = 0;

    // Traverse the Set
    int size = arrayNumber.size();
    // int size = sizeof(arrayNumber) / sizeof(arrayNumber[0]);
    for (int i = 0; i < size; i++)
    {
        if (arrayNumber[i] == numberToSearch)
            return Index;
        Index++;
    }
    return -1;
}

int main()
{
    vector<int> numerosPrimos;
    int size = 100;
    int arraySize = size;
    int numeros[size];

    // Inicializar el arreglo
    for (int i = 0; i < size; i++)
    {
        numerosPrimos.push_back(i + 1);
        numeros[i] = i + 1;
        // cout << numerosPrimos[i] << "\n";
    }
    ///////////////////////////////
    //   Evaluar numeros primos  //
    ///////////////////////////////

    // El primer numero primo es el 2
    for (int numeroPrimo = 1; numeroPrimo < arraySize; numeroPrimo++)
    {
        // Se multiplica el numero primo por si mismo para eliminar los numeros no primos
        int startNumber = numerosPrimos[numeroPrimo] * numerosPrimos[numeroPrimo];

        // Si el numero no primo es mayor que el tamaño del arreglo, se termina el ciclo
        if (startNumber > size)
            break;

        // cout << "\n\n startNumber: " << startNumber << " numero primo: " << numeros[numeroPrimo] << "\n";

        // Eliminar numeros no primos
        int nextNumeroNoPrimo = 0;
        for (int i = numeroPrimo + 1; i < arraySize; i++)
        {
            nextNumeroNoPrimo = (i * numeros[numeroPrimo]) - 1;
            if (nextNumeroNoPrimo > size)
                break;
            // cout << "i: " << i << " Number: " << numeros[nextNumeroNoPrimo] << "\n";
            if (FindNumber(numerosPrimos, nextNumeroNoPrimo + 1) != -1)
            {
                numerosPrimos.erase(find(numerosPrimos.begin(), numerosPrimos.end(), nextNumeroNoPrimo + 1));
            }
            // numerosPrimos.erase(find(numerosPrimos.begin(), numerosPrimos.end(), numeros[nextNumeroNoPrimo]));
        }
        arraySize = numerosPrimos.size();
    }
    numerosPrimos.erase(find(numerosPrimos.begin(), numerosPrimos.end(), 1));

    // Imprimir numeros primos
    for (int i = 0; i < numerosPrimos.size(); i++)
    {
        cout << numerosPrimos[i] << "\n";
    }
    return numerosPrimos.size();
}
