Name:           cvmfs-stratum-uploader-config
Version:        0.1.6
Release:        1%{?dist}
Summary:        Provides example configuration for cvmfs-stratum-uploader.

Group:          Development/Libraries
License:        Apache License
URL:            git://github.com/mknapik/cvmfs-stratum-uploader-config.git
Source0:        %name
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-${version}-${release}-root-%(%{__id_u} -n)

Vendor:         STFC GridPP, Michal Knapik <Michal.Knapik@stfc.ac.uk>
Packager:       Michal.Knapik@stfc.ac.uk

#BuildRequires:  

AutoReqProv: no
Requires: httpd >= 2.2.15, cvmfs-stratum-uploader >= 0.1.6

%description
Provides configuration for cvmfs-stratum-uploader.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
# create dirs
install -d $RPM_BUILD_ROOT/var
install -d $RPM_BUILD_ROOT/var/www
install -d $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader
install -d $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/db
install -d $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/media
install -d $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/static
# create files
install %{SOURCE0}/var/www/cvmfs-stratum-uploader/site.httpd.conf $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/
install %{SOURCE0}/var/www/cvmfs-stratum-uploader/application.cfg $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/
install %{SOURCE0}/var/www/cvmfs-stratum-uploader/db/db.sqlite3 $RPM_BUILD_ROOT/var/www/cvmfs-stratum-uploader/db/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(700,apache,apache) /var/www/cvmfs-stratum-uploader/db
%attr(744,apache,apache) /var/www/cvmfs-stratum-uploader/media
%attr(744,apache,apache) /var/www/cvmfs-stratum-uploader/static
%config %attr(644,-,-) /var/www/cvmfs-stratum-uploader/site.httpd.conf
%config %attr(644,-,-) /var/www/cvmfs-stratum-uploader/application.cfg
%config %attr(700,apache,apache) /var/www/cvmfs-stratum-uploader/db
%config %attr(600,apache,apache) /var/www/cvmfs-stratum-uploader/db/db.sqlite3
%defattr(-,root,root,-)
%doc

%post
sed -i -e 's/__FULL_HOST_NAME__/'`hostname`'/g' /var/www/cvmfs-stratum-uploader/site.httpd.conf
ln -sf /var/www/cvmfs-stratum-uploader/site.httpd.conf /etc/httpd/conf.d/cvmfs-stratum-uploader.conf
DJANGO_CONFIG_FILE=/var/www/cvmfs-stratum-uploader/application.cfg DJANGO_CONFIGURATION=production manage-cvmfs-stratum-uploader.py collectstatic --noinput --verbosity=0
DJANGO_CONFIG_FILE=/var/www/cvmfs-stratum-uploader/application.cfg DJANGO_CONFIGURATION=production manage-cvmfs-stratum-uploader.py syncdb --verbosity=0
DJANGO_CONFIG_FILE=/var/www/cvmfs-stratum-uploader/application.cfg DJANGO_CONFIGURATION=production manage-cvmfs-stratum-uploader.py migrate --verbosity=0

%postun
rm /etc/httpd/conf.d/cvmfs-stratum-uploader.conf
rm -r /var/www/cvmfs-stratum-uploader/collectstatic

%changelog

