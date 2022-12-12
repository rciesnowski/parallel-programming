import threading
 
w_ = 0

def sarrus(matrix):
    w = 0
    for j in range(3):
        matrix_mala = [matrix[i] for i in range(9) if i % 3 != j and i >= 3]
        w += ((matrix_mala[0] * matrix_mala[3]) - (matrix_mala[1] * matrix_mala[2])) * matrix[j] * ((-1)**(j+2))
    return w
    
def thread_task(matrix, element, j):
    global w_
    w_ += sarrus(matrix) * element * ((-1)**(j+2))
    
def wyznacznik_dla(matrix):
    global w_
    w_ = 0
    lista_watkow = []
    for j in range(4):
        matrix_mala = [matrix[i] for i in range(16) if i % 4 != j and i >= 4]
        lista_watkow.append(threading.Thread(target = thread_task(matrix_mala, matrix[j], j)))
    for watek in lista_watkow:
        watek.start()
    for watek in lista_watkow:
        watek.join()
    
    macierz = ""
    for i in range(16):
        if i == 0:
            macierz += "\n|"
        elif (i)%4 == 0:
            macierz += " |\n|"
        macierz += " " + str(matrix[i])
        if i == 15:
            macierz += " |"
    print(macierz, "\twyznacznik macierzy = ", w_, "\n")
        
wyznacznik_dla([3, 2, 1, 2, 4, 3, 2, 1, 1, 2, 2, 5, 1, 6, 0, 1])
wyznacznik_dla([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 5, 0, 0, 0, 0])
wyznacznik_dla([0, 1, 2, 7, 1, 2, 3, 4, 5, 6, 7, 8, -1, 1, -1, 1])
