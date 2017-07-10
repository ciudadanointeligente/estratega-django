from django.db import models

# Create your models here.


class Estrategia(models.Model):
    titulo = models.CharField(max_length=1000)

    def __str__(self):
        return self.titulo


class Problematica(models.Model):
    estrategia = models.ForeignKey(Estrategia)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Causa(models.Model):
    estrategia = models.ForeignKey(Estrategia)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class SolucionPolitica(models.Model):
    estrategia = models.ForeignKey(Estrategia)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Objetivo(models.Model):
    estrategia = models.ForeignKey(Estrategia)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class ResultadoIntermedio(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class FactorHabilitante(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Barrera(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    texto = models.TextField()

    def __str__(self):
        return self.texto


class ActorRelevante(models.Model):
    objetivo = models.ForeignKey(Objetivo)
    nombre = models.CharField(max_length=200)
    justificacion = models.TextField()

    def __str__(self):
        return self.nombre

