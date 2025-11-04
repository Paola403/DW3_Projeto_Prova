from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

class List_Contact_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='admin@fatec.sp.gov.br', username='admin')
        new_user.set_password('fatec')
        new_user.save()
        self.login_url = reverse('login')
        self.list_url = reverse('show_contact')
        self.agenda = Agenda.objects.create(
            nome_completo='paola test',
            telefone='19977550903',
            email='paola.teste@fatec.sp.gov.br',
            observacao='teste'
        )
        self.agenda2 = Agenda.objects.create(
            nome_completo='paola test 2',
            telefone='19988309957',
            email='paola.teste2@fatec.sp.gov.br',
            observacao='teste 2'
        )
        
    def test_Not_Logged_List_Template(self):
        response = self.client.get(self.list_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'{self.login_url}?next={self.list_url}')
    
    def test_Logged_List_Template(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'show_contact.html')

    def test_list_contacts(self): ##Esqueci de colocar test no nome :v
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'show_contact.html')
        self.assertContains(response, 'paola test')
        self.assertContains(response, 'paola test 2')
        self.assertContains(response, '19977550903')
        self.assertContains(response, '19988309957')
        self.assertContains(response, 'paola.teste@fatec.sp.gov.br')
        self.assertContains(response, 'paola.teste2@fatec.sp.gov.br')

    def test_list_contacts_empty(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        Agenda.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'show_contact.html')
        self.assertContains(response, 'Nenhum contato encontrado.')
        self.assertNotContains(response, 'paola test')
        self.assertNotContains(response, 'paola test 2')
        self.assertNotContains(response, '19977550903')
        self.assertNotContains(response, '19988309957')