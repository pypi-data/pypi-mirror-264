# CHANGELOG



## v7.0.3 (2023-12-04)

### Build

* build: convert to pyproject.toml ([`88f5bd8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/88f5bd86e87cfac8bb86806028f278b1dd9e503a))

### Chore

* chore: add Python 3.10 and 3.11 classifiers ([`817ae3d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/817ae3d5d77246f54b1c9975417bccb19308dfa3))

### Ci

* ci: use &#34;python:3.12-rc&#34; for pynext test ([`48529fb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/48529fbc43e98059aaaeaa1177d2e3adae35ff8f))

### Fix

* fix: update ZipWrapper to not leak resources in threaded environments ([`11b0ab5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/11b0ab5941efaa526ba2a027bb4958e6b320179c))

### Test

* test: update to latest Pytest ([`46018ed`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/46018ed89f42e7551fb1738fcaa77a8e937912c7))

### Unknown

* Merge branch &#39;pyconfig&#39; into &#39;master&#39;

build: convert to pyproject.toml

See merge request momotor/engine-py3/momotor-bundles!17 ([`ac25fe4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ac25fe4bb005b160d8645069fcef093ea9f8f4aa))


## v7.0.2 (2023-06-19)

### Fix

* fix: incorrect fetching of `executable` attribute ([`97653fa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/97653fa866833acd0376fc4764a28473875a0ed6))

### Unknown

* 7.0.2

&#39;chore: bump version number&#39; ([`72fef72`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/72fef720079998ecdb86874f5b3484a8ea5013da))

* Merge remote-tracking branch &#39;origin/master&#39; ([`b5225c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b5225c1e2b2a2860d012679b41ab88d14fc09377))

* doc: all attachment nodes now support directory attachments ([`fc80712`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fc8071225e8b383e8eea7a0409f1273b3b919950))


## v7.0.1 (2022-11-21)

### Fix

* fix: correctly handle empty directory attachments when exporting a bundle ([`a3cb87e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a3cb87efb079bd78a8a57ae2de458cc88287e1f8))

### Unknown

* 7.0.1

&#39;chore: bump version number&#39; ([`cf182a9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cf182a92b555a2f811f4243143b7a024a17a0323))


## v7.0.0 (2022-10-06)

### Breaking

* fix: better handling of directory attachments

BREAKING CHANGE: File and Repository methods changes:

* attachment methods can now also throw IsADirectoryError exceptions
* File and Repository elements throw exception in .file_size() method if src does not exist or is a directory ([`e15b079`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e15b079b1243384bf066f78a302c3a59418a1774))

### Feature

* feat: add `rglob` and `irglob` lookups to filters ([`3d694da`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d694da0ad6975d97a6c5308fb979951e2b10033))

### Fix

* fix: remove unnecessary requirement from requirements.txt ([`876970d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/876970de92c812b278b7b4018eb9157cf29221db))

### Refactor

* refactor: create a new type for NO_CONTENT ([`392f945`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/392f94529d2fc8699b5a4a97905d1832d4779a88))

### Unknown

* 7.0.0

&#39;chore: bump version number&#39; ([`fe837e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fe837e91c695804e443d860c669b1319fff2ea6c))

* Merge branch &#39;v7&#39; into &#39;master&#39;

Merge branch &#39;v7&#39;

Closes #32

See merge request momotor/engine-py3/momotor-bundles!16 ([`d92b4b1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d92b4b1fbfcb705aaf85e53a128b6553f275b136))

* doc: document File.create(), especially the `src` parameter details (closes #32) ([`065c4ea`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/065c4ead455ccf042a2a1b4791c6174c9f26b6b8))

* doc: add `momotor.bundles.elements.content` to the documentation ([`6554f60`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6554f604eebc9482e4f59f66b02b8672eb69cd98))


## v6.1.0 (2022-03-24)

### Ci

* ci: drop &#39;rc&#39; build tasks, as semver now generates rc versions automatically [skip-ci] ([`c6e25e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c6e25e87a5f3e501df5ef9feb4de2e6521aab23c))

* ci: remove SSH setup, use GL_TOKEN instead ([`ef83c41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ef83c41f426dd1473c5050bd60db08e73ab8536a))

* ci: do not fail pipeline if semver fails on non-default branch ([`4aee0b0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4aee0b0eb8a9bc1a05bd425a03139172b4799a42))

### Feature

* feat: move recoding of content to bundle creation stage. Adds an argument `optimize`. Recoding is done with optimize is set. ([`c44c4e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c44c4e822045b0a6c6055d208874387908c681a1))

* feat: add &#39;recode_content&#39; argument to Result.recreate (closes #31) ([`801ff6b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/801ff6b289fe5fa5770861329f499e7dcdf3b159))

### Unknown

* 6.1.0

&#39;chore: bump version number&#39; ([`87ccd4d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/87ccd4d37addcf4b0fa5e55e140a1a2a79a223ce))

* Merge branch &#39;31-fast-copying-of-content-nodes&#39; into &#39;master&#39;

Resolve &#34;&#34;fast&#34; copying of content nodes&#34;

Closes #31

See merge request momotor/engine-py3/momotor-bundles!15 ([`52a196e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/52a196eabb58c5ef29da7e7beaca8c033b27f02a))


## v6.0.1 (2022-01-20)

### Fix

* fix: removed deprecation for &#39;int&#39; option type, added &#39;bool&#39; and &#39;boolean&#39; type ([`a144ef9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a144ef960d32f4ad1bf8b3df4f1ea3e7e8278067))

### Unknown

* 6.0.1

&#39;chore: bump version number&#39; ([`509bec3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/509bec376d6161755a916e5664ea89c79e45a44a))


## v6.0.0 (2022-01-17)

### Chore

* chore: sphinx-autodoc-typehints==1.14.0 breaks doc builds ([`40fb259`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/40fb259f4b7c98f266bbc7089dbeebaa3dfc31e8))

### Ci

* ci: bit less verbose sphinx output ([`9f60c33`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9f60c3363541722f8f0e4dcd9c95e63269cbf735))

* ci: verbose Sphinx output ([`5a22764`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5a22764a0d9e5cbba1857e5680f7952334426f7a))

### Feature

* feat: make Outcome a separate enum from OutcomeSimpleType, add OutcomeLiteral type ([`3d50a53`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d50a53d70e99e56399debdd3cacbf685fd4bb56))

### Fix

* fix: correct typehint for `cls` ([`95bd649`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/95bd64910123292d4e01c1b19c867884958d8f8a))

* fix: add OutcomeLiteral type ([`c88109e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c88109e20d8f490a67b2412970679b9eb1618bbb))

### Unknown

* 6.0.0

&#39;chore: bump version number&#39; ([`68e937a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/68e937a6c69fb768d84037169627c33f76fdd66b))

* Merge branch &#39;epic-skip-tasks&#39; into &#39;master&#39;

Epic skip tasks

Closes #24 and #25

See merge request momotor/engine-py3/momotor-bundles!14 ([`8216314`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8216314b15aeabea596c7346fdb9211f6cc19e75))

* Merge branch &#39;master&#39; into epic-skip-tasks

# Conflicts:
#	src/momotor/bundles/utils/step_condition.py
#	tests/utils/test_step_condition.py ([`fa20558`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa205585bde7a41d308fda6527d5925585446ed8))


## v5.2.0 (2021-12-30)

### Breaking

* refactor: move all options related methods to a new package `momotor-engine-options`

BREAKING CHANGE: Several modules have moved to another package

Modules `momotor.bundles.utils.dependencies`, `momotor.bundles.utils.option`, `momotor.bundles.utils.result_query`, `momotor.bundles.utils.skip`, `momotor.bundles.utils.step_condition` and `momotor.bundles.utils.tasks` moved to new package `momotor-engine-options` ([`5e15ea3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e15ea3a1544da38b746e04a12c3424955056f56))

### Chore

* chore: add &#39;skip&#39; to unit tests ([`ea9b0e6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ea9b0e6e497dc76c221187640eb747b0daffcdf4))

* chore: add &#39;skip&#39; to unit tests ([`f6f16bd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f6f16bd239cba8b4e02e975f0cb67a6dcb8ca59d))

### Ci

* ci: correct PEP440 rc version number ([`7bef25c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7bef25ccafeb5cd12edbc4b591209106dc6e686e))

* ci: add stages to build and publish release candidates ([`54d82d4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/54d82d4fb0e4e4424a1d096c25abc95c95cbfc42))

### Feature

* feat: add &#34;skip&#34; as value for task outcomes (closes #24) ([`7fd8a7f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7fd8a7f1f334e465d5e0f418bd55567c34ef5fed))

* feat: add &#39;properties&#39; argument to create_error_result_bundle ([`337284c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/337284c36e9b4d7a99e6bf162a25cca65e50aec4))

* feat: add skip-if property checking ([`2ec1bec`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2ec1bec8495faedeed41e799ae1f3e870de7ffbe))

* feat: add result filtering and matching functions from base checklet (closes #25) ([`ccfec9d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ccfec9d7817692b3ca46b31b89967fbebce9caa8))

* feat: add &#34;skip&#34; as value for task outcomes (closes #24) ([`aa6933e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/aa6933e9abe7956ce370c65418445d184ef3e224))

### Fix

* fix: use outcome directly (create accepts both enum and str) ([`64bbadf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/64bbadf94dff7430c499a971e28fe2cbbdf745ad))

* fix: use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`30c1abf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/30c1abfc168f930ae7c3d4d1c250de6aca6b79e3))

* fix: use outcome directly (create accepts both enum and str) ([`06fe917`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/06fe9178e9125948f3f0e24e63c940e49a783dc9))

* fix: imports ([`1644ae7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1644ae73aa31fc25b93fa5fec92f5553cd4dd961))

* fix: create_error_result_bundle() function ([`5ee5048`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5ee5048281914b264d90453c5a691997171ae6f7))

* fix: add &#34;test**&#34; id query feature ([`d3e7c37`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d3e7c370758915ac744b276e9961b544e9639b50))

* fix: use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`4bf371b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4bf371b7c7feec600785e9f98bb46cb9e57aad1c))

### Unknown

* 5.2.0

&#39;chore: bump version number&#39; ([`802a67d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/802a67d63295edfd8b3facddd833d6bba7be8a2c))

* doc: add &#39;skip&#39; outcome to table ([`904abf5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/904abf552c6777a6b14d2fedcb602d4bbcbb9697))

* Merge remote-tracking branch &#39;origin/epic-skip-tasks&#39; into epic-skip-tasks ([`a3dc7b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a3dc7b212ec89e5a7902a84192fdafd0dace8f3b))

* revert: rogue renaming ([`fad5c8d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fad5c8d79ec3698899cae91f2eb360befa18eacb))

* doc: add &#39;skip&#39; outcome to table ([`b328b07`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b328b07c0b688acc6fe03d96baaf9067cc4bdd54))


## v5.1.2 (2021-12-21)

### Breaking

* refactor: move all options related methods to a new package `momotor-engine-options`

BREAKING CHANGE: Several modules have moved to another package

Modules `momotor.bundles.utils.dependencies`, `momotor.bundles.utils.option`, `momotor.bundles.utils.result_query`, `momotor.bundles.utils.skip`, `momotor.bundles.utils.step_condition` and `momotor.bundles.utils.tasks` moved to new package `momotor-engine-options` ([`6034cbb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6034cbb46cfd43de26a3f75565b07ae152226bcf))

### Chore

* chore: add &#39;skip&#39; to unit tests ([`c921e93`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c921e937454dad62c1f0d20e4ba190b9208c4953))

### Feature

* feat: add &#39;properties&#39; argument to create_error_result_bundle ([`812bc61`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/812bc615a1944045f38562c942c90adddadea025))

* feat: add skip-if property checking ([`b829353`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b82935342973b565d6a3eea2e65b1d46bd4b3701))

* feat: add result filtering and matching functions from base checklet (closes #25) ([`2428675`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/24286756dcb34fd4eccfa8864e97e9178805dbb6))

* feat: add &#34;skip&#34; as value for task outcomes (closes #24) ([`635b7f0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/635b7f0b655f0c6cbd3bfe659f688a4025c5000e))

### Fix

* fix: only raise InvalidDependencies for explicit dependencies, not for wildcard or placeholder ones ([`7f737e6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7f737e6d3765660f211495503452b7ede48a8394))

* fix: use outcome directly (create accepts both enum and str) ([`54d067f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/54d067fcb745abbc01dcd47b6a6b9c5c8e211e2b))

* fix: imports ([`35e5c47`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/35e5c47622bc7f4532bad5bdf12fb2eda332491f))

* fix: create_error_result_bundle() function ([`e02b295`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e02b295d508008dfd94a4bde0a4070a9ab72cdfd))

* fix: add &#34;test**&#34; id query feature ([`2b768fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2b768fec07c81699d36a1f243e066aa5dee31f86))

* fix: use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`57ad63e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/57ad63e6c55ebb3f3554b85de327d65fb9b041bf))

### Unknown

* 5.1.2

&#39;chore: bump version number&#39; ([`717c5f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/717c5f3ca1742414aa90ba0c0067f0c831503712))

* revert: rogue renaming ([`7d0443e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d0443ee1ec336c329a6e276eb00fe8028db4028))

* doc: add &#39;skip&#39; outcome to table ([`cfa7f29`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cfa7f29d8358097d781dcb0cc038978d3f804615))


## v5.1.1 (2021-11-26)

### Fix

* fix: if `executable` attribute is a string value, convert it to boolean ([`0d46c05`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d46c05652bee309c5ec1f323ed03108749a3f8a))

### Refactor

* refactor: include option name in ValueError exception ([`26922fc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/26922fc4b8de45d2e4ad5541dde4645da02369e9))

### Unknown

* 5.1.1

&#39;chore: bump version number&#39; ([`6cc4f81`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6cc4f81496690b55c804be130f8d2f4c0ca63370))


## v5.1.0 (2021-11-23)

### Chore

* chore: update project ([`79619a7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/79619a73a7fa41eada46dfb88b403429189df5d2))

### Feature

* feat: add wildcard dependencies and ignore dependencies with arithmetic errors ([`b553f6a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b553f6a3488e6b3848cf8528177ea4477cbcf3e2))

* feat: add simple arithmetic to `apply_task_number` ([`0390416`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/03904162ced5b45b6a33599e4c42cad85e736560))

### Fix

* fix: _get_full_deps ([`44553e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/44553e844d4d88df4bd369a8d629463069cc4c10))

* fix: changed dependency calculation methods to return a tuple instead of a set, to maintain step ordering ([`f5a02ee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f5a02ee10e7d265274f3cf0efe0faecf6b8494c1))

### Refactor

* refactor: cleanup and optimizations ([`184e924`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/184e924277ca7e599e05f2752a303975309ed22e))

### Unknown

* 5.1.0

&#39;chore: bump version number&#39; ([`32fa94d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/32fa94daa5736f4c6ef489c4fdffd9ff4b2ccdbf))

* Merge branch &#39;23-allow-dependencies-on-sub-tasks-support-simple-arithmetic-in-task-references&#39; into &#39;master&#39;

Resolve &#34;Allow dependencies on sub-tasks, support simple arithmetic in task references&#34;

Closes #23

See merge request momotor/engine-py3/momotor-bundles!13 ([`c8d70e2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c8d70e21bea0af7cdd7cc5fb9a68add74bbd2c93))

* doc: correct table header ([`b6a8d55`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b6a8d550bb64dd8b3710f5868218195da2c142ff))

* doc: small doc fixes ([`ff21760`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ff217608fad1b3df38986e5b17ab2db695550449))

* doc: add momotor.bundles.utils.tasks to documentation ([`f6dbecd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f6dbecda4f951833799bd8be895938104bfcc2f5))


## v5.0.0 (2021-11-19)

### Breaking

* feat: support multiple tasks per step

BREAKING CHANGE: interface of `momotor.bundles.utils` package changed to support task ids ([`3841148`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3841148996e45d16395d68261468816cb381fdde))

### Chore

* chore: update project files ([`1c75bf5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1c75bf51097605eb70359db20c6f4f0ddba7dae9))

* chore: version tag is in os.environ on CI ([`b246e9f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b246e9f76189febb394f47ac9cb86a3261dc2846))

* chore: link to documentation with the correct version number ([`395ae50`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/395ae50bb9dd2dbaaecca2daccd4b79417761854))

* chore: link to dev documentation for dev versions ([`1a1772d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1a1772d4b541b9468b94c6b76ac86cb5b4d5edac))

* chore: update project files ([`09c2d56`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/09c2d56632c80019569f614d4705b9910b74267b))

* chore: update project files ([`a5428a5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a5428a5a080f680703b1d9c744b2e9095f63e9e3))

### Ci

* ci: sync gitlab-ci and semver files across projects ([`d6ca9f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d6ca9f35fd8e1f7fec7b068213a608c0f35fd1ff))

* ci: run tests against Python 3.10 ([`a64ded6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a64ded65b1939d1d0a80727ec638b2a39d85bb4f))

* ci: set pip upgrade strategy [skip-ci] ([`ce7592a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ce7592acff33a0913fcd46631dbeefe72a3ec52c))

* ci: persist pip cache [skip-ci] ([`0274fc2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0274fc20415a284ff309865e158322e336074e66))

### Feature

* feat: make `FilesType` public ([`003a359`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/003a3599f74d07dbdf4e488e713e50f2bd50fc29))

* feat: made `apply_task_number` public and added `make_result_id_re` ([`9c5ab14`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9c5ab14dc14839cba4b94cdb2de5c4bb4b8384bf))

* feat: add task utility methods `task_number_from_id` and `task_id_from_number` ([`3e66a83`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3e66a838ec24a31964d8a64335b19e677cb386a0))

* feat: when recreating a result, allow changing the step_id ([`93b049d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/93b049d1db2849d330b00b75ed000db9000054bb))

* feat: add types for locations and providers ([`db36dde`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/db36dde59080f0c4780fafd25df1169719fa7ccc))

* feat: changes to dependencies and tasks methods ([`b5832f0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b5832f0d081487aa2a4c44e8dfa0ccec84aa5b4b))

### Fix

* fix: self.depends can be None ([`2ab3196`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2ab3196ac48c87af41e0841eacc294fbdb7fcc99))

* fix: get_task_dependencies() returned incorrect mapping ([`7984431`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/798443155c37aa79e3a3b1b964f7932fcd4a803a))

* fix: KeyedTuple.get() raises KeyError when item does not exist ([`cee605a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cee605a777f2163b22c28e2482234aab4d31b525))

* fix: cleanup and optimization ([`034475e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/034475e14f5a8ef84445669437f5ea0e6458b0cb))

* fix: typing ([`e09129c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e09129cc26ec28f4602925e1834965ca02f48974))

* fix: relax XML dependency and result step-id types ([`28c388a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/28c388ae255a9ccc76a9482661d92b2e221a4ee2))

* fix: install xsdata[cli] in development ([`fcfc65c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fcfc65cd3254f77c5253d38b309cd3e3b68508a4))

* fix: more verbose file exceptions ([`ba6de38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ba6de386519e9f497f239ab2299df7b5d5eaddc7))

* fix: period in step-id is not a problem ([`4f4fc78`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4f4fc78f8a0d2ee01b50835f0c341c4f7ab8a7ec))

* fix: unit tests ([`ddab49b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ddab49b90edde9f655eca5e73ac213f22e45ddc3))

* fix: clearer assertion error messages ([`e3ac2ca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e3ac2ca6693491987f5cd1f1758038dccc89bd59))

### Unknown

* 5.0.0

&#39;chore: bump version number&#39; ([`9e3f958`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9e3f95894e84c2b37a539050d1004ddbc2a0a7bc))

* Merge branch &#39;multiple-step-tasks&#39; into &#39;master&#39;

Resolve &#34;Implement changes required for multiple tasks per step&#34;

Closes #22

See merge request momotor/engine-py3/momotor-bundles!12 ([`1ef8a2f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1ef8a2f875bf7647de29e0ca5f02ac97d0cec0a7))

* doc: update docstring ([`10fa95a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/10fa95a72e15c0ed514b2c8a0e39459a1fba6512))


## v4.1.0 (2021-09-23)

### Feature

* feat: make exported attachment file names pure ASCII (closes #21) ([`244edef`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/244edef5b3aaab11e276a1144374a37562f0a099))

### Unknown

* 4.1.0

&#39;chore: bump version number&#39; ([`2b135e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2b135e0f184fa0ab9b37ffc0c98a2d415a82483f))

* Merge branch &#39;21-only-use-ascii-characters-for-attachment-file-names-and-limit-length&#39; into &#39;master&#39;

Resolve &#34;Only use ASCII characters for attachment file names and limit length&#34;

Closes #21

See merge request momotor/engine-py3/momotor-bundles!11 ([`e461030`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e461030f2f5bf632af688a30663b9f6fedf40c3f))


## v4.0.3 (2021-09-14)

### Chore

* chore: update project files ([`d5df95e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d5df95e613528be6fa5359f22a7367264973b4e2))

### Fix

* fix: do not strip trailing whitespace from quopri encoded inline content ([`023da26`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/023da2640f25ae626bbc98e308611d9be8e762ec))

### Unknown

* 4.0.3

&#39;chore: bump version number&#39; ([`4648858`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/46488581b7f172eb6148c5eab6d0d2d410532509))


## v4.0.2 (2021-08-21)

### Fix

* fix: tests for directories in zip bundles ([`256755e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/256755e05ac17d6a70d6beb08939d6685583e262))

* fix: if path validation fails silently, set path to None ([`26cae68`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/26cae685cc231c9f390dd0b6e802495949da1ba1))

* fix: added `legacy` argument to factory arguments, only ignore checklet src errors when legacy mode is enabled ([`79175d5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/79175d5a4d88d56d8a437a3c72ab7f2ca08342c2))

### Unknown

* 4.0.2

&#39;chore: bump version number&#39; ([`c58892f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c58892fd5093b4939ed14d760443037caee22696))

* Merge remote-tracking branch &#39;origin/master&#39; ([`b75f8db`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b75f8db29e2558f7d18c46b262f2ecbd13ef8984))


## v4.0.1 (2021-08-20)

### Fix

* fix: result nodes may contain checklets with invalid `src` attribute

Disabling validation for those nodes ([`227258d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/227258d6cce058158438cb9de3bced0bbb7a4c26))

* fix: honour the `validate_signature` setting when creating checklet element from node ([`6c10099`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c10099ad315a539a7803c3e54e3adb1de1c0b8e))

### Test

* test: update test recipe ([`336096a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/336096a5487e4eb13ff03fda7bd4e01b87777240))

### Unknown

* 4.0.1

&#39;chore: bump version number&#39; ([`d7ce393`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d7ce393f0b6cfce75c97f7ca6553ec8e2e4dc2a1))


## v4.0.0 (2021-08-17)

### Chore

* chore: remove old attachments code ([`48c3229`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/48c322949f133966b015aee749cb33165e7ee143))

* chore: mark as production/stable ([`7493e56`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7493e56344826bf4fdf48512cdf57a6e595f07db))

* chore: correct xdata[lxml] dependency ([`eac9a7a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/eac9a7a83a6ed3e39ea089a3a84ee44a23ea6a20))

* chore: better exception message ([`f0f16d0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f0f16d08570defb0e4eaf9385a870fe297455e86))

* chore: add pytest.ini ([`7c94dc4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7c94dc41fc591c63cb5a849f9516d6e66353f1ae))

* chore: result step attributes should be ID, not IDREF ([`f185b22`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f185b220fabd1b142354e0206527fc3013c20ae9))

### Ci

* ci: run nolxml tests ([`3d998ad`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d998ad7731959d8b78af351a86bf41edfdd51e7))

### Feature

* feat: add `Bundle.detect` ([`4988f57`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4988f577ba2f617d81d95a65052dbad8d9989ea1))

* feat: add `condition` to `Outcome` for the common use case where a bool needs to be converted into an outcome ([`2c01d38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2c01d38594db25b531e71ab7dbc8a20342f7a612))

* feat: support Decimal values as alternatives to floats ([`dc98e5c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dc98e5c34e410ea042b8bf440e69cf194e2b60b4))

* feat: add `enable` field to OptionDefinition ([`e95cacf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e95cacfd5ee10c50db00a2e40bb2f39ea21fc4c9))

* feat: warn about missing attachments if `validate_signature` is False ([`16d0512`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/16d051242f0a29d8caf0b2dd5604fca636e48191))

* feat: validate attachment paths on creation ([`9250262`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/92502626ae0acdde65fc85a549cdb4ffc703b33b))

* feat: allow renaming in the recreate method ([`de8e4cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/de8e4cbcfa82edeb6ed0e141c709aa6b6643fd99))

* feat: update xsdata dependency to version 21.7 ([`604ff41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/604ff41f2852534e8ad22e2bc6ad0c45d7d8c66d))

* feat: always convert `name` attribute for content nodes into a `PurePosixPath` ([`8334fe4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8334fe47e02c2e0a3b67444a3b6e96d5e226f72d))

* feat: Implement ~ operator for All() and Any() filters ([`b421a5f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b421a5f2da236ae2f69e668a8a7bf5e8828dc82d))

* feat: Move and rename `Result.OutcomeType` to `Outcome` for easier imports ([`35f0c33`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/35f0c333b2459494b6c68114a3a4b8f9a62593f6))

* feat: added &#39;legacy&#39; option to write XML compatible with the old parser ([`506e93c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/506e93cdf44721f2363f932a08eb98fc90a13b04))

* feat: implement hash validation on bundle load ([`bde7fd6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bde7fd6cf51a1be635c129c6e752ebe8d5d704c5))

* feat: add BundleFactoryArguments ([`c4c1338`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c4c13387b6f770fa44f59d854aa4e0c7fbae59cc))

* feat: implement checklet.repository attachments ([`f4a6f34`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f4a6f34ef55bcd395d0fa657f78e604ba9b3ae3d))

* feat: add `size`, `executable` and hashing attributes to file nodes ([`f098321`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f098321701b2f8c5a8becf75126c4b4d37793f80))

* feat: create dataclasses for the bundle creation options and provide the options to the deeper _construct* methods ([`4899c0d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4899c0dedb9b6a2281b16c01024a3d444f939c4a))

* feat: support referencing files in another bundle (for recreate) ([`477c8b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/477c8b2a2693efc4039cc62dbc17fef6bf916bfc))

* feat: rewrite files and attachments system (WIP) ([`047f8ca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/047f8ca11953fac79af2fc2eaea786e4072f46d1))

* feat: file handling changes

* add FilterableFileList and FilterableFileTuple classes
* add `basename` and `postprocess` arguments to ContentSrcElement.copy_to
* add File.copy_to ([`4bae2d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4bae2d3718713f83e33b796f80c45ae02ea9a1b3))

* feat: change handling of content nodes

* Renamed `ContentElement` mixins
* Added special value `NO_CONTENT` and exceptions `NoContent` and `FileContent` to indicate content nodes with either no content or using the `src` attribute
* Documented conversion from raw to processed content and vice versa ([`3bc4b82`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3bc4b82cac9f31cd8bd9abd256f3e092c5b2efee))

### Fix

* fix: typing.Literal is Python 3.8+ ([`399f4f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/399f4f37faf93064124e2e8fc02d11acf69715d5))

* fix: `has_inline_content` could be incorrect if content was not processed ([`e6eba4d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e6eba4db3083802bd32dd90fcd18f93d42fbb17d))

* fix: correct handling of numeric properties ([`20a0dc6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/20a0dc61256ab402e4fc869b55832d687191b824))

* fix: various fixes and enhancements for `make_matcher_fn` ([`fa81d0e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa81d0e6b143816fae3cce87ea1a363f52d22ca6))

* fix: create directory as documented ([`282b01a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/282b01a231c29cc740205b632fdb7e9067bd1061))

* fix: unused import ([`bc3db17`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bc3db17d2fafd19f623214df610bce1d7e8ffaf6))

* fix: attachment linking ([`6c7a6aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c7a6aa67e322e38fea531f5a97787c323841813))

* fix: results attribute should never be `None` ([`8247e8c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8247e8cef19e56b7e2244cd5967a265d1b967f7d))

* fix: unused target_basesrc argument ([`5f92c82`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5f92c82d80ac254c25777ee16f2697f344f522e2))

* fix: typing.Protocol is Python 3.8+ ([`828e9e1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/828e9e18d62e7c4ad96b5b674e3e395ba8999a04))

* fix: cast Path-like objects to strings, convert to posix paths if possible ([`e3d66d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e3d66d36a59d9cfa1eed31f37435e4d8abe3f9c8))

* fix: provide default checklet.entrypoint value ([`87fa1ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/87fa1aba50f5a81b541074e12681c22ce3b4a670))

* fix: correctly export directory attachments ([`ed7abda`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ed7abdafefeff203e538ae2291d917be46085db5))

* fix: add missing parent node ([`304c6d2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/304c6d2fc6ae7a7ecc614feb025c973ded8e20f4))

* fix: make `export_src` read-only, allow multiple calls to `_export_path()` ([`5147f2b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5147f2baa9923e4dc38c333d89607ed6adba15eb))

* fix: empty attachment nodes ([`6add05d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6add05d0edeadb3503023aee44758d3063b0f3d8))

* fix: handle name arguments ([`9b7bebb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9b7bebb5336a48214b33e3962652b9999c25b08f))

* fix: setting `executable` attribute from file mode doesn&#39;t work on Windows, so just require it to always be manually set ([`3a174b1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3a174b1229a97677fa053584305d5d6e8868f0fb))

* fix: add missing attachments.rst ([`94e7852`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/94e7852a2f538a2a3902f522505a7feef31d73f5))

* fix: prevent import error when lxml is not installed ([`7c6b4f6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7c6b4f607ec04c3a01efdd9a136840fd2aa485e4))

### Refactor

* refactor: remove unused import ([`8ed9fc3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8ed9fc38efc327e68a6cd111d5eef7303ece3c4e))

* refactor: more strict typing ([`635caa3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/635caa332190150f4b53ceff8e635528840e8ed2))

* refactor: add typing for the ZipWrapper attributes ([`8107715`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/81077156d0de0b940547a5f31133047a151b4f3b))

* refactor: move `momotor.bundles.utils.attachments` to `momotor.bundles.mixins.attachments` ([`c26a586`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c26a586dda95c9d61b6e4dc6adfeb4bd71cf13f3))

* refactor: export `to_bool`, make all arguments of`OptionProviders` optional, added __str__ to `OptionNameDomain` ([`a802a2f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a802a2f5fe2c2bbba200d8ff3bdb42d3daf532a0))

* refactor: change _construct* methods to have args as a keyword argument for consistency with _create_from_node ([`9c68e3b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9c68e3b287682fedcf8ca09be32a08b459e219dc))

* refactor: rename BundleConstructionArguments to BundleConstructionOptions ([`c1cc2f8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c1cc2f87de38570f877e5ec8a4f152c6ec4130ae))

* refactor: cleanup ([`9e4466f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9e4466f6a36a12d6fc9a69e6ca9c6564327ac786))

* refactor: cleanup, and make copy actions identical regardless of source bundle ([`1de47b8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1de47b8db9379e6d229c6bfd3bc660ad670e1d78))

* refactor: drop unused `target_basesrc` argument from `recreate()` method ([`178e52b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/178e52b9e34d8a197af2a371c2feeec0d3239b12))

* refactor: remove unused imports ([`c18d43e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c18d43e3952e50f10c04552c6a2bb7ae6a9d9275))

* refactor: remove unused code ([`951505e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/951505ec142116df0fe76d5bc608da3a90b6cfc5))

* refactor: delete unused _dom_path() ([`15147c4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/15147c4e8e296898fb6dac268d4e41e8f04089de))

### Test

* test: add more test cases for non-existent property ([`f0d61bf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f0d61bf684ca829829c1433067b54fca8db2fb5a))

* test: fix unit tests ([`98e7093`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/98e7093c9cf689f39ff77cc88b3e22e3cbd5805d))

* test: base path is not needed to create a bundle ([`ba08a00`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ba08a0009bd6f6a42e827db73fc6c637d4fbc494))

* test: add python_paths option to pytest.ini ([`5948a55`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5948a5590736e9cf7e2bb3f056cd067616b64a9f))

* test: ignore line ending encoding differences ([`a02749a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a02749a9b1819ff43e5059209baaf9ff5d3dc69e))

* test: add test case for Bundle.to_directory ([`05b4caa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/05b4caa25b1ecb1ece7b17b6ec9b1aad014683ee))

* test: add test case for opening an empty file node (failing) ([`5e83671`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e83671d38bb0e2da701bce21e94b8ff5c9b85ba))

* test: create separate test cases for file hashes ([`7bc02fa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7bc02fa94dd3052a74d20a373ce33ee2d1e95b4b))

* test: extend test_copy_to ([`e592131`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e592131338e1894c1b3e83206043258180023979))

* test: make test_files.py and test_repository.py similar ([`805f96e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/805f96ef9e42b0516585aa570571bc35ab9e8cea))

* test: tell git to keep test files in LF format ([`991b10e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/991b10e70bb93a6a7927e4a443aa56a918eba834))

* test: add labels to lxml pytest mark helpers ([`582f65d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/582f65d7fc8ab450ccbb077b9ee90956a2dcf22f))

* test: fix exception in SAX parser ([`abfdac7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/abfdac790ff399c4d4706202fac9f784abd9d940))

* test: skip tests requiring lxml if it is not installed ([`7ce5ffc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7ce5ffc957bff35cbfb8e60c1c2ec95f14ad457f))

### Unknown

* 4.0.0

&#39;chore: bump version number&#39; ([`5dbf235`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5dbf235112c721418187296c0b7a83cf336ae4ce))

* Merge branch &#39;version-4&#39; into &#39;master&#39;

feat: many changes related to supporting Python 3 in checklets

Closes #14, #12, #11, and #1

See merge request momotor/engine-py3/momotor-bundles!10 ([`335119b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/335119b0c802c1d722c5496c6a0705b28380d10b))

* doc: link to filters documentation section ([`ec6810f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ec6810f82115f53bdc49b3e787598ccc34646791))

* doc: extend documentation for `assertions` module ([`494cf03`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/494cf03e3e767c26849eca6974ea52fafa482728))

* doc: remove ascii module from docs ([`0ee4fc4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0ee4fc4683b900b0d964b756ba703d4e805ca5ee))

* doc: update documentation for bundle constuction and factory argument classes ([`46472d7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/46472d75ee5ed61f7d9796f49a4af647818422fd))

* doc: document `Outcome` type ([`44394d5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/44394d534b78278adb230144d864692ba835133c))

* doc: add missing bundle properties and methods ([`3f53747`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3f5374792d28fcc57061672eeab7c799a0f279a0))

* doc: creation is not limited to result bundles anymore ([`f553b7d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f553b7de1e93b350f5cb1479cee85935aaa79391))

* doc: document that accessing a bundle after closing it is undefined ([`28741fd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/28741fd7301c8be51eaeadfa6988b2d4a1379dc9))

* doc: document `recreate()` changes ([`acb0e38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/acb0e38f4127007d24426dd4c00f7e09245a0d1a))

* doc: fix documentation issues ([`757e14a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/757e14a2c1a1f13b5c0a3d79274320ff37fc08b0))

* Merge branch &#39;attachments-rewrite&#39; into &#39;version-4&#39;

Rewrite the handling of attachments

See merge request momotor/engine-py3/momotor-bundles!9 ([`7db29fc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7db29fca1fa29cb267eda22b25e6331694db0b28))

* Merge branch &#39;version-4&#39; into attachments-rewrite

# Conflicts:
#	src/momotor/bundles/elements/checklets.py ([`6301776`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6301776dbcf660bee21fcf68c5ddf05eaf3c9f8b))

* Merge branch &#39;version-4&#39; into attachments-rewrite ([`a3debda`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a3debda5b81cf057cd9c7c88a6bb355a40457275))

* Merge branch &#39;master&#39; into version-4 ([`9d86d8d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9d86d8d54f19e406bd1b792536d4be02e33ef762))

* Merge branch &#39;master&#39; into attachments-rewrite ([`4bf671f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4bf671f1b8ac8f2731bfb04b30e65994a47e4f57))

* Merge branch &#39;master&#39; into version-4

# Conflicts:
#	.gitlab-ci.yml
#	src/momotor/bundles/binding/momotor_1_0.py ([`62bd5ed`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/62bd5ed92940c9a601b68567e5e7fc2828d1b355))

* Merge remote-tracking branch &#39;origin/master&#39; ([`d488100`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d48810081ead97ca045a73626e2171e0c7b3e191))


## v3.4.0 (2021-04-23)

### Feature

* feat: bump xsdata version to ==21.4 ([`52704ef`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/52704ef3b389e7ead93804bf89d32efb64a4ba31))

* feat: recipes have files at the top level ([`7ecfc1d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7ecfc1ddfb7f8cc52e64ec555d7af55e48a7a2e0))

### Unknown

* 3.4.0

&#39;chore: bump version number&#39; ([`3e48955`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3e4895583a1163e8aca4fa515b56f0585553151b))


## v3.3.4 (2021-03-30)

### Breaking

* feat: changed inheritance of option domains, added test cases

BREAKING CHANGE: semantics of option domain inheritance has changed ([`598e4f4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/598e4f4391b29891f5af3b8288f7cf75498fb23e))

* feat: remove &lt;options&gt; from &lt;depends&gt; nodes

BREAKING CHANGE: Removes unused &lt;options&gt; from &lt;depends&gt; ([`bbb4a9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bbb4a9ae17e51ca7369252fd58cecef6ed63182c))

* feat: make bundles immutable and unify interfaces

BREAKING CHANGE: bundles are now immutable. List attributes are now tuples, setters raise an exception when called twice ([`d16c9f5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d16c9f56291764e2083d3a102d8bde838d043348))

### Chore

* chore: update gitlab-ci ([`165f7e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/165f7e0503c75f9a017e07cd88b859bab7bb11e9))

* chore: update gitlab-ci ([`fd71755`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fd71755b773f315806bc256c82d4d4b62e03e6d9))

* chore: update gitlab-ci ([`87f029f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/87f029f579c7a03ff2f5fd56e4a6f172ba63c82c))

* chore: update gitlab-ci ([`731b0c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/731b0c17654b4a74085c80bc7e3ac6990374cc71))

* chore: update gitlab-ci to use rules ([`d12f7a5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d12f7a5704d6911aec6ee9f613c8142d31fd27ae))

* chore: update gitlab-ci to use rules ([`8fc223a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8fc223a761498a37744832f913987c742f35e2aa))

* chore: project file update ([`f0f6146`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f0f6146a9957a53f3aef1e47db4394d9be0a9886))

* chore: use the more standard setup.cfg for pytest settings ([`81c2813`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/81c281317336b2dfa788f7d9fc256ff9c3e0deb8))

### Feature

* feat: update options ([`fd100c2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fd100c220e46d4aaa3be8f0b315708fec2433cfd))

* feat: handle subdomains in OptionDefinition.resolve ([`14dcb46`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/14dcb463a5769ff68d32b56c819148559a8ccc87))

* feat: implement OptionDefinition. Based on StepOption from version 0 step base ([`bb48dbd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bb48dbd5cd9dd293b9fcbf6c941eb4e1d36d02f5))

* feat: drop unused &#39;external&#39; attribute from option nodes ([`456c1b6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/456c1b6d589c7d85ba9471d2940201b0db05210b))

* feat: add types for sequences of options/properties/resources. the getters always return a sequence ([`0d1a818`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d1a8180afee29ed447c657f20013d420cc74714))

* feat: result.outcome property accepts both strings and OutcomeSimpleTypes ([`0e843ba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0e843ba8d1600e2de1b66450bf6949e311bfc9e3))

* feat: add Checklet.get_dist_name() ([`fbf64a4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fbf64a4912a79411dfdb2a3c60264f9ea9d7dfbd))

* feat: use FilterableTuple for file functions ([`66a5666`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/66a56669a62c85c20e1501906369a69104ac9418))

* feat: use FilterableTuple for all sequences of elements ([`8bef5a6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8bef5a620d22f1f6df687514cf2293af7a8e84bb))

* feat: ingest the filtering from momotor-common, modified, added documentation ([`0bb1455`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0bb1455156dffaf785c510b8da75f099a42f9505))

* feat: ingest step_condition.py from base checklet ([`d2cbddf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d2cbddfc78d60d67c81014154e167cab19be1f38))

### Fix

* fix: throw `InvalidDependencies` exception when steps depend on non-existent steps (fixes #20) ([`9204d6b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9204d6b4d2e44e8ab3bdebbaf6c5ad3b2d85cce5))

* fix: Recipe.steps and Recipe.tests always return a KeyedTuple. Setting Recipe.tests should be ignored instead of throwing an exception ([`688e0ac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/688e0ac3032bd6c39f22a83374df9d6d90dc4d45))

* fix: more deprecated imports ([`85466f2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/85466f29a938ff3d85f7838ab9c71f69a799e59f))

* fix: deprecated imports ([`7d3b5aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d3b5aa5cd981ded39779205b5f2da6a70881307))

* fix: skip doctest with known SyntaxError ([`0b696a8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0b696a8a3c3d7bb02e1810ba98cfb129e608a7ab))

* fix: typing.final import in Python 3.7 ([`0754dca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0754dca3730ccb117230ded5afe4e663011a6941))

* fix: move DEFAULT_DOMAIN into Options class ([`d9e89c0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d9e89c04412e44b8890650bfd3e04eaab39b007d))

* fix: add Result.outcome_enum ([`1441a9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1441a9ab483c0aaa7cb027ee2a0046379690318f))

### Refactor

* refactor: export OutcomeSimpleType as Result.OutcomeType ([`8a128aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8a128aa432777eeb6bd9aea009915b4d5dd88fb2))

* refactor: make group_by_attr more generic ([`9a2a09f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9a2a09fb4b7cc72b37992c9a8a5711532ecff8b2))

### Test

* test: add more unittests for option definitions ([`f133d5a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f133d5aac6d3e20969c77b9564a782aeefe7d62a))

### Unknown

* 3.3.4

&#39;chore: bump version number&#39; ([`6f6c241`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6f6c2410fe6ecca85df3496567adb76e1f500cf6))

* doc: add doctest-plus Sphinx extension ([`9a07b38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9a07b38591de37a2bc93ad588aee738d200fcd1e))

* doc: more documentation for F() ([`1c84ad7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1c84ad7a12e69ed0eefb27b347d4d5195ea4bd84))

* doc: correct use of dataclass in doctest ([`493882d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/493882d5397ffcdd79833d92121ad2d6098a021a))


## v3.3.3 (2021-02-11)

### Fix

* fix: __doc__ is not available when running Python with the -OO option ([`3443a3f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3443a3ff002d7c261821cb804df645da65935f3f))

### Unknown

* 3.3.3

&#39;chore: bump version number&#39; ([`eb0ba2f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/eb0ba2ff3bf65894b3384669c9324e08d26bacb6))

* doc: link to Results element ([`6fa8280`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6fa82800e2c9c2f41c5af3041f05f412f1fb6f3d))


## v3.3.2 (2021-02-02)

### Fix

* fix: update xsdata version requirement in setup.py ([`7792b5a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7792b5a7bb252f8b48400ecae2657027884f7a91))

### Unknown

* 3.3.2

&#39;chore: bump version number&#39; ([`c56e811`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c56e8112d3c494690ca4352d3b6e0e2d67822bb3))

* Merge remote-tracking branch &#39;origin/master&#39; ([`b79c27e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b79c27efd33023f0d27b11a50c8b0a5e72ab99ee))


## v3.3.1 (2021-02-02)

### Chore

* chore: remove noisy output from test case ([`cfd47d6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cfd47d65d42160c34bef7b94f1d63c86f7d9fd29))

* chore: correct url to commit in CHANGELOG.md ([`df211e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/df211e9ab70b32f2c5b8d6206867c875085b4c16))

### Fix

* fix: update xsdata to 21.1, undo workarounds (Closes #18) ([`a1ccd2c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a1ccd2cebb6a49153d5b9bffb08812c0ce0e63ed))

### Unknown

* 3.3.1

&#39;chore: bump version number&#39; ([`34cb485`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/34cb48560e2ab0a294e49bedd557bdfa71e5126b))


## v3.3.0 (2020-12-17)

### Feature

* feat: update to xsdata 20.12 ([`90da816`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/90da816bc5d4f1d69e96aff99e627d37811e7bd0))

### Unknown

* 3.3.0

&#39;chore: bump version number&#39; ([`bbb3a80`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bbb3a80c991dc8a9517f9fec05070de2667aa91f))


## v3.2.2 (2020-12-10)

### Fix

* fix: also work around #18 when creating from node ([`586b748`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/586b7484dab3acfdb4f34351aff9feb024e9d148))

### Unknown

* 3.2.2

&#39;chore: bump version number&#39; ([`8e20bf1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8e20bf1a032b472fe0e875d5975a969525a4f303))

* Merge remote-tracking branch &#39;origin/master&#39; ([`c76d31c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c76d31c0ab1f5d788e5e3030f459d1ea1b8850ea))


## v3.2.1 (2020-12-10)

### Chore

* chore: remove print statement ([`63e8474`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/63e847471d8cd8c51685784b9d96f770823c9244))

* chore: correct urls in CHANGELOG.md ([`f2071e3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f2071e37a558987cefcae8ad316cf9f2a25a9f23))

### Fix

* fix: workaround for issue in `xsdata` that tries to convert an attribute value to a QName if it starts with a &#39;{&#39; ([`cdbb172`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cdbb1727ace9c39a094e627b0f2b0cfad1351bfa))

### Unknown

* 3.2.1

&#39;chore: bump version number&#39; ([`fa22c1a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa22c1aa23363a08c33fe3ed40e32b0507686796))


## v3.2.0 (2020-12-07)

### Chore

* chore: include schema files in distribution ([`3cd6023`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3cd602357f612c97dc6f64297e4743766beb7dad))

### Ci

* ci: nolxml test doesn&#39;t work with xsdata ([`bd5beeb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bd5beeb2fab50842764c6da6246d838a1f24f385))

* ci: test against Python 3.9 ([`a34f4f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a34f4f3abe7158c11eec76e1613dee6488812b2f))

### Feature

* feat: drop unused `momotor.bundles.utils.content` ([`fa7db1b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa7db1b044e0e699496ae10d9374376b906cf9ff))

* feat: implement XML validation ([`199a4db`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/199a4db1adf80a0e29b47b8f416e36f46a3ae65e))

* feat: replace pyxb with xsdata lib ([`bb04bab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bb04babba57b10724773b17e8b4bc1f7ad6e3d09))

* feat: replace all pxby related imports ([`05fe125`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/05fe1257629bacf05d03ede5ce851e2be58c27a5))

* feat: replace pxyb install with xsdata ([`5907c56`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5907c56442d3624e36262d3515aae6249ce3eb09))

### Fix

* fix: correct namespace ([`11af2f4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/11af2f4f316c3089ca36312a510eb2e4980d92f2))

* fix: collecting properties ([`975c9c8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/975c9c8b0f6ec47597087bd811fd7a0402210a95))

* fix: correct conversion to and from wildcard attributes ([`1fe986a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1fe986a009d1747bf581b6e313abfcdc59ddd12f))

* fix: correct conversion to and from checklet link/index/repository/package-version elements ([`7da5343`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7da53439a6cdc11d6d4c29f38422b713e4e6608d))

* fix: implement missing method ([`dda46d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dda46d3ab7508aea3da8ba2eb61a19e906070c9b))

* fix: typing.Final ([`4529fc0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4529fc047e28725018e11aa698064db5d9341db4))

* fix: xsdata version requirement ([`42f7068`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/42f7068eba04ce1c6ffe83fb2b6c6df07543a853))

* fix: return a dict of tuples from group_by_attr [skip-ci] ([`b01b007`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b01b007bbf2c8b212b870ca1e601c23601988584))

* fix: group_by_attr should return a normal dict, not a defaultdict [skip-ci] ([`e1e9fce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e1e9fce9c357904aa476c9104f8ca8ac10983f6f))

### Refactor

* refactor: split into several methods ([`fb14d6e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fb14d6eb7742cfbe95607d9d91e317bfca13047a))

* refactor: change named tuples into dataclasses ([`8c45df9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8c45df9932ea26c1c0d324ed08c378e9c8670f68))

* refactor: make local versions of the serializer classes ([`70d27e3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/70d27e3d4158633e35c4f931586e733c835be54f))

* refactor: cache XML schema ([`cd4b9ce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cd4b9ce0d1205b552cdf4cb932bea090443b4aa9))

* refactor: move get_node_type ([`f3fcce2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f3fcce298bfa2d325f554feb513e3e841dc01b1e))

* refactor: namespace use changes ([`faf3086`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/faf3086ba277f99080b6f3c8b4cfc2266cfe9720))

### Test

* test: extend xml creation test cases for lxml and pretty printed variants ([`bc227e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bc227e9df8fcb18771002c58fba43474bef461d3))

### Unknown

* 3.2.0

&#39;chore: bump version number&#39; ([`4eccc70`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4eccc704340d76d852a12da1fc650383ef9da613))

* Merge branch &#39;7-replace-pyxb-eol&#39; into &#39;master&#39;

Resolve &#34;Replace PyXB (EOL)&#34;

Closes #7

See merge request momotor/engine-py3/momotor-bundles!7 ([`3229f55`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3229f5551401f0ae6a8414e2d8c5ac41a087e389))

* doc: add link to xsdata documentation ([`855b7c3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/855b7c3c25f31e574bd041f4d178f0f6b8b98524))

* doc: fix url ([`6949edf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6949edf93f1279634e666bebc23f78f687144aad))


## v3.1.0 (2020-11-02)

### Chore

* chore: update/move PyCharm module files ([`0d6c156`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d6c156f80abb3bf6d70e92a75b44675c62a95f0))

* chore: update Python SDK ([`7d23268`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d23268896f40c24b5cd0a590dc20d006c40b8bb))

* chore: update Python version classifiers ([`6c38f24`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c38f2460a5b4e316c9898214cad92635576f12a))

### Ci

* ci: run nolxml tests with Python 3.8 ([`2760d9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2760d9a6fe6356ba1a1f609fecc5132bc42b94c2))

* ci: configure new hvcs option of python-semantic-release ([`2936739`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/293673934ac6b5c20f9328c19d81b194017a6e45))

### Feature

* feat: add ElementMixinProtocol to help with static type checking of mixins ([`cc514ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cc514ab0be3d3f540e8118604207e8c3c2a19446))

### Refactor

* refactor: fix introspection warnings, add more typehints, move variable definitions from __init__ to class, deduplicate code, docs ([`acd2af1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/acd2af10b3aeda929190e0e76b2f65535fcb7b37))

### Unknown

* 3.1.0

&#39;chore: bump version number&#39; ([`6d88dba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6d88dbaea93090b38a422bc3ad0ad834e8459ce0))


## v3.0.0 (2020-08-17)

### Breaking

* feat: changed minimum Python requirement to 3.7

BREAKING CHANGE: Requires Python 3.7 or higher ([`c5d3a65`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c5d3a65f15e737c1033a5ce4a98e9250cb7b2b0f))

### Unknown

* 3.0.0

&#39;chore: bump version number&#39; ([`a8666fc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a8666fc4b24af6439eabaaa529bc7dc2f803e019))


## v2.4.1 (2020-08-13)

### Ci

* ci: don&#39;t run docs:dev and pypi:dev stages if build:dev stage did not run ([`b9a9a22`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b9a9a22a7bd29e0f2a49d54bd5e426eda0829f2c))

### Fix

* fix: export `create_error_result_bundle` ([`126246c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/126246c90c7889de2b109c2f535f371fe72c54ed))

### Unknown

* 2.4.1

&#39;chore: bump version number&#39; ([`75bfd9b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/75bfd9bc0dff2832fccd5621e9cad0c182b2e673))


## v2.4.0 (2020-06-29)

### Ci

* ci: do pip install --upgrade ([`f38fac7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f38fac7d9b6d5f229b53fddde332a8322474dd24))

* ci: fix .gitlab-ci.yml ([`c5e0deb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c5e0debf86967fa85bcd4e27a44436894e8da0ce))

* ci: fix issues ([`67085ad`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/67085addddc795868531673b28b8c568aa73c0f2))

* ci: make semver.sh work in both alpine and debian based python images ([`61f69a9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/61f69a9cf68df3595f1740741b008bb51a5ee20d))

### Feature

* feat: add properties to product bundle ([`b1612f2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b1612f26f549102ccfd55fda8aea9503c3f05d4c))

### Fix

* fix: rebuild pyxb ([`9120a38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9120a382410cf364718c42f688d0c31a1a02fd8b))

### Unknown

* 2.4.0

&#39;chore: bump version number&#39; ([`a672929`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a67292970b31790d697ff292b97895c4581bd68c))

* Merge branch &#39;16-add-properties-to-product-bundles&#39; into &#39;master&#39;

Resolve &#34;Add properties to product bundles&#34;

Closes #16

See merge request momotor/engine-py3/momotor-bundles!6 ([`bda8ba1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bda8ba1cf6c7454036bbdced762964d2c0268246))

* project: correct docs/build exclusion ([`9cd0ea0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9cd0ea01e5f53fd6dc183b8dd89ce6b4fb90bfa0))


## v2.3.3 (2020-04-14)

### Ci

* ci: run semver in python:3.8 docker ([`385c226`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/385c2268cd8f5ee3759f4962a5c3dc58100a59b6))

* ci: only enable docs/pypi stages on pushes ([`a25314e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a25314e2d13da839b29863bcd99a7a2f99b8cbf1))

### Fix

* fix: Restored Element.recreate_list(). It was removed from public API by mistake ([`8465348`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/846534868dfcad5cda454275b31ce0acdb477d5a))

### Unknown

* 2.3.3

&#39;chore: bump version number&#39; ([`67788da`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/67788da5f97e998b25c3cca0e82e8264a611becd))


## v2.3.2 (2020-03-19)

### Ci

* ci: prevent pip from installing editables in src/
ci: tell pytest not to recurse into the .git and editables directories ([`51d1642`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/51d16424192d5583fd3b18c587ff4e81ef2f7ed2))

* ci: update commit message for version bumps ([`fade4ea`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fade4eaac51289a49868777b7e56b489f421001d))

### Fix

* fix: to_buffer() already closes the bundle ([`b0d2cb6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b0d2cb618115c4f97a9bb6bc7f88294dfea87eb4))

### Refactor

* refactor: close the bundle in all to_* methods ([`6fdb57f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6fdb57f3f98d86f2723fb871fbeb5f28254657ba))

### Unknown

* 2.3.2

&#39;chore: bump version number&#39; ([`922faf6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/922faf665533228f65ed497094a1c197a948268f))

* doc: correct type hint for creating results ([`6d7a844`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6d7a844803a7fe767ed3e302346074830b69d2c1))

* doc: clarify close() behaviour ([`a8b34e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a8b34e941a69fc7a2b4c4af9ea7a1e6b98900a7b))

* doc: remove html_short_title ([`a8a14c8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a8a14c810f3fe40cb1863d72291ddf1f98c84941))


## v2.3.1 (2020-03-13)

### Fix

* fix: Bundle.close() should just close the bundle, not destroy it ([`32ecba7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/32ecba7949d79254366584bae2d40ab32d8d72b2))

### Refactor

* refactor: correct typing ([`b21dcee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b21dcee41f3fe06a9619fe167d2575b0cffe5855))

### Unknown

* 2.3.1

&#39;[ci skip] Automated release&#39; ([`205c51e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/205c51e504d7abdae2982a99199a5238aa821515))

* Merge remote-tracking branch &#39;origin/master&#39; ([`8d9d0ee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8d9d0eecdabf39049043c00db97eda585856f1e6))

* doc: correct example ([`0f39ea8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0f39ea8491e586cb691c95edc5fdc20e713e1672))


## v2.3.0 (2020-03-12)

### Ci

* ci: correct PyPI repository url ([`0306f03`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0306f0389b98ea225bd5015c95f9c76a924abb3b))

### Feature

* feat: add Bundle.close() ([`0d0fc37`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d0fc37218905167a81d94d7d5de329df6a5a0e1))

### Fix

* fix: checklet node is optional ([`242d64c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/242d64c95254b944d9206b32b10797a0fd4ff96e))

### Unknown

* 2.3.0

&#39;[ci skip] Automated release&#39; ([`3b2d392`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3b2d392558b9b5b51c38c6ebb726131b958e813e))

* doc: correct type hints for File.create name and src arguments ([`1de9e00`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1de9e00375ad8bd5f7a5a4f62a2b4bcdcce02e9a))

* doc: parameterize urls ([`e268741`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e26874174997fcc5c27060f5d9a9b0b0ad7c5a05))

* doc: add project links to documentation side bar ([`a29d394`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a29d394e1aca1ea0b851ab67fa0b932da5fd70a4))

* Merge branch &#39;pypi&#39; into &#39;master&#39;

Publish to PyPI

See merge request momotor/engine-py3/momotor-bundles!5 ([`54dc877`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/54dc877eeb7dd015d0a83a3061e8ad1256651e6b))

* Publish to PyPI ([`5e8d6e5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e8d6e58ad6f7f64cd4108cdb180b40a55d16331))

* doc: add src dir to Python path ([`7234463`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/723446335b2fb032e9272504de044b4f94cb1000))


## v2.2.0 (2020-03-03)

### Build

* build: update project file ([`a679916`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a679916fc34e992d049a2ef49a08e3b7dc5d4ec4))

* build: pkgutil-style namespace package ([`c4b171a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c4b171a7fe61bfba42646a8b2cbd9fee410bd80d))

* build: document that a newer (not-yet existing, possible never) version of PyXB is needed on Python 3.9+ ([`d35d289`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d35d289d3f375a809725d2ff1e2c2c87657d4945))

* build: document that a newer (not-yet existing, possible never) version of PyXB is needed on Python 3.9+ ([`60dae7e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/60dae7e67dac9bf51f43a2e3b4c4ca236a04bda1))

* build: split &#39;dev&#39; extras into &#39;test&#39; and &#39;tools&#39; ([`54351df`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/54351df61e2b975e6fb338e5ddf0e36894962d18))

### Ci

* ci: execute publish script on remote server ([`622c2a2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/622c2a2b8968c92fd4bf8fa0d46fcb2deb1699dd))

* ci: fix ([`538a510`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/538a510cf6067c3b7c53301015e3990ad4388e18))

* ci: fix ([`b42917b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b42917b14bb4b85977b1963966775fc79cdb22ba))

* ci: publish docs (WIP) ([`a4783c4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a4783c4ebf1f51cab4cafdfab1ef5a363b9c9c1e))

* ci: set git username ([`4d44110`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4d4411060d411ac564cbf72a4b66e0405d73da21))

* ci: update setup.cfg for all semver runs ([`50163f6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/50163f6b45b0d2bfe58209caab2056e8a97df767))

* ci: run semver on branches too, without committing the new version number ([`5cbdeed`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5cbdeed5cf8dc3cc4568baaf16aa99b3d53be405))

* ci: fix version tag ([`65fe7fd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/65fe7fd8d58d28f4f97b8463d7452cfa44b0be67))

* ci: install zip ([`6090d35`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6090d35b40293a5ee1b059848881f681d11eebcd))

* ci: base build on full python-3.7 docker image which has all the required build dependencies installed ([`a4f59df`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a4f59df73a2d3d61d15088c6eb0c348865c14d91))

* ci: install even more build dependencies ([`3a7430d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3a7430d8ddda3b0d2fabe5736f357b71700dbdfa))

* ci: install even more build dependencies ([`8077f8f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8077f8f8cbc44182044ee19e788367ca047428ef))

* ci: install even more build dependencies ([`acf4949`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/acf494940edd4d4534295064928e9c514b90f985))

* ci: install even more build dependencies ([`ba04e47`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ba04e47ccec6c6f0243cdfd18c7ab63208b8aa4d))

* ci: install build dependencies ([`3b68b7a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3b68b7ab03ce6fbdca6f3e6740ef7d411306889f))

* ci: install more binary dependencies ([`bc85363`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bc85363fdce7bb40f85c1a9dc9c55ace5a302261))

* ci: install binary dependencies ([`e3e10d8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e3e10d820282ded8fc3cabfa46bfca3eba81f3b1))

* ci: build documentation ([`96bf544`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/96bf544afaaa4a25e17f89a8b761bd404df60db3))

### Feature

* feat: prefix internal methods with an underscore ([`4eb2216`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4eb2216fdc38f5c314f404b94589a78a4c3c16c0))

* feat: add KeyedList ([`bbcd52c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bbcd52cd7a39f68e8cecb5d080283426b193efc9))

### Fix

* fix: always return a time_struct for the timestamp of file_info() ([`5e384c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e384c175df82b5096205e87e4aa238e1bb87e63))

* fix: deprecation warning when type &#39;int&#39; is used ([`3e8dc02`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3e8dc026b0981437f7ab096d5c8e413c68a121a3))

* fix: accept &#39;int&#39; as type ([`6e4db61`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6e4db6112664feb49b399b7c9118ed7ba86e06bb))

* fix: define types and fix parameter for to_directory ([`b9fa16b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b9fa16b7702e2e26ebe37bc3b6be2efd42ba541d))

* fix: always return a results list ([`855e12a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/855e12a08d75c8df4588e97b11c2ddb2610db44a))

* fix: remove __slots__ as it still breaks Python 3.6 ([`33a044f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/33a044fba46ba86ac9a348bcf87841a188ca49d4))

* fix: rename KeyedList__items to __dict to fix a name conflict in Python 3.6 ([`ec92105`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ec9210594144e22a5d0f2fbab9d0132c2f56473b))

* fix: added implementation for KeyedList.count(), remove() and popitem()
fix: some other smaller issues and optimizations
test: added test cases and fixed some issues ([`ef09f88`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ef09f880e8aa95361702d583eccbcaba4fe081b5))

### Refactor

* refactor: use &#34;momotor.bundles.Bundle&#34; as type hint instead of &#34;momotor.bundles.base.Bundle&#34; ([`0923f87`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0923f8725d37cccfdd54eccf5fb5db95cf6ab7bd))

* refactor: move ZipWrapper to utils ([`2c505e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2c505e0934a195cadf7e4f4503cd3c29c4a218ba))

* refactor: add __all__ ([`62f1394`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/62f13949c1924d4840d4321fb7b5607ccc84d40d))

* refactor: correct order of assertion ([`357bbc0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/357bbc02e1640c97486dba78f7d478dd0aca8b0c))

### Unknown

* 2.2.0

&#39;[ci skip] Automated release&#39; ([`36c2389`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/36c23895f62cf71dc4095c5f3b19d2b0f7eb1b76))

* Merge branch &#39;13-documentation&#39; into &#39;master&#39;

Resolve &#34;Documentation&#34;

Closes #13

See merge request momotor/engine-py3/momotor-bundles!4 ([`ab73054`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ab73054536447f540f8b3ba8428e376337df339a))

* Merge branch &#39;master&#39; into 13-documentation

# Conflicts:
#	momotor-bundles.iml ([`0b12c7b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0b12c7beed80f41a240ce41ad2c4417199a840a0))

* doc: fix short underline ([`561ffed`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/561ffed53ab332a4b0bb8ea9841b86ae67b111a2))

* doc: add top-level documentation for all Element subclasses ([`f4ceef2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f4ceef292569545db067aecc5fb38435ae76a9da))

* doc: update documentation of bundle constructors, include ZipWrapper in documentation ([`0f111e5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0f111e5e6bf73b08bd225c29ce246a49a742c7cf))

* doc: correct and extend documentation of the from_XXX_factory factories ([`36718f8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/36718f8ae937260a40aa833c103c793ee16bda41))

* doc: add TODO ([`baf8fff`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/baf8fffb87c4b8aaaa1a5b281f1f52918d2c3b40))

* doc: enable intersphinx extension ([`ee3ebe0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ee3ebe04df7ab88523cbc178b78667f8018bb411))

* doc: extend Bundle documentation ([`4ba6858`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4ba68583413bf596b6d8ac7f5d3bd0d070793d0a))

* doc: update documentation for .create method ([`3cafce9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3cafce9255d419763dd015e7c3ac252d154952a1))

* doc: document ResultKeyedList ([`e7ef3cd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e7ef3cd9da84721cafa516a7663e6b86cfed066a))

* doc: extend example ([`da4b6b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/da4b6b28f50223b43bf6dd978fafbaf4c7157246))

* doc: creation only supported for *result* bundles ([`398a8e2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/398a8e25967ea0b8de54605c4700dd7f07870852))

* doc: add usage examples ([`fe6055d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fe6055d089e40daac0be554d6e1ad8fda66056d8))

* doc: documentation touch-ups ([`66d373a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/66d373a6a3215b08f9e1680b9bf497c82dd71845))

* doc: update bundle classes documentation ([`fe0cf5c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fe0cf5c851c3046e3c4c0cf61136570b3ddd306c))

* doc: update documentation for Bundle class ([`5e5b507`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e5b507110420abaa5f374f26e4b027dcdaf952e))

* doc: edit docs ([`a18af41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a18af418a0ab4f1614a556202bf88e29f3ba14c7))

* doc: update utils doc ([`633afcf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/633afcf1ed4130ca4b2bc7961f3a698e58a93167))

* doc: use autoclass with specific options for each class ([`f511f33`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f511f33fa5da3d9b26276727e93084c879b5faf9))

* doc: document Step ([`57051e4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/57051e45b4e977b67a40d6532580b6955fe6a571))

* doc: document Result and Results ([`fed1231`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fed1231c7e178e67bd188c901ef87d3ea9743f28))

* doc: remove __all__ ([`8e2befb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8e2befb2d892b15d7f4bba9c55594d97e6d8dfd7))

* doc: use Sequence instead of List for setters ([`dff6341`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dff634178511b1197120a43b5df0a8d8326a387a))

* doc: document unimplemented recreate() ([`863295d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/863295db31de1f4085e1661d0408bdd66efaec68))

* doc: document Option, Property and Resource ([`c22b0bd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c22b0bdc954ea31c92a090b2108cac8ec0ac2660))

* doc: update documentation for create_from_node ([`733957e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/733957ee13475bb53942a76b27b0542e8dabae88))

* doc: document content elements and file ([`6ae77fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6ae77feec6d6b1001cf19279b338481645c5477c))

* doc: document elements ([`4cf9e14`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4cf9e14a89b073e870a1a783e4c338c897708264))

* doc: order class members by group ([`75760ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/75760ab265dca779443063beb6d546612f870333))

* doc: update documentation for create() method ([`14f85cf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/14f85cfdb12be16c12a4fa5e8acde1243ae0aaa9))

* doc: add sphinx-autodoc-typehints extension ([`c8b8fc3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c8b8fc39e53a4aff9a6945a24d6b4ba61ad07665))

* doc: fix typo ([`8a1aa5a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8a1aa5a937879f501ba71e89d31269c8cebe6589))

* doc: use the &#39;classic&#39; Sphinx theme ([`7d110a2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d110a2eb5cc4ed3afc2d37feb6e621482f8fcfe))

* doc: split into sections ([`dd9229a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dd9229a181fc0a6bcdeb427e6edc7dc18eaca474))

* doc: document the other Bundles
refactor: to better document class variables, they are made private and properties to access them have been added ([`2e69b3a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2e69b3a3d057d2c6b5eaf61e35b366ebbfcd6965))

* doc: correct documention for create() ([`48c47c7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/48c47c75326a9388d83378f0cc1ed9484256a91f))

* doc: document ConfigBundle ([`f2d59ca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f2d59ca8cc34a42ace2d358f38ec3002a08a6c11))

* doc: document abstract base classes ([`ac2b7d4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ac2b7d44ed862f9b6b5434697bba8cdfb9faf690))

* doc: link Python documentation ([`63ebe39`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/63ebe39341e0bdca34de45d14edad316f0f2ab8c))

* doc: run Sphinx quick start ([`cfc72c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cfc72c132b197e5949dcf4a7f84191988a436a38))


## v2.1.2 (2019-11-04)

### Build

* build: extract test specific dependencies into requirements.test.txt ([`c331dba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c331dbae4b3d02ce71387e6c9b1f7f307ab26334))

### Ci

* ci: enable tests on Python 3.8 ([`7de62ad`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7de62ad6dbed9e7ed19de6b44fbf2d05b061af8a))

### Fix

* fix: import collections types from collections.abc ([`84f2af0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/84f2af0b62e3474c0f4afa8a5f92fee3159c0e30))

### Refactor

* refactor: use ExitStack to replace a try/finally and with ([`c85848f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c85848fd22163d8ee85e64912f3acb2d4c067a24))

### Unknown

* 2.1.2

&#39;[ci skip] Automated release&#39; ([`fedd59a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fedd59a65e2182f043048329163279a276dd01d8))


## v2.1.1 (2019-09-24)

### Fix

* fix: location_base already does what original_file_name tries to do ([`fc321e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fc321e864ab0fff38b2ca566e502d63e6c1d7409))

* fix: zip might already be closed ([`3fddbf4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3fddbf4b2515a08caba553ffcbb22af4cd203bac))

### Unknown

* 2.1.1

&#39;[ci skip] Automated release&#39; ([`2c49da2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2c49da24025b72970a21e3aa29c69672a2ab6600))

* Merge remote-tracking branch &#39;origin/master&#39; ([`fca884a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fca884a5d17ac66802947839c0545d1e94683433))


## v2.1.0 (2019-09-23)

### Feature

* feat: rewrite ValidationError to BundleFormatError

Added `original_file_name` argument to Bundle.from_xxx_factory to rewrite temporary file names in error messages ([`e329f97`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e329f97347f8870a2099b34c29fa87e369402047))

### Test

* test: fix unit test ([`73e2690`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/73e2690fb3a25767f2be51031791e8345acd2d88))

### Unknown

* 2.1.0

&#39;[ci skip] Automated release&#39; ([`3755717`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3755717aba4c66940648ed8f46504ee66ae7dfaf))


## v2.0.0 (2019-09-23)

### Breaking

* feat: Changed exceptions

All exceptions thrown by the Bundle class are now subclasses of BundleError,
SAX and LXML parser exceptions have been unified.

This fixes an issue where LXML exceptions thrown were breaking process
executors since they cannot be pickled.

BREAKING CHANGE: Type of exceptions returned by Bundle.from_*_factory changed ([`2b3fc24`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2b3fc247f98ba2e04d7a5a0acb86a432dddb8a11))

### Unknown

* 2.0.0

&#39;[ci skip] Automated release&#39; ([`6c00ed2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c00ed2137c830372f46430c6eb6258a7db627b9))


## v1.4.3 (2019-09-22)

### Build

* build: project files updated after switch to PyCharm ([`31ea8a7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/31ea8a7767fd914603be3e7703e32904f66f6888))

### Fix

* fix: enable &#34;huge_tree&#34; option when parsing with lxml ([`35d97fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/35d97fe47e5299c06dfc6de4e3bb0109ce206364))

### Unknown

* 1.4.3

&#39;[ci skip] Automated release&#39; ([`502d915`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/502d915e611f17513113213f9709f42cc4a0799d))


## v1.4.2 (2019-09-17)

### Fix

* fix: correct conversion of src to PurePosixPath ([`113e7d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/113e7d3e3b551006cfadf1fab949a7c0fa902441))

### Unknown

* 1.4.2

&#39;[ci skip] Automated release&#39; ([`a31f2d2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a31f2d2bfc4e8597907784abd2ccf57e547e48f1))


## v1.4.1 (2019-08-27)

### Fix

* fix: checklet is optional ([`a053176`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a053176bf4bbbc827575d2d0b8c93fc63e548a8e))

### Unknown

* 1.4.1

&#39;[ci skip] Automated release&#39; ([`9e86573`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9e865738d64f9be0d2881d8b4b0ed48e4ee38a33))


## v1.4.0 (2019-08-22)

### Ci

* ci: manual test:pynext stage ([`f5b4e6e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f5b4e6e757dd3cdfe98b407731f3680424cb9c42))

### Feature

* feat: add resources complex type ([`84eb4e2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/84eb4e26e9e5ec02edac31230630970ff818b2e8))

### Unknown

* 1.4.0

&#39;[ci skip] Automated release&#39; ([`9246d6e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9246d6ee87035b63aa66aa9413b7aecaf31af102))

* Merge branch &#39;8-add-executor-complextype-to-checklet-nodes&#39; into &#39;master&#39;

Resolve &#34;Add executor complexType to checklet nodes&#34;

Closes #8

See merge request momotor/engine-py3/momotor-bundles!3 ([`191b474`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/191b47468652f7d7c4ab197bbed43b55fb642594))


## v1.3.1 (2019-05-23)

### Ci

* ci: Updated CI

* Add semver and build stages
* Use alpine images for test stages
* Replaced 3.8-rc with rc-alpine image, to always test against next Python version ([`58a9159`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/58a9159fd31baa0707aa27bacbd4efbfef597ec2))

### Fix

* fix(files): correctly handle path types for `name` and `src` attributes ([`d0b0b0b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d0b0b0b5a6bcf5d610eeecb03bf73837291dab23))

* fix: accept any relative Path and convert to PurePosixPath ([`6a6d70d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6a6d70df14c275492e7d0d4beb784f662a1c8be9))

### Unknown

* 1.3.1

&#39;[ci skip] Automated release&#39; ([`c4e0c1c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c4e0c1c628b799f51d4b7dc6a2a80ddbe33f8a7b))

* Merge branch &#39;ci-build&#39; into &#39;master&#39;

ci: add build to ci

See merge request momotor/engine-py3/momotor-bundles!2 ([`671fc74`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/671fc744d5596bd4ceb7632b21e9e4a708ee1809))

* Python3.8 tests are allowed to fail for now ([`4f310e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4f310e9a26e14c63193d8958e920c1c596a08dbe))

* Fix(Result): use of old attribute name in create_error_result()

Property.create `content` attribute was renamed to `value` ([`de3d2de`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/de3d2de5831d0adc8c6a0c0918bb1e1258c11317))


## v1.3.0 (2019-05-02)

### Unknown

* Added support for Windows, specifically windows file paths and line endings in test cases ([`45dd067`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/45dd0672931ea69a7a6f2e16208a0d905f31c20f))

* Removed dependency on curses module, as it does not work on Windows without an extra dependency ([`96baf12`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/96baf12867b8d114f1413dfe4099f420fc1ee18d))

* Use correct way of adding result to a new bundle ([`c0c7578`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c0c7578a432b51dfd97e1da28706fdfbf40f5613))

* Also suppress the &#39;Unable to convert DOM node ...&#39; warnings from PyXB when writing ([`f9f7db9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f9f7db9144afa4fa343fb9d0de92730565414dc5))

* Test warnings suppression with and without lxml ([`49ff550`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/49ff55006d6ce30fa0dfad5630dd8e08a4098bc2))

* Suppress the &#39;Unable to convert DOM node ...&#39; warnings from PyXB (Closes #6) ([`d06b486`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d06b48615e66a07fa902dd3fdcc965261ad1fc03))

* Checking for expected XML using XML literal text is fragile, because attribute ordering is not guaranteed.
Use the xmljson package to convert generated XML into a dict for more robust tests. ([`aff0f52`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/aff0f52deec032f8a80b4a20e0c9c0de0bcffcc3))

* Added test job for Python 3.8-rc ([`1bf5cd3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1bf5cd3f6ff87bf088027cceec62ab762941845e))

* Correct backwards compatible handling of the &#39;domain&#39; attribute ([`8e03d77`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8e03d779ee031278f5f62ba4a16b4a59f7da8efe))

* ContentElement is abstract ([`f8303cf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f8303cf2a788f1d2ef1ae8761f29c5c6ea3c3e6b))

* Also handle &#39;type&#39; for src type nodes ([`c4d8120`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c4d81202ce49f5f60b9670ffd826bd07af99adcb))

* Correctly handle the dual interpretation of the &#39;type&#39; attribute of content nodes. ([`ac1ba26`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ac1ba266f1868f14246eedab8edfa17306f271ab))

* Unify content handling of File and Option/Property nodes (Closes #4) ([`2b4220f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2b4220fe30590784f8dadeb5a25b1fc36b3076a5))

* Rewrote mixin for content nodes (Partial #4)
Includes deferring content decoding until content is needed (Closes #5) ([`e9fbddb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e9fbddbe5a108f91298ab5219bd674e20b306b54))

* Prevent pytest from using TestResultBundle as a test case ([`0fbdb3a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0fbdb3a8d67677536c38df732959631c01e194ce))

* Fixed reading entities in options and properties ([`59ede3a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/59ede3ad4f6294c55193b0554cc066baeef6d9c8))

* Optimization ([`fa1be22`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa1be22684c4f65ef984ed9a4325f664e76d86f5))

* Process mixed element and non-element contents:
* If the non-element content is only whitespace, it is removed
* A warning is given for mixed content, and non-element content is ignored ([`f0bef66`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f0bef66bff40c7bcbfceac3fc6639d7acc4df466))

* Fixed returning wrong property ([`7620a3b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7620a3bd49e2fcd1c3a98f1e5ee8c970bd8e2e6a))

* Added validate_xml option to Bundle from_xxx_factory methods ([`d921039`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d921039f66ac248da8a0c38762e6b63a2acc162d))

* Warn on invalid outcome value ([`d3619d6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d3619d641ce9bb8d173519821c1ad30fccaca565))

* Unified content reading for properties and options ([`25faf3d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/25faf3d4bc96b2795910dae377e275fea08b4034))

* * Added &#39;filter&#39; argument to Element.recreate_list(), useful to recreate bundles partially
* Handle option nodes with encoded content ([`a2d2946`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a2d294698b8bb8a3f1dc658ba8da1bd550bad471))

* Prevent writing the same file multiple times to a zip bundle. Workaround until #2 is fixed ([`862c9bf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/862c9bfd2e6b81fa205b737c8261fa045489d8b5))

* Use typed version of namedtuple ([`d53d21f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d53d21f1fb1025cdff8c94f542a6dfb11b84f5ca))

* Bumped version number ([`95c778d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/95c778ddbef163e9e80d34e9676cdaef4b65e169))

* IDNA encoding breaks on strings with two consecutive dots, use a custom split/merging encoding of path parts based on punycode
Added test cases for it ([`7cff91a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7cff91aeac66a19b7270d58ee57961b116950c17))

* Bumped version number ([`7ed951e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7ed951e9c2b04795767f50fbce137cf1bdb88bba))

* Use zip_file.get_info instead of open to detect file existance ([`820aafa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/820aafacd322ebe6aec166c13cfd3254c1bf030e))

* Only set ZipInfo._compresslevel on Python 3.7+ ([`ad52d86`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ad52d86591f294c82bbe77afca7679e520012c03))

* Set compression, size and timestamp values for zip attachments ([`ce8d9fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ce8d9fe410c2c10f4284362ebd4a9a90fc69f82c))

* Give a warning if the file source path contains non-ascii characters ([`75eda84`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/75eda84ea3525ab2b3388c03ff9f045172f19bd3))

* Encode src paths ([`6b794cc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6b794cce6cb327b1b99fa67a41155a696e6cbf27))

* target_src should be relative to target_basesrc, if possible ([`115f36a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/115f36acf0f0b686926207300c6e006134b32d07))

* compresslevel argument is only available in Python 3.7+ ([`7d2b574`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d2b5745b56cf2e1685205184a822125ea6e169e))

* Use deflate as default compression for zip, added compresslevel argument ([`e7eff31`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e7eff312d974c2d4b8e46e42beca9b33a588f134))

* * Renamed `Bundle.to_bundle` to `Bundle.to_buffer`
* Added `Bundle.to_file` ([`634f186`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/634f186c2d4ca14232e442211a7b46c7808f12a1))

* Added ZipWrapper allow bundles to be pickled with multiprocessing ([`e130797`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e130797f261fb4e81cb0053f398c45bc2b96e5fa))

* Get version without doing an import in setup.py ([`59e4cc4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/59e4cc40ffce1f8bd45b1a875978362e48a1ce26))

* Updated version for initial public release ([`44675f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/44675f3e57268a1c01b405dd85b76d8274f314e0))

* Handle repository type checklet nodes ([`4de5c86`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4de5c868d9b8347802b95b2f607a5137c26b9808))

* Fixed more directory issues ([`6045b13`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6045b1383e587411c32504e044ee5688bc9376b8))

* Exclude egg-info ([`b2c9f8e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b2c9f8e29597a3e5ae4897c2f9e63cf6ce89f65d))

* Optimized imports ([`e5588e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e5588e9646db8a868afb56c93e6bdadf052479ee))

* Merge remote-tracking branch &#39;origin/master&#39;

# Conflicts:
#	setup.py ([`6e5dfbd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6e5dfbdea169f40c6d84e89d151771d52187cd40))

* Use find_namespace_packages() ([`ad05eb1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ad05eb1da3dda08caaa66efd917920398c21ef94))

* Use find_packages() ([`bd35f19`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bd35f199b00179271c210c064d5dd17c02dddbc7))

* Fixed unclosed files ([`792c6a4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/792c6a454ef8ae4f0f9351d466ab5ad98a26f808))

* Added TODO ([`aadaf22`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/aadaf221173b15e6535f3b104b0a4e8b17309369))

* Removed BundleCategory.RESULT ([`dc3acec`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dc3acecb12e15546e7f529f02f2eba15cde452d0))

* Fixed properties encoding ([`4516fe1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4516fe145406f2853fed015542ef98b90510487e))

* Added/fixed options node support ([`bad7333`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bad733346a0319ca653df006e49400117907a1e1))

* Added &#39;create_error_result(_bundle)&#39; helpers ([`0e52bb3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0e52bb3505156d379a9d98a446a0bfce33737049))

* Dropped ResultBundle. Using ResultsBundle with a single result node for single task results ([`f12a348`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f12a3481885130253509732a26f688a2e6fb60cb))

* Handle file exceptions ([`33b4e53`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/33b4e53ec57dbaf5b3cf5e351287b30ff0d17134))

* Dropped default value for checklet-entrypoint ([`069556b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/069556bf2aa7a57c06c55bb18ad68918da2b2a5e))

* Added Result.recreate_as_bundle() ([`c8ab88a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c8ab88a47e8f247fc0b43d3359b293e15b4b6623))

* Added non-file attachments, currently used for inline checklet links ([`513b0b4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/513b0b465be24a0bdfedd6cb5d93c136a3989af1))

* Added content encoding for property nodes ([`58616ee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/58616ee3c8963d26c80cce2cdbbe06d82fbe77cd))

* Implement construct_node for config, product and recipe ([`b47c183`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b47c1838b5a44bd558fb2fe63509972285097824))

* Added support for properties
Added argument to _construct_XXX_nodes methods ([`b49d76b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b49d76be9579f4ffcf9b9f2c0f6b6ae3af67c5e7))

* Added missing &#39;class&#39; attribute to &lt;file&gt; nodes
Process wildcard attributes of &lt;file&gt; nodes
Use orderedContent() to read &lt;file&gt; node content ([`ae41471`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ae41471f1b44946d0c06ebab1e4e6361c9934940))

* PyXB renames &#39;value&#39; attributes to &#39;value_&#39; ([`92adde9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/92adde9c31afa1c0aad94ebffcabc9fc8e70bb02))

* Changes to accommodate the worker ([`0e3d447`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0e3d44767e7a5392003287e97c7a76af6bcd081f))

* Fully implemented checklet element ([`40311fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/40311fea9f65d74b8e17dd9366785e5f8f74048c))

* Added option elements ([`c8a7b05`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c8a7b051355a96309f312664026b37e58d4715d4))

* Added Bundle.to_directory ([`14c2cae`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/14c2cae41bc77dcce9fb643a32de7e022dd617bd))

* Added pretty_xml argument to to_bundle() ([`6f8b14c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6f8b14c9cf32011fe45800757fbb16ca84067190))

* Move `get_complete_step_dependencies` to bundles package ([`58545bc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/58545bc83a8d372fa7e7513ac4ac58ff7998e9cd))

* PEP8 fixes ([`3d16b44`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d16b44f5997cd480f199fcbdcaec6a834be0ce4))

* Fixed setup.py ([`718d196`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/718d196ed12b29c084ff21683a39d81ab048c88d))

* Strip optional &#39;file:&#39; prefix from file src attribute ([`64d64ae`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/64d64ae6cc9de7859f02e28be2cf4c46c7e757c3))

* Added BundleCategory enum ([`cbc87ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cbc87ab29959ef8883472cc4c4787059d7f5393e))

* Renamed AssetType to AssetFormat ([`2e6c7ea`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2e6c7ea8f4560fc176425945c73e7b2f159391b4))

* pathlib.Path is not PathLike..? ([`0b348e9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0b348e907aec2065d73d834cb821ea90852f45d6))

* Added id attribute ([`b4f7030`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b4f7030316518fb85f28018e5efe8563df1e1ab8))

* Make results of TestResult and Results bundles a dict ([`3cb4c74`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3cb4c74227852b791f6272b8923d2b6af2ad834c))

* Added test case that empty content throws an XML exception ([`288394a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/288394acc5d32895bb0a6931a734726138689ed3))

* Make pytest xfail strict by default ([`81c2584`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/81c25849d478c8cf35bccdc6ead0e4879c79121b))

* Handle non-lxml environment ([`4ba52a8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4ba52a8946fb02df18c3bf5e6ba4c73352c51b45))

* Added -y argument to pip uninstall ([`39bd6e3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/39bd6e3e8fce6e522fe149ba240e60b8bd19cabf))

* Added CI test for Python without lxml installed ([`4f57990`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4f57990f41c73aae2d47f8fdbffd12d6341c781a))

* Test all combinations of has_lxml and lxml argument to _from_io ([`916537c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/916537c73c666b8feb084cd2e87d4a3babf1b3d0))

* Simplify XMl literal creation ([`322b52a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/322b52ab3ed3de63e7dae376c7f0d8a4f69a7ad5))

* Use .coveragerc instead of all these #pragma lines ([`2c3aa91`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2c3aa911fd60a53aa5ad5cc03ffa5321cb33f4f7))

* Abstract and not implemented methods do not need coverage ([`5d3ce5f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5d3ce5f2ee47dff2712fe796e012fceadc8fb25d))

* Added element re-creation including file relocation ([`469b41d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/469b41d5588c7e8e5c56cb116b79e9ed6a7f5c2c))

* Small changes ([`f2c3f2f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f2c3f2fd43dbc788b487720912d944a6c36b4fcd))

* Gave Bundle classes arguments defaults ([`db0cf83`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/db0cf8377b721b8aaffbf0ce579d7625f4c6b044))

* Fixed results bundle creation ([`25b0af8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/25b0af81d6eca797f81dda1bda4bab66d1629a3d))

* Added bundle creation ([`73d17f6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/73d17f6d5d0d5c70a698cb3e0837709c854293e0))

* Added test (and fixes) for TestResult attachment groups ([`e628692`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e6286924b434eff0191ebc4a7c4823636e56b512))

* Test result creation
Removed (incomplete) product creation ([`0e23d03`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0e23d03bf4485f451ed970eb25256551b424ff1c))

* Collect all files in Bundle, to make it easier to deduplicate them later ([`e11eaf6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e11eaf62052dd63dea030eca81acfbb6f0067307))

* Collect all files in Bundle, to make it easier to deduplicate them later ([`e7b8095`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e7b8095b1be6418b8be7b7b0f67e5a5a6dfddf40))

* Bundle parsing and creation rebuilt, no reference to the source dom is kept anymore
Correct handling of ref-nodes ([`e7e579b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e7e579b07f9e1402c86ac4a669fe65f6b6965375))

* Cleanup and minor changes ([`0506dac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0506dac40c6022086a23a21d6411c0c93db4d08b))

* More reorganizations ([`ee4f0e7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ee4f0e78c5bbbbbe61613d48fe4d3b2e678326f3))

* Split ResultBundle into a mixin to create a Result element ([`2722601`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2722601f9bc8a5aa2322e56f0daf6f8540dc9682))

* Reorganized momotor-bundles package ([`0969207`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/09692071d4290d10ad725520332c029d73a3e1e7))

* Added tests for file-refs ([`d008c7d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d008c7d9c6448ef8a2d5e280c239230568ebc490))

* Fixes directory listing ([`9d0cb02`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9d0cb02ba58ea28c56c771b1d4f02baf46479059))

* Cleaner test case ([`3a9b1eb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3a9b1eb7b50f10f11fcfae375d13631494c9e7fc))

* Added handling of files ([`9c1741e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9c1741eb8f355a38c4998c1a4515477b0dc4a505))

* There should be only one checklet per step ([`1cc9c3e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1cc9c3ec7555e9668b95463163cb0098d1763ddd))

* Added checklets and reference finding ([`cb321ce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cb321cedb670d6cd230834789e76665caa3fb958))

* Added classes for Step and Depends node instances
Added mixins for common properties ([`6656e02`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6656e0290a186e0c39346dfa16c7108b625ce838))

* Added &#39;result&#39; as a valid root node ([`8f6a412`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8f6a4126fb541f9693a1ccf5cbdae687c4aff6a5))

* Simplified bundles package API ([`edf7e07`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/edf7e07dc9b6e6e482c3153999a5137b30a4cbc5))

* Added ResultBundle
Added some test cases ([`85c9c8c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/85c9c8c902dd91b5046ce75daede3a8e603e39f1))

* Added AssetQuery type
Removed AssetPool.get_all
Rewrote Controller.start_job ([`9ac42cd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9ac42cdf9c1ed895f003dbfc2d2774e84bce0924))

* Started with an end-to-end unit test case that test the run of a complete processing job ([`e8654c7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e8654c7b424308f8e2edfacdc57916679179a684))

* WIP: Started with adding worker tasks ([`4444a90`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4444a9088dddfc88a658d21fe65b16dd22b573ce))

* Extract step ids and dependencies from recipe
Added scheduler to controller (WIP)
Separated tests in for job start en scheduling ([`9ffdf2a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9ffdf2a62efae603790837e3e478736076d73064))

* Added broker.core.controller
Refactored several parts to implement the controller ([`7c12ed7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7c12ed79c45afa38168c232cbe1e62b520c0c53f))

* Remove momotor/__init__.py after build because that breaks package resolving ([`9b3077d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9b3077d38d3b97cee362f10f974e2740f452af7a))

* Fixed test case ([`fb1eb1f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fb1eb1ff636e3f87183c3b684f87ea21ce4c3198))

* Removed superfluous __init__ files ([`b49cde6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b49cde63d6928931eedab0c8fc36988296b4d94c))

* Use &#39;pytest-pythonpath&#39; to set Python path for tests
Add &#39;--cov=src&#39; option in pytest.ini ([`9ad242d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9ad242dc2924df0023dc5ff33ee2fbf90486366b))

* Moved pip install to before_script section ([`fa99807`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa99807b43e1fb5f8502d06050911c00626532e9))

* Added pytest-cov ([`caa57ff`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/caa57ff890e8dfc2107edb8aa064abc163b215ef))

* Colorful pytests ([`080ecb4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/080ecb4b42a88816de3f5118c0a5ec246607fa23))

* More verbose pytests ([`12a1275`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/12a12750be0565f7fab4f86d9fab3c233e0e3e8b))

* Merged ([`57f94cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/57f94cb7d436bce2db429e83b973dd6d55ba5166))

* Add .gitlab-ci.yml ([`897b370`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/897b370d7a2548cce11a0a35eb566916ada38b39))

* Cleaned up imports ([`264ffac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/264ffacf8441cab3b178763875a3dbb2b270e1d5))

* Simplified tests ([`a99d041`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a99d04159be3cfb28af9a72aceda592acf9636cd))

* Removed xslt option from fromIO, when lxml is available, just always check for a stylesheet
Removed lxml option from Bundle.fromFile, always use lxml when installed ([`5642427`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/564242707ec2a8d5b60ff08868dddff71ed2c87a))

* Added lxml parser with xslt support ([`1fde82b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1fde82b9fd9951640f3505971b0f1b01bfcd5985))

* Added lxml parser with xslt support ([`1ea3811`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1ea3811a612c2c70a61f45f16b24d7145ef3f64a))

* Set Python 3.6 minimum ([`8297a32`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8297a321cfea826476db676ab14b91c226ead2eb))

* Separate &#39;base&#39; and &#39;zip_file&#39;, so base can actually be used to refer to a subdir within the zip ([`a6f87d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a6f87d30d63786a22b77b5cb3379222536070d84))

* Added bundle reader classes and test cases (WIP) ([`f3edd83`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f3edd83dd3b4ac6962ee337497d9d5450bba7f7a))

* * Add xmlns:xsi attribute to created xml document
* Renamed &#39;readable&#39; parameter into &#39;pretty&#39;
* Added testcase for invalid xml ([`219fd80`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/219fd8066fbb8676206b3d64922f9bd226d37807))

* Initial commit ([`1c2f2e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1c2f2e8ba84504c0f6175be221754237def71366))
