
import java.awt.image.BufferedImage;    // all for compressed JPG export
import javax.imageio.plugins.jpeg.*;
import javax.imageio.*;
import javax.imageio.stream.*;

/*
CREATE NEW ZOOM LEVEL
Jeff Thompson | jeffreythompson.org | 2017

Creates a new slippy map zoom level from a previous one. (Essentially
just combines four tiles into one, meaning (with this code) you can
only make zoomed-out tiles, not zoomed-in ones – sorry!)

*/


int prevZoom =     1;            // for getting file path
int numX =         312;          // largest-numbered folder in that zoom level
int numY =         316;          // largest-numbered image in each X folder
color bg =         color(255);   // if we run out of tilesœ

String tilePath =  "../Website/tiles/";

float compressionLevel = 0.5;          // jpg compression, 0.5 = 50% quality
String extension =       ".jpg";


void setup() {
  
  int newZoom = prevZoom - 1;
  if (newZoom < 1) {
    println("WARNING: new zoom level less than 1!");
  }
  
  int newNumX = ceil(numX/2);
  int newNumY = ceil(numY/2);
  println("Refactoring to " + newNumX + " x " + newNumY + " tiles...");
  
  for (int x=0; x<numX; x+=2) {
    for (int y=0; y<numY; y+=2) {
      println("- " + x + " x " + y);
      PGraphics pg = createGraphics(256,256);
      pg.beginDraw();
      pg.background(bg);
      for (int tx=0; tx<2; tx++) {
        for (int ty=0; ty<2; ty++) {
          try {
            PImage img = loadImage(tilePath + prevZoom + "/" + (x+tx) + "/" + (y+ty) + extension);
            pg.image(img, tx*128, ty*128, 128,128);
          }
          catch (Exception e) {
            // ran out of images, skip
          }
        }
      }
      pg.endDraw();
      
      // save tile based on specified format
      String outputPath = sketchPath(tilePath) + newZoom + "/" + int(x/2) + "/" + int(y/2) + extension;
      if (extension.equals(".jpg")) {
        PImage out = pg.get();
        saveCompressedJPG(out, compressionLevel, outputPath);
      } 
      else {
        pg.save(outputPath);
      }
    }
  }
  
  println("DONE");
  exit();
}