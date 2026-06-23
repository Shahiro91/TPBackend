from django.db import models 
 
class Alumno(models.Model): 
    nombre = models.CharField(max_length=100) 
    apellido = models.CharField(max_length=100) 
    DNI = models.IntegerField(unique=True)
    Ingresos = models.IntegerField(default=0)  # Número de ingresos al gym
    MontoDeuda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Deuda en pesos
    ultimo_ingreso = models.DateTimeField(null=True, blank=True)
 
    def __str__(self): 
        return f"{self.nombre} {self.apellido}"