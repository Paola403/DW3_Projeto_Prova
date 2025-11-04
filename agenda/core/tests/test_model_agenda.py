from django.test import TestCase
from core.models import Agenda

class AgendaModelTest(TestCase):
    def setUp(self):
        self.agenda = Agenda.objects.create(
            nome_completo="Gustavo Silveira",
            telefone="(19)93370-88847",
            email="gustavao@gmail.com",
            observacao="Cliente Legal"
        )

    def test_agenda_criada_com_sucesso(self):
        self.assertEqual(self.agenda.nome_completo, "Gustavo Silveira")
        self.assertEqual(self.agenda.telefone, "(19)93370-88847")
        self.assertEqual(self.agenda.email, "gustavao@gmail.com")
        self.assertEqual(self.agenda.observacao, "Cliente Legal")

    def test_str_retorna_nome_e_email(self):
        self.assertEqual(str(self.agenda), "Gustavo Silveira - gustavao@gmail.com")
