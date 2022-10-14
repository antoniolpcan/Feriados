from django.test import TestCase
from .models import FeriadoModel
from datetime import datetime
from core.forms import FeriadoForm

class NatalTest(TestCase):
    
    def setUp(self):
        self.resp = self.client.get('/')
    
    def test_200_response(self):
        self.assertEqual(200, self.resp.status_code)
    
    def test_texto(self):
        self.assertContains(self.resp, 'não é feriado')

    def test_template_natal(self):
        self.assertTemplateUsed(self.resp, 'feriado.html')

class FeriadoModelTest(TestCase):
    def setUp(self):
        hoje = datetime.today()
        feriado = FeriadoModel(nome = "teste", dia=hoje.day, mes = hoje.month)
        feriado.save()
        self.resp = self.client.get('/')

    def test_created(self):
        self.assertTrue(FeriadoModel.objects.exists())

    def test_200_response(self):
        self.assertTrue(FeriadoModel.objects.exists())
    
    def test_texto(self):
        self.assertContains(self.resp, 'teste')

    def test_template_natal(self):
        self.assertTemplateUsed(self.resp, 'feriado.html')

class FeiadoModelTest(TestCase):
    def setUp(self):
        self.feriado = 'teste'
        self.mes = 10
        self.dia = 4
        self.cadastro = FeriadoModel(
            nome = self.feriado,
            dia = self.dia,
            mes = self.mes,
        )
        self.cadastro.save()

    def test_created(self):
        self.assertTrue(FeriadoModel.objects.exists())
    
    def test_modificado_em(self):
        self.assertIsInstance(self.cadastro.modificado_em, datetime)

    def test_nome_feriado(self):
        nome = self.cadastro.__dict__.get('nome', '')
        self.assertEqual(nome, self.feriado)


class FeriadoFormTest(TestCase):
    def test_form_has_fields(self):
        form = FeriadoForm()
        expected = ['nome', 'dia', 'mes']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_must_be_capitalized(self):
        form = self.make_validated_form(nome='dia de são nunca')
        self.assertEqual('DIA DE SÃO NUNCA', form.cleaned_data['nome'])

    def test_must_be_capitalized(self):
        form = self.make_validated_form()
        self.assertEqual('TIRADENTES', form.cleaned_data['nome'])
    
    def make_validated_form(self, **kwargs):
        valid = dict(
            nome='Tiradentes',
            dia=14,
            mes=4
        )       
        data = dict(valid, **kwargs)
        form = FeriadoForm(data)
        form.is_valid()
        return 