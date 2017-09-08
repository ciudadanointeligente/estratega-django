from django.db import models
from django.contrib.auth.models import User


class Estrategia(models.Model):
    dueno = models.ForeignKey(User, null=True)
    titulo = models.CharField(max_length=200, default='')
    problematica = models.TextField(default='')
    causas = models.TextField(default='')
    solucionpolitica = models.TextField(default='')
    objetivos = models.ManyToManyField('Objetivo')

    def __str__(self):
        return self.titulo

    def has_problematica(self):
        if self.problematica == '':
            return False
        else:
            return True

    def has_causas(self):
        if self.causas == '':
            return False
        else:
            return True

    def has_solucionpolitica(self):
        if self.solucionpolitica == '':
            return False
        else:
            return True

    def has_objetivos(self):
        objetivo = self.get_objetivo_prioritario()

        if (objetivo is None) or (objetivo == ''):
            return False
        else:
            return True

    def has_resultadosintermedios(self):
        return False

    def has_factoreshabilitantes(self):
        return False

    def has_barreras(self):
        return False

    def has_actoresrelevantes(self):
        return False

    # Este metodo chequea el contenido de la estrategia y
    # devuelve un texto que indica que parte de la estrategia
    # es la que debiera ser completada en el siguiente paso.
    #
    # El metodo es usado por el menu de arriba del flujo principal
    # (el flujo que se usa para crear estrategias) para saber que 
    # partes del menu habilitar en cada etapa. 
    def me_next(self):
        if not self.has_problematica():
            me_next = 'problematica'
        elif not self.has_causas():
            me_next = 'causas'
        elif not self.has_solucionpolitica():
            me_next = 'solucionpolitica'
        elif not self.has_objetivos():
            me_next = 'objetivos'
        elif not self.has_resultadosintermedios():
            me_next = 'resultadosintermedios'
        elif not self.has_factoreshabilitantes():
            me_next = 'factoreshabilitantes'
        elif not self.has_barreras():
            me_next = 'barreras'
        elif not self.has_actoresrelevantes():
            me_next = 'actoresrelevantes'
        else:
            me_next = False

        return me_next

    def get_objetivo_prioritario(self):
        try:
            prioritario = self.objetivos.order_by('prioridad')[0]
            return prioritario
        except:
            return None


class Objetivo(models.Model):
    objetivo = models.TextField()
    prioridad = models.IntegerField(default=1)

    resultadosintermedios = models.TextField()
    factoreshabilitantes = models.TextField()
    barreras = models.TextField()

    def __str__(self):
        return self.objetivo
