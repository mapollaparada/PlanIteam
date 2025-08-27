from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Espacio, Nota, Tarea, Presupuesto, Categoria
from django.http import JsonResponse
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import NotaSerializer, TareaSerializer, PresupuestoSerializer, CategoriaSerializer, EspacioSerializer

@login_required
def dashboard(request):
    usuario = request.user
    espacios = Espacio.objects.filter(usuarios=usuario)
    espacio_id = request.GET.get('espacio')
    tipo = request.GET.get('tipo')  # nota, tarea, presupuesto
    categoria_id = request.GET.get('categoria')
    page = request.GET.get('page', 1)
    per_page = 10

    # Determinar si es vista personal o de espacio
    if espacio_id:
        espacio = get_object_or_404(Espacio, id=espacio_id, usuarios=usuario)
        notas = Nota.objects.filter(espacio=espacio).order_by('id')
        tareas = Tarea.objects.filter(espacio=espacio).order_by('id')
        presupuestos = Presupuesto.objects.filter(espacio=espacio).order_by('id')
        categorias = Categoria.objects.filter(espacio=espacio)
        vista = 'espacio'
    else:
        espacio = None
        notas = Nota.objects.filter(usuario=usuario, espacio__isnull=True)
        tareas = Tarea.objects.filter(usuario=usuario, espacio__isnull=True)
        presupuestos = Presupuesto.objects.filter(usuario=usuario, espacio__isnull=True)
        categorias = Categoria.objects.filter(usuario=usuario, espacio__isnull=True)
        vista = 'personal'

    # Filtros por tipo
    if tipo == 'nota':
        tareas = []
        presupuestos = []
    elif tipo == 'tarea':
        notas = []
        presupuestos = []
    elif tipo == 'presupuesto':
        notas = []
        tareas = []

    # Filtro por categoría
    if categoria_id:
        notas = [n for n in notas if n.categoria and str(n.categoria.id) == categoria_id]
        tareas = [t for t in tareas if t.categoria and str(t.categoria.id) == categoria_id]
        presupuestos = [p for p in presupuestos if p.categoria and str(p.categoria.id) == categoria_id]

    # Paginación
    notas_paginator = Paginator(notas, per_page)
    tareas_paginator = Paginator(tareas, per_page)
    presupuestos_paginator = Paginator(presupuestos, per_page)
    notas_page = notas_paginator.get_page(request.GET.get('notas_page', 1))
    tareas_page = tareas_paginator.get_page(request.GET.get('tareas_page', 1))
    presupuestos_page = presupuestos_paginator.get_page(request.GET.get('presupuestos_page', 1))

    return render(request, 'core/dashboard.html', {
        'espacios': espacios,
        'espacio': espacio,
        'notas': notas_page,
        'tareas': tareas_page,
        'presupuestos': presupuestos_page,
        'categorias': categorias,
        'vista': vista,
        'tipo': tipo,
        'categoria_id': categoria_id,
        'notas_paginator': notas_paginator,
        'tareas_paginator': tareas_paginator,
        'presupuestos_paginator': presupuestos_paginator,
    })

@login_required
def exportar_csv(request):
    usuario = request.user
    espacio_id = request.GET.get('espacio')
    tipo = request.GET.get('tipo')
    categoria_id = request.GET.get('categoria')
    # Determinar ítems a exportar
    if tipo == 'nota':
        items = Nota.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Nota.objects.filter(espacio_id=espacio_id)
    elif tipo == 'tarea':
        items = Tarea.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Tarea.objects.filter(espacio_id=espacio_id)
    elif tipo == 'presupuesto':
        items = Presupuesto.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Presupuesto.objects.filter(espacio_id=espacio_id)
    else:
        items = list(Nota.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Nota.objects.filter(espacio_id=espacio_id))
        items += list(Tarea.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Tarea.objects.filter(espacio_id=espacio_id))
        items += list(Presupuesto.objects.filter(usuario=usuario, espacio__isnull=True) if not espacio_id else Presupuesto.objects.filter(espacio_id=espacio_id))
    if categoria_id:
        items = [i for i in items if hasattr(i, 'categoria') and i.categoria and str(i.categoria.id) == categoria_id]
    # Crear CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    writer = csv.writer(response)
    if tipo == 'nota':
        writer.writerow(['ID', 'Título', 'Contenido', 'Categoría'])
        for n in items:
            writer.writerow([n.id, n.titulo, n.contenido, n.categoria.nombre if n.categoria else ''])
    elif tipo == 'tarea':
        writer.writerow(['ID', 'Título', 'Descripción', 'Estado', 'Fecha inicio', 'Fecha fin', 'Recurrencia', 'Categoría'])
        for t in items:
            writer.writerow([t.id, t.titulo, t.descripcion, t.estado, t.fecha_inicio, t.fecha_fin, t.recurrencia, t.categoria.nombre if t.categoria else ''])
    elif tipo == 'presupuesto':
        writer.writerow(['ID', 'Título', 'Descripción', 'Link', 'Precio', 'Categoría'])
        for p in items:
            writer.writerow([p.id, p.titulo, p.descripcion, p.link, p.precio, p.categoria.nombre if p.categoria else ''])
    else:
        writer.writerow(['Tipo', 'ID', 'Título', 'Descripción/Contenido', 'Estado/Link/Precio', 'Categoría'])
        for i in items:
            if isinstance(i, Nota):
                writer.writerow(['Nota', i.id, i.titulo, i.contenido, '', i.categoria.nombre if i.categoria else ''])
            elif isinstance(i, Tarea):
                writer.writerow(['Tarea', i.id, i.titulo, i.descripcion, i.estado, i.categoria.nombre if i.categoria else ''])
            elif isinstance(i, Presupuesto):
                writer.writerow(['Presupuesto', i.id, i.titulo, i.descripcion, i.precio, i.categoria.nombre if i.categoria else ''])
    return response

@login_required
@require_POST
def crear_nota(request):
    usuario = request.user
    titulo = request.POST.get('titulo')
    contenido = request.POST.get('contenido')
    categoria_id = request.POST.get('categoria')
    espacio_id = request.POST.get('espacio')
    categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    espacio = Espacio.objects.filter(id=espacio_id).first() if espacio_id else None
    nota = Nota.objects.create(
        titulo=titulo,
        contenido=contenido,
        usuario=usuario,
        espacio=espacio,
        categoria=categoria
    )
    # Redirigir a la misma vista con los mismos filtros
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def crear_tarea(request):
    usuario = request.user
    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    fecha_inicio = request.POST.get('fecha_inicio') or None
    fecha_fin = request.POST.get('fecha_fin') or None
    estado = request.POST.get('estado', 'pendiente')
    recurrencia = request.POST.get('recurrencia', 'ninguna')
    categoria_id = request.POST.get('categoria')
    espacio_id = request.POST.get('espacio')
    categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    espacio = Espacio.objects.filter(id=espacio_id).first() if espacio_id else None
    tarea = Tarea.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado=estado,
        recurrencia=recurrencia,
        usuario=usuario,
        espacio=espacio,
        categoria=categoria
    )
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def crear_presupuesto(request):
    usuario = request.user
    titulo = request.POST.get('titulo')
    descripcion = request.POST.get('descripcion')
    link = request.POST.get('link')
    precio = request.POST.get('precio') or None
    categoria_id = request.POST.get('categoria')
    espacio_id = request.POST.get('espacio')
    categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    espacio = Espacio.objects.filter(id=espacio_id).first() if espacio_id else None
    presupuesto = Presupuesto.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        link=link,
        precio=precio,
        usuario=usuario,
        espacio=espacio,
        categoria=categoria
    )
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def crear_categoria(request):
    usuario = request.user
    nombre = request.POST.get('nombre')
    espacio_id = request.POST.get('espacio')
    espacio = Espacio.objects.filter(id=espacio_id).first() if espacio_id else None
    categoria = Categoria.objects.create(
        nombre=nombre,
        usuario=usuario if not espacio else None,
        espacio=espacio
    )
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    nombre = request.POST.get('nombre')
    if nombre:
        categoria.nombre = nombre
        categoria.save()
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return redirect(redirect_url)

@login_required
@require_POST
def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)
    nota.titulo = request.POST.get('titulo')
    nota.contenido = request.POST.get('contenido')
    categoria_id = request.POST.get('categoria')
    nota.categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    nota.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)
    nota.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.titulo = request.POST.get('titulo')
    tarea.descripcion = request.POST.get('descripcion')
    tarea.fecha_inicio = request.POST.get('fecha_inicio') or None
    tarea.fecha_fin = request.POST.get('fecha_fin') or None
    tarea.estado = request.POST.get('estado', 'pendiente')
    tarea.recurrencia = request.POST.get('recurrencia', 'ninguna')
    categoria_id = request.POST.get('categoria')
    tarea.categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    tarea.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def marcar_tarea_completada(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    if tarea.espacio:
        tarea.usuario = request.user  # último en completar
    tarea.estado = 'hecha'
    tarea.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def editar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, usuario=request.user)
    presupuesto.titulo = request.POST.get('titulo')
    presupuesto.descripcion = request.POST.get('descripcion')
    presupuesto.link = request.POST.get('link')
    presupuesto.precio = request.POST.get('precio') or None
    categoria_id = request.POST.get('categoria')
    presupuesto.categoria = Categoria.objects.filter(id=categoria_id).first() if categoria_id else None
    presupuesto.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def eliminar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, usuario=request.user)
    presupuesto.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Nota.objects.filter(usuario=self.request.user)
class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Presupuesto.objects.filter(usuario=self.request.user)
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EspacioViewSet(viewsets.ModelViewSet):
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer

# Create your views here.
