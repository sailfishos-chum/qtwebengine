# Qt WebEngine packaging for Sailfish OS

As SB2 has some limitations, there are few workarounds used in this
packaging. Some of them are applied as patches, some as workarounds
that have to be applied with every update.

On updates, check Fedora packaging and their patches at their
[site](https://src.fedoraproject.org/rpms/qt5-qtwebengine/tree/rawhide).
Qt WebEngine source consists of two nested submodules.  Due to
Sailfish SDK being picky in applying the patches, patches have to be
applied for each submodule sources separately. This is due to the
interaction of patching and git. So, sometimes Fedora patches have to
be split into two parts accordingly. Patches also have to be applied
while in the corresponding folder. See RPM SPEC for application of
patches and add/remove new ones accordingly.

During a build, Chromium generates V8 snapshot. This is done by
running `upstream/src/core/release/mksnapshot` that is created during
a build. On Aarch64, it fails as it tries to `mmap` 8GB of RAM. As SDK
is using 32bit tools, it is no wonder that this program fails under
`sb2`. Corresponding info at
[forum](https://forum.sailfishos.org/t/sb2-fails-to-mmap-8gb-in-aarch64/15159).
To work around it, there are two files that are injected into the
build: embedded.S and snapshot.cc. On update of WebEngine, proceed as follows:

1. clone this repository recursively

2. start the build by first preparing sources:

```
mb2 -t devel-aarch64 prepare .
```

3. remove in your working copy, files `rpm/aarch64-embedded.S`
`rpm/aarch64-snapshot.cc`

4. start the build:

```
mb2 -t devel-aarch64 build .
```

5. wait till it fails and copy `upstream/src/core/release/mksnapshot` to Aarch64 device.

6. run it as follows on device:

```
./mksnapshot --turbo_instruction_scheduling --target_os=linux --target_arch=arm64 --embedded_src embedded.S --embedded_variant Default --random-seed 314159265 --startup_src snapshot.cc --no-native-code-counters
```

Alternative is to install QEMU with Aarch64 as user target (`QEMU_USER_TARGETS`
on Gentoo and run as in
```
qemu-aarch64 -L ~/mer/targets/devel-aarch64 \
   ./mksnapshot --turbo_instruction_scheduling --target_os=linux --target_arch=arm64 \
   --embedded_src gen/v8/embedded.S --embedded_variant Default --random-seed 314159265 \
   --startup_src gen/v8/snapshot.cc --no-native-code-counters
```

where ~/mer/targets/devel-aarch64 is your SFOS aarch64 target.

7. copy `snapshot.cc` and `embedded.S` from device to this repo and
add under `rpm/` as `rpm/aarch64-embedded.S` `rpm/aarch64-snapshot.cc`

8. try to build again with `mb2 -t devel-aarch64 build .`.

9. if it works, submit the changes as PR
