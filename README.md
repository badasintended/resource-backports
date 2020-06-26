# Resource Backports ![m][badge]
Undo [The Flattening][wiki/flattening] of Minecraft and backport most of the [New Texture][wiki/texture_update] to old versions, avaliable to `1.6.1` until `1.12.2`, with some [limitation](#limitations). 
## Why?
**Why the script to do it? Isn't uploading the converted pack enough?**  
Well, although it will be easier to the players and especially **me**, it breaks Minecraft's [EULA][eula] and Mojang's [Terms and Use][terms], which is a bad thing to do.

## How?
### Windows
1. Download the latest [release][releases],
2. Copy exe to an empty folder
3. Open command prompt (`Win+R cmd`),
4. Run these on cmd:
   ```cmd
   cd C:\path\to\download\folder
   resource_backports
   ```

### Unix
On an empty folder, run these on terminal:
```bash
wget -q https://raw.githubusercontent.com/deirn/resource-backports/master/resource_backports.py 
python3 resource_backports.py 
```
Or:  
1. Download the latest [release][releases],
2. On the download folder:
   ```bash
   chmod +x resource_backports
   ./resource_backports
   ```

## Limitations
### Bed
On `1.10` and before, bed is a regular block, not a block entity. Therefore the texture structure is different from version `1.11` and after. A model workaround is required. See [`bed_foot.json`][bed_f] and [`bed_head.json`][bed_h]

### Dragon Fireball
Still based on texture version `3.6` appear on client version `1.14`. The thing is, in `1.15` it messed up with chests' model and that means it'll broke the ender chest texture if I update it. I decided to ignore the fireball since it less common.

### Horses
Model changed, so texture breaks on older version. <sup><sub><sup><sub><sup><sub><sup><sub>To hard to do right now, might add later.</sup></sub></sup></sub></sup></sub></sup></sub>


[badge]: https://img.shields.io/badge/Minecraft-Java%20Edition-brightgreen
[wiki/flattening]: https://minecraft.gamepedia.com/Java_Edition_1.13/Flattening
[wiki/texture_update]: https://minecraft.gamepedia.com/Texture_Update
[eula]: https://account.mojang.com/documents/minecraft_eula
[terms]: https://account.mojang.com/terms
[releases]: https://github.com/deirn/resource-backports/releases
[bed_f]: workarounds/bed_foot.json
[bed_h]: workarounds/bed_head.json
