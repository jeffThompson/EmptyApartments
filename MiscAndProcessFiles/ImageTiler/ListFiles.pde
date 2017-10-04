
// get a list of all files in a directory and all subdirectories
ArrayList<File> listFiles(String dir) {
   ArrayList<File> fileList = new ArrayList<File>(); 
   recurseDir(fileList,dir);
   return fileList;
}

// recursive function to traverse subdirectories
void recurseDir(ArrayList<File> a, String dir) {
  File file = new File(dir);
  if (file.isDirectory()) {  
    File[] subfiles = file.listFiles();
    for (int i = 0; i < subfiles.length; i++) {
      recurseDir(a,subfiles[i].getAbsolutePath());
    }
  } else {
    if (file.getName().endsWith(".jpg")) a.add(file);
  }
}