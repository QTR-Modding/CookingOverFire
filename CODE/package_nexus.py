"""Generate CODE/package, ready to archive manually for Nexus. Replaces prior output."""

from pathlib import Path
import hashlib
import re
import runpy
import shutil
import xml.etree.ElementTree as ET

from config import cfg


ROOT = Path(__file__).resolve().parent.parent


def validate_installer(package):
    installer = ET.parse(package / "fomod/ModuleConfig.xml")
    for node in installer.iter():
        attribute = "source" if node.tag in {"file", "folder"} else "path"
        if node.tag not in {"file", "folder", "moduleImage", "image"}:
            continue
        relative = Path(node.attrib[attribute].replace("\\", "/"))
        target = (package / relative).resolve()
        if not target.is_relative_to(package.resolve()) or not target.exists():
            raise ValueError(f"Missing or invalid installer path: {relative}")


def file_hashes(folder):
    return {
        path.relative_to(folder).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in folder.rglob("*") if path.is_file()
    }


def clear_generated_folder(folder):
    if folder.resolve().parent != ROOT / "CODE" or folder.is_symlink():
        raise ValueError(f"Unexpected output location: {folder}")
    if folder.exists():
        shutil.rmtree(folder)


def main():
    version = ET.parse(ROOT / "nexus/fmod-essentials/fomod/info.xml").findtext("Version", "").strip()
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", version):
        raise ValueError(f"Invalid FOMOD version: {version!r}")
    output = Path(cfg["PATH"]["OUTPUT"])
    package = ROOT / "CODE/package"

    clear_generated_folder(output)
    clear_generated_folder(package)
    runpy.run_path(str(ROOT / "CODE/preset_creator_BBQ.py"), run_name="__main__")
    shutil.copytree(output, package)

    assets = ROOT / "nexus"
    shutil.copytree(assets / "AoT - BBQ- add-this-to-main-in-fomod", package / "main", dirs_exist_ok=True)
    shutil.copytree(assets / "fmod-essentials", package, dirs_exist_ok=True)
    turkey = "LvxMagicks - Turkey Dinner - CoF_Patch"
    shutil.copytree(assets / turkey, package / turkey, dirs_exist_ok=True)
    validate_installer(package)

    expected = file_hashes(output)
    for source, prefix in [
        (assets / "AoT - BBQ- add-this-to-main-in-fomod", "main/"),
        (assets / "fmod-essentials", ""),
        (assets / turkey, turkey + "/"),
    ]:
        expected.update({prefix + path: digest for path, digest in file_hashes(source).items()})
    if file_hashes(package) != expected:
        raise ValueError("Package verification failed")

    print(f"\nReady to archive: {package} (version {version})\nVerified {len(expected)} files.")


if __name__ == "__main__":
    main()
