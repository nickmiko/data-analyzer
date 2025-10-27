from typing import Callable, Any, Dict, List, Tuple, Optional

def menu(label: str | None = None, order: int | None = None, section: str | None = None):
    """Decorator to mark methods as menu items with optional label, order, and section (submenu)."""
    def decorator(func: Callable):
        setattr(func, "_menu_meta", {
            "label": label or func.__name__.replace("_", " "),
            "order": order,
            "section": section
        })
        return func
    return decorator


class MenuSelector:
    """Auto-discovers decorated methods and supports one-level submenus via 'section'."""
    def __init__(self):
        # Each item: (order, section, label, func)
        self._items: List[Tuple[int, Optional[str], str, Callable]] = []

    def discover(self, obj: Any):
        """Scan obj for callables decorated with @menu and store metadata."""
        items: List[Tuple[int, Optional[str], str, Callable]] = []
        for attr_name in dir(obj):
            if attr_name.startswith("_"):
                continue
            candidate = getattr(obj, attr_name)
            if callable(candidate) and hasattr(candidate, "_menu_meta"):
                meta = getattr(candidate, "_menu_meta", {})
                label = meta.get("label") or attr_name.replace("_", " ")
                order = meta.get("order")
                section = meta.get("section")
                sort_order = order if isinstance(order, int) else 10_000
                items.append((sort_order, section, label, candidate))
        # Stable sort by (order asc, label asc)
        items.sort(key=lambda t: (t[0], (t[1] or "").lower(), t[2].lower()))
        self._items = items

    def is_empty(self) -> bool:
        return not self._items

    def sections(self) -> List[str]:
        """Return sorted list of sections (submenus)."""
        section_map: Dict[str, int] = {}
        for order, section, _, _ in self._items:
            if section:
                if section not in section_map or order < section_map[section]:
                    section_map[section] = order
        # Sort sections by min order then name
        return sorted(section_map.keys(), key=lambda s: (section_map[s], s.lower()))

    def actions_in_root(self) -> List[Tuple[str, Callable]]:
        """Items without a section."""
        actions = [(label, func) for _, section, label, func in self._items if not section]
        actions.sort(key=lambda t: t[0].lower())
        return actions

    def actions_in_section(self, section: str) -> List[Tuple[str, Callable]]:
        """Items within a given section."""
        actions = [(label, func) for _, sec, label, func in self._items if sec == section]
        actions.sort(key=lambda t: t[0].lower())
        return actions

    def items_table(self, section: str | None = None) -> List[Dict[str, str]]:
        """
        Build a display table for the current view.
        - Root: shows root actions and sections.
        - Section: shows actions in the section and a Back option as id '0'.
        """
        rows: List[Dict[str, str]] = []
        if section is None:
            # Root actions first
            combined: List[Tuple[str, str]] = []
            for label, _ in self.actions_in_root():
                combined.append(("action", label))
            # Then sections (mark visually)
            for sec in self.sections():
                combined.append(("section", f"{sec} ▶"))

            rows = [{"id": str(i + 1), "action": label} for i, (_, label) in enumerate(combined)]
        else:
            actions = self.actions_in_section(section)
            rows = [{"id": str(i + 1), "action": label} for i, (label, _) in enumerate(actions)]
            # Add Back row as id '0'
            rows.insert(0, {"id": "0", "action": "◀ Back"})
        return rows

    def select(self, choice: str, section: str | None = None) -> Tuple[str, Any] | None:
        """
        Map a choice to a result:
        - Root: returns ('action', func) or ('section', section_name)
        - Section: returns ('action', func) or ('back', None)
        """
        choice = choice.strip()
        if section is not None:
            if choice == "0":
                return ("back", None)
            actions = self.actions_in_section(section)
            try:
                idx = int(choice) - 1
            except ValueError:
                return None
            if 0 <= idx < len(actions):
                _, func = actions[idx]
                return ("action", func)
            return None

        # Root view
        combined: List[Tuple[str, Any]] = []
        for label, func in self.actions_in_root():
            combined.append(("action", func))
        for sec in self.sections():
            combined.append(("section", sec))
        try:
            idx = int(choice) - 1
        except ValueError:
            return None
        if 0 <= idx < len(combined):
            return combined[idx]
        return None