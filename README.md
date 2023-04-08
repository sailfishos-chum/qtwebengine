# Qt WebEngine packaging for Sailfish OS

As SB2 has some limitations, Qt WebEngine has to be compiled natively. In practice, 
you have to use Docker based Sailfish OS build environment which avoids using SB2.

On updates, check Fedora packaging and their patches at their
[site](https://src.fedoraproject.org/rpms/qt5-qtwebengine/tree/rawhide).
Qt WebEngine source consists of two nested submodules.  Due to
Sailfish SDK being picky in applying the patches, patches have to be
applied for each submodule sources separately. This is due to the
interaction of patching and git. So, sometimes Fedora patches have to
be split into two parts accordingly. Patches also have to be applied
while in the corresponding folder. See RPM SPEC for application of
patches and add/remove new ones accordingly.
