Delfine schlafen nicht wie Menschen. Sie schlafen nur mit einer Hälfte ihres Gehirns, während die andere Hälfte wach bleibt, um sie vor Gefahren zu schützen. Dieser Zustand wird als unihemisphärisches Schlafen bezeichnet. Delfine schlafen auch nicht lange. Sie schlafen nur für kurze Zeiträume, normalerweise weniger als eine Stunde.

import numpy as np # //Refactoring, dependend https://ibmquantumawards.bemyapp.com/#/event
OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
cx q[0], q[1];
x q[3];
ccx q[0], q[1], q[2];
x q[0];
ccx q[1], q[2], q[3];
ccx q[0], q[1], q[2];
h q[3];
h q[0];
p(pi / 2) q[0];
p(pi / 2) q[1];
z q[2];
h q[3];
measure q[0] -> c[0];
measure q[1] -> c[1];
tdg q[0];
tdg q[1];
rccx q[1], q[2], q[3];
h q[2];
h q[3];
h q[0];
measure q[1] -> c[1];
h q[2];
z q[0];
h q[3];
h q[1];
p(pi / 2) q[1];
p(pi / 2) q[3];
p(pi / 2) q[2];
measure q[0] -> c[0];
p(pi / 2) q[0];