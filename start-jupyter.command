#!/bin/sh
# Corpus Analysis Masterclass - macOS and Linux launcher.
#
# Double-click this file. It finds conda, offers to install it if you have none,
# builds the course environment the first time, then starts JupyterLab.
#
# There is no "conda activate" step, because "conda run" does the same job without
# needing "conda init" to have been run first.

cd "$(dirname "$0")" || exit 1

MINIFORGE_HOME="$HOME/miniforge3"

pause_and_exit() {
    printf "\nPress Return to close this window. "
    read -r _
    exit "$1"
}

find_conda() {
    for candidate in \
        "$MINIFORGE_HOME/bin/conda" \
        "$HOME/miniconda3/bin/conda" \
        "$HOME/anaconda3/bin/conda" \
        "$HOME/opt/miniconda3/bin/conda" \
        "$HOME/opt/anaconda3/bin/conda" \
        "/opt/miniforge3/bin/conda" \
        "/opt/homebrew/Caskroom/miniforge/base/bin/conda" \
        "/opt/miniconda3/bin/conda"
    do
        if [ -x "$candidate" ]; then
            echo "$candidate"
            return
        fi
    done
    command -v conda 2>/dev/null
}

download() {
    # $1 is the URL, $2 is where to put it.
    if command -v curl >/dev/null 2>&1; then
        curl -fL --progress-bar -o "$2" "$1"
    elif command -v wget >/dev/null 2>&1; then
        wget -q --show-progress -O "$2" "$1"
    else
        echo "This machine has neither curl nor wget, so the download cannot start."
        return 1
    fi
}

install_miniforge() {
    case "$(uname -s)" in
        Darwin) platform="MacOSX" ;;
        Linux)  platform="Linux" ;;
        *)      echo "Unrecognised system: $(uname -s)."; return 1 ;;
    esac
    case "$(uname -m)" in
        arm64|aarch64) machine="arm64" ;;
        x86_64)        machine="x86_64" ;;
        *)             echo "Unrecognised processor: $(uname -m)."; return 1 ;;
    esac
    if [ "$platform" = "Linux" ] && [ "$machine" = "arm64" ]; then
        machine="aarch64"
    fi

    installer="Miniforge3-$platform-$machine.sh"
    url="https://github.com/conda-forge/miniforge/releases/latest/download/$installer"

    echo
    echo "This machine has no conda, which is what builds the course environment."
    echo
    echo "I can install Miniforge, the community build of conda. If you say yes:"
    echo
    echo "  - about 60 MB is downloaded from conda-forge.org"
    echo "  - everything goes in one folder, $MINIFORGE_HOME"
    echo "  - no administrator password is needed"
    echo "  - your shell settings and your existing Python are left alone"
    echo "  - to undo it later, delete that one folder"
    echo
    printf "Install Miniforge now? [y/N] "
    read -r answer
    case "$answer" in
        [Yy]*) ;;
        *) echo; echo "Nothing was installed."; return 1 ;;
    esac

    tmp_installer="${TMPDIR:-/tmp}/$installer"
    echo
    echo "Downloading $installer ..."
    if ! download "$url" "$tmp_installer"; then
        return 1
    fi

    echo "Installing into $MINIFORGE_HOME ..."
    # -b installs without prompting and without touching your shell profile.
    # -p says exactly where to put it.
    if ! sh "$tmp_installer" -b -p "$MINIFORGE_HOME"; then
        echo "The Miniforge install did not finish."
        return 1
    fi
    rm -f "$tmp_installer"
    echo "Miniforge installed."
    return 0
}

CONDA=$(find_conda)

if [ -z "$CONDA" ]; then
    if install_miniforge; then
        CONDA=$(find_conda)
    fi
fi

if [ -z "$CONDA" ]; then
    echo
    echo "Without conda the course notebooks cannot run."
    echo "Ask an instructor, or open the notebooks in Google Colab instead."
    pause_and_exit 1
fi

echo "Using conda at: $CONDA"

if "$CONDA" env list | grep -q "^corpusanalysis[[:space:]]"; then
    echo "The corpusanalysis environment is already built."
else
    echo
    echo "First run: building the corpusanalysis environment."
    echo "This downloads a few hundred megabytes and takes several minutes."
    echo "Leave it alone until it finishes."
    echo
    if ! "$CONDA" env create -f environment.yml; then
        echo
        echo "The environment did not build. Show this window to an instructor."
        pause_and_exit 1
    fi
fi

# CI sets COURSE_LAUNCHER_SELFTEST to check this script end to end without leaving a
# server running forever. Students never set it, so they never see this branch.
if [ -n "$COURSE_LAUNCHER_SELFTEST" ]; then
    echo
    echo "Self-test: confirming JupyterLab runs, rather than starting it."
    "$CONDA" run --no-capture-output -n corpusanalysis jupyter lab --version
    exit $?
fi

echo
echo "Starting JupyterLab. Your browser should open on its own."
echo "Leave this window open while you work, and close it when you are done."
echo
"$CONDA" run --no-capture-output -n corpusanalysis jupyter lab
