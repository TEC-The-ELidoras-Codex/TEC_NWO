"""Standalone TEC ThoughtMap Phase 2 module with AI expansion hotkey.

Ctrl+Space on a selected node triggers expansion suggestions via ai_expander.expand_node.
Saves/loads JSON with schemaVersion=2.
"""
from __future__ import annotations
import json
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path

try:
    from .ai_expander import expand_node, synthesize
except Exception:  # pragma: no cover
    from ai_expander import expand_node, synthesize  # type: ignore


@dataclass
class ThoughtNode:
    id: int
    title: str
    x: int
    y: int
    children: List[int] = field(default_factory=list)


class TECThoughtMap:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TEC-ThoughtMap - Phase 2")
        self.canvas = tk.Canvas(self.root, width=1200, height=800, bg="#0f1115")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.status = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status, anchor="w")
        self.status_bar.pack(fill=tk.X)
        self.nodes: Dict[int, ThoughtNode] = {}
        self.node_items: Dict[int, int] = {}  # node.id -> rectangle id
        self.text_items: Dict[int, int] = {}
        self.next_id = 1
        self.selected: Optional[int] = None
        self.file_path: Optional[Path] = None
        self._build_menu()
        self._bind_events()
        self._create_root_node()
        self.update_status("Ready – Ctrl+Space to expand node")

    def _build_menu(self):
        bar = tk.Menu(self.root)
        file_m = tk.Menu(bar, tearoff=0)
        file_m.add_command(label="New", command=self.new_map)
        file_m.add_command(label="Open", command=self.load)
        file_m.add_command(label="Save", command=self.save)
        file_m.add_command(label="Save As", command=lambda: self.save(as_new=True))
        file_m.add_separator()
        file_m.add_command(label="Export Graph JSON", command=self.export_graph)
        bar.add_cascade(label="File", menu=file_m)

        node_m = tk.Menu(bar, tearoff=0)
        node_m.add_command(label="Add Child", command=self.add_child)
        node_m.add_command(label="Expand (AI)", command=self.expand_selected_ai)
        node_m.add_command(label="Synthesize Branch", command=self.synthesize_branch)
        bar.add_cascade(label="Node", menu=node_m)

        self.root.config(menu=bar)

    def _bind_events(self):
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.root.bind("<Control-space>", lambda e: self.expand_selected_ai())

    def _create_root_node(self):
        self.create_node("Guardian's Burden", 600, 400)

    def create_node(self, title: str, x: int, y: int) -> int:
        node_id = self.next_id
        self.next_id += 1
        n = ThoughtNode(id=node_id, title=title, x=x, y=y)
        self.nodes[node_id] = n
        rect = self.canvas.create_rectangle(x-80, y-25, x+80, y+25, fill="#1e2430", outline="#4e5a6e")
        text = self.canvas.create_text(x, y, text=title, fill="#d7e1ed", font=("Segoe UI", 11, "bold"))
        self.node_items[node_id] = rect
        self.text_items[node_id] = text
        return node_id

    def add_child(self):
        if not self.selected:
            self.update_status("Select a node first")
            return
        title = simpledialog.askstring("New Child", "Title:")
        if not title:
            return
        parent = self.nodes[self.selected]
        nid = self.create_node(title, parent.x + 200, parent.y + 100 * (len(parent.children)+1))
        parent.children.append(nid)
        self._draw_edge(parent.id, nid)

    def expand_selected_ai(self):
        if not self.selected:
            self.update_status("Select a node for expansion")
            return
        parent = self.nodes[self.selected]
        suggestions = expand_node(parent.title, strategy="concept", count=4)
        base_y = parent.y - 120
        for i, s in enumerate(suggestions):
            nid = self.create_node(s, parent.x - 250, base_y + i*90)
            parent.children.append(nid)
            self._draw_edge(parent.id, nid)
        self.update_status(f"Expanded {parent.title} with {len(suggestions)} children")

    def synthesize_branch(self):
        if not self.selected:
            self.update_status("Select a node first")
            return
        branch_children = [self.nodes[cid].title for cid in self.nodes[self.selected].children]
        summary = synthesize(branch_children)
        messagebox.showinfo("Branch Synthesis", summary)

    def save(self, as_new: bool = False):
        if as_new or not self.file_path:
            path = filedialog.asksaveasfilename(defaultextension=".json", title="Save ThoughtMap")
            if not path:
                return
            self.file_path = Path(path)
        data = {
            "schemaVersion": 2,
            "nodes": [
                {"id": n.id, "title": n.title, "x": n.x, "y": n.y, "children": n.children}
                for n in self.nodes.values()
            ]
        }
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.update_status(f"Saved to {self.file_path}")

    def load(self):
        path = filedialog.askopenfilename(filetypes=[["JSON", "*.json"]], title="Load ThoughtMap")
        if not path:
            return
        self.file_path = Path(path)
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        self._clear()
        for n in raw.get("nodes", []):
            nid = self.create_node(n["title"], n["x"], n["y"])
            self.nodes[nid].children = n.get("children", [])
        for n in self.nodes.values():
            for child in n.children:
                if child in self.nodes:
                    self._draw_edge(n.id, child)
        self.update_status(f"Loaded {path}")

    def export_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", title="Export Graph JSON")
        if not path:
            return
        payload = {
            "type": "thoughtmap.export",
            "schemaVersion": 2,
            "nodes": [
                {"id": n.id, "title": n.title, "children": n.children}
                for n in self.nodes.values()
            ],
            "edges": [
                {"from": p.id, "to": c, "type": "concept"}
                for p in self.nodes.values() for c in p.children if c in self.nodes
            ]
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.update_status(f"Exported graph {path}")

    def _on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        for nid, rect in self.node_items.items():
            if rect == item[0] or self.text_items[nid] == item[0]:
                self.selected = nid
                self.update_status(f"Selected {self.nodes[nid].title}")
                return

    def _on_drag(self, event):
        if not self.selected:
            return
        n = self.nodes[self.selected]
        n.x, n.y = event.x, event.y
        self._redraw_node(n.id)
        self.canvas.delete("edge")
        for parent in self.nodes.values():
            for c in parent.children:
                if c in self.nodes:
                    self._draw_edge(parent.id, c)

    def _draw_edge(self, a: int, b: int):
        na, nb = self.nodes[a], self.nodes[b]
        self.canvas.create_line(na.x, na.y, nb.x, nb.y, fill="#3a4454", width=2, tags="edge")

    def _redraw_node(self, nid: int):
        n = self.nodes[nid]
        self.canvas.coords(self.node_items[nid], n.x-80, n.y-25, n.x+80, n.y+25)
        self.canvas.coords(self.text_items[nid], n.x, n.y)

    def _clear(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.node_items.clear()
        self.text_items.clear()
        self.next_id = 1

    def new_map(self):
        if messagebox.askyesno("Confirm", "Discard current map?"):
            self._clear()
            self._create_root_node()

    def update_status(self, msg: str):
        self.status.set(msg)

    def run(self):
        self.root.mainloop()


def run():
    TECThoughtMap().run()

if __name__ == "__main__":
    run()
