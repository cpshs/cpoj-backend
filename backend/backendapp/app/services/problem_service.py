import hashlib
import os
import shutil
from typing import Optional, List, Tuple
from ..models.problem_odm import Problem, Subtask, Template, Testcase

class ProblemService:
    @staticmethod
    def create_problem(
        base_dir: str = "/problems",
    ) -> str:
        problem = Problem(title="New-Problem",
                          statement="",
                          judge_method="default").save()
        pid = str(problem.id)
        os.makedirs(os.path.join(base_dir, pid), exist_ok=True)
        return pid

    @staticmethod
    def update_problem(
        problem_id: str,
        title: Optional[str] = None,
        statement: Optional[str] = None,
        judge_script: Optional[str] = None,
        judge_method: Optional[str] = None,
        status: Optional[int] = None,
        subtasks: Optional[List[Tuple[str, List[Tuple[str, str]], int]]] = None,
        hidden_subtasks: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        template_dir: Optional[str] = None,
        utils_dir: Optional[str] = None,
        base_dir: str = "/problems",
    ) -> str:
        prob = Problem.objects(id=problem_id).first()
        if title is not None:
            prob.title = title
        if statement is not None:
            prob.statement = statement
        if judge_script is not None:
            prob.judge_script = judge_script
        if judge_method is not None:
            prob.judge_method = judge_method
        if status is not None:
            prob.status = status
        if tags is not None:
            prob.tags = tags
        if subtasks is not None:
            hidden_subtasks = hidden_subtasks or []
            docs = []
            for name, case_list, pts in subtasks:
                tc_docs = []
                for inp, ans in case_list:
                    hi = hashlib.sha256(inp.encode()).hexdigest()
                    ha = hashlib.sha256(ans.encode()).hexdigest()
                    tc_docs.append(Testcase(hashed_input=hi, hashed_answer=ha))
                docs.append(Subtask(name=name, hidden=(name in hidden_subtasks), testcases=tc_docs, points=pts))
            prob.subtasks = docs
        prob.save()

        problem_path = os.path.join(base_dir, problem_id)
        if os.path.isdir(problem_path):
            for item in os.listdir(problem_path):
                item_path = os.path.join(problem_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        else:
            os.makedirs(problem_path, exist_ok=True)

        if utils_dir and os.path.isdir(utils_dir):
            dst = os.path.join(problem_path, "utils")
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(utils_dir, dst, dirs_exist_ok=True)

        if template_dir and os.path.isdir(template_dir):
            dst = os.path.join(problem_path, "templates")
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(template_dir, dst, dirs_exist_ok=True)

        if subtasks is not None:
            for _, case_list, _ in subtasks:
                for inp, ans in case_list:
                    hi = hashlib.sha256(inp.encode()).hexdigest()
                    ha = hashlib.sha256(ans.encode()).hexdigest()
                    with open(os.path.join(problem_path, f"{hi}"), "w") as f:
                        f.write(inp)
                    with open(os.path.join(problem_path, f"{ha}"), "w") as f:
                        f.write(ans)

        return problem_id
