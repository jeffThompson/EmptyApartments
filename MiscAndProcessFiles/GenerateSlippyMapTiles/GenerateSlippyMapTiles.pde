
import java.awt.image.BufferedImage;    // all for compressed JPG export
import javax.imageio.plugins.jpeg.*;
import javax.imageio.*;
import javax.imageio.stream.*;

/*
GENERATE SLIPPY MAP TILES
 Jeff Thompson | 2017 | jeffreythompson.org
 
 TODO
 - seems to generate about 2x the number of rows vs cols... why? fix that?
 
 Generates tiles for "slippy maps" at various zoom levels. Generates only
 one row at a time (even if the images don't quite fill a row or need to be
 cropped) meaning you can create really large maps that wouldn't be able
 to be loaded into RAM all at once.
 
 TILE DIMENSIONS
 In a normal slippy map, the outputted tile images are 256x256 pixels, regardless
 of the zoom level. At zoom level 0, the entire map can be seen in a single tile.
 Each zoom level doubles the number of tiles used; if zoom 0 = 1 tile,
 zoom 1 = 2x2 tiles (4 total), zoom 2 = 4x4, zoom 3 = 8x8, etc. For map
 data, that usually means 22 zoom levels are required.
 
 In this case, since we're not using a map image but a set of disparate images
 to place, we specify the height that we want those images to appear onscreen.
 
 More info:
 
   http://wiki.openstreetmap.org/wiki/Zoom_levels
   
 
 OUTPUT FILE STRUCTURE
 Tiles are saved to a series of folders, in the following format:
 
   <outputFolder>/<zoomLevel>/x/y.png
 
 POTENTIAL PROBLEMS (AND SOLUTIONS)
 + If you get a weird sun.awt.image error about color conversion, it's likely
   some or all of your images aren't in RGB colorspace (probably because they
   came from the internet, or were processed first elsewhere). To fix that, use
   ImageMagick's "mogrify" command to batch process. Navigate into your image
   directory (this command is recursive, so it's ok if you have subfolders) and run:
 
     find . -name '*.jpg' -execdir mogrify -colorspace RGB {} \;
 
 */

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
int outputWidth =        203000;       // final montage image width (and height)
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
int outputHeight = outputWidth;
long totalPx = -1;
ArrayList<File> files = new ArrayList<File>();


void setup() {

  // load list of image files
  println("Loading images...");
  String[] imagePaths = loadStrings(imageListFilename);
  println(imagePaths[imagePaths.length-1]);
  for (String path : imagePaths) {
    files.add(new File(path));
  }  
  numFiles = files.size();
  println("- found " + nfc(numFiles) + " images to place");


  // if specified, get stats from the entire set of images
  if (getImageStats) {
    println("Calculating image stats (may take a while)...");
    long totalWidth = 0;
    for (int i=0; i<files.size(); i++) {
      println("- " + (i+1) + " / " + numFiles);
      PImage img = loadImage(files.get(i).toString());
      totalWidth += img.width;
      if (i == 0) inputHeight = img.height;
    }
    println("- input height: " + inputHeight + " px");
    totalPx = totalWidth * inputHeight;
    println("- total pixels in all images: " + totalPx + " px");
    averageWidth = (int) totalWidth/files.size();
    println("- average width of an image: " + averageWidth + " px");
    outputWidth = outputHeight = ceil(sqrt(totalPx));
    println("- using output dimensions: " + outputWidth + " x " + outputHeight + " px");
  }


  // placement stats
  println("Calculating placement stats...");
  numRows = int(outputHeight / inputHeight);
  println("- using " + numRows + " rows of images");
  int imagesPerRow = outputWidth / averageWidth;
  int totalImagesPlaced = imagesPerRow * numRows;
  println("- approx " + imagesPerRow + " images per row = total of " + nfc(totalImagesPlaced) + " images placed");
  int filesLeft = numFiles - totalImagesPlaced;
  if (filesLeft >= 0) println("- not enough room, ~" + filesLeft + " image files not placed");
  else println("- all images placed, extra space for ~" + abs(filesLeft) + " files");


  // do it
  println("\n" + "Generating tiles...");
  generate();


  // bye
  println("ALL DONE!");
  exit();
}