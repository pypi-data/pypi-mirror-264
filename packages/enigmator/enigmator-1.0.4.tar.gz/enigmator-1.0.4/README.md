# De(s)cription
This is a python package for enrypting messages with the historic enigma machine.
I spent quite some time trying to find a suitable existing project and ended up implementing it myself.

This library answers the question no one asked:

> _"How can I annoy my surroundings by sending them trivial encrypted messages and make them go through the process of deciphering?"_

No dependecies to other python packages necessary to decrypt messages and free for use and further adaption (MIT license).

# Usage
```
from enigmator import (ROTOR_I, ROTOR_II, ROTOR_III, ROTOR_IV, ROTOR_V,
                       REFLECTOR_A, REFLECTOR_B, REFLECTOR_C,
                       Enigma,
                       Plugboard)

EnigmaMachine = Enigma(reflector=REFLECTOR_B, 
                       left_rotor=ROTOR_III, 
                       middle_rotor=ROTOR_II, 
                       right_rotor=ROTOR_I, 
                       rotor_positions="16 10 1",
                       ring_positions="3 1 17",
                       plugboard=Plugboard("CE KL FP MD")
                       )

x=EnigmaMachine.encipher('Jeder Mensch sollte wissen, wie man Enigma-Maschine verwendet.')

print('Result is:')
print(x)
```

Result is:

LVUBS FKTKJZ EXDYQP XFYEHV, AZS BVR WBGXXW-CTYXLRDK LMTLDALNQ.


To decipher back to plain text, just pass the decypted text back into the EnigmaMachine:

```
EnigmaMachine.encipher('LVUBS FKTKJZ EXDYQP XFYEHV, AZS BVR WBGXXW-CTYXLRDK LMTLDALNQ.')
```

# Resources & Acknowledgment:
https://web.archive.org/web/20060720040135/http://members.fortunecity.com/jpeschel/gillog1.htm

http://www.softdoc.de/mr/de/downloads/files/EnigmaTechnischeDetails.pdf

https://www.youtube.com/watch?v=RzWB5jL5RX0

https://github.com/mikepound/enigma