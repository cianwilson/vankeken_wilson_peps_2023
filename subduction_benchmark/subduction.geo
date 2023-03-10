resscale = ${resscale};

uclcdepth = 15;
mohodepth = 40;
iodepth = 139;

// POINTS
// top left
Point(1) = {0, 0, 0, 2.0*resscale};
// top right
Point(2) = {400, 0, 0, 4.0*resscale};
// right upper crust base
Point(3) = {400, -uclcdepth, 0, 4.0*resscale};
// right lower crust base (moho)
Point(4) = {400, -mohodepth, 0, 4.0*resscale};
// bottom right
Point(5) = {400, -200, 0, 6*resscale};
// lower left
Point(6) = {0, -200, 0, 6*resscale};
// slab upper crust base
Point(7) = {2*uclcdepth, -uclcdepth, 0, 2*resscale};
// slab lower crust base (moho)
Point(8) = {2*mohodepth, -mohodepth, 0, 1*resscale};
// slab id start
Point(9) = {140, -70, 0, 1*resscale};
// slab partial coupling depth
Point(10) = {160, -80, 0, 1*resscale};
// slab id end
Point(11) = {240, -120, 0, 1*resscale};
// slab full coupling depth
Point(12) = {165, -82.5, 0, 1*resscale};
// moho id start
Point(13) = {140, -mohodepth, 0, 1*resscale};
// moho id end
Point(14) = {240, -mohodepth, 0, 1*resscale};
// in/out point on rhs boundary
Point(15) = {400, -iodepth, 0, 4*resscale};
//+

// LINES
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 15};
//+
Line(5) = {15, 5};
//+
Line(6) = {5, 6};
//+
Line(7) = {6, 1};
//+
Line(8) = {1, 7};
//+
Line(9) = {7, 8};
//+
Line(10) = {8, 9};
//+
Line(11) = {9, 10};
//+
Line(12) = {10, 12};
//+
Line(13) = {12, 11};
//+
Line(14) = {11, 5};
//+
Line(15) = {7, 3};
//+
Line(16) = {8, 13};
//+
Line(17) = {13, 14};
//+
Line(18) = {14, 4};
//+
Line(19) = {13, 9};
//+
Line(20) = {14, 11};
//+
Curve Loop(1) = {8, 15, -2, -1};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {9, 16, 17, 18, -3, -15};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {10, -19, -16};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {11, 12, 13, -20, -17, 19};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {14, -5, -4, -18, 20};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {6, 7, 8, 9, 10, 11, 12, 13, 14};
//+
Plane Surface(6) = {6};

// PHYSICAL LINES
// slab interface down to "coupling zone"
Physical Curve(1) = {8, 9, 10};
// above coupling depth of coupling zone
Physical Curve(2) = {11, 12};
// below coupling depth of coupling zone
Physical Curve(3) = {13};
// lower slab interface
Physical Curve(4) = {14};
// top of domain
Physical Curve(5) = {1};
// rhs of upper crust
Physical Curve(7) = {2};
// base of upper crust
Physical Curve(8) = {15};
// rhs of lower crust
Physical Curve(9) = {3};
// top of coupling zone
Physical Curve(10) = {17};
// top of wedge (excluding coupling zone)
Physical Curve(11) = {16, 18};
// sides of coupling zone
Physical Curve(12) = {20, 19};
// base
Physical Curve(13) = {6};
// lhs
Physical Curve(14) = {7};
// wedge rhs above inout depth
Physical Curve(16) = {4};
// wedge rhs below inout depth
Physical Curve(17) = {5};

// PHYSICAL SURFACES
// Upper crust
Physical Surface(1) = {1};
// Lower crust
Physical Surface(2) = {2};
// Coupling zone
Physical Surface(3) = {4};
// Rest of wedge
Physical Surface(4) = {3, 5};
// Slab
Physical Surface(5) = {6};
