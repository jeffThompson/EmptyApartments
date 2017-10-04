
void generate() {
  int imageIndex = 0;
  int rowCount = 0;

  // rows
  int y = 0;
  while (true) {
    if (rowCount == numRows*2) {
      break;
    }
    
    // let us know where we're at
    println("- row " + (rowCount+1) + "/" + numRows + " (" + percentDone(rowCount+1, numRows) + "%)");

    // create two rows, top and bottom
    PGraphics top = createGraphics(outputWidth, tileHeight);
    top.beginDraw();
    top.background(bg);

    PGraphics bottom = createGraphics(outputWidth, tileHeight);
    bottom.beginDraw();
    top.background(bg);

    // images in row
    println("  - populating row with images...");
    int x = 0;
    while (true) {
      PImage img = loadImage(files.get(imageIndex).toString());
      img.resize(0, inputHeight-(border*2));

      // if past the edge, we're done with populating this row
      if (x + img.width > outputWidth) {
        x -= border;    // subtract border from final image width (for centering)
        break;
      }

      top.image(img, x, 0);                     // top half of image
      bottom.image(img, x, -img.height/2);      // bottom half
      x += img.width + border;
      imageIndex += 1;
    }
    top.endDraw();
    bottom.endDraw();

    // center row
    println("  - centering images in row...");
    PGraphics topOutput = createGraphics(outputWidth, tileHeight);
    topOutput.beginDraw();
    topOutput.background(bg);
    topOutput.image(top, topOutput.width/2-x/2, 0);
    topOutput.endDraw();
    if (saveRows) {
      println("  - saving top row image...");
      topOutput.save("topOutput.png");
    }

    PGraphics bottomOutput = createGraphics(outputWidth, tileHeight);
    bottomOutput.beginDraw();
    bottomOutput.background(bg);
    bottomOutput.image(bottom, bottomOutput.width/2-x/2, 0);
    bottomOutput.endDraw();
    if (saveRows) {
      println("  - saving bottom row image...");
      bottomOutput.save("bottomOutput.png");
    }

    // split into tiles
    println("  - splitting row into tiles...");
    for (int tx=0; tx<outputWidth/tileHeight; tx++) {
      PImage tileImage = topOutput.get(tx*tileHeight, 0, tileHeight, topOutput.height);
      String path = outputFolder + "/" + zoomLevel + "/" + tx + "/" + rowCount + imageFormat;
      if (imageFormat.equals(".jpg")) {
        saveCompressedJPG(tileImage, compressionLevel, path);
      } else {
        tileImage.save(path);
      }

      tileImage = bottomOutput.get(tx*tileHeight, 0, tileHeight, bottomOutput.height);
      path = outputFolder + "/" + zoomLevel + "/" + tx + "/" + (rowCount+1) + imageFormat;
      if (imageFormat.equals(".jpg")) {
        saveCompressedJPG(tileImage, compressionLevel, path);
      } else {
        tileImage.save(path);
      }
    }
    
    // how far did we get?
    println("  - so far...");
    println("    - used " + nfc(imageIndex) + " images (" + percentDone(imageIndex, numFiles) + "%)");
    println("    - " + nfc(y) + "px down");

    // update variables, onto next row
    println("  - done" + "\n");
    y += inputHeight;
    rowCount += 2;      // +2 since we're making two rows at once
  }
}