
import java.io.FilenameFilter;
import java.util.List;
import java.util.Arrays;
import java.util.Collections;

/*
IMAGE TILER
 Jeff Thompson | 2016 | jeffreythompson.org
 
 Creates a tiled montage from a set of images, resizing
 to fit. Used prior to the Python GenerateSlippyMapTiles
 program to create big collages of apartment images.
 
 Similar to ImageMagick's 'montage' command, but
 lets you fill to edges, rather than tile #s (good
 for differently-sized images).
 
 TO DO:
 - don't need to grab random images, just walk through
 - auto-size output image to fit input (will be approx, but better than now); should be square
 - recursive file find to get from multiple folders
 
 */

String imageListFilename = "/Users/JeffThompson/Documents/EmptyApartments/ApartmentImages/AllApartments_RANDOMIZED.txt";
String outputFilename =  "output.jpg";

int tileHeight =       400;          // height to resize images to (px)
int averageWidth =     478;          // not necessary, but helps set size (determined from actual images)
int outputWidth =      158696;       // final montage image dims (px)
int outputHeight =     158696;       // (set by sqrt(total px wide * height) + some fiddling

boolean resizeImages = false;        // resize image? (will be much slower)

color bg =             color(255);   // background color
int border =           10;           // add border? (in px, 0 = none)
boolean centerRow =    true;         // center rows in the image? (slower but looks better)

boolean verbose =      true;         // print updates as we go along?

PGraphics out;
int count = 0;
int numRows;
ArrayList<File> files = new ArrayList<File>();
int numFiles;


void setup() {
  size(200,200, P2D);       // required for really big graphics

  // load list of image files
  println("Loading images...");
  String[] imagePaths = loadStrings(imageListFilename);
  for (String path : imagePaths) {
    files.add(new File(path));
  }  
  numFiles = files.size();
  println("- found " + nfc(numFiles) + " images to place");
  
  
  // placement stats
  numRows = int(outputHeight / tileHeight);
  int imagesPerRow = outputWidth / averageWidth;
  int totalImagesPlaced = imagesPerRow * numRows;
  println("- approximately " + imagesPerRow + " images per row = " + nfc(totalImagesPlaced) + " images placed");
  int filesLeft = numFiles - totalImagesPlaced;
  if (filesLeft >= 0) println("- not enough room, " + filesLeft + " image files not placed");
  else println("- all images placed, extra space for " + abs(filesLeft) + " files");
  
  
  // generate output image
  println("Generating montage (may take a long time)...");  
  out = createGraphics(outputWidth, outputHeight);
  out.beginDraw();
  out.background(0);
  out.endDraw();
  //montage();
  println("Image finished...");
  println("- used " + count + " of " + numFiles + " photos");

  // save it
  println("Saving to file...");
  out.save(outputFilename);

  println("DONE!");
  exit();
}