
String tilePath = "../Website/tiles/0/";
int numTilesY =   42;
int numTilesX =   39;
int tileSize =    256;
color bgColor =   color(255);


void setup() {
  
  println("creating pgraphics context...");
  PGraphics pg = createGraphics(tileSize*numTilesX, tileSize*numTilesY);
  pg.beginDraw();
  pg.background(bgColor);
  println("- " + pg.width + " x " + pg.height);
  
  println("drawing images...");
  for (int y=0; y<numTilesY; y++) {
    println("- row " + (y+1) + " / " + numTilesY);
    for (int x=0; x<numTilesX; x++) {
      String path = tilePath + x + "/" + y + ".jpg";
      PImage tile = loadImage(path);
      pg.image(tile, x*tileSize, y*tileSize);
    }
  }
  
  println("saving...");
  pg.save("Poster.tiff");
  println("- all done");
  
  exit();
}