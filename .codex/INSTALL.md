# Installing Refinex Harness Skills for Codex

Internal-first installation guide for using the Harness family in Codex via native skill discovery.

## Quick install

```bash
mkdir -p ~/.agents/skills
ln -s /Users/refinex/develop/code/refinex/Refinex-Skills/skills ~/.agents/skills/refinex-skills
```

Restart Codex after creating the symlink.

## Verify

```bash
ls -la ~/.agents/skills/refinex-skills
```

You should see a symlink that points to this repository's `skills/` directory.

## Suggested first check

Open a new Codex session and ask one of:

- `初始化 Harness`
- `这个仓库的控制面可能漂移了`
- `做这个功能`
- `修复这个 bug`

Codex should route into the appropriate Harness skill family member.

## Uninstall

```bash
rm ~/.agents/skills/refinex-skills
```

## Notes

- This repository is optimized for internal use, not marketplace packaging.
- `harness-using` is the preferred entry discipline for repo tasks.
- `harness-verify` should be expected near completion or handoff.
