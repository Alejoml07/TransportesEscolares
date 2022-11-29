from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 

#Mensaje tipo cookie temporales 
from django.contrib import messages

#Gestion de errores de base de datos 
from django.db import IntegrityError

from .models import Cliente,Beneficiarios,Comentarios,Servicios,Peticiones, Vehiculo

from django.db.models import Q

from django.core.paginator import Paginator

from django.core.files.storage import FileSystemStorage

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

from os import remove, path



# Create your views here.

def index(request):
    login = request.session.get('logueo', False)
    if login:
        return render(request, 'transportes/index.html')
    else:
        messages.warning(request, "Inicie sesión primero...")
        return redirect('transportes:loginFormulario')

def loginFormulario(request):
        return render(request, 'transportes/login/login.html')


def login(request):
    if request.method == "POST":
        try:
            user = request.POST["usuario"]
            passw = request.POST["clave"]

            q = Cliente.objects.get(usuario = user, clave = passw)
            # crear la sesión
            request.session["logueo"] = [q.nombre, q.apellido, q.rol, q.id, q.get_rol_display()]

            messages.success(request, "Bienvenido!!")
            return redirect('transportes:index')     

        except Cliente.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect('transportes:loginFormulario')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('transportes:loginFormulario')
    else:
        messages.warning(request, "Usted no ha enviado datos...")
        return redirect('transportes:loginFormulario')

def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!!")
        return redirect('transportes:index')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('transportes:index')
#--------------------------USUARIOS-----------------------------------------------------
def listarUsuario(request):
     #Obtener la sesión
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        q = Cliente.objects.all()
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...
        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        contexto = {'datos': q}
        return render(request, 'transportes/login/usuarios/listarUsuario.html', contexto)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')


def registrarUsuario(request):
    return render(request, 'transportes/login/usuarios/registrarUsuario.html')

def guardarUsuario(request):
    try:
        if request.method == "POST":
            
            
                
            q = Cliente(nombre = request.POST["nombre"],
                        apellido = request.POST["apellido"],
                        correo = request.POST["correo"],
                        direccion = request.POST["direccion"],
                        documento = request.POST["documento"],
                        fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Usuario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')


def formularioEditar(request, id):
    p = Cliente.objects.get(pk = id)
    contexto = { "cliente": p }
    return render(request, 'transportes/login/usuarios/editarUsuario.html', contexto)


def actualizarUsuario(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Cliente.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.apellido = request.POST["apellido"]
            p.correo = request.POST["correo"]
            p.direccion = request.POST["direccion"]
            p.documento = request.POST["documento"]
            p.fecha_nacimiento = request.POST["fecha_nacimiento"]

            
            p.save()
            messages.success(request, "Usuario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')


def eliminarUsuario(request, id):
    try:
        p =  Cliente.objects.get(pk = id)
        p.delete()
        messages.success(request, "Usuario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarUsuario')

def buscarProducto(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Cliente.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datos": q }
        return render(request, 'transportes/login/usuarios/listar_Usuario_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarUsuario')
    


#-------------------------BENEFICIARIO--------------------------------------------


def listarBeneficiario(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        b = Beneficiarios.objects.all()
        paginator = Paginator(b, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        b = paginator.get_page(page_number)
        contextob = {'datosB': b}

        return render(request, 'transportes/login/beneficiarios/listarBeneficiario.html', contextob)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')

def registrarBeneficiario(request):
    u = Cliente.objects.all()
    contexto = {'cli': u}
    return render(request, 'transportes/login/beneficiarios/registrarBeneficiario.html', contexto)

def guardarBeneficiario(request):
    try:
        if request.method == "POST":
            u =  Cliente.objects.get(pk = request.POST["cliente"])
            q = Beneficiarios(
                cliente = u,
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                documento = request.POST["documento"],
                fecha_nacimiento = request.POST["fecha_nacimiento"])
            q.save()

            messages.success(request, "Beneficiario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def formularioEditarBeneficiario(request, id):
    p = Beneficiarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/beneficiarios/editarBeneficiario.html', contexto)


def actualizarBeneficiario(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Beneficiarios.objects.get(pk = request.POST["id"])
            c =  Cliente.objects.get(pk = request.POST["cliente"])
            p.cliente = c
            p.nombre = request.POST["nombre"]
            p.apellido = request.POST["apellido"]
            p.documento = request.POST["documento"]
            p.fecha_nacimiento = request.POST["fecha_nacimiento"]

            p.save()
            messages.success(request, "Beneficiario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')


def eliminarBeneficiario(request, id):
    try:
        p =  Beneficiarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Beneficiario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarBeneficiario')

def buscarBeneficiario(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Beneficiarios.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosB": q }
        return render(request, 'transportes/login/beneficiarios/listar_Beneficiario_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarBeneficiario')

#--------------------COMENTARIOS----------------------------------------
def listarComentarios(request):
    login = request.session.get('logueo', False)

    if login:
        c = Comentarios.objects.all()
        paginator = Paginator(c, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        c = paginator.get_page(page_number)
        contextoC = {'datosC': c}

        return render(request, 'transportes/login/comentarios/listarComentarios.html', contextoC)
    else:
        messages.warning(request, "Inicie sesión primero...")
        return redirect('transportes:loginFormulario')

def registrarComentarios(request):
    u = Cliente.objects.all()
    contexto = {'cli': u,}
    return render(request, 'transportes/login/comentarios/registrarComentarios.html',contexto)

def guardarComentarios(request):
    try:
        if request.method == "POST":
            u =  Cliente.objects.get(pk = request.POST["cliente"])

            q = Comentarios(
                cliente = u,
                tipo = request.POST["tipo"],
                desc = request.POST["desc"])
            q.save()

            messages.success(request, "Comentario guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def formularioEditarComentarios(request, id):
    p = Comentarios.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "beneficiario": p, "cli":c }
    return render(request, 'transportes/login/comentarios/editarComentario.html', contexto)


def actualizarComentarios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Comentarios.objects.get(pk = request.POST["id"])
            c =  Cliente.objects.get(pk = request.POST["cliente"])
            p.cliente = c
            p.tipo = request.POST["tipo"]
            p.desc = request.POST["desc"]
           
            p.save()
            messages.success(request, "Comentario actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')


def eliminarComentarios(request, id):
    try:
        p = Comentarios.objects.get(pk = id)
        p.delete()
        messages.success(request, "Comentario eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarComentarios')

def buscarComentarios(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Comentarios.objects.filter( Q(tipo__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosC": q }
        return render(request, 'transportes/login/comentarios/listar_Comentarios_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarComentarios')

#--------------------SERVICIOS----------------------------------------

def listarServicios(request):
    t = Servicios.objects.all()
    paginator = Paginator(t, 3) # Mostrar 3 registros por página...

    page_number = request.GET.get('page')
    #Sobreescribir la salida de la consulta.......
    t = paginator.get_page(page_number)
    contextoT = {'datosT': t}

    return render(request, 'transportes/login/servicios/listarServicios.html', contextoT)

def registrarServicios(request):
    return render(request, 'transportes/login/servicios/registrarServicios.html')

def guardarServicios(request):
    try:
        if request.method == "POST":
            q = Servicios(nombre = request.POST["nombre"],caracteristicas = request.POST["caracteristicas"])
            q.save()

            messages.success(request, "servicio guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def formularioEditarServicios(request, id):
    p = Servicios.objects.get(pk = id)
    contexto = { "servicios": p }
    return render(request, 'transportes/login/servicios/editarServicios.html', contexto)


def actualizarServicios(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Servicios.objects.get(pk = request.POST["id"])
            
            p.nombre = request.POST["nombre"]
            p.caracteristicas = request.POST["caracteristicas"]
            p.save()
            messages.success(request, "servicio actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')


def eliminarServicios(request, id):
    try:
        p = Servicios.objects.get(pk = id)
        p.delete()
        messages.success(request, "servicio eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarServicios')

def buscarServicios(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Servicios.objects.filter( Q(nombre__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosT": q }
        return render(request, 'transportes/login/servicios/listar_Servicios_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarServicios')



#--------------------PETICIONES----------------------------------------
def listarPeticiones(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "C"):
        p = Peticiones.objects.all()
        paginator = Paginator(p, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        p = paginator.get_page(page_number)
        contextoP = {'datosP': p}

        return render(request, 'transportes/login/peticiones/listarPeticiones.html', contextoP)
    else:
        if login and (login[2] != "A" and login[2] != "C"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')

def registrarPeticiones(request):
    c = Cliente.objects.all()
    s = Servicios.objects.all()
    contexto = {'cli':c,'servicios':s}
    return render(request, 'transportes/login/peticiones/registrarPeticiones.html',contexto)

def guardarPeticiones(request):
    try:
        c =  Cliente.objects.get(pk = request.POST["cliente"])
        s =  Servicios.objects.get(pk = request.POST["servicios"])


        if request.method == "POST":
            q = Peticiones(
                cliente = c,
                servicios = s,
                direccion = request.POST["direccion"],
                colegio = request.POST["colegio"],
                horario = request.POST["horario"],
                comentario_add = request.POST["comentario_add"])
            q.save()

            messages.success(request, "Peticion guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')


def formularioEditarPeticiones(request, id):
    p = Peticiones.objects.get(pk = id)
    s = Servicios.objects.all()
    c = Cliente.objects.all()
    contexto = { "peticiones": p, "cli":c, 'servicios':s }
    return render(request, 'transportes/login/peticiones/editarPeticiones.html', contexto)


def actualizarPeticiones(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Peticiones.objects.get(pk = request.POST["id"])
            s = Servicios.objects.get(pk = request.POST["servicios"])
            c = Cliente.objects.get(pk = request.POST["cliente"])


            p.cliente = c
            p.servicios = s
            p.direccion = request.POST["direccion"]
            p.colegio = request.POST["colegio"]
            p.horario = request.POST["horario"]
            p.comentario_add = request.POST["comentario_add"]
           

            p.save()
            messages.success(request, "Peticion actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')


def eliminarPeticiones(request, id):
    try:
        p =  Peticiones.objects.get(pk = id)
        p.delete()
        messages.success(request, "Peticion eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarPeticiones')

def buscarPeticiones(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Peticiones.objects.filter( Q(colegio__icontains = dato ) |Q(direccion__icontains = dato ))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosP": q }
        return render(request, 'transportes/login/peticiones/listar_Peticiones_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarPeticiones')

    
#--------------------VEHICULOS----------------------------------------


def listarVehiculo(request):
    login = request.session.get('logueo', False)

    if login and (login[2] == "A" or login[2] == "P"):
        b = Vehiculo.objects.all()
        paginator = Paginator(b, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        v = paginator.get_page(page_number)
        contextob = {'datosV': v}

        return render(request, 'transportes/login/vehiculo/listarVehiculo.html', contextob)
    else:
        if login and (login[2] != "A" and login[2] != "P"):
            messages.warning(request, "Usted no tiene autorización para acceder al módulo...")
            return redirect('transportes:index')
        else:
            messages.warning(request, "Inicie sesión primero...")
            return redirect('transportes:loginFormulario')


def registrarVehiculo(request):
    u = Cliente.objects.all()
    contexto = {'cliente': u}
    return render(request, 'transportes/login/vehiculo/registrarVehiculo.html', contexto)

def guardarVehiculo(request):
    try:
        if request.method == "POST":
            
            if request.FILES:
                fss = FileSystemStorage()
                f = request.FILES["foto"]
                file = fss.save("transportes/fotos/" + f.name, f)
            else:
                file = 'transportes/fotos/default.webp'
                
            u = Cliente.objects.get(pk = request.POST["cliente"])
            q = Vehiculo(
                proveedor = u,
                placa = request.POST["placa"],
                marca = request.POST["marca"],
                color = request.POST["color"],
                foto = file)
            q.save()

            messages.success(request, "Vehiculo guardado exitosamente")
        else:
            messages.warning(request, "No se han enviado datos...")

    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')

def formularioEditarVehiculo(request, id):
    p = Vehiculo.objects.get(pk = id)
    c = Cliente.objects.all()
    contexto = { "vehiculo": p, "cliente":c }
    return render(request, 'transportes/login/vehiculo/editarVehiculo.html', contexto)


def actualizarVehiculo(request):
    try:
        if request.method == "POST":
            #Obtener la instancia de producto a modificar
            p =  Vehiculo.objects.get(pk = request.POST["id"])
            c =  Cliente.objects.get(pk = request.POST["cliente"])
            p.cliente = c
            p.placa = request.POST["placa"]
            p.marca = request.POST["marca"]
            p.color = request.POST["color"]
            p.foto = request.POST["foto"]

            p.save()
            messages.success(request, "Vehiculo actualizado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos...")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')


def eliminarVehiculo(request, id):
    try:
        p =Vehiculo.objects.get(pk = id)
        
         #Obtener ruta de la foto
        foto = str(BASE_DIR) + str(p.foto.url) 
        
        #Averiguar si existe la foto en esa ruta obtenida
        if path.exists(foto):
            #Caso especial no borrar foto por defecto.
            if p.foto.url != '/uploads/transportes/fotos/default.webp':
                remove(foto)
        else:
            messages.warning(request, "No se encontró la foto...")
            
        p.delete()
        messages.success(request, "Vehiculo eliminado correctamente!!")
    except IntegrityError:
        messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect('transportes:listarVehiculo')

def buscarVehiculo(request):
    
    if request.method == "POST":
        dato = request.POST["buscar"]
        q = Vehiculo.objects.filter( Q(id__icontains = dato))
        
        paginator = Paginator(q, 3) # Mostrar 3 registros por página...

        page_number = request.GET.get('page')
        #Sobreescribir la salida de la consulta.......
        q = paginator.get_page(page_number)
        
        contexto = { "datosV": q }
        return render(request, 'transportes/login/vehiculo/listar_Vehiculo_ajax.html', contexto)
    else:
        messages.error(request, "Error no envió datos...")
        return redirect('transportes:listarVehiculo')