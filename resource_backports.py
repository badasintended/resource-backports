#!/usr/bin/env python3

import urllib.request
import json
import hashlib
import shutil
import os
from threading import Thread
from pathlib import Path
from zipfile import ZipFile

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


def parse_json(path):
    raw_file = Path(path).read_text()
    parsed_file = json.loads(raw_file)
    return parsed_file


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

You need an internet connection to use this script, atleast for
the first time, to download the client.jar avaliable from Mojang

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
        print("Found latest client jar with correct SHA1, skipping download.")
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

mappings_path = join_path(root_dir, "mappings.json")

mappings = parse_json(mappings_path)


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

if target_version in ["1.8", "1.10"]:
    source_workaround = [
        join_path(root_dir, "workarounds/bed_foot.json"),
        join_path(root_dir, "workarounds/bed_head.json")
    ]
    target_workaround = [
        join_path(target_root_dir, "assets/minecraft/models/block/bed_foot.json"),
        join_path(target_root_dir, "assets/minecraft/models/block/bed_head.json")
    ]
    for i in [0, 1]:
        create_dir(target_workaround[i].parent)
        func = lambda: shutil.copyfile(source_workaround[i], target_workaround[i])
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
