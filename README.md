# Resource Backports ![m][badge1]
Undo [The Flattening][wiki/flattening] of Minecraft and backport most of the [New Texture][wiki/texture_update] to old versions, avaliable to `1.6.1` until `1.12.2`, with some [limitation](#limitation). 
## Why?
**Why the script to do it? Isn't uploading the converted pack enough?**  
Well, although it will be easier to the players and especially **me**, it breaks Minecraft's [EULA][eula] and Mojang's [Terms and Use][terms], which is a bad thing to do.

## How?
### Windows
TBA

### Unix
On your preffered folder, run these on terminal:
```bash
git clone https://github.com/deirn/resource-backports.git
cd resource-backports
chmod +x resource_backports.py
./resource_backports.py
```
Or
```bash
python3 resource-backports.py
```

## Limitations
### Bed
On `1.10` and before, bed is a regular block, not a block entity. Therefore the texture structure is different from version `1.11` and after. A model workaround is required. See [`bed_foot.json`][bed_f] and [`bed_head.json`][bed_h]

### Effect Icons
Effect icons is separated from Player Inventory GUI's texture and splitted to one image per effect. Generating image is too hard to do right now with my limited knowledge<sup>[*to be added later, maybe*]().</sup>

### Dragon Fireball
Still based on texture version `3.6` appear on client version `1.14`. The thing is, in `1.15` it messed up with chests' model and that means it'll broke the ender chest texture if I update it. I decided to ignore the fireball since it less common.


[badge1]: https://img.shields.io/badge/Minecraft-Java%20Edition-brightgreen
[wiki/flattening]: https://minecraft.gamepedia.com/Java_Edition_1.13/Flattening
[wiki/texture_update]: https://minecraft.gamepedia.com/Texture_Update
[eula]: https://account.mojang.com/documents/minecraft_eula
[terms]: https://account.mojang.com/terms
[client.jar]: https://launcher.mojang.com/v1/objects/8c325a0c5bd674dd747d6ebaa4c791fd363ad8a9/client.jar
[mappings]: mappings.json
[bed_f]: workarounds/bed_foot.json
[bed_h]: workarounds/bed_head.json
[update_aquatic]: https://minecraft.gamepedia.com/Update_Aquatic