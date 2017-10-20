from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from .models import Estrategia, Objetivo
from .forms import EstrategiaTituloForm,\
                   EstrategiaLoginForm,\
                   EstrategiaProblematicaForm,\
                   EstrategiaCausasForm,\
                   EstrategiaSolucionPoliticaForm,\
                   EstrategiaObjetivoForm,\
                   EstrategiaResultadosIntermediosForm,\
                   EstrategiaBarrerasForm,\
                   EstrategiaFactoresHabilitantesForm,\
                   EstrategiaActoresRelevantesForm


def index(request):
    return render(request, 'estratega/index.html', {})


def metodologia(request):
    return render(request, 'estratega/metodologia.html', {})


def log_out(request):
    logout(request)
    return redirect('/')

def error_inesperado(request):
    return render(request, 'estratega/error_inesperado.html', {})

# Login

class EstrategaLoginView(LoginView):
    template_name = 'estrategias/login.html'
    form_class = EstrategiaLoginForm


# Mis Estrategias

class MisEstrategiasView(LoginRequiredMixin, generic.ListView):
    model = Estrategia
    template_name = 'estrategias/mis_estrategias.html'
    context_object_name = 'estrategias'
    login_url = '/login'

    def get_queryset(self):
        qs = super(MisEstrategiasView, self).get_queryset()
        return qs.filter(dueno=self.request.user)


# Estrategia

class EstrategiaView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/estrategia.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        if self.object.me_next() == 'estrategia':
            return super(EstrategiaView, self).get(request, *args, **kwargs)
        elif self.object.me_next() == 'actoresrelevantes':
            return redirect(reverse('estrategias:actoresrelevantes_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        elif self.object.me_next() == 'factoreshabilitantes':
            return redirect(reverse('estrategias:factoreshabilitantes_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        elif self.object.me_next() == 'barreras':
            return redirect(reverse('estrategias:barreras_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        elif self.object.me_next() == 'resultadosintermedios':
            return redirect(reverse('estrategias:resultadosintermedios_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        elif self.object.me_next() == 'objetivos':
            return redirect(reverse('estrategias:objetivos_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        elif self.object.me_next() == 'solucionpolitica':
            return redirect(reverse('estrategias:solucionpolitica', kwargs={'pk': self.object.id}))
        elif self.object.me_next() == 'causas':
            return redirect(reverse('estrategias:causas', kwargs={'pk': self.object.id}))
        elif self.object.me_next() == 'problematica':
            return redirect(reverse('estrategias:problematica', kwargs={'pk': self.object.id}))

    def get_context_data(self, **kwargs):
        context = super(EstrategiaView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


# Nueva Estrategia

class NuevaEstrategiaView(LoginRequiredMixin, generic.edit.FormView):
    form_class = EstrategiaTituloForm
    template_name = 'estrategias/nueva_estrategia.html'
    success_url = '/estrategias/nueva_estrategia'
    login_url = '/login'

    def form_valid(self, form):
        # se crea la estrategia      
        estrategia = Estrategia.objects.create(titulo=form.instance.titulo, dueno=self.request.user)
        estrategia.save()

        # se crea tambien un primer objetivo en esta etapa,
        # para que no fallen ciertos forms mas adelante
        objetivo = Objetivo.objects.create()
        objetivo.save()
        estrategia.objetivos.add(objetivo)
        estrategia.save()

        return redirect(reverse('estrategias:problematica', kwargs={'pk': estrategia.id}))


# Problematica

class ProblematicaView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/problematica.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        if self.object.problematica == '':
            return redirect(reverse('estrategias:problematica_edit', kwargs={'pk': self.object.id}))
        else:
            return super(ProblematicaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblematicaView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class ProblematicaEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaProblematicaForm
    template_name = 'estrategias/problematica_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(ProblematicaEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(ProblematicaEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblematicaEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.object.problematica == "":
            context['empezovacio'] = True
        
        return context

    def form_valid(self, form):
        estrategia = self.object
        estrategia.problematica = form.instance.problematica
        estrategia.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:causas_pre', kwargs={'pk': self.object.pk}))
        else:
            return redirect(reverse('estrategias:problematica', kwargs={'pk': self.object.pk}))

    def get_initial(self):
        initial = super(ProblematicaEditView, self).get_initial()
        initial['problematica'] = self.object.problematica

        return initial


# Causas

class CausasPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/causas_pre.html'
    login_url = '/login'


class CausasView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/causas.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        if self.object.causas == '':
            return redirect(reverse('estrategias:causas_edit', kwargs={'pk': self.object.id}))
        else:
            return super(CausasView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CausasView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class CausasEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaCausasForm
    template_name = 'estrategias/causas_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(CausasEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(CausasEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CausasEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.object.causas == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        estrategia = self.object
        estrategia.causas = form.instance.causas
        estrategia.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:solucionpolitica_pre', kwargs={'pk': self.object.id}))
        else:
            return redirect(reverse('estrategias:causas', kwargs={'pk': self.object.id}))

    def get_initial(self):
        initial = super(CausasEditView, self).get_initial()
        initial['causas'] = self.object.causas

        return initial


# Solución Política

class SolucionPoliticaPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/solucionpolitica_pre.html'
    login_url = '/login'


class SolucionPoliticaView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/solucionpolitica.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        if self.object.solucionpolitica == '':
            return redirect(reverse('estrategias:solucionpolitica_edit', kwargs={'pk': self.object.id}))
        else:
            return super(SolucionPoliticaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolucionPoliticaView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class SolucionPoliticaEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaSolucionPoliticaForm
    template_name = 'estrategias/solucionpolitica_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(SolucionPoliticaEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            if self.object.has_varios_objetivos():
                self.objetivo = None
            else:
                self.objetivo = self.object.get_objetivo_prioritario()

        return super(SolucionPoliticaEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SolucionPoliticaEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.object.solucionpolitica == "":
            context['empezovacio'] = True
        
        return context

    def form_valid(self, form):
        estrategia = self.object
        estrategia.solucionpolitica = form.instance.solucionpolitica
        estrategia.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:objetivos_pre', kwargs={'pk': self.object.pk}))
        else:
            return redirect(reverse('estrategias:solucionpolitica', kwargs={'pk': self.object.pk}))

    def get_initial(self):
        initial = super(SolucionPoliticaEditView, self).get_initial()
        initial['solucionpolitica'] = self.object.solucionpolitica

        return initial


# Objetivos

class ObjetivosPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/objetivos_pre.html'
    login_url = '/login'


class ObjetivosView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/objetivos.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.has_objetivos():
            return redirect(reverse('estrategias:objetivos_nuevo', kwargs={'pk': self.object.pk}))
        else:
            return super(ObjetivosView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObjetivosView, self).get_context_data(**kwargs)

        context['objetivo'] = None

        return context


class ObjetivosNuevoView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaObjetivoForm
    template_name = 'estrategias/objetivos_nuevo.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(ObjetivosNuevoView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(ObjetivosNuevoView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        objetivo = Objetivo.objects.create()
        objetivo.objetivo = form.instance.objetivo
        objetivo.save()
        self.object.objetivos.add(objetivo)
        self.object.save()

        return redirect(reverse('estrategias:resultadosintermedios_pre', kwargs={'pk': self.object.id}) + '?oid=' + str(objetivo.id))


class ObjetivosDetailEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaObjetivoForm
    template_name = 'estrategias/objetivos_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ObjetivosDetailEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ObjetivosDetailEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObjetivosDetailEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.objetivo.objetivo == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        self.objetivo.objetivo = form.instance.objetivo
        self.objetivo.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:resultadosintermedios_pre', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return redirect(reverse('estrategias:resultadosintermedios', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))

    def get_initial(self):
        initial = super(ObjetivosDetailEditView, self).get_initial()

        initial['objetivo'] = self.objetivo.objetivo

        return initial


class ObjetivosEliminarView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            # si no se ha especificado el id del objetivo, devolver a
            # vista error inesperado
            return redirect(reverse('error_inesperado'))

        # borramos el objetivo
        self.objetivo.delete()

        # redirigimos a la lista de objetivos
        return redirect(reverse('estrategias:objetivos', kwargs={'pk': self.object.pk}))


class ResultadosIntermediosPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/resultadosintermedios_pre.html'
    login_url = '/login'


class ResultadosIntermediosView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/resultadosintermedios.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        if not self.object.has_resultadosintermedios(objetivo=self.objetivo):
            return redirect(reverse('estrategias:resultadosintermedios_edit', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return super(ResultadosIntermediosView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResultadosIntermediosView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class ResultadosIntermediosEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaResultadosIntermediosForm
    template_name = 'estrategias/resultadosintermedios_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ResultadosIntermediosEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ResultadosIntermediosEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ResultadosIntermediosEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.objetivo.resultadosintermedios == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        self.objetivo.resultadosintermedios = form.instance.resultadosintermedios
        self.objetivo.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:barreras_pre', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return redirect(reverse('estrategias:resultadosintermedios', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))

    def get_initial(self):
        initial = super(ResultadosIntermediosEditView, self).get_initial()

        initial['resultadosintermedios'] = self.objetivo.resultadosintermedios

        return initial


class BarrerasPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/barreras_pre.html'
    login_url = '/login'


class BarrerasView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/barreras.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        if not self.object.has_barreras(objetivo=self.objetivo):
            return redirect(reverse('estrategias:barreras_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        else:
            return super(BarrerasView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BarrerasView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class BarrerasEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaBarrerasForm
    template_name = 'estrategias/barreras_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(BarrerasEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(BarrerasEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BarrerasEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.objetivo.barreras == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        self.objetivo.barreras = form.instance.barreras
        self.objetivo.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:factoreshabilitantes_pre', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return redirect(reverse('estrategias:barreras', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))

    def get_initial(self):
        initial = super(BarrerasEditView, self).get_initial()

        initial['barreras'] = self.objetivo.barreras

        return initial


class FactoresHabilitantesPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/factoreshabilitantes_pre.html'
    login_url = '/login'


class FactoresHabilitantesView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/factoreshabilitantes.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        if not self.object.has_factoreshabilitantes(objetivo=self.objetivo):
            return redirect(reverse('estrategias:factoreshabilitantes_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        else:
            return super(FactoresHabilitantesView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FactoresHabilitantesView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class FactoresHabilitantesEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaFactoresHabilitantesForm
    template_name = 'estrategias/factoreshabilitantes_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(FactoresHabilitantesEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(FactoresHabilitantesEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FactoresHabilitantesEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.objetivo.factoreshabilitantes == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        self.objetivo.factoreshabilitantes = form.instance.factoreshabilitantes
        self.objetivo.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:actoresrelevantes_pre', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return redirect(reverse('estrategias:factoreshabilitantes', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))

    def get_initial(self):
        initial = super(FactoresHabilitantesEditView, self).get_initial()

        initial['factoreshabilitantes'] = self.objetivo.factoreshabilitantes

        return initial


class ActoresRelevantesPreView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/actoresrelevantes_pre.html'
    login_url = '/login'


class ActoresRelevantesView(LoginRequiredMixin, generic.DetailView):
    model = Estrategia
    template_name = 'estrategias/actoresrelevantes.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        if not self.object.has_actoresrelevantes(objetivo=self.objetivo):
            return redirect(reverse('estrategias:actoresrelevantes_edit', kwargs={'pk': self.object.id}) + '?oid=' + str(self.objetivo.id))
        else:
            return super(ActoresRelevantesView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActoresRelevantesView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        return context


class ActoresRelevantesEditView(LoginRequiredMixin, generic.detail.SingleObjectMixin, generic.edit.FormView):
    form_class = EstrategiaActoresRelevantesForm
    template_name = 'estrategias/actoresrelevantes_edit.html'
    model = Estrategia
    login_url = '/login'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ActoresRelevantesEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            id_objetivo = self.request.GET['oid']
            self.objetivo = self.object.objetivos.get(id=id_objetivo)
        except:
            self.objetivo = self.object.get_objetivo_prioritario()

        return super(ActoresRelevantesEditView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ActoresRelevantesEditView, self).get_context_data(**kwargs)

        context['objetivo'] = self.objetivo

        if self.objetivo.actoresrelevantes == "":
            context['empezovacio'] = True

        return context

    def form_valid(self, form):
        self.objetivo.actoresrelevantes = form.instance.actoresrelevantes
        self.objetivo.save()

        if 'empezovacio' in self.request.POST:
            return redirect(reverse('estrategias:estrategia', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))
        else:
            return redirect(reverse('estrategias:actoresrelevantes', kwargs={'pk': self.object.pk}) + '?oid=' + str(self.objetivo.id))

    def get_initial(self):
        initial = super(ActoresRelevantesEditView, self).get_initial()

        initial['actoresrelevantes'] = self.objetivo.actoresrelevantes

        return initial
