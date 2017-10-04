
void generate() {
  println("\n" + "GENERATING...");

  boolean done = false;   // have we run out of images yet?
  int yOffset = 0;        // keep track for rows that span two tiles
  int stripWidth = 0;     // overall width of the current strip (for centering in the row)
  PGraphics row;          // full row, made of up several strips of images

  // create an empty variable here for strips of images
  // avoids variable errors below (a hack)
  PGraphics strip = createGraphics(0, 0);

  // do it all
  while (!done) {

    // create a row, and an empty strip (to avoid errors later)
    println("Row " + tileY + "...");
    row = createGraphics(rowWidth, tileHeight);
    row.beginDraw();
    row.background(bg);

    // if the previous row ran off the bottom edge,
    // start by drawing what was cut off
    int y = 0;
    if (yOffset < 0) {
      println("  - offsetting for prev strip: " + yOffset + "px");
      y = yOffset;
      row.image(strip, row.width/2-stripWidth/2, y);
      y += outputImageHeight + border;
    }

    // generate strips of images
    while (y < tileHeight && !done) {

      // generate a strip of images
      int x = 0;
      strip = createGraphics(rowWidth, outputImageHeight);
      strip.beginDraw();
      strip.background(bg);
      while (true) {

        // load the next image
        try {
          PImage img = loadImage(files.get(index).toString());
          img.resize(0, outputImageHeight);

          // if we'll go past the edge, stop here
          if (x + img.width > rowWidth) {
            stripWidth = x - border;
            break;
          }

          // otherwise, draw the image and update variables
          strip.image(img, x, 0);
          x += img.width + border;
          index += 1;
        }
        // if we have run out of images, draw this last strip
        catch (IndexOutOfBoundsException ioobe) {
          done = true;
          break;
        }
      }

      // add strip to row, centered
      strip.endDraw();
      row.image(strip, row.width/2-stripWidth/2, y);
      y += outputImageHeight + border;
    }

    // calculate negative offset if image overlaps bottom
    // essentially: how much image was shown?
    yOffset = y - tileHeight - outputImageHeight - border;

    // split into tile-sized pieces and save
    println("  - splitting into tiles...");
    row.endDraw();
    for (int tileX = 0; tileX < numTilesX; tileX++) {
      PImage tileImage = row.get(tileX*tileHeight, 0, tileHeight, tileHeight);
      String path = sketchPath(outputFolder + "/" + zoomLevel + "/" + tileX + "/" + tileY + imageFormat);

      // save tile based on specified format
      if (imageFormat.equals(".jpg")) {
        saveCompressedJPG(tileImage, compressionLevel, path);
      } 
      else {
        tileImage.save(path);
      }
    }
    tileY += 1;    // update count for file naming

    // how are we doing overall?
    println("  - used " + nfc(index) + " images (" + percentDone(index, numFiles) + "%)");
  }

  // we're all done!
  println("  - OUT OF IMAGES TO USE!");
}