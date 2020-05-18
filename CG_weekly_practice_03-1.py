import glfw
from OpenGL.GL import *
import numpy as np

def render(trmType) :
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	glBegin(trmType)
	glColor3ub(255, 255, 255)
	glVertex2fv(np.array([np.cos(np.radians(0)), np.sin(np.radians(0))]))
	glVertex2fv(np.array([np.cos(np.radians(30)),np.sin(np.radians(30))]))
	glVertex2fv(np.array([np.cos(np.radians(60)),np.sin(np.radians(60))]))
	glVertex2fv(np.array([np.cos(np.radians(90)),np.sin(np.radians(90))]))
	glVertex2fv(np.array([np.cos(np.radians(120)),np.sin(np.radians(120))]))
	glVertex2fv(np.array([np.cos(np.radians(150)),np.sin(np.radians(150))]))
	glVertex2fv(np.array([np.cos(np.radians(180)),np.sin(np.radians(180))]))
	glVertex2fv(np.array([np.cos(np.radians(210)),np.sin(np.radians(210))]))
	glVertex2fv(np.array([np.cos(np.radians(240)),np.sin(np.radians(240))]))
	glVertex2fv(np.array([np.cos(np.radians(270)),np.sin(np.radians(270))]))
	glVertex2fv(np.array([np.cos(np.radians(300)),np.sin(np.radians(300))]))
	glVertex2fv(np.array([np.cos(np.radians(330)),np.sin(np.radians(330))]))
	glEnd()
trm = 4
def key_callback(window, key, scancode, action, mods) :
	global trm
	if key==glfw.KEY_0:
		trm = 0
	elif key==glfw.KEY_9:
		trm = 9
	elif key==glfw.KEY_8:
		trm = 8
	elif key==glfw.KEY_7:
		trm = 7
	elif key==glfw.KEY_6:
		trm = 6
	elif key==glfw.KEY_5:
		trm = 5
	elif key==glfw.KEY_4:
		trm = 4
	elif key==glfw.KEY_3:
		trm = 3
	elif key==glfw.KEY_2:
		trm = 2
	elif key==glfw.KEY_1:
		trm = 1

def main() :
	if not glfw.init() :
		return

	window = glfw.create_window(480, 480, "CG_weekly_practice_03-1_2018008759", None, None)
	if not window:
		glfw.terminate()
		return

	glfw.set_key_callback(window, key_callback)

	glfw.make_context_current(window)
	render(GL_LINE_LOOP)
	global trm
	while not glfw.window_should_close(window) :
		glfw.poll_events()
		if trm == 1:
			render(GL_POINTS)
		elif trm == 2:
			render(GL_LINES)
		elif trm == 3:
			render(GL_LINE_STRIP)
		elif trm == 4:
			render(GL_LINE_LOOP)
		elif trm == 5:
			render(GL_TRIANGLES)
		elif trm == 6:
			render(GL_TRIANGLE_STRIP)
		elif trm == 7:
			render(GL_TRIANGLE_FAN)
		elif trm == 8:
			render(GL_QUADS)
		elif trm == 9:
			render(GL_QUAD_STRIP)
		elif trm == 0:
			render(GL_POLYGON)
		glfw.swap_buffers(window)

	glfw.terminate()

if __name__ == "__main__":
	main()
