from relation import TeacherSubject


class TeachersSubjectsRepository:
    @staticmethod
    def get_subjects_for_teacher(teacher_id):
        return TeacherSubject.query.filter(TeacherSubject.teacher_id == teacher_id).all()
