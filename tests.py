import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_choice_generates_sequential_ids():
    question = Question(title='Matemática')
    c1 = question.add_choice('Opção A')
    c2 = question.add_choice('Opção B')
    
    assert c1.id == 1
    assert c2.id == 2

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('Remover esta')
    
    question.remove_choice_by_id(choice.id)
    
    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id_raises_exception():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match="Invalid choice id"):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices_updates_status():
    question = Question(title='q1')
    c1 = question.add_choice('Errada', is_correct=False)
    
    question.set_correct_choices([c1.id])
    
    assert c1.is_correct is True

def test_correct_selected_choices_returns_only_correct_ones():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('Correta 1', is_correct=True)
    c2 = question.add_choice('Incorreta', is_correct=False)
    
    results = question.correct_selected_choices([c1.id, c2.id])
    
    assert c1.id in results
    assert c2.id not in results

def test_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([c1.id, c2.id])

def test_choice_text_validation_empty():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice("")

def test_choice_text_validation_too_long():
    question = Question(title='q1')
    
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice("a" * 101)

def test_points_out_of_range_raises_exception():
    with pytest.raises(Exception):
        Question(title='q1', points=0) # Abaixo do mínimo
    
    with pytest.raises(Exception):
        Question(title='q1', points=101) # Acima do máximo

@pytest.fixture
def question_with_choices():
    """Retorna uma questão de múltipla escolha com 4 alternativas, sendo 2 corretas."""
    q = Question(title="Quais são cores primárias?", max_selections=3)
    q.add_choice("Azul", is_correct=True)
    q.add_choice("Amarelo", is_correct=True)
    q.add_choice("Verde", is_correct=False)
    q.add_choice("Preto", is_correct=False)
    return q

def test_correct_selected_choices_with_partial_success(question_with_choices):
    # Usuário seleciona Azul (1), Amarelo (2) e Verde (3)
    selected_ids = [1, 2, 3]
    
    correct_results = question_with_choices.correct_selected_choices(selected_ids)
    
    # Deve retornar apenas os IDs 1 e 2 (Azul e Amarelo)
    assert len(correct_results) == 2
    assert 1 in correct_results
    assert 2 in correct_results
    assert 3 not in correct_results

def test_remove_all_choices_behavior(question_with_choices):
    assert len(question_with_choices.choices) == 4
    
    question_with_choices.remove_all_choices()
    
    assert len(question_with_choices.choices) == 0
    
    new_choice = question_with_choices.add_choice("Nova Opção")
    assert new_choice.id == 1

def test_set_correct_choices_bulk_update(question_with_choices):
    # Verde (3) e Preto (4) eram falsos. Vamos torná-los verdadeiros.
    question_with_choices.set_correct_choices([3, 4])
    
    # Verifica se os objetos foram atualizados
    assert question_with_choices.choices[2].is_correct is True # Verde
    assert question_with_choices.choices[3].is_correct is True # Preto