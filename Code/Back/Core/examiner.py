from dataclasses import dataclass


@dataclass
class Question:
    native_phrase: str
    references: list[str]


class Examiner:
    @staticmethod
    def next_question(username: str = None, user_pass: str = None) -> Question:
        return Question(native_phrase="Кошка сидит на столе",
                        references=["A cat sits on the table",
                                    "The cat sits on the table",
                                    "A cat is sitting on the table",
                                    "The cat is sitting on the table"])
