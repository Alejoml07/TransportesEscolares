from django.urls import path
from . import views


app_name= "transportes"
urlpatterns = [
    path('', views.index, name = "index"),
    path('loginFormulario/', views.loginFormulario, name="loginFormulario" ),
    path('login/', views.login, name="login" ),
    path('logout/', views.logout, name="logout" ),

    #--------------------------Usuario-----------------------------------
    path('listarUsuarios/', views.listarUsuario, name = "listarUsuario"),
    path('registrarUsuario/', views.registrarUsuario, name = "registrarUsuario"),
    path('guardarUsuario/', views.guardarUsuario, name = "guardarUsuario"),
    path('formularioEditar/<int:id>', views.formularioEditar, name = "formularioEditar"),
    path('actualizarUsuario/', views.actualizarUsuario, name = "actualizarUsuario"),
    path('eliminarUsuario/<int:id>', views.eliminarUsuario, name = "eliminarUsuario"),
    path('buscarProducto/', views.buscarProducto, name="buscarProducto"),

    #--------------------------Beneficiario-----------------------------------
    path('listarBeneficiario/', views.listarBeneficiario, name = "listarBeneficiario"),
    path('registrarBeneficiario/', views.registrarBeneficiario, name = "registrarBeneficiario"),
    path('guardarBeneficiario/', views.guardarBeneficiario, name = "guardarBeneficiario"),
    path('formularioEditarBeneficiario/<int:id>', views.formularioEditarBeneficiario, name = "formularioEditarBeneficiario"),
    path('actualizarBeneficiario/', views.actualizarBeneficiario, name = "actualizarBeneficiario"),
    path('eliminarBeneficiario/<int:id>', views.eliminarBeneficiario, name = "eliminarBeneficiario"),
    path('buscarBeneficiario/', views.buscarBeneficiario, name="buscarBeneficiario"),

    #--------------------------Comentarios-----------------------------------
    path('listarComentarios/', views.listarComentarios, name = "listarComentarios"),
    path('registrarComentarios/', views.registrarComentarios, name = "registrarComentarios"),
    path('guardarComentarios/', views.guardarComentarios, name = "guardarComentarios"),
    path('formularioEditarComentarios/<int:id>', views.formularioEditarComentarios, name = "formularioEditarComentarios"),
    path('actualizarComentarios/', views.actualizarComentarios, name = "actualizarComentarios"),
    path('eliminarComentarios/<int:id>', views.eliminarComentarios, name = "eliminarComentarios"),
    path('buscarComentarios/', views.buscarComentarios, name="buscarComentarios"),

    #--------------------------Servicios-----------------------------------
    path('listarServicios/', views.listarServicios, name = "listarServicios"),
    path('registrarServicios/', views.registrarServicios, name = "registrarServicios"),
    path('guardarServicios/', views.guardarServicios, name = "guardarServicios"),
    path('formularioEditarServicios/<int:id>', views.formularioEditarServicios, name = "formularioEditarServicios"),
    path('actualizarServicios/', views.actualizarServicios, name = "actualizarServicios"),
    path('eliminarServicios/<int:id>', views.eliminarServicios, name = "eliminarServicios"),
    path('buscarServicios/', views.buscarServicios, name="buscarServicios"),

    #--------------------------Peticiones-----------------------------------
    path('listarPeticiones/', views.listarPeticiones, name = "listarPeticiones"),
    path('registrarPeticiones/', views.registrarPeticiones, name = "registrarPeticiones"),
    path('guardarPeticiones/', views.guardarPeticiones, name = "guardarPeticiones"),
    path('formularioEditarPeticiones/<int:id>', views.formularioEditarPeticiones, name = "formularioEditarPeticiones"),
    path('actualizarPeticiones/', views.actualizarPeticiones, name = "actualizarPeticiones"),
    path('eliminarPeticiones/<int:id>', views.eliminarPeticiones, name = "eliminarPeticiones"),
    path('buscarPeticiones/', views.buscarPeticiones, name="buscarPeticiones"),

    #--------------------------Vehiculo-----------------------------------
    path('listarVehiculo/', views.listarVehiculo, name = "listarVehiculo"),
    path('registrarVehiculo/', views.registrarVehiculo, name = "registrarVehiculo"),
    path('guardarVehiculo/', views.guardarVehiculo, name = "guardarVehiculo"),
    path('formularioEditarVehiculo/<int:id>', views.formularioEditarVehiculo, name = "formularioEditarVehiculo"),
    path('actualizarVehiculo/', views.actualizarVehiculo, name = "actualizarVehiculo"),
    path('eliminarVehiculo/<int:id>', views.eliminarVehiculo, name = "eliminarVehiculo"),
    path('buscarVehiculo/', views.buscarVehiculo, name="buscarVehiculo"),


   
   


]