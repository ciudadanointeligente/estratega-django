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

        if (objetivo is None) or (objetivo.objetivo == ''):
            return False
        else:
            return True

    def has_resultadosintermedios(self, objetivo=None):
        if objetivo is None:
            objetivo = self.get_objetivo_prioritario()

        if objetivo and objetivo.resultadosintermedios != '':
            return True
        else:
            return False

    def has_factoreshabilitantes(self, objetivo=None):
        if objetivo is None:
            objetivo = self.get_objetivo_prioritario()

        if objetivo and objetivo.factoreshabilitantes != '':
            return True
        else:
            return False

    def has_barreras(self, objetivo=None):
        if objetivo is None:
            objetivo = self.get_objetivo_prioritario()

        if objetivo and objetivo.barreras != '':
            return True
        else:
            return False

    def has_actoresrelevantes(self, objetivo=None):
        if objetivo is None:
            objetivo = self.get_objetivo_prioritario()

        if objetivo and objetivo.actoresrelevantes != '':
            return True
        else:
            return False

    def has_varios_objetivos(self):
        if len(self.objetivos.all()) > 1:
            return True
        else:
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
            me_next = 'estrategia'

        return me_next

    def get_objetivo_prioritario(self):
        try:
            prioritario = self.objetivos.order_by('prioridad')[0]
            return prioritario
        except:
            return None

    def delete_all_objetivos(self):
        try:
            for objetivo in self.objetivos:
                self.objetivos.remove(objetivo)
                objetivo.delete()
            
            return True
        except:
            return False

class Objetivo(models.Model):
    objetivo = models.TextField()
    prioridad = models.IntegerField(default=1)

    resultadosintermedios = models.TextField()
    factoreshabilitantes = models.TextField()
    barreras = models.TextField()
    actoresrelevantes = models.TextField()

    def __str__(self):
        return self.objetivo

    def has_objetivo(self):
        if self.objetivo != '':
            return True
        else:
            return False

    def has_resultadosintermedios(self):
        if self.resultadosintermedios != '':
            return True
        else:
            return False

    def has_factoreshabilitantes(self):
        if self.factoreshabilitantes != '':
            return True
        else:
            return False

    def has_barreras(self):
        if self.barreras != '':
            return True
        else:
            return False

    def has_actoresrelevantes(self):
        if self.actoresrelevantes != '':
            return True
        else:
            return False

    def me_next(self):
        if not self.has_objetivo():
            me_next = 'objetivos'
        elif not self.has_resultadosintermedios():
            me_next = 'resultadosintermedios'
        elif not self.has_barreras():
            me_next = 'barreras'
        elif not self.has_factoreshabilitantes():
            me_next = 'factoreshabilitantes'
        elif not self.has_actoresrelevantes():
            me_next = 'actoresrelevantes'
        else:
            me_next = False

        return me_next