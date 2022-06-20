# LLJam 0001 - LC-3b
An implementation of LC-3b for the Low Level Jam 0001


This implementation uses UDP Multicast packets as the system bus between the CPU, Memory and any device attached to it. This allows for simpler interactions between all parts of the system. It also allows for device to communicate directly with each other over the bus, making some stuff that would be hard to implement easier, such as a DMA controller. 


## Resources about the LC-3 / LC-3b

[LC-3b ISA](https://web.archive.org/web/20220620174056/http://users.ece.utexas.edu/~patt/21s.460n/handouts/appA.pdf)

[Wikipedia Page on the LC-3 / LC-3b](https://en.wikipedia.org/wiki/Little_Computer_3#The_LC-3b)

[State Machine as defined by the creator of the LC-3 / LC-3b](https://web.archive.org/web/20081008155158/https://users.ece.utexas.edu/~patt/07s.360N/handouts/state_fixed.pdf)

[Website for the textbook based around the LC-3](https://highered.mheducation.com/sites/0072467509/student_view0/index.html)

