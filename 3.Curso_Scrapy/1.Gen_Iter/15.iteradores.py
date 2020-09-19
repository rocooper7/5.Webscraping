my_list = [1, 2, 3, 4, 5]   #Iterable, como funciona for 
my_iter = iter(my_list)    #Se convierte en iterador

print(type(my_iter))

# Extraer los elementos

print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))