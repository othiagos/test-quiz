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