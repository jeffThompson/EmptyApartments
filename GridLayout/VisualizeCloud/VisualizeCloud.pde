
/*
VISUALIZE CLOUD
Jeff Thompson | 2017 | jeffreythompson.org

Displays a cloud of images organized by t-SNE. Helpful
for sharing your cool project, but also for debugging, too.

*/

int imageSize =        60;      // how big should the images be?
int margin =           50;      // keep a margin around outside, please

String inputFilename = "../data/MulticoreTSNE_2dims_30perplexity.csv";
String outputFilname = "../renderings/MulticoreTSNE_2dims_30perplexity.jpg";


void setup() {
 
  // create our output context
  PGraphics pg = createGraphics(30000, 30000);
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
    x = map(x, 0, 1, margin, pg.width-imageSize-margin);
    y = map(y, 0, 1, margin, pg.height-imageSize-margin);
    pg.image(img, x, y, imageSize, imageSize);
    i += 1;
  }
  pg.endDraw();
  pg.save(outputFilname);

  // later
  println("ALL DONE!");
  exit();
}