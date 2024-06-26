#!/bin/bash

# Script for building Qt WebEngine packages for Chum. Run this script
# in top directory of checked out qtwebengine repository. May have to
# run it with sudo - depending on docker requirements

set -e

RELEASES="4.5.0.24"
ARCH="i486 aarch64 armv7hl"
BUILDER="${1:-docker}"

# either testing or regular
OBS_REPO_BASE=https://repo.sailfishos.org/obs/sailfishos:/chum:/testing

for release in $RELEASES; do
    for arch in $ARCH; do
        R=`echo $release | cut -d . -f 1-2`
	TARGET=${R}-${arch}
	if compgen -G "RPMS/${TARGET}/*.rpm" > /dev/null; then
	    echo "RPMs for ${TARGET} are found in RPMS/$TARGET, skipping"
	else
	    echo "Building RPMs for ${TARGET}"
	    rm -rf RPMS/${TARGET}
	    $BUILDER run --rm -it -v `pwd`:/source \
		   sailfishos-${arch}-${release} \
		   buildrpm -v chum \
		   -r ${OBS_REPO_BASE}/${release}_${arch}/
	    pushd RPMS
	    mkdir $TARGET
	    mv *.rpm $TARGET
	    tar zcvf ${TARGET}.tar.gz $TARGET
	    popd
	    echo "RPMs for ${TARGET} ready"
	fi
    done
done
