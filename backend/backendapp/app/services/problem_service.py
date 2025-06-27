import hashlib
import os
from typing import Optional, List, Tuple
from models.problem_odm import Problem, Subtask, Testcase

class ProblemService:
    @staticmethod
    def create_problem(
        title: str,
        statement: str,
        template: str = "",
        judge_script: str = "",
        judge_method: str = "default",
        status: int = 0,
        subtasks: Optional[List[Tuple[List[Tuple[str, str]], int]]] = None,
        base_dir: str = "/problems",
    ) -> Problem:
        subtask_docs = []

        if subtasks is None:
            subtasks = []

        for testcase_tuples, points in subtasks:
            testcase_docs = []
            for input_str, answer_str in testcase_tuples:
                input_hash = hashlib.sha256(input_str.encode()).hexdigest()
                answer_hash = hashlib.sha256(answer_str.encode()).hexdigest()

                testcase_docs.append(Testcase(
                    hashed_input=input_hash,
                    hashed_answer=answer_hash
                ))

            subtask_docs.append(Subtask(testcases=testcase_docs, points=points))

        problem = Problem(
            title=title,
            statement=statement,
            template=template,
            judge_script=judge_script,
            judge_method=judge_method,
            status=status,
            subtasks=subtask_docs,
        ).save()

        problem_path = os.path.join(base_dir, str(problem.id))
        os.makedirs(problem_path, exist_ok=True)

        for testcase_tuples, _ in subtasks:
            for input_str, answer_str in testcase_tuples:
                input_hash = hashlib.sha256(input_str.encode()).hexdigest()
                answer_hash = hashlib.sha256(answer_str.encode()).hexdigest()

                with open(os.path.join(problem_path, f"{input_hash}.in"), "w") as f_in:
                    f_in.write(input_str)

                with open(os.path.join(problem_path, f"{answer_hash}.out"), "w") as f_out:
                    f_out.write(answer_str)

        return problem
