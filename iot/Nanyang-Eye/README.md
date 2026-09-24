# Nanyang Eye

### Author: Mujabeast

At 02:13, NTU SOC captured traffic from NANYANG-EYE-03, a retired PTZ camera
that should have been offline.

The camera has been repurposed by a group calling itself ORION. A recovered
packet capture and damaged Python control client show that its maintenance
interface was used to redirect the camera from its normal view.

Analyse the evidence, recover the control details, and repair the supplied
client on your own laptop.

Your final operation must be performed at the Camera Bay organiser workstation.
Restore the camera's view and locate the flag.

Flag format: `sentctf{...}`

## Files

- `dist/project_orion.zip`

Extract the archive before beginning. The Camera Bay workstation is available
only for the final physical operation. It starts at a normal Linux terminal
prompt with a fresh working copy of the client; it does not open an editor
automatically.
