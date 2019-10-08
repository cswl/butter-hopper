#!/bin/sh

# This script installs the Nix package manager on your system by
# downloading a binary distribution and running its installer script
# (which in turn creates and populates /nix).

{ # Prevent execution if this script was only partially downloaded
oops() {
    echo "$0:" "$@" >&2
    exit 1
}

tmpDir="$(mktemp -d -t nix-binary-tarball-unpack.XXXXXXXXXX || \
          oops "Can't create temporary directory for downloading the Nix binary tarball")"


require_util() {
    command -v "$1" > /dev/null 2>&1 ||
        oops "you do not have '$1' installed, which I need to $2"
}

case "$(uname -s).$(uname -m)" in
    Linux.x86_64) system=x86_64-linux; hash=e43f6947d1f302b6193302889e7800f3e3dd4a650b6f929c668c894884a02701;;
    Linux.i?86) system=i686-linux; hash=e1c6fa89a0d55a56cddb5f26598a15e0f238115423ad884a3673a3e4815fd33b;;
    Linux.aarch64) system=aarch64-linux; hash=b31d50b34f2aeacdecbe97e56d5661b59b49ec84fa5ea3f8ddb022ab1bb5de56;;
    Darwin.x86_64) system=x86_64-darwin; hash=972ff28bf5786a079856cba6941a6001046e4bdbc99cb2f114e6fce31b9265ba;;
    *) oops "sorry, there is no binary distribution of Nix for your platform";;
esac

url="https://nixos.org/releases/nix/nix-2.3/nix-2.3-$system.tar.xz"

tarball="$tmpDir/$(basename "$tmpDir/nix-2.3-$system.tar.xz")"

require_util curl "download the binary tarball"
require_util tar "unpack the binary tarball"

echo "downloading Nix 2.3 binary tarball for $system from '$url' to '$tmpDir'..."
curl -L "$url" -o "$tarball" || oops "failed to download '$url'"

if command -v sha256sum > /dev/null 2>&1; then
    hash2="$(sha256sum -b "$tarball" | cut -c1-64)"
elif command -v shasum > /dev/null 2>&1; then
    hash2="$(shasum -a 256 -b "$tarball" | cut -c1-64)"
elif command -v openssl > /dev/null 2>&1; then
    hash2="$(openssl dgst -r -sha256 "$tarball" | cut -c1-64)"
else
    oops "cannot verify the SHA-256 hash of '$url'; you need one of 'shasum', 'sha256sum', or 'openssl'"
fi

if [ "$hash" != "$hash2" ]; then
    oops "SHA-256 hash mismatch in '$url'; expected $hash, got $hash2"
fi

unpack=$tmpDir/unpack
mkdir -p "$unpack"
tar -xf "$tarball" -C "$unpack" || oops "failed to unpack '$url'"

script=$(echo "$unpack"/*/install)

[ -e "$script" ] || oops "installation script is missing from the binary tarball!"
#"$script" "$@"

} # End of wrapping
