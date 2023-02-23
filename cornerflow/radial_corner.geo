l=${res};
//+
Point(1) = {0, 0, 0, l};
//+
Extrude {1, 0, 0} {
  Point{1}; 
}
//+
Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Curve{1}; 
}
//+
Physical Curve(1) = {2};
//+
Physical Curve(2) = {3};
//+
Physical Curve(3) = {1};
//+
Physical Surface(4) = {4};
