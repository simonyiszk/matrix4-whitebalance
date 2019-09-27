# matrix4-whitebalance
UI for setting white balance on muebs.

```
python white_balance.py
```

##Scales
Manual scale: each level of the three colors can be adjusted independently.

Global scale: each color has a single slider (multiplier) for adjustment. Individual levels of a color is automatically calculated.

##Buttons
Each room (2 windows) is represented by a button. Select the rooms in need of white balance correction, or click "Select All" or "Deselect all". Selected rooms turn yellow.

Use "Send" button to adjust selected rooms. In this case an UDP datagram is sent to each selected muebs IP.

Use "SendAll" button to update all rooms' white balance setting. This way a single datagram is sent to the broadcast IP (10.6.255.255)

