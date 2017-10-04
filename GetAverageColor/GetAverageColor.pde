
println("Getting image list...");
String imageListFilename = "../ApartmentImages/AllApartments_GRID.txt";
ArrayList<File> files = new ArrayList<File>();
String[] imagePaths = loadStrings(imageListFilename);
for (String path : imagePaths) {
  files.add(new File(path));
}

println("Finding average colors...");
color[] mean = new color[files.size()];
for (int i=0; i<files.size(); i++) { 
  println("- " + (i+1) + "/" + files.size());
  PImage img = loadImage(files.get(i).toString());
  
  int r = 0;
  int g = 0;
  int b = 0;
  img.loadPixels();
  for (color c : img.pixels) {
    r += (c >> 16 & 0xFF);
    g += (c >> 8 & 0xFF);
    b += (c & 0xFF);
  }
  r /= img.pixels.length;
  g /= img.pixels.length;
  b /= img.pixels.length;
  
  mean[i] = color(r, g, b);
}

println("Computing overall average...");
int r = 0;
int g = 0;
int b = 0;
for (color c : mean) {
  r += (c >> 16 & 0xFF);
  g += (c >> 8 & 0xFF);
  b += (c & 0xFF);
}
r /= mean.length;
g /= mean.length;
b /= mean.length;
println("- " + r + ", " + g + ", " + b);
exit();



  
    