# pylint: disable=too-few-public-methods,no-member.
"""
Здесь будут прописаны виды.
Они связывают воедино форму, модель и шаблон страницы
"""
import random
from django.shortcuts import render
from django.views import View
from .forms import CardForm, SequenceForm, NucleotideForm
from .models import Card, Sequence, Nucleotide
#disable=no-member

class CheckStructureView(View):
    """
    Класс для отображении игры по 
    отгадыванию аминокислотных
    остатков
    """
    def get(self, request):
        """
        Человек не ввел ничего в форму, нажал сабмит.
        Это его стартовое состояние.
        """
        structures = list(Card.objects.all())

        if structures:
            random_structure = random.choice(structures)
            request.session['random_structure_id'] = random_structure.id
            pdb_url = f"https://www.rcsb.org/structure/{random_structure.protein}"

        else:
            random_structure = None
            request.session['random_structure_id'] = None
            pdb_url = None
        form = CardForm()

        context = {
            'random_structure': random_structure,
            'form': form,
            'pdb_url' : pdb_url
            }
        return render(request, 'cards/check_structure.html', context)

    def post(self, request):
        """
        Метод для проверки правильности формы.
        Генерируется новая страница, если нажата
        кнопка генерации в шаблоне
        """
        if 'generate_new' in request.POST:
            return self.get(request)

        form = CardForm(request.POST)
        if form.is_valid():
            res1 = form.cleaned_data['res1']
            res2 = form.cleaned_data['res2']
            random_structure_id = request.session.get('random_structure_id')
            if random_structure_id:
                try:
                    random_structure = Card.objects.get(id=random_structure_id)
                    pdb_url = f"https://www.rcsb.org/structure/{random_structure.protein}"

                    if random_structure.res1 == res1 and random_structure.res2 == res2:
                        result = "Correct!"
                    else:
                        result = "Incorrect. Please try again."
                except Card.DoesNotExist:
                    result = "Structure not found. Please try again."
                    pdb_url = None
            else:
                result = "No structure selected. Please try again."
                pdb_url = None

            context = {
                'random_structure': random_structure,
                'form': form,
                'pdb_url' : pdb_url,
                'result': result
            }
            return render(request, 'cards/check_structure.html', context)

        context = {
            'form': form
        }
        return render(request, 'cards/check_structure.html', context)

class CheckSequenceView(View):
    """
    Класс для игры перевода ДНК в белок
    """
    def get(self, request):
        """
        Стартовое состояние
        """
        seq = list(Sequence.objects.all())

        if seq:
            random_seq = random.choice(seq)
            request.session['random_seq_id'] = random_seq.id

        else:
            random_seq = None
            request.session['random_seq_id'] = None
        form = SequenceForm()
        context = {
            'random_seq': random_seq,
            'form': form,
        }
        return render(request, 'cards/check_seq.html', context)

    def check_mistake(self, s, ans):
        """
        Проверка правилности ответов
        """
        if s == ans:
            res = 'Correct!'
        else:
            for i in enumerate(ans):
                if i < len(s) and s[i] != ans[i]:
                    res = f"Mistake in position {i + 1}."
                elif i == len(s):
                    res = "Your sequence is too short. Try again"
            res = "Too many symbols"
        return res

    def post(self, request):
        """
        Заполнение формы, проверка результатов, генерация новой
        """
        if 'generate_new' in request.POST:
            return self.get(request)

        form = SequenceForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            random_seq_id = request.session.get('random_seq_id')
            result = None
            if random_seq_id:
                try:
                    random_seq = Sequence.objects.get(id=random_seq_id)
                    result = self.check_mistake(answer, random_seq.answer)
                except Sequence.DoesNotExist:
                    result = "Sequence not found. Please try again."

            context = {
                'random_seq': random_seq,
                'form': form,
                'result': result
            }
            return render(request, 'cards/check_seq.html', context)

        context = {
            'form': form
        }
        return render(request, 'cards/check_seq.html', context)


class CheckNucleotideView(View):
    """
    Игра по определению нуклеотидов
    """
    def get(self, request):
        """
        Стартовое состояние страницы
        """
        nucl = list(Nucleotide.objects.all())
        html = 'cards/check_nucl.html'
        if nucl:
            random_nucl = random.choice(nucl)
            request.session['random_nucl_id'] = random_nucl.id
            if 'c' not in request.session:
                request.session['c'] = 0
            context = {
                'random_nucl': random_nucl,
                'form': NucleotideForm(),
                'score': request.session.get('score', 0),
                'c': request.session.get('c', 0)
            }

            if request.session['c'] >= 4:
                context = {
                    'score': request.session.get('score', 0),
                    'c': request.session.get('c', 0)
                }
                request.session['c'] = 0
                request.session['score'] = 0
                html = 'cards/check_nucl_result.html'

        else:
            random_nucl = None
            request.session['random_nucl_id'] = None

        context = {
            'random_nucl': random_nucl,
            'form': NucleotideForm(),
        }
        return render(request, html, context)

    def check_mistake(self, request, lst1, lst2):
        """
        Проверка ошибок после заполнения формы
        """
        s1, s2 = lst1
        ans1, ans2 = lst2
        if 'score' not in request.session:
            request.session['score'] = 0
        if s1.upper() == ans1.upper() and s2.lower() == ans2.lower():
            request.session['score'] += 1
            res = "Correct!"
        elif 'phosp' in s2.lower():
            res = 'You need to write down only nucleobase name!'
        else:
            res ='There is a mistake!'
        return res

    def post(self, request):
        """
        Генерация нового нуклеотида, фидбэк о заполнение формы
        """
        if 'generate_new' in request.POST:
            return self.get(request)

        form = NucleotideForm(request.POST)
        if form.is_valid():
            answer1 = form.cleaned_data['answer1']
            answer2 = form.cleaned_data['answer2']
            random_nucl_id = request.session.get('random_nucl_id')

            if random_nucl_id:
                try:
                    random_nucl = Nucleotide.objects.get(id=random_nucl_id)
                    answers = [answer1, answer2]
                    correct = [random_nucl.answer1, random_nucl.answer2]
                    result = self.check_mistake(request, answers, correct)
                    request.session['c'] += 1
                except Nucleotide.DoesNotExist:
                    result = "Nucleotide not found"
            else:
                result = "No nucleotide selected"
            tmp1 = request.session.get('score', 0)
            tmp2 = request.session.get('c', 0)
            context = {
                'random_nucl': random_nucl,
                'form': form,
                'result': result,
                'score': tmp1,
                'c': tmp2
            }
            return render(request, 'cards/check_nucl.html', context)

        context = {
            'form': form,
            'score': request.session.get('score', 0),
            'c': request.session.get('c', 0)
        }
        return render(request, 'cards/check_nucl.html', context)



class InfoPage(View):
    """
    Информационная страница
    """
    def get(self, request):
        """
        Тут форм заполнять не нужно
        Просто выводится страница стартовая
        """
        nucl = list(Nucleotide.objects.all())
        context = {}
        for n in nucl:
            context[n.answer1] = n

        return render(request, 'cards/info_nucl.html', context)
