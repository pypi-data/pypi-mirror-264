# Hack4U academy courses library

una biblioteca python para consultar cursos de la academia hack4u

## Cursos disponibles:

-introduccion a linux [15]
-personalizacion de linux [3]
-introduccion al hacking [53]

## Instalacion 

Instala el paquete usando `pip3`:

```python3
pip3 install hack4
```

## Uso básico

## Listar todos los cursos 

```python3
from hack4u import list_courses

from course in list_courses():
     print(course)
```

## obtener un curso por nombre

```python
from hack4u import get_course_by_name

course = get_course_by_name("Introduccion a linux")
print(course)
```

## calcular duracion total de los recursos

```python3
from hack4u.utils import total_duration

print(f"duracion total: {total_duration()} horas")
```
