
class Button():
	"""
    A class used to represent a button.

    Attributes:
    ----------
    image : pygame.image
        The image with the button background
    x_pos : int
        The position x of the button
    y_pos : int
        The position y of the button
    font : Font (pygame.font)
        The font of the button text
    base_color : string
        The color of the button text. Example: "#b68f40"
    hovering_color : string
        The color of the button text when the mouse is over it. Example: "#d7fcd4"
    text_input : string
        The text string of the button
    text : Surface (pygame)
        The text of the button (Surface with the specified text rendered on it)
    rect : Rect (pygame)
        The position and size from the image. Pygame object for storing rectangular coordinates
	text_rect : Rect (pygame)
		The position and size from the text. Pygame object for storing rectangular coordinates
    """

	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		"""Initializes a button.

        Params:
        ----------
        image : pygame.image
            The image with the button background
        pos : (int, int)
            The position of the button
        text_input : string
            The text string of the button
        font : Font (pygame.font)
            The font of the button text
        base_color : string
            The color of the button text. Example: "#b68f40"
        hovering_color : string
            The color of the button text when the mouse is over it. Example: "#d7fcd4"
        """
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		"""Draws the button.

        Params:
        ----------
        screen : 
            The screen where draws the button
        """
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		"""Check if the mouse is on the button.

        Params:
        ----------
        position : (int, int)
            The position where the mouse is (x, y)
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		"""Check if the mouse is on top and has to change the color button.

        Params:
        ----------
        position : (int, int)
            The position where the mouse is (x, y)
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

	def changeText(self, new_text):
		"""Changes the text of the button.

        Params:
        ----------
        new_text : string
            The new text of the button
        """
		self.text_input = new_text
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))