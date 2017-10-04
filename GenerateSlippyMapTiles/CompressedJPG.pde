

void saveCompressedJPG(PImage img, float compression, String outputFilename) {
  try {
    
    // create path to file
    File outputFile = new File(outputFilename);
    outputFile.getParentFile().mkdirs();    
    
    // setup JPG output
    JPEGImageWriteParam jpegParams = new JPEGImageWriteParam(null);
    jpegParams.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
    jpegParams.setCompressionQuality(compressionLevel);
    final ImageWriter writer = ImageIO.getImageWritersByFormatName("jpg").next();
    writer.setOutput(new FileImageOutputStream(outputFile));

    // load image to compress
    img.loadPixels();

    // output to BufferedImage object
    // create the object, then write the pixel data to it
    BufferedImage out = new BufferedImage(img.width, img.height, BufferedImage.TYPE_INT_RGB);
    for (int i=0; i<img.pixels.length; i++) {
      out.setRGB(i%img.width, i/img.width, img.pixels[i]);
    }

    // save it!
    writer.write(null, new IIOImage(out, null, null), jpegParams);
  }
  catch (Exception e) {
    println("  - error saving compressed JPG");
    println(e);
  }
}