from dataclasses import dataclass

@dataclass
class Category:
    id: int
    category_name: str

    def __str__(self):
        return self.category_name

    def __repr__(self):
        return self.category_name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id