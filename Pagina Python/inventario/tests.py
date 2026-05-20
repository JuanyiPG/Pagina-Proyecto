from django.test import TestCase
from . import reverse
from . models import Proveedor
# Create your tests here.
class  ProveedorViewsTest(TestCase):
    def setUp(self):
        #Crear persona de prueba
        self.proveedor=Proveedor.objects.create(
            documento=80160,
            nombre='Carlos',
            apellido='Rodriguez',
            direccion='Calle 65',
            email='rodri@gmail.com'
            )
        
    def test_incio(self):
        response=self.client.get(reverse('inicio'))
        
        self.assertEqual(response.status_code,200)
        self.assertIn('opciones_edad',response.context)
        self.assertTemplateUsed(response, 'persona/registro.html')
        
    def text_registro(self):
        response=self.client.post(reverse('registrar_persona'), {
                'documento':80160,
                'nombre':'Carlos',
                'apellido':'Rodriguez',
                'direccion':'Calle 65',
                'email':'rodri@gmail.com'})
        
        self.assertEqual(Proveedor.objects.count(),2)
        self.assertEqual(Proveedor.objects.get(documento=80160).nombre, 'Carlos')
        self.assertEqual(response.status_code, 302)