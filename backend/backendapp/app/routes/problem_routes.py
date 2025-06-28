import zipfile, tempfile, os, yaml
from fastapi import FastAPI, Request, UploadFile, File

def register_problem_routes(app: FastAPI):
    @app.post("/")
    async def create_problem(request: Request):
        pid = request.app.state.problem_service.create_problem()
        return {"id": pid}

    @app.put("/{problem_id}")
    async def update_problem(request: Request, problem_id: str, file: UploadFile = File(...)):
        with tempfile.TemporaryDirectory() as tmp:
            arc = os.path.join(tmp, file.filename)
            with open(arc, "wb") as f:
                f.write(await file.read())
            with zipfile.ZipFile(arc, 'r') as z:
                z.extractall(tmp)

            cfg = yaml.safe_load(open(os.path.join(tmp, "config.yaml")))
            pconf = cfg.get("problem", {})
            title = pconf.get("title", None)
            judge_method = pconf.get("judge_method", None)
            status = pconf.get("status", None)
            hidden_list = pconf.get("hidden-subtasks", None)
            tags = pconf.get("tags", None)

            stmt = open(os.path.join(tmp, "statement.md")).read()
            subt_d = os.path.join(tmp, "subtasks")
            tpl_d = os.path.join(tmp, "templates")
            tpl_arg = tpl_d if os.path.isdir(tpl_d) else None
            utils_d = os.path.join(tmp, "utils")

            subs = []
            for nm in sorted(os.listdir(subt_d)):
                path = os.path.join(subt_d, nm)
                if os.path.isdir(path):
                    cases = []
                    for fn in sorted(os.listdir(path)):
                        if fn.endswith(".in"):
                            b = fn[:-3]
                            cases.append((
                                open(os.path.join(path, b + ".in")).read(),
                                open(os.path.join(path, b + ".ans")).read()
                            ))
                    pts = int(open(os.path.join(path, "point.txt")).read())
                    subs.append((nm, cases, pts))

            svc = request.app.state.problem_service
            svc.update_problem(
                problem_id=problem_id,
                title=title,
                statement=stmt,
                judge_method=judge_method,
                status=status,
                subtasks=subs,
                hidden_subtasks=hidden_list,
                tags=tags,
                template_dir=tpl_arg,
                utils_dir=utils_d
            )
            return {"id": problem_id, "message": "Updated"}
