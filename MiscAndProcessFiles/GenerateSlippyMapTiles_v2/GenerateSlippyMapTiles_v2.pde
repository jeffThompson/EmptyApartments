// list of filenames, in order they should appear, one per line
// note this is 1D, like a list of pixel values in an image
String imageListFilename = "../ApartmentImages/AllApartments_GRID.txt";

// folder to save tiles to
// will be placed in <outputFolder>/<zoomLevel>/x/y.png
String outputFolder =      "../Tiles";

String imageFormat =     ".png";       // format for saving (if jpg, set compression level)
float compressionLevel = 0.5;          // jpg compression, 0.5 = 50% quality

boolean getImageStats =  false;        // get average width, image height, etc
// (may be really slow with long lists of images)

int inputHeight =        512;          // height of images coming in (px)
int outputImageHeight =  150;          // 

int rowWidth =           203000;       // final montage image width (and height)
// sqrt(totalNumPx) with some fiddling to get it right

color bg =               color(255);   // background color (will be the border color too)
int border =             10;           // add border? (in px, 0 = none)

int zoomLevel =          3;            // for file-naming convention

boolean saveRows =       false;        // save entire row images too? 
// (slows things down a lot)

// not necessary, but these help let you know how many images will 
// be placed in the specified area
int averageWidth =       612;          // of incoming images to be tiled

int tileHeight =         256;          // height of output slippy tiles
// DON'T CHANGE (unless you know what you're doing)

int numFiles, numRows;
int outputHeight = rowWidth;
long totalPx = -1;
ArrayList<File> files = new ArrayList<File>();
int imageIndex = 0;
int yOffset = 0;


void setup() {

  // load list of image files
  println("Loading images...");
  String[] imagePaths = loadStrings(imageListFilename);
  for (String path : imagePaths) {
    files.add(new File(path));
  }  
  numFiles = files.size();
  println("- found " + nfc(numFiles) + " images to place");


  rowWidth = 600;

  // create array of PGraphics, enough to fill the row vertically
  int stripsPerRow = ceil(tileHeight / float(outputImageHeight + border));
  Strip[] strips = new Strip[stripsPerRow];

  for (int i=0; i<strips.length; i++) {
    strips[i] = new Strip(0);
  }

  //PGraphics row = createGraphics(rowWidth, tileHeight);
  //row.beginDraw();
  //row.background(bg);
  //int y = 0;
  //for (int i=0; i<strips.length; i++) {
  //  row.image(strips[i], 0, y);
  //  y += outputImageHeight + border;
  //}
  //row.endDraw();
  //row.save("row.jpg");
  
  
  exit();
}


class Strip {
  PGraphics strip;
  int startIndex, numImagesUsed;
  int w;

  Strip(int index) {
    startIndex = index;
    generate();
    center();
  }

  void generate() {
    strip = createGraphics(rowWidth, outputImageHeight);
    strip.beginDraw();
    strip.background(bg);
    
    int x = 0;
    int index = startIndex;
    while (true) {
      PImage img = loadImage(files.get(index).toString());
      img.resize(0, outputImageHeight);
      
      if (x + img.width > rowWidth) {
        w = x;
        numImagesUsed = index - startIndex;
        break;
      }
      
      strip.image(img, x, 0);
      index += 1;
      x += img.width + border;
    }
    strip.endDraw();
    
    println(w);
  }
  
  void center() {
    PGraphics 
    
  }
}



/*int startIndex = 0;
 int y = 0;
 for (int i=0; i<3; i++) {
 
 // create PGraphics for row
 PGraphics row = createGraphics(rowWidth, tileHeight);
 row.beginDraw();
 row.background(bg);
 
 
 if (y > tileHeight) {
 imageIndex = startIndex;
 y = -(y - tileHeight);
 } 
 else {
 y = 0;
 }
 
 // iterate until we've gone to the bottom of the row
 while (true) {
 
 // iterate images across the row
 int x = 0;
 startIndex = imageIndex;
 while (true) {
 PImage img = loadImage(files.get(imageIndex).toString());
 img.resize(0, outputImageHeight);
 
 // if we're past the right edge, stop
 if (x + img.width > rowWidth) {
 break;
 }
 
 // otherwise, draw and update x and index
 row.image(img, x, y);
 imageIndex += 1;
 x += img.width + border;
 }
 y += outputImageHeight + border;
 if (y > tileHeight) {
 break;
 }
 }
 
 // save it!
 row.endDraw();
 row.save(i + ".jpg");
 }
 */