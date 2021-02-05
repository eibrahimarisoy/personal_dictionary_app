import json
import random

import requests
from app import db
from app.helpers.decorators import login_required
from app.models import Synonym, UserDict, Word
from app.models.definition import Definition
from app.models.user import User
from flask import (Blueprint, g, redirect, render_template,
                   request, url_for)
from sqlalchemy.sql.expression import func
from config import configuration


module = Blueprint('word', __name__, url_prefix='/word')


@module.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    context = dict()
    query = (request.args.get('search')).rstrip()
    user = g.user
    word = Word.query.filter_by(title=query).first()
    context['definitions'] = []

    if word:

        if not (user.words.filter_by(id=word.id).first()):
            user.words.append(word)
            db.session.add(user)
            db.session.commit()

        if not user.can_practice:
            if (user.words.count()) >= 10:
                user.can_practice = True

        context['definitions'] = Definition.query.filter_by(
            word_id=word.id
            ).all()
        user_dict = UserDict.query.filter_by(
            user_id=user.id,
            word_id=word.id).first()

        if not user_dict:
            user_dict = UserDict(
                user_id=user.id,
                word_id=word.id,
                search_count=1
            )
        else:
            user_dict.search_count += 1

        db.session.add(user_dict)
        db.session.commit()

    else:
        response = requests.request(
            'GET',
            f"{configuration.URL}{query}",
            headers=configuration.HEADERS
        )

        if response.status_code != 200:
            return render_template('user/index.html', content=context)

        items = json.loads(response.content)
        if response.status_code == 200 and items['results']:
            word = Word(title=query)
            db.session.add(word)
            db.session.commit()
            user.words.append(word)
            if not user.can_practice:
                if (user.words.count()) >= 10:
                    user.can_practice = True
            for item in items['results']:
                definition = Definition(
                    content=item['definition'],
                    word_id=word.id,
                    part_of_speech=item.get('partOfSpeech')
                )
                db.session.add(definition)
                db.session.commit()
                if item.get('synonyms'):
                    for synonym in item.get('synonyms'):
                        synonym = Synonym(title=synonym)
                        db.session.add(synonym)
                        definition.synonyms.append(synonym)

                db.session.add(user)
                db.session.add(definition)
                db.session.commit()
            user_dict = UserDict(
                user_id=user.id,
                word_id=word.id,
                search_count=1
            )

            db.session.add(user_dict)
            db.session.commit()

            context['definitions'] = Definition.query.filter_by(
                word_id=word.id
                ).all()

    return render_template('user/index.html', content=context)


@module.route('/details/<id>', methods=['GET'])
@login_required
def details(id):
    context = dict()
    word = Word.query.get(id)
    print(word)
    context['word'] = word
    return render_template('user/details.html', content=context)


@module.route('/practice', methods=['GET', 'POST'])
@login_required
def practice():
    context = dict()
    return render_template('user/practice.html', content=context)


@module.route('/practicing', methods=['GET'])
@login_required
def practicing():
    context = dict()
    user = User.query.get(g.user.id)
    three_words = user.words.order_by(func.random()).limit(3).all()
    querying_word = random.choice(three_words)
    user_dict = UserDict.query.filter_by(
        user_id=g.user.id,
        word_id=querying_word.id
        ).first()
    user_dict.appearance_count_update()
    querying_definition = Definition.query.filter_by(
        word_id=querying_word.id
        ).order_by(func.random()).first()

    context = json.dumps({
        'querying_definition': querying_definition.content,
        'first_word': three_words[0].title,
        'second_word': three_words[1].title,
        'third_word': three_words[2].title,
        })
    return context


@module.route('/check', methods=['POST'])
@login_required
def check():
    context = dict()
    if request.method == 'POST':
        querying_definition = request.form.get('querying_definition')
        answer = request.form.get('answer')

        definition_obj = Definition.query.filter_by(
            content=querying_definition
            ).first()
        exact_word = Word.query.get(definition_obj.word_id)
        user_dict_answer = UserDict.query.filter_by(
            user_id=g.user.id,
            word_id=exact_word.id
            ).first()
        user_dict_exact_answer = UserDict.query.filter_by(
            user_id=g.user.id,
            word_id=exact_word.id
            ).first()

        if exact_word.title == answer:
            user_dict_answer.practice_point += 1
            db.session.add(user_dict_answer)
            db.session.commit()

            context = json.dumps({
                'result': 'Contragulations. Your answer is correct',
                'definition': querying_definition,
                'word': exact_word.title,
            })
            return context

        else:
            words = request.form.getlist('words[]')
            words.remove(exact_word.title)
            user_dict_exact_answer.practice_point -= 2
            db.session.add(user_dict_exact_answer)
            db.session.commit()

            for item in words:
                word = Word.query.filter_by(title=item).first()
                user_dict_other = UserDict.query.filter_by(
                    user_id=g.user.id,
                    word_id=word.id
                ).first()
                user_dict_other.practice_point -= 1
                db.session.add(user_dict_other)
                db.session.commit()

            context = json.dumps({
                'result': 'Opps. Your answer is incorrect',
                'definition': querying_definition,
                'word': exact_word.title,
            })
            return context


@module.route('/exit-practice', methods=['GET'])
@login_required
def exit_practice():
    return redirect(url_for('word.practice'))
