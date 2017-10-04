
/*
VISUALIZE GRID
Jeff Thompson | 2017 | jeffreythompson.org

Displays a grid of images organized by Rasterfairy. Helpful
for sharing your cool project, but also for debugging the layout.

*/

int imageSize =         40;        // how big should the images be?
int numSquaresWide =    361;       // size for output image (in images, not px)
int numSquaresHigh =    361;       // ditto height

String inputFilename =  "../data/Grid_30perplexity.csv";
String outputFilename = "../renderings/Grid_30perplexity.jpg";


void setup() {
 
  // create our output context
  PGraphics pg = createGraphics(imageSize*numSquaresWide, imageSize*numSquaresHigh);
  pg.beginDraw();
  pg.background(255);

  // load the data, draw
  Table table = loadTable(inputFilename, "header");
  int i = 0;
  for (TableRow row : table.rows()) {
    String filename = row.getString("path");
    println(i + ": " + filename);
    PImage img = loadImage("../" + filename);
    float x = row.getFloat("x");
    float y = row.getFloat("y");
    //println(i + ": " + x + ", " + y);
    pg.image(img, x*imageSize, y*imageSize, imageSize, imageSize);
    i += 1;
  }
  pg.endDraw();
  pg.save(outputFilename);

  // later
  println("ALL DONE!");
  exit();
}