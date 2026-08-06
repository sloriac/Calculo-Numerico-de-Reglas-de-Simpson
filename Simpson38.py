import math #Se utiliza para las funciones trigonométricas
import time

#El :.6 es para obtener 6 decimales

#Crea una variable que contenga los posibles caracteres que se utilizarán para aproximar el valor de la integral
entorno_matematico = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

#Toma el string ingresado y lo convierte a caracteres matemáticos a resolver
def crear_funcion(expresion):
    def funcion_evaluable(x):
        #Asignar el valor actual de x (variable) al entorno
        entorno_matematico['x'] = x
        try:
            #Evaluamos el string matemático
            return eval(expresion, {"__builtins__": None}, entorno_matematico)
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión '{expresion}' con x={x}. Debido a: {e}")

    return funcion_evaluable

#Función que ejecuta el método principal de la Regla de Simpson 3/8
def simpson_3_8(funcion_fx, a, b, n):

    #Formula para obtener el valor de h.
    #h es el ancho de cada subintervalo a evaluar.
    h = (b - a) / n

    print(f"\nPaso 2: Obtener h\n({b} - {a}) / {n} = {h}")

    #Generar los puntos x0, x1, ..., xn
    x_valores = [a + i * h for i in range(n + 1)] #Límite inferior + índice de x * ancho del subintervalo
    #Evaluar todos estos puntos en la funcion "funcion_fx"
    f_valores = [funcion_fx(xi) for xi in x_valores]

    print("\nPaso 3: Obtener los puntos x_i y evaluarlos en f(x_i):")
    for i in range(n + 1):
        #Imprime el número de índice de x, el valor de la misma, y la función evaluada en ese punto
        print(f"  x_{i} = {x_valores[i]:.6f}   f(x_{i}) = {f_valores[i]:.6f}")

    #Aplicar sumatoria del método Simpson 3/8, desde 0 hasta n
    sumatoria = f_valores[0] + f_valores[n]

    print("\nPaso 4: Clasificación de cada punto interno por coeficientes")
    for i in range(1, n): #Desde 1 hasta n
        if i % 3 == 0:
            coeficiente = 2
        else:
            coeficiente = 3

        sumatoria += coeficiente * f_valores[i]
        #Mostrar el coeficiente, y la evaluación en f(x)
        print(f"  x_{i}: coeficiente {coeficiente}  =  {coeficiente} * f(x_{i}) = {coeficiente * f_valores[i]:.6f}")

    #Variable que contiene toda la operación del método Simpson 3/8
    integral = (3 * h / 8) * sumatoria
    print(f"\nPaso 5: Conseguir la suma total ponderada = {sumatoria:.6f}")

    #Muestra el proceso de solución, juntando los pasos anteriores y dando el resultado al final
    print(f"Paso 6: Integral = (3h/8) * sumatoria = (3*{h:.6f}/8) * {sumatoria:.6f} = {integral:.6f}")

    return integral

#Función para calcular el error con respecto al valor exacto
def calcular_error(valor_aproximado, valor_exacto):

    #Cálculo del error tipo absoluto (numérico)
    error_absoluto = abs(valor_exacto - valor_aproximado)

    #Cálculo del error tipo relativo (porcentaje)
    if valor_exacto != 0:
        error_relativo = (error_absoluto / abs(valor_exacto)) * 100
    else:
        error_relativo = 0.0
    return error_absoluto, error_relativo


#Función para medir el tiempo de ejecución del programa, además de la cantidad de iteraciones realizadas durante la ejecución del mismo
def ejecutar_y_medir(funcion_fx, a, b, n):
    
    inicio_tiempo = time.perf_counter()
    resultado = simpson_3_8(funcion_fx, a, b, n)
    fin_tiempo = time.perf_counter()

    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    iteraciones = n
    return resultado, tiempo_ejecucion, iteraciones

#Función para solicitar la integral a resolver mediante Simpson 3/8
def solicitar_funcion():

    print("\n--- Ingresar función a integrar ---")
    print("Utilice 'x' como variable y sintaxis de Python (ej: x**2, sin(x), exp(x))")

    while True:
        nueva_f = input("Ingrese la función f(x): ").strip()
        nueva_F = input("Ingrese la antiderivada exacta F(x) (utilizada para realizar el cálculo del error): ").strip()

        if not nueva_f or not nueva_F:
            print("\nDebe ingresar ambas expresiones. Intente de nuevo. . .\n")
            continue

        try:
            # Validar que las funciones sirvan probándolas con x=1
            temp_f = crear_funcion(nueva_f)
            temp_F = crear_funcion(nueva_F)
            temp_f(1)
            temp_F(1)

            print("\nFunción y antiderivada cargadas correctamente.")
            return nueva_f, nueva_F, temp_f, temp_F
        except Exception as e:
            print(f"\nHubo un error con la sintaxis de la función: {e}")
            print("Intente de nuevo. . .\n")

#Función que realiza un menú con las opciones para ingresar o cambiar la integral, y su antiderivada, función para calcular la integral y el error, y función para salir del programa
def menu_principal():
    #Inicializar las funciones vacías para poder editarlas a gusto
    expr_f = None
    expr_F = None
    funcion_fx = None
    F_func = None

    while True:
        print("\n    MENÚ PRINCIPAL - MÉTODO DE SIMPSON 3/8")
        print("================================================")
        print(f"Función actual f(x) : {expr_f if expr_f else '(Vacío)'}")
        print(f"Antiderivada F(x)   : {expr_F if expr_F else '(Vacío)'}")
        print("================================================")
        print("1. Ingresar / cambiar la función a integrar")
        print("2. Calcular integral con la función actual")
        print("3. Salir")
        print("================================================")

        opcion = input("Elige una opción (1, 2 o 3): ")

        if opcion == '1':
            expr_f, expr_F, funcion_fx, F_func = solicitar_funcion()

        elif opcion == '2':
            if funcion_fx is None or F_func is None:
                print("\nTodavía no se ha ingresado ninguna función, utilice la opción 1 para ingresarla.")
                continue

            try:
                print("\n--- Ingrese los parámetros de integración ---")
                A = float(input("Límite inferior (a): "))
                B = float(input("Límite superior (b): "))
                N = int(input("Número de particiones (n, múltiplo de 3): "))

                if N <= 0:
                    print("\nError: El número de particiones debe ser mayor a 0.")
                    continue
                if N % 3 != 0:
                    print("\nError: El número de particiones (n) debe ser múltiplo de 3.")
                    continue

                print("\nCálculo de la integral\n")

                #Ejecutar método
                resultado_aprox, tiempo, cantidad_iteraciones = ejecutar_y_medir(funcion_fx, A, B, N)

                #Calcular valor exacto usando la antiderivada evaluada en los límites
                valor_exacto = F_func(B) - F_func(A)
                err_abs, err_rel = calcular_error(resultado_aprox, valor_exacto)

                #Mostrar resultados
                print("================================================")
                print("RESULTADOS FINALES")
                print("================================================")
                print(f"Integral Aproximada : {resultado_aprox:.6f}")
                print(f"Valor Exacto        : {valor_exacto:.6f}")
                print(f"Error Absoluto      : {err_abs:.6e}")
                print(f"Error Relativo      : {err_rel:.6f}%")
                print(f"Iteraciones (n)     : {cantidad_iteraciones}")
                print(f"Tiempo de ejecución : {tiempo:.6f} segundos")
                print("================================================")

                input("\nPresiona Enter para continuar...")

            except ValueError as e:
                print(f"\nError de valor: {e}")
            except Exception as e:
                print(f"\nOcurrió un error: {e}")

        elif opcion == '3':
            print("\nSaliendo del programa")
            break

        else:
            print("\nOpción no válida. Ingresa 1, 2 ó 3.")

if __name__ == "__main__":
    menu_principal()