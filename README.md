# PRP comparative analysis

Research sources and results for the protocol and stack comparison consumed by the PRP website. This repository contains comparison material, not the PRP protocol implementation or its dependencies.

The current result is [revision 8.04](results/comparison-8.04.json), covering 62 criteria and 28 stacks. Review of the retained evidence moved two annotations from assumed to documented since [revision 8.03](results/comparison-8.03.json). The NET/ROM manual documents circuit continuity across an available alternate route. Linux v6.12 documents proactive batman-adv broadcast duplication across eligible paths. The matrix contains 912 Yes, 769 No and 55 Pending verdicts. The website reads the single current result and its SHA-256 from [provenance.json](provenance.json).

Each cell includes its rationale, qualifications, evidence level and source citations. Public source URLs point to their original publishers. Non-URL evidence references identify research records not shipped here; do not turn them into repository links. Logo filenames and attribution metadata are preserved, but image assets are not included; consumers must not assume these files exist.

See [METHODOLOGY.md](METHODOLOGY.md) for the existing assessment policy and [RIGHTS.md](RIGHTS.md) for distribution limits.

The comparison annotation logic is in `tools/evidence_levels.py`. Its `annotate` function requires a separate review input that is not included; this module alone is not a complete regeneration pipeline.

Website consumers should select an exact Git commit and verify the result digest before importing an update. A new research revision does not automatically change the version displayed by the website.
