
import java.awt.image.BufferedImage;    // all for compressed JPG export
import javax.imageio.plugins.jpeg.*;
import javax.imageio.*;
import javax.imageio.stream.*;

/*
 GENERATE SLIPPY MAP TILES
 Jeff Thompson | 2017 | jeffreythompson.org
 
 TODO
 - automatic overall-width based on num of tiles?
 - should borders shrink with diff sizes?
 
 Generates tiles for "slippy maps" at various zoom levels from a set of
 random images, meaning you can create really cool tiled montages of images
 that can be navigated, zoomed, and explored.
 
 Generates only one row of tiles at a time, meaning you can work with a set
 of files far too large to be loaded into RAM all at once.
 
 IMAGE PREP
 Images should ideally all be the same height – resizing can be done with
 a separate Processing sketch, or something like ImageMagick. If they aren't
 the same height, it will be difficult for you to guess how wide the rows
 should be.
 
 Instead of traversing a bunch of directories, this sketch assumes you have
 a text file listing all the images, and loads the images from there. This is
 useful if you have a really complex directory structure, perhaps mirrored
 from a website.
 
 TILE DIMENSIONS
 In a normal slippy map, the outputted tile images are 256x256 pixels, regardless
 of the zoom level. At zoom level 0, the entire map can be seen in a single tile.
 Each zoom level doubles the number of tiles used; if zoom 0 = 1 tile,
 zoom 1 = 2x2 tiles (4 total), zoom 2 = 4x4, zoom 3 = 8x8, etc. For map
 data, that usually means 22 zoom levels are required.
 
 In this case, since we're not using a map image but a set of disparate images
 to place, we specify the height that we want those images to appear onscreen.
 You can create various arbitrary zoom levels, for example with images appearing
 at 50, 100, and 200 pixels high.
 
 More info on zoom levels and how to map to lat/long here:
 
   http://wiki.openstreetmap.org/wiki/Zoom_levels
   
 
 OUTPUT FILE STRUCTURE
 Tiles are saved to a series of folders, in the following format:
 
   <outputFolder>/<zoomLevel>/x/y.png
 
 POTENTIAL PROBLEMS (AND SOLUTIONS)
 If you get a weird sun.awt.image error about color conversion, it's likely
 some or all of your images aren't in RGB colorspace (probably because they
 came from the internet, or were processed first elsewhere). To fix that, use
 ImageMagick's "mogrify" command to batch process. Navigate into your image
 directory (this command is recursive, so it's ok if you have subfolders) and run:
 
   find . -name '*.jpg' -execdir mogrify -colorspace RGB {} \;

 Enjoy!

*/


// list of filenames, in order they should appear, one per line
// note this is 1D, like a list of pixel values in an image
String imageListFilename = "Grid_30perplexity-SORTED.txt";

// folder to save tiles to
// will be placed in <outputFolder>/<zoomLevel>/x/y.png
String outputFolder =    "tiles";

int inputImageHeight =   512;          // height of images coming in (px)

int outputImageHeight =  200;          // height images should be onscreen          

int rowWidth =           80000;        // final montage image width (and height)

color bg =               color(255);   // background color (will be the border color too)
int border =             10;           // add border? (in px, 0 = none)

int zoomLevel =          3;            // for file-naming convention – you can specify
                                       // any outputImageHeight for each zoom level

String imageFormat =     ".jpg";       // format for saving (if jpg, set compression level)
float compressionLevel = 0.5;          // jpg compression, 0.5 = 50% quality

int tileHeight =         256;          // height of outputted slippy tiles
                                       // DON'T CHANGE (unless you know what you're doing,
                                       // it may break your site)
                                       
int index = 0;                         // which image are we at?
int tileY = 0;                         // keep track of tile count vertically
ArrayList<File> files;                 // list of image files
int numFiles, numTilesX;               // how many files, how many tiles horizontally


void setup() {

  // load list of image files
  files = new ArrayList<File>();
  println("Loading images...");
  String[] imagePaths = loadStrings(imageListFilename);
  for (String path : imagePaths) {
    files.add(new File(path));
  }  
  numFiles = files.size();
  println("- found " + nfc(numFiles) + " images to place");

  // how many tiles horizontally?
  numTilesX = ceil(rowWidth / float(tileHeight));
  println("- using " + numTilesX + " tiles per row");
  
  // do it
  generate();
  println("\n" + "Ended at " + nfc(tileY) + " rows of " + nfc(numTilesX) + " tiles each");
  
  // generate some leaflet.js variables to plug in
  println("\n" + "Leaflet.js vars (paste into your code)...");
  println("  var w = " + rowWidth + ";");
  println("  var h = " + (tileY*tileHeight) + ";");
  
  // bye
  println("\n" + "ALL DONE!");
  exit();
}