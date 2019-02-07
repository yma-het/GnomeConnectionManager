VERSION = $(shell rpmspec -q --queryformat \%{VERSION} gnome-connection-manager.spec)
TARBALL_NAME = $(shell echo "v_${VERSION}")

clean:
	rm -rf rpm-build

rpm: 
	mkdir -p rpm-build
	tar --exclude="*rpm-build" --exclude="*.git" --exclude="*Makefile" --exclude="*.spec" -czvf rpm-build/${TARBALL_NAME}.tar.gz ./
	rpmbuild --define "_topdir %(pwd)/rpm-build" --define "_builddir %{_topdir}" --define "_rpmdir %{_topdir}" --define "_srcrpmdir %{_topdir}" --define "_specdir %{_topdir}" --define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' --define "_sourcedir  %{_topdir}" -ba gnome-connection-manager.spec
