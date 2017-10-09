# Image manipulation
#
# You'll need Python 2.7 and must install these packages:
#
#   numpy, PyOpenGL, Pillow

import sys, os, numpy

try: # Pillow
  from PIL import Image
except:
  print 'Error: Pillow has not been installed.'
  sys.exit(0)

try: # PyOpenGL
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print 'Error: PyOpenGL has not been installed.'
  sys.exit(0)

  
  
# Constants
maxIntensity = 235



# Globals

windowWidth  = 600 # window dimensions
windowHeight =  600

factor = 1 # factor by which luminance is scaled
term = 0 # term by which luminance is transformed


# Image directory and pathe to image file

imgDir      = 'images'
imgFilename = 'mandrill.png'

imgPath = os.path.join( imgDir, imgFilename )

currentImage = Image.open( imgPath )
outputImage = Image.open( imgPath )
  
  

# File dialog

import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()



# Copy output image to current image

def copyOutputImageToCurrentImage():

  global currentImage
  
  if(currentImage.size[0] != outputImage.size[0] or currentImage.size[1] != outputImage.size[1]):
    print 'Image dimensions to do not match!'
    return
    
  width  = currentImage.size[0]
  height = currentImage.size[1]  
  tmpPixels = outputImage.load()
  crtPixels = currentImage.load()
  
  for i in range(width):
    for j in range(height):

      # read pixel in temporary image
  
      r,g,b = tmpPixels[i,j]
  
      # write to current image
  
      crtPixels[i,height-j-1] = (r,g,b)

  # Done
  


# Modify the current image and write to temporary image

def buildOutputImage():

  # Read image and convert to YCbCr

  print imgPath
  global outputImage
  
  if(currentImage.size[0] != outputImage.size[0] or currentImage.size[1] != outputImage.size[1]):
    print 'Image dimensions to do not match!'
    return
    
  src = currentImage.convert( 'YCbCr' )
  srcPixels = src.load()
  outputImage = outputImage.convert( 'YCbCr' )
  dstPixels = outputImage.load()

  width  = src.size[0]
  height = src.size[1]

  # Build destination image from source image

  for i in range(width):
    for j in range(height):

      # read source pixel
      
      y,cb,cr = srcPixels[i,j]

      # ---- MODIFY PIXEL ----

      y = int(factor * y + term)
      
      # write destination pixel
      
      dstPixels[i,height-j-1] = (y,cb,cr)

  # Done

  outputImage = outputImage.convert( 'RGB' )



# Set up the display and draw the current image

def display():

  # Clear window

  glClearColor ( 1, 1, 1, 0 )
  glClear( GL_COLOR_BUFFER_BIT )

  # get the output image

  img = outputImage

  width  = img.size[0]
  height = img.size[1]

  # Find where to position lower-left corner of image

  baseX = (windowWidth-width)/2
  baseY = (windowHeight-height)/2

  glWindowPos2i( baseX, baseY )

  # Get pixels and draw

  imageData = numpy.array( list( img.getdata() ), numpy.uint8 )

  glDrawPixels( width, height, GL_RGB, GL_UNSIGNED_BYTE, imageData )

  glutSwapBuffers()


  
# Handle keyboard input

def keyboard( key, x, y ):

  if key == '\033': # ESC = exit
    sys.exit(0)

  elif key == 'l':
    path = tkFileDialog.askopenfilename( initialdir = imgDir )
    if path:
      loadImage( path )

  elif key == 's':
    outputPath = tkFileDialog.asksaveasfilename( initialdir = '.' )
    if outputPath:
      saveImage( outputPath )

  else:
    print 'key =', key    # DO NOT REMOVE THIS LINE.  It will be used during automated marking.

  glutPostRedisplay()


  
# Reset editor

def resetEditor():
  
  global term, factor
  
  term = 0
  factor = 1

# Load and save images.
#
# Modify these to load to the current image and to save the current image.
#
# DO NOT CHANGE THE NAMES OR ARGUMENT LISTS OF THESE FUNCTIONS, as
# they will be used in automated marking.

def loadImage( path ):

  global imgPath, currentImage, outputImage
  
  imgPath = path
  currentImage = Image.open(imgPath)
  width = currentImage.size[0]
  height = currentImage.size[1]
  outputImage = Image.new( 'YCbCr', (width,height) )
  resetEditor()
  buildOutputImage()
  print imgPath

def saveImage( path ):

  currentImage.save( path )

  

# Handle window reshape

def reshape( newWidth, newHeight ):

  global windowWidth, windowHeight

  windowWidth  = newWidth
  windowHeight = newHeight

  glutPostRedisplay()



# Mouse state on initial click

button = None
initX = 0
initY = 0
initFactor = 1
initTerm = 0



# Handle mouse click/unclick

def mouse( btn, state, x, y ):

  global button, initX, initY, initFactor

  if state == GLUT_DOWN:
	button = btn     
	initX = x     
	initY = y 	

  elif state == GLUT_UP:

    button = None
    copyOutputImageToCurrentImage()



# Handle mouse motion

def motion( x, y ):

  diffX = x - initX
  diffY = y - initY

  global factor, term

  factor = initFactor - diffY / float(windowHeight)
  term = initTerm + diffX / float(windowWidth) *  maxIntensity
  # print "initFactor => %f  diffY => %f  height => %f  factor => %f  term => %f" %(initFactor, diffY, windowHeight, factor, term)

  if factor < 0:
    factor = 0

  buildOutputImage()
  glutPostRedisplay()
  

    
# Run OpenGL
loadImage(imgPath)
glutInit()
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( windowWidth, windowHeight )
glutInitWindowPosition( 50, 50 )

glutCreateWindow( 'imaging' )

glutDisplayFunc( display )
glutKeyboardFunc( keyboard )
glutReshapeFunc( reshape )
glutMouseFunc( mouse )
glutMotionFunc( motion )

glutMainLoop()
