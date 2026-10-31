import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


installer = module("install_skill")
builder = module("build_release")


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_install_is_idempotent_and_dry_run_does_not_write(self):
        dest = self.root / "skills"
        self.assertEqual(installer.install(dest, dry_run=True)["status"], "dry run")
        self.assertFalse(dest.exists())
        result = installer.install(dest)
        self.assertTrue((Path(result["path"]) / "SKILL.md").is_file())
        self.assertEqual(installer.install(dest)["status"], "already installed")

    def test_existing_user_edits_require_replace_and_are_backed_up(self):
        dest = self.root / "skills"
        target = Path(installer.install(dest)["path"])
        (target / "my-notes.txt").write_text("Keep this user edit")
        with self.assertRaises(FileExistsError):
            installer.install(dest)
        self.assertEqual((target / "my-notes.txt").read_text(), "Keep this user edit")
        result = installer.install(dest, replace=True)
        backup = Path(result["backup"])
        self.assertEqual((backup / "my-notes.txt").read_text(), "Keep this user edit")
        self.assertFalse((target / "my-notes.txt").exists())
        self.assertNotEqual(backup.parent, dest)

    def test_symlink_target_is_not_overwritten(self):
        dest = self.root / "skills"
        dest.mkdir()
        external = self.root / "important"
        external.mkdir()
        try:
            (dest / installer.NAME).symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("Host cannot create symlinks")
        with self.assertRaises(ValueError):
            installer.install(dest, replace=True)
        self.assertTrue(external.exists())

    def test_archives_have_expected_entry_points_and_no_host_paths(self):
        archives = builder.build(self.root / "dist")
        for filename in archives:
            if not filename.endswith(".zip"):
                continue
            with zipfile.ZipFile(filename) as z:
                names = z.namelist()
                self.assertFalse(any("__pycache__" in n or "/.git/" in n for n in names))
                for n in names:
                    if n.endswith((".py", ".json", ".md", ".yaml", ".txt")):
                        data = z.read(n)
                        self.assertNotIn(b"/workspace/" + b"scratch/", data, n)
                        self.assertNotIn(b"/root/" + b".codex/", data, n)
                if "-plugin-" in filename:
                    self.assertIn("plugin.json", names)
                    self.assertIn("skills/draft-cad-from-images/SKILL.md", names)
                elif "-skill-" in filename:
                    self.assertIn("draft-cad-from-images/SKILL.md", names)
                else:
                    self.assertIn("photo-to-autocad/README.md", names)
                    self.assertIn("photo-to-autocad/.agents/plugins/marketplace.json", names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
