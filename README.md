# drumpy
Contains python code for generating time signature varying drum patterns in a human way. 

This dataset incorporates the notion of varying tempo to model small inter beat errors made by humans, based on a random function. 

The different components (snare/kick/hi-hat) can also be misaligned at a beat location. This has also been modelled by having slight timing difference in the positions of these components. 

The intensity of the drum hit has been modelled by also randomizing the amplitude of each component at each beat instant (snare/hat/kick), except the downbeat which usually has the maximum amplitude. 
