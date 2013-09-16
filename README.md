cvmfs-stratum-uploader-config
=============================

  Provides configuration for [cvmfs-stratum-uploader](https://github.com/mknapik/cvmfs-stratum-uploader).


## Building RPM

### Prerequisites

+ **rpm-builder** `4.8.0` - `yum install rpm-build`
+ **git** `>=1.5` - `yum install git`

### Dependencies

1. Download all dependencies:
    + [Django](https://www.djangoproject.com/) `>=1.5.1`
    + [South](http://south.aeracode.org/) `>=0.8.1`

### Setup the environment

1. Create user `rpmbuilder` and set a password:

  ```bash
  useradd rpmbuilder
  passwd rpmbuilder
  ```
2. Switch to `rpmbuilder` user and always build RPMS in context of that user:

  ```bash
  su rpmbuilder
  cd ~/
  ```

### Build from sources

1. Fetch the project and link it to `~/rpmbuild` directory:

  ```bash
  git clone https://github.com/mknapik/cvmfs-stratum-uploader-config
  ln -s cvmfs-stratum-uploader-config rpmbuild
  ```

2. Amend the configuration if needed.
3. Build the project with `rpmbuild`:

  ```bash
  cd ~/rpmbuild
  rpmbuild -bb -v SPECS/cvmfs-stratum-uploader-config.spec
  ```

4. Get RPM from `RPMS` directory and package is ready to install!

  ```bash
  cp RPMS/noarch/cvmfs-stratum-uploader-config-*\.rpm ~/
  cd ~/
  rpm -i cvmfs-stratum-uploader-config-*\.rpm
  ```

## Customize Configuration

The configuration package consist basically of two config files:

1. `site.httpd.conf` - defines configuration for *Apache* `httpd`,
tells the web server where the application is placed, 
what is the Python path and specifies which SLL Certificate configuration
2. `application.cfg` - contains the application specific configuration.
It uses standard [ConfigParser](http://docs.python.org/2/library/configparser.html) syntax.
The file defines database credentials, project paths and others Django settings.

Both files have special character sequences with `__` prefix and suffix (e.g. `__PROJECT_ROOT__`).
These sequences are replaced with smart defaults while installing the RPM.

### `site.httpd.conf`

Usually files like this one should be placed in `sites-available` of `httpd` server 
so the site could be easily enabled and disabled with `a2ensite` and `a2dissite`.
However Scientific Linux does not follow this convention and these two simple commands so usually 
site config files are placed in `/etc/httpd/conf.d/` directory.

By default application's site config is placed in `/var/www/cvmfs-stratum-uploader/site.httpd.conf`
and symbolic link is created to `/etc/httpd/conf.d/cvmfs-stratum-uploader.conf`.

The following settings of the config might be amended if needed:

1. `__PYTHON_PATH__` is autodiscovered by installation script.
To check which environment is going to be chosen run the script:

  ```bash
  python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"
  ```
Variable is used in two places by `WSGIPythonPath` and `WSGIScriptAlias`.

2. `SSL*` file paths might be changed if stored in different directory than `/etc/grid-security`.
[`SSLCertificateFile`](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcertificatefile)
,
[`SSLCertificateKeyFile`](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcertificatekeyfile)
and
[`SSLCACertificatePath`](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html#sslcacertificatepath)
are widely documented in [the mod_ssl](http://httpd.apache.org/docs/2.2/mod/mod_ssl.html) documentation.
The default values are:

  ```httpd
    SSLCertificateFile    __CERTIFICATE_PATH__/hostcert.pem
    SSLCertificateKeyFile __CERTIFICATE_PATH__/hostkey.pem
    SSLCACertificatePath  __CERTIFICATE_PATH__/certificates
  ```
where `__CERTIFICATE_PATH__=/etc/grid-security`.

3. `__FULL_HOST_NAME__` is autodiscovered by installation script.
Default value is fetched with shell command:

  ```bash
  `hostname`
  ```
If you cannot rely on that command `ServerName` can be changed manually.

4. `__PROJECT_ROOT__` points to the directory inside `DocumentRoot`.
By default it contains application and server config files, database file, static assets (images, stylesheets, etc.)
and all the uploads.
If `__PROJECT_ROOT__/uploads` or `__PROJECT_ROOT__/static` is changed
the analogous section in `application.cfg` has to be fixed.


### `application.cfg`

