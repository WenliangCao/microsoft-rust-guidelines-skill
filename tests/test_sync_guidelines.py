"""Behavior checks for snapshot preservation, discovery, and integrity."""

from pathlib import Path
import tempfile
import unittest

from scripts import sync_guidelines as sync


REVISION = "a" * 40


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.output = self.root / "output"
        self.guidelines = self.source / "src/guidelines"
        self.add_file("README.md", b"# About\n\nVersion: 1.0\n")
        (self.source / "LICENSE.md").write_bytes(b"MIT License\nCopyright Example\n")
        self.add_file("apps/README.md", b"# Application Guidelines\n")
        self.rule = (
            b"\xef\xbb\xbf<!-- Copyright Example -->\r\n\r\n"
            b"## Use an app error (M-APP-ERROR) { #M-APP-ERROR }\r\n\r\n"
            b"Applications may choose an error crate.\r\n\r\n"
            b"![Example](example.png)\r\n"
        )
        self.add_file("apps/M-APP-ERROR.md", self.rule)
        self.image = b"\x89PNG\r\n\x1a\n\x00example illustration"
        self.add_file("apps/example.png", self.image)

    def add_file(self, path, content):
        target = self.guidelines / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def snapshot(self):
        files = sync.build_snapshot(self.source, REVISION)
        sync.write_snapshot(self.output, files)
        return sync.check_snapshot(self.output)

    def test_preserves_original_bytes_and_resolves_index_links(self):
        manifest = self.snapshot()
        self.assertEqual(manifest["rule_count"], 1)
        self.assertEqual((self.output / sync.UPSTREAM / "apps/M-APP-ERROR.md").read_bytes(), self.rule)
        self.assertEqual((self.output / sync.UPSTREAM / "apps/example.png").read_bytes(), self.image)
        index = (self.output / sync.INDEX).read_text()
        self.assertIn(
            "[M-APP-ERROR — Use an app error](upstream/apps/M-APP-ERROR.md)", index
        )
        self.assertEqual(
            (self.output / sync.UPSTREAM / "LICENSE.md").read_bytes(),
            (self.source / "LICENSE.md").read_bytes(),
        )

    def test_discovers_new_topics_and_removes_deleted_rules(self):
        self.add_file("new-topic/README.md", b"# New Topic\n")
        self.add_file("new-topic/M-NEW.md", b"## New advice (M-NEW) { #M-NEW }\n")
        manifest = self.snapshot()
        self.assertEqual((manifest["rule_count"], manifest["topic_count"]), (2, 2))
        (self.guidelines / "new-topic/M-NEW.md").unlink()
        self.snapshot()
        self.assertFalse((self.output / sync.UPSTREAM / "new-topic/M-NEW.md").exists())

    def test_refresh_preserves_authored_files(self):
        self.output.mkdir()
        entrypoint = self.output / "SKILL.md"
        entrypoint.write_text("Hand-maintained entrypoint\n")
        self.snapshot()
        self.snapshot()
        self.assertEqual(entrypoint.read_text(), "Hand-maintained entrypoint\n")

    def test_check_rejects_changed_missing_or_extra_files(self):
        self.snapshot()
        rule = self.output / sync.UPSTREAM / "apps/M-APP-ERROR.md"
        for change in ("changed", "missing", "extra"):
            with self.subTest(change=change):
                if change == "changed":
                    rule.write_bytes(self.rule + b"altered\n")
                elif change == "missing":
                    rule.unlink()
                else:
                    (rule.parent / "M-UNRECORDED.md").write_text("Unexpected rule")
                with self.assertRaises(ValueError):
                    sync.check_snapshot(self.output)
                self.snapshot()

    def test_rejects_duplicate_ids_across_topics(self):
        self.add_file("other/README.md", b"# Other\n")
        self.add_file("other/M-APP-ERROR.md", self.rule)
        with self.assertRaisesRegex(ValueError, "duplicate rule ID"):
            sync.build_snapshot(self.source, REVISION)

    def test_rejects_filename_and_heading_id_mismatch(self):
        self.add_file("apps/M-APP-ERROR.md", b"## Other advice (M-OTHER) { #M-OTHER }\n")
        with self.assertRaisesRegex(ValueError, "rule ID"):
            sync.build_snapshot(self.source, REVISION)

    def test_missing_illustration_fails_before_changing_snapshot(self):
        self.snapshot()
        before = (self.output / sync.MANIFEST).read_bytes()
        (self.guidelines / "apps/example.png").unlink()
        with self.assertRaises(FileNotFoundError):
            sync.build_snapshot(self.source, REVISION)
        self.assertEqual((self.output / sync.MANIFEST).read_bytes(), before)
        sync.check_snapshot(self.output)


if __name__ == "__main__":
    unittest.main()
