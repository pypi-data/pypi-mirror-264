import json
from typing import Any
from difflib import get_close_matches




class GPT:
    def __init__(self, *args: tuple[Any], **kwds: tuple[Any]) -> None:
        self.__args = args

    def __call__(self):
        self.__q = []
        for arg in self.__args:
            self.__q.append(arg)

        knowledge_base: dict = self.__load_knowledge_base(
            ".\\torelib\\v1torelib\\gpt\\_knowledge_base.json"
        )

        while True:
            user_input: str = input("You: ")

            if user_input.lower() in ["quit", "exit", "bye"]:
                break

            best_match: str | None = self.__find_best_match(
                user_input, [q["question"] for q in knowledge_base["questions"]]
            )

            if best_match:
                answer: str = self.__get_answer_for_question(best_match, knowledge_base)
                print(f"Bot: {answer}")
            else:
                print("Bot: I don't know the answer. Can you teach me?")
                new_answer: str = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != "skip":
                    knowledge_base["questions"].append(
                        {"question": user_input, "answer": new_answer}
                    )
                    self.__save_knowledge_base(
                        ".\\torelib\\v1torelib\\gpt\\_knowledge_base.json", knowledge_base
                    )
                    print("Bot: Thank you! I learned a new response!")

    def __load_knowledge_base(self, __file_path: str) -> dict:
        with open(__file_path, "r") as file:
            data: dict = json.load(file)
        return data

    def __save_knowledge_base(self, __file_path: str, data: dict) -> None:
        with open(__file_path, "w") as file:
            json.dump(data, file, indent=2)

    def __find_best_match(self, user_question: str, questions: list[str]) -> str | None:
        matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def __get_answer_for_question(
        self, question: str, knowledge_base: dict
    ) -> str | None:
        for q in knowledge_base["questions"]:
            if q["question"] == question:
                return q["answer"]


gpt: GPT = GPT()
gpt()
