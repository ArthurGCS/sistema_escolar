from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UnidadeEscolar, Perfil
from apps.professores.models import Disciplina
from apps.alunos.models import Turma


class Command(BaseCommand):
    help = 'Configura dados iniciais do sistema escolar'

    def handle(self, *args, **options):
        self.stdout.write('Configurando dados iniciais...')
        
        # Criar unidades escolares
        unidade1, created = UnidadeEscolar.objects.get_or_create(
            nome='Escola Municipal João da Silva',
            defaults={
                'endereco': 'Rua das Flores, 123 - Centro',
                'telefone': '(11) 1234-5678',
                'email': 'contato@escolajoao.com.br',
                'ativo': True
            }
        )
        
        unidade2, created = UnidadeEscolar.objects.get_or_create(
            nome='Escola Municipal Maria Santos',
            defaults={
                'endereco': 'Av. Principal, 456 - Jardim',
                'telefone': '(11) 9876-5432',
                'email': 'contato@escolamaria.com.br',
                'ativo': True
            }
        )
        
        # Criar usuário administrador
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'email': 'admin@escola.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            
            Perfil.objects.create(
                usuario=admin_user,
                tipo_usuario='administrador',
                unidade_escolar=unidade1
            )
        
        # Criar disciplinas básicas
        disciplinas = [
            {'nome': 'Matemática', 'codigo': 'MAT001', 'carga_horaria': 80},
            {'nome': 'Português', 'codigo': 'PORT001', 'carga_horaria': 80},
            {'nome': 'História', 'codigo': 'HIST001', 'carga_horaria': 60},
            {'nome': 'Geografia', 'codigo': 'GEO001', 'carga_horaria': 60},
            {'nome': 'Ciências', 'codigo': 'CIEN001', 'carga_horaria': 60},
            {'nome': 'Educação Física', 'codigo': 'EDF001', 'carga_horaria': 40},
            {'nome': 'Arte', 'codigo': 'ART001', 'carga_horaria': 40},
            {'nome': 'Inglês', 'codigo': 'ING001', 'carga_horaria': 40},
        ]
        
        for disc in disciplinas:
            Disciplina.objects.get_or_create(
                codigo=disc['codigo'],
                defaults={
                    'nome': disc['nome'],
                    'carga_horaria': disc['carga_horaria'],
                    'ativa': True
                }
            )
        
        # Criar turmas de exemplo
        turmas = [
            {'nome': '1º Ano A', 'ano': 2024, 'turno': 'manha'},
            {'nome': '1º Ano B', 'ano': 2024, 'turno': 'tarde'},
            {'nome': '2º Ano A', 'ano': 2024, 'turno': 'manha'},
            {'nome': '2º Ano B', 'ano': 2024, 'turno': 'tarde'},
            {'nome': '3º Ano A', 'ano': 2024, 'turno': 'manha'},
            {'nome': '3º Ano B', 'ano': 2024, 'turno': 'tarde'},
        ]
        
        for turma_data in turmas:
            Turma.objects.get_or_create(
                nome=turma_data['nome'],
                unidade_escolar=unidade1,
                ano=turma_data['ano'],
                defaults={
                    'turno': turma_data['turno'],
                    'ativa': True
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Dados iniciais configurados com sucesso!')
        )
        self.stdout.write('Usuário admin criado:')
        self.stdout.write('Username: admin')
        self.stdout.write('Password: admin123')
