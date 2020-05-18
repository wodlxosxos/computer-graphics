import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
# draw coordinate
	glBegin(GL_LINES)
	glColor3ub(255, 0, 0)
	glVertex2fv(np.array([0.,0.]))
	glVertex2fv(np.array([1.,0.]))
	glColor3ub(0, 255, 0)
	glVertex2fv(np.array([0.,0.]))
	glVertex2fv(np.array([0.,1.]))
	glEnd()
# draw triangle
	glBegin(GL_TRIANGLES)
	glColor3ub(255, 255, 255)
	glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
	glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
	glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
	glEnd()

r = 0
lth = np.radians(10)
B = np.array([[1.,0.,0.],
			  [0.,1.,0.],
			  [0.,0.,1.]])

M = np.array([[1.,0.,-0.1],
			  [0.,1.,0.],
			  [0.,0.,1.]])

P = np.array([[1.,0.,0.1],
			  [0.,1.,0.],
			  [0.,0.,1.]])

L = np.array([[np.cos(lth),-np.sin(lth),0.],
			  [np.sin(lth),np.cos(lth),0.],
			  [0.,0.,1.]])

def key_callback(window, key, scancode, action, mods) :
	global B, M, P, R, L, th, r, lth
	if key == glfw.KEY_Q and action == glfw.PRESS:
		B = M@B
#			render(B@R)
	elif key == glfw.KEY_E and action == glfw.PRESS:
		B = P@B
#			render(B@R)
	elif key == glfw.KEY_A and action == glfw.PRESS:
		r = r + 1
#			render(B@R)
	elif key == glfw.KEY_D and action == glfw.PRESS:
		r = r - 1
#			render(B@R)
	elif key == glfw.KEY_1 and action == glfw.PRESS:
		B = np.array([[1.,0.,0.],
					  [0.,1.,0.],
					  [0.,0.,1.]])
		r = 0
	elif key == glfw.KEY_W and action == glfw.PRESS:
		S = np.array([[0.9,0.,0.],
					  [0.,1.,0.],
					  [0.,0.,1.]])
		B = S@B
	elif key == glfw.KEY_S and action == glfw.PRESS:
		B = L@B

def main() :
	if not glfw.init() :
		return

	window = glfw.create_window(480,480,"CG_weekly_practice_03_2018008759",None,None)
	if not window:
		glfw.terminate()
		return
	
	glfw.set_key_callback(window, key_callback)

	glfw.make_context_current(window)
	glfw.swap_interval(1)
	global B, R, r
	while not glfw.window_should_close(window) :
		glfw.poll_events()
		th = np.radians(10*r)
		R = np.array([[np.cos(th),-np.sin(th),0.],
					  [np.sin(th),np.cos(th),0.],
					  [0.,0.,1.]])
		render(B@R)
		glfw.swap_buffers(window)
	glfw.terminate()

if __name__ == "__main__":
	main()
