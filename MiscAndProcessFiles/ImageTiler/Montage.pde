
void montage() {
  out.noSmooth();
  out.beginDraw();  
  out.fill(bg);
  out.noStroke();
  out.rect(0, 0, out.width, out.height);

  PImage img;
  PGraphics row, prev;
  int x = 0;
  int y = 0;
  int rowCount = 1;
  while (y < outputHeight) {
    if (verbose) println("  - filling row " + rowCount + " / " + numRows);

    // initial image in row
    try {
      int i = int(random(0,files.size()));
      img = loadImage(((File) files.get(i)).getAbsolutePath());
      files.remove(i);
    }
    catch (ArrayIndexOutOfBoundsException aioobe) {
      println("Ran out of images! Saving...");
      return;
    }
    if (resizeImages) img.resize(0, tileHeight);

    row = createGraphics(img.width, tileHeight);
    row.beginDraw();
    row.image(img, x, 0);
    if (border > 0) {
      row.strokeWeight(border);
      row.stroke(bg);
      row.noFill();
      row.rect(x+border/2-1, border/2-1, img.width-border/2+1, img.height-border/2+1);
    }
    row.endDraw();

    prev = createGraphics(row.width, tileHeight);
    prev.beginDraw();
    prev.image(row, 0, 0);
    prev.endDraw();

    x += img.width;
    count += 1;

    // fill in across
    while (true) {
      try {
        int i = int(random(0,numFiles));
        img = loadImage(((File) files.get(i)).getAbsolutePath());
        files.remove(i);
      }
      catch (Exception e) {
        println("Ran out of images! Saving...");
        return;
      }
      img.resize(0, tileHeight);
      
      // next image puts us past edge? end row
      if (x + img.width > out.width) break; 

      row = createGraphics(img.width + prev.width, tileHeight);
      row.beginDraw();
      row.image(prev, 0, 0);
      row.image(img, x, 0);
      if (border > 0) {
        row.strokeWeight(border);
        row.stroke(bg);
        row.noFill();
        row.rect(x+border/2-1, border/2-1, img.width-border/2+1, img.height-border/2+1);
      }
      row.endDraw();

      prev = createGraphics(row.width, tileHeight);
      prev.beginDraw();
      prev.image(row, 0, 0);
      prev.endDraw();

      x += img.width;
      count += 1;
    }
    
    // end of row, add to image
    if (centerRow) out.image(row, out.width/2-row.width/2, y);
    else out.image(row, 0, y);
    y += tileHeight;
    rowCount += 1;
    x = 0;
  }
  
  // all done, image finished!
}