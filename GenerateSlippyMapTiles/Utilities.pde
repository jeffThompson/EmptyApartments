
String percentDone(float i, float n) {
  return percentDone(i, n, 2);
}

String percentDone(float i, float n, int precision) {
  return nf((i / n) * 100.0, 0, precision);
}