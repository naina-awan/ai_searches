import tkinter as tk

from constants import clr


class ControlPanel:
    def __init__(self, parent, state, callbacks):
        self.state = state
        self.callbacks = callbacks
        self._build(parent)

    def _build(self, parent):
        p = tk.Frame(parent, bg="#111827")
        p.pack(fill="both", expand=True, padx=10, pady=10)

        self._section(p, "grid config")
        self._label(p, "rows")
        self._scale(p, self.state["rows"], 5, 35)
        self._label(p, "columns")
        self._scale(p, self.state["cols"], 5, 55)
        tk.Button(
            p, text="apply size", bg="#6366f1", fg="white", bd=0, pady=4,
            font=("courier", 8, "bold"), cursor="hand2",
            command=self.callbacks["apply_size"],
        ).pack(fill="x", pady=1)
        self._label(p, "obstacle density")
        self._scale(p, self.state["density"], 0.05, 0.60, 0.01)

        bf = tk.Frame(p, bg="#111827")
        bf.pack(fill="x", pady=2)
        for txt, bg, key in [("generate", "#4f46e5", "generate"), ("clear", "#374151", "clear")]:
            tk.Button(
                bf, text=txt, bg=bg, fg="white", bd=0, pady=4,
                font=("courier", 8, "bold"), cursor="hand2",
                command=self.callbacks[key],
            ).pack(side="left", fill="x", expand=True, padx=1)

        self._section(p, "algorithm")
        self._radios(p, [("a* search", "astar"), ("greedy bfs", "gbfs")], self.state["algo"])

        self._section(p, "heuristic")
        self._radios(p, [("manhattan", "manhattan"), ("euclidean", "euclidean")], self.state["heur"])

        self._section(p, "map editor")
        self._radios(
            p,
            [("set start", "start"), ("set goal", "goal"), ("draw wall", "wall"), ("erase", "erase")],
            self.state["paint"],
        )

        self._section(p, "dynamic mode")
        tk.Checkbutton(
            p, text=" dynamic obstacles", variable=self.state["dyn_mode"],
            bg="#111827", fg="#e2e8f0", selectcolor="#6366f1",
            activebackground="#111827", font=("courier", 9), cursor="hand2",
        ).pack(anchor="w")

        self._section(p, "metrics")
        self.mn = self._metric_row(p, "nodes visited")
        self.mc = self._metric_row(p, "path cost")
        self.mt = self._metric_row(p, "time (ms)")

        self._section(p, "legend")
        for color, text in [
            (clr["start"], "start"), (clr["goal"], "goal"), (clr["path"], "path"),
            (clr["frontier"], "frontier"), (clr["visited"], "visited"),
            (clr["wall"], "wall"), (clr["agent"], "agent"),
        ]:
            row = tk.Frame(p, bg="#111827")
            row.pack(fill="x", pady=1)
            tk.Label(row, bg=color, width=2).pack(side="left", padx=(0, 5))
            tk.Label(row, text=text, bg="#111827", fg="#64748b", font=("courier", 8)).pack(side="left")

    def _section(self, parent, title):
        tk.Label(parent, text=title, bg="#111827", fg="#6366f1",
                 font=("courier", 8, "bold")).pack(anchor="w", pady=(8, 0))
        tk.Frame(parent, bg="#1f2937", height=1).pack(fill="x", pady=(2, 4))

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg="#111827", fg="#94a3b8",
                 font=("courier", 8)).pack(anchor="w")

    def _scale(self, parent, var, lo, hi, step=1):
        tk.Scale(
            parent, from_=lo, to=hi, resolution=step, orient="horizontal",
            variable=var, bg="#111827", fg="#e2e8f0",
            highlightthickness=0, troughcolor="#1f2937", font=("courier", 8),
        ).pack(fill="x")

    def _radios(self, parent, options, var):
        for text, value in options:
            tk.Radiobutton(
                parent, text=text, variable=var, value=value,
                bg="#111827", fg="#e2e8f0", selectcolor="#6366f1",
                activebackground="#111827", font=("courier", 9),
                indicatoron=0, padx=6, pady=3, bd=0, cursor="hand2",
            ).pack(fill="x", pady=1)

    def _metric_row(self, parent, label):
        row = tk.Frame(parent, bg="#111827")
        row.pack(fill="x", pady=1)
        tk.Label(row, text=label, bg="#111827", fg="#64748b",
                 font=("courier", 8), width=13, anchor="w").pack(side="left")
        v = tk.Label(row, text="—", bg="#111827", fg="#6366f1",
                     font=("courier", 10, "bold"))
        v.pack(side="right")
        return v

    def update_metrics(self, nodes, cost, ms):
        self.mn.config(text=str(nodes))
        self.mc.config(text=str(cost))
        self.mt.config(text=f"{ms} ms")
