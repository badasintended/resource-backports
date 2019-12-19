#!/usr/bin/env python3

import urllib.request
import json
import hashlib
import shutil
import os
import requests
from threading import Thread
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

BUFF_SIZE = 65536

root_dir = Path(__file__).parent


def create_dir(path):
    if not Path(path).exists():
        Path(path).mkdir(parents=True)


def loading(target, message):
    bg_thread = Thread(target=target)
    bg_thread.start()
    spinner = ["-", "\\", "|", "/"]
    i = 0
    while bg_thread.is_alive():
        print("%s %s" % (message, spinner[i]), end="\r")
        i += 1
        if i >= 4:
            i = 0
        bg_thread.join(0.2)
    print("%s [Done]" % message)


def join_path(path1, path2):
    return Path("%s/%s" % (path1, path2))


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


input_path = join_path(root_dir, "input")
create_dir(input_path)

clear()

print("""
Resource Backports v0.1
github.com/deirn/resource-backports
Undo The Flattening(TM)!

You need an internet connection to use this script.

Select target version:
1.) 1.6.1-1.8.9
2.) 1.9–1.10.2
3.) 1.11–1.12.2
or q to cancel

"""[1:-1])

target_input = str(input("[1/2/3/q]: ")).lower()
while True:
    if target_input in ["1", "2", "3", "q"]:
        break
    target_input = str(input("Try again. [1/2/3/q]: ")).lower()

if target_input == "q":
    exit()

clear()

client_url = "https://launcher.mojang.com/v1/objects/8c325a0c5bd674dd747d6ebaa4c791fd363ad8a9/client.jar"
client_sha1 = "8c325a0c5bd674dd747d6ebaa4c791fd363ad8a9"
client_file_name = "1.14.jar"
client_path = join_path(input_path, client_file_name)

dl_client = True

if Path(client_path).exists():
    sha1 = hashlib.sha1()
    with Path(client_path).open(mode="rb") as f:
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            sha1.update(data)
    if sha1.hexdigest() == client_sha1:
        print("Found 1.14 client jar with correct SHA1, skipping download.")
        dl_client = False

if dl_client:
    func = lambda: urllib.request.urlretrieve(client_url, client_path)
    loading(func, "Downloading %s" % client_url)

client_dir = join_path(input_path, "1.14")
create_dir(client_dir)

with ZipFile(client_path, "r") as client_zip:
    func = lambda: client_zip.extractall(client_dir)
    loading(func, "Extracting %s" % client_path)

target_versions = ["1.8", "1.10", "1.12"]
target_version = target_versions[int(target_input) - 1]

output_dir = join_path(root_dir, "output")
create_dir(output_dir)

source_texture_dir = join_path(client_dir, "assets/minecraft/textures")

target_root_dir = join_path(output_dir, target_version)
create_dir(target_root_dir)

target_texture_dir = join_path(target_root_dir, "assets/minecraft/textures")
create_dir(target_texture_dir)

raw_github_url = "https://raw.githubusercontent.com/deirn/resource-backports/master"

mappings = requests.get("%s/mappings/normal.json" % raw_github_url).json()


def copy_texture(source, target):
    source_path = join_path(source_texture_dir, "%s" % source)
    target_path = join_path(target_texture_dir, "%s" % target)
    target_dir = target_path.parent
    create_dir(target_dir)
    func = lambda: shutil.copyfile(source_path, target_path)
    loading(func, "Copying %s to %s" % (source, target))


for source, target in mappings.items():
    if not isinstance(target, str):
        for x in target:
            copy_texture(source, x)
        continue
    copy_texture(source, target)


# Villager and Zombie Villager Skin
villager_mappings = requests.get("%s/mappings/villager.json" % raw_github_url).json()

entity_source_dir = join_path(source_texture_dir, "entity")
entity_target_dir = join_path(target_texture_dir, "entity")


def villager_create_image(layer0, layer1, layer2, target_path):
    bg = Image.open(layer0)
    fg1 = Image.open(layer1)
    fg2 = Image.open(layer2)
    bg.paste(fg1, (0, 0), fg1)
    bg.paste(fg2, (0, 0), fg2)
    bg.save(target_path)


def villager(prefix=""):
    layer0 = join_path(entity_source_dir, "%svillager/%svillager.png" % (prefix, prefix))
    layer1 = join_path(entity_source_dir, "%svillager/type/plains.png" % prefix)
    layer2_dir = join_path(entity_source_dir, "%svillager/profession" % prefix)
    target_dir = join_path(entity_target_dir, "%svillager" % prefix)
    create_dir(target_dir)
    for source, target in villager_mappings.items():
        layer2 = join_path(layer2_dir, "%s.png" % source)
        target_path = join_path(entity_target_dir, "%svillager/%s%s.png" % (prefix, prefix, target))
        func = lambda: villager_create_image(layer0, layer1, layer2, target_path)
        loading(func, "Creating Villager Texture (%s%s)" % (prefix, target))


villager()           # Regular
villager("zombie_")  # Zombie villager

# Zombie Villager Edits: Hat and hand
hat_area = Image.new("RGBA", (32, 20), (255, 255, 255, 0))


def zombie_villager_edit(target_image, target_path):
    target_image.paste(hat_area, (32, 0))
    hand_area = target_image.crop((44, 22, 60, 38))
    target_image.paste(hand_area, (44, 38), hand_area)
    target_image.save(target_path)


for unused, target in villager_mappings.items():
    target_path = join_path(entity_target_dir, "zombie_villager/zombie_%s.png" % target)
    target_image = Image.open(target_path).convert("RGBA")
    func = lambda: zombie_villager_edit(target_image, target_path)
    loading(func, "Editing zombie_%s.png" % target)


# GUI Effects
gui_effect_mapping = requests.get("%s/mappings/gui_effect.json" % raw_github_url).json()

gui_source_path = join_path(source_texture_dir, "gui/container/inventory.png")
effect_source_dir = join_path(source_texture_dir, "mob_effect")

gui_target_dir = join_path(target_texture_dir, "gui/container")
create_dir(gui_target_dir)

gui_target_path = join_path(gui_target_dir, "inventory.png")

func = lambda: shutil.copyfile(gui_source_path, gui_target_path)
loading(func, "Copying gui/container/inventory.png to gui/container/inventory.png")


def gui_effect_edit(effect, coordinates):
    effect_path = join_path(effect_source_dir, "%s.png" % effect)
    bg = Image.open(gui_target_path)
    fg = Image.open(effect_path)
    bg.paste(fg, coordinates, fg)
    bg.save(gui_target_path)


for effect, coordinates in gui_effect_mapping.items():
    func = lambda: gui_effect_edit(effect, coordinates)
    loading(func, "Adding %s effect texture to gui/container/inventory.png" % effect)


# Bed Workaround
if target_version in ["1.8", "1.10"]:
    source_workaround = [
        requests.get("%s/workarounds/bed_foot.json" % raw_github_url).text,
        requests.get("%s/workarounds/bed_head.json" % raw_github_url).text
    ]
    target_workaround = [
        join_path(target_root_dir, "assets/minecraft/models/block/bed_foot.json"),
        join_path(target_root_dir, "assets/minecraft/models/block/bed_head.json")
    ]
    for i in [0, 1]:
        create_dir(target_workaround[i].parent)
        target_workaround_file = open(target_workaround[i], "w")
        func = lambda: target_workaround_file.write(source_workaround[i])
        loading(func, "Copying workaround (%s/2)" % str(i))


pack_mcmeta = """
{
    "pack": {
        "pack_format": %s,
        "description": "Resource Backports script by deirn"
    }
}
"""[1:-1] % int(target_input)

pack_mcmeta_path = join_path(target_root_dir, "pack.mcmeta")
pack_mcmeta_file = open(pack_mcmeta_path, "w")
func = lambda: pack_mcmeta_file.write(pack_mcmeta)
loading(func, "Creating pack.mcmeta")
pack_mcmeta_file.close()

source_pack_icon = join_path(client_dir, "pack.png")
target_pack_icon = join_path(target_root_dir, "pack.png")
func = lambda: shutil.copyfile(source_pack_icon, target_pack_icon)
loading(func, "Copying pack.png")

output_zip_path = join_path(output_dir, target_version)
func = lambda: shutil.make_archive(output_zip_path, "zip", target_root_dir, "assets")
loading(func, "Compressing resource pack to zip")

output_zip = ZipFile("%s.zip" % output_zip_path, "a")
func = lambda: output_zip.write(pack_mcmeta_path, os.path.basename(pack_mcmeta_path))
loading(func, "Adding pack.mcmeta to zip")
func = lambda: output_zip.write(target_pack_icon, os.path.basename(target_pack_icon))
loading(func, "Adding pack.png to zip")
output_zip.close()

shutil.rmtree(client_dir)
shutil.rmtree(target_root_dir)

print("Done, enjoy JAPPA's Textures. DO NOT DISTRIBUTE THE PACK!")
