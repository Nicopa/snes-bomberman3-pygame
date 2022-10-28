from models.Cell import Cell

class Wall(Cell):
	def __init__(self, left: int, top: int, width: int, height: int):
		super().__init__(left, top, width, height)