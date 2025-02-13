# Contributing to GradBench

<!-- toc -->

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [CLI](#cli)
- [Docker](#docker)
  - [Multi-platform images](#multi-platform-images)
  - [Manual images](#manual-images)
- [Tools](#tools)
- [JavaScript](#javascript)
  - [Markdown](#markdown)
  - [Website](#website)
- [Python](#python)
- [C++](#c)

<!-- tocstop -->

## Prerequisites

Make sure to have these tools installed:

- [Git][]
- [Rust][]
- [Docker][]

We build [multi-platform images][] to support both x86 and ARM chips, so to build those, you need to enable [containerd][] in Docker. If you're running Docker Engine on Linux, without Docker Desktop, you also need to install [QEMU][].

Other tools that are optional but useful:

- [GitHub CLI][]
- [Bun][]
- [uv][]
- [Make][]

## Setup

Once you've installed all prerequisites, clone this repo, e.g. with GitHub CLI:

```sh
gh repo clone gradbench/gradbench
```

Then open a terminal in your clone of it; for instance, if you cloned it via the terminal, run this command:

```sh
cd gradbench
```

## CLI

Many tasks make use of the GradBench CLI, which you can build using this command:

```sh
cargo build --release
```

That is strictly optional though, and is only listed here because it provides a progress indicator which is convenient when building for the first time. To actually run the CLI, use the `./gradbench` script:

```sh
./gradbench --help
```

This script will always automatically rebuild the CLI if it is not already up to date.

## Docker

Use the `run` subcommand to run a given eval on a given tool. You can use pass any commands for the eval and tool, but to use the Docker images, the easiest way is to use the `repo eval` and `repo tool` subcommands:

```sh
./gradbench run --eval './gradbench repo eval hello' --tool './gradbench repo tool pytorch'
```

Some evals support further configuration via their own CLI flags, which you can see by passing `--help` to the eval itself:

```sh
./gradbench repo eval gmm -- --help
```

So for instance, to increase `n` for the GMM eval:

```sh
./gradbench run --eval './gradbench repo eval gmm -- -n10000' --tool './gradbench repo tool pytorch'
```

### Multi-platform images

The `repo eval` and `repo tool` subcommands are just for convenience when building and running the Docker images locally; they do not build multi-platform images. If you have followed the above instructions to configure Docker for building such images, you can do so using the `--cross` flag on the `repo build-eval` and `repo build-tool` subcommands:

```sh
./gradbench repo build-eval --cross hello
./gradbench repo build-tool --cross pytorch
```

This typically takes much longer, so it tends not to be convenient for local development.

### Manual images

All the Docker images for individual autodiff tools are in the `tools` directory and built automatically in GitHub Actions. However, some of those `Dockerfile`s are built `FROM` base images that we are unable to build in GitHub Actions. All such base images are in the `docker` directory. Each must have an `ENTRYPOINT` that simply prints the tag of the image. _If you have write access to the GradBench organization on GitHub_, you can build, tag, and push one of these images by first [log in to GHCR][] and then running the `repo manual` subcommand:

```sh
./gradbench repo manual mathlib4
```

## Tools

If you'd like to contribute a new tool: awesome! We're always excited to expand the set of automatic differentiation tools in GradBench. All you need to do is create a subdirectory under the `tools` directory in this repo, and create a `Dockerfile` in that new subdirectory. Other than having an `ENTRYPOINT`, you can pretty much do whatever you want; take a look at the already-supported tools to see some examples! You must include the following as the last line in your `Dockerfile`, though:

```Dockerfile
LABEL org.opencontainers.image.source=https://github.com/gradbench/gradbench
```

We'd really appreciate it if you also write a short `README.md` file next to your `Dockerfile`; this can be as minimal as just a link to the tool's website, but can also include more information, e.g. anything specific about this setup of that tool for GradBench.

Before taking a look at any of the other evals, you should implement the [`hello` eval](evals/hello) for the tool you're adding! This will help you get all the structure for the GradBench protocol working correctly first, after which you can implement other evals for that tool over time.

## JavaScript

We use Bun for JavaScript code in this repository. First install all dependencies from npm:

```sh
bun install
```

### Markdown

This file and [`README.md`](README.md) use [markdown-toc][] to generate the table of contents at the top. If you add/modify/delete any Markdown section headers, run this command to regenerate those tables of contents:

```sh
bun run toc
```

### Website

We use [Vite][] for the website. To develop the website locally, run this command:

```sh
bun run --filter=gradbench dev
```

This will log a `localhost` URL to your terminal; open that URL in your browser. Any changes you make to files in `packages/gradbench/src` should automatically appear.

## Python

The Docker images should be considered canonical, but for local development, it can be more convenient to instead install and run tools directly. You can use `uv run` to do this:

```sh
./gradbench run --eval './gradbench repo eval hello' --tool 'uv run python/gradbench/gradbench/pytorch/run.py'
```

We autoformat Python code using [Black][] and [isort][]. If you're using [VS Code][], our configuration in this repository should automatically recommend that you install the corresponding extensions for those formatters, as well as automatically run them whenever you save a Python file. You can also run them manually via the command line:

```sh
uv run black .
uv run isort .
```

## C++

Some tools make use of C++ code shared in the `cpp` directory; if doing local development with any of those tools, you must first run the following command:

```sh
make -C cpp
```

[black]: https://black.readthedocs.io/en/stable/
[bun]: https://bun.sh/
[containerd]: https://docs.docker.com/storage/containerd/
[docker]: https://docs.docker.com/engine/install/
[git]: https://git-scm.com/downloads
[github cli]: https://github.com/cli/cli#installation
[isort]: https://pycqa.github.io/isort/
[log in to GHCR]: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic
[make]: https://en.wikipedia.org/wiki/Make_(software)
[markdown-toc]: https://www.npmjs.com/package/markdown-toc
[multi-platform images]: https://docs.docker.com/build/building/multi-platform/
[qemu]: https://docs.docker.com/build/building/multi-platform/#qemu-without-docker-desktop
[rust]: https://www.rust-lang.org/tools/install
[uv]: https://docs.astral.sh/uv
[vite]: https://vitejs.dev/
[vs code]: https://code.visualstudio.com/
