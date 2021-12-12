import argparse
import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from datacenter.models import (Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject)


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid_id=schoolkid.id, points__lte=3)
    count = 0
    for mark in marks:
        mark.points = 5
        count += 1
    Mark.objects.bulk_update(marks, ['points'])
    return count


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid_id=schoolkid.id)
    return chastisements.delete()[0]


def create_commendation(schoolkid, lesson_title):
    commendations = ["Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!", "Ты меня приятно удивил!",
                     "Великолепно!", "Прекрасно!", "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!",
                     "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!", "Очень хороший ответ!",
                     "Талантливо!",
                     "Ты сегодня прыгнул выше головы!", "Я поражен!", "Уже существенно лучше!", "Потрясающе!",
                     "Замечательно!", "Прекрасное начало!", "Так держать!", "Ты на верном пути!", "Здорово!",
                     "Это как раз то, что нужно!", "Я тобой горжусь!", "С каждым разом у тебя получается всё лучше!",
                     "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!", "Ты растешь над собой!",
                     "Ты многое сделал, я это вижу!", "Теперь у тебя точно все получится!"]

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=lesson_title
        ).order_by('-date')

    if Commendation.objects.filter(
            created=lesson[0].date, schoolkid_id=schoolkid.id, subject_id=lesson[0].subject.id
            ).count() != 0:
        raise Lesson.DoesNotExist

    commendation = Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson[0].date,
        schoolkid_id=schoolkid.id,
        subject_id=lesson[0].subject.id,
        teacher_id=lesson[0].teacher.id
        )
    return commendation


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('surname', help='Имя ученика')
    parser.add_argument('subject', help='Предмет')
    args = parser.parse_args()
    surname = args.surname
    subject = args.subject
    year_of_study = 6
    group_letter = 'А'
    try:
        schoolkid = Schoolkid.objects.get(
            full_name__contains=surname,
            year_of_study=year_of_study,
            group_letter=group_letter
            )
        print(f'Исправлено оценок - {fix_marks(schoolkid)}')
        print(f'Удалено замечаний - {remove_chastisements(schoolkid)}')
        subject = Subject.objects.get(title=subject, year_of_study=year_of_study)
        commmendation = create_commendation(schoolkid, subject)
        print(
            f'Похвала: {commmendation.text} от'
            f' {commmendation.teacher} по'
            f' {commmendation.subject}'
            )
    except Schoolkid.DoesNotExist:
        print(f'Нет такого ученика {surname} в классе {year_of_study}{group_letter}')
    except Schoolkid.MultipleObjectsReturned:
        print(f'Несколько учеников {surname} в классе {year_of_study}{group_letter}')
    except Subject.DoesNotExist:
        print(f'Предмет  {subject} в классе {year_of_study} не найден')
    except Lesson.DoesNotExist:
        print('Урок не найден')


if __name__ == '__main__':
    main()
