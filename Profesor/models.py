from django.db import models

# Modelo Profesor que representa la tabla
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    clases = models.ManyToManyField('Clase.Clase', related_name='profesores', blank=True)
    

    # Método que define cómo se muestra el profesor en el admin y en el shell
    def __str__(self):
        return f"{self.nombre} {self.apellido}"