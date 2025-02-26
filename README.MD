2025-02-26 11:02:05,148 - DEBUG - Using proactor: IocpProactor
[32mINFO[0m:     Started server process [[36m1608[0m]
[32mINFO[0m:     Waiting for application startup.
2025-02-26 11:02:05,347 - DEBUG - executing <function connect.<locals>.connector at 0x0000026FF82E2520>
2025-02-26 11:02:05,349 - DEBUG - operation <function connect.<locals>.connector at 0x0000026FF82E2520> completed
[31mERROR[0m:    Traceback (most recent call last):
  File "C:\Users\automation_svc\Documents\HexIT\venv\Lib\site-packages\starlette\routing.py", line 693, in lifespan
    async with self.lifespan_context(app) as maybe_state:
               ~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "C:\Users\automation_svc\Documents\HexIT\venv\Lib\site-packages\starlette\routing.py", line 569, in __aenter__
    await self._router.startup()
  File "C:\Users\automation_svc\Documents\HexIT\venv\Lib\site-packages\starlette\routing.py", line 670, in startup
    await handler()
  File "C:\Users\automation_svc\Documents\HexIT\src\api\endpoints.py", line 19, in startup_event
    graph = await init_graph()  # This ensures the graph is compiled once.
            ^^^^^^^^^^^^^^^^^^
  File "C:\Users\automation_svc\Documents\HexIT\src\flow\graph.py", line 42, in init_graph
    _graph = builder.compile(checkpointer=memory)
  File "C:\Users\automation_svc\Documents\HexIT\venv\Lib\site-packages\langgraph\graph\state.py", line 539, in compile
    self.validate(
    ~~~~~~~~~~~~~^
        interrupt=(
        ^^^^^^^^^^^
    ...<3 lines>...
        )
        ^
    )
    ^
  File "C:\Users\automation_svc\Documents\HexIT\venv\Lib\site-packages\langgraph\graph\graph.py", line 390, in validate
    raise ValueError(
        f"At '{start}' node, '{cond}' branch found unknown target '{end}'"
    )
ValueError: At 'evaluate_flow_decision' node, 'determine_flow_outcome' branch found unknown target 'END'

[31mERROR[0m:    Application startup failed. Exiting.
