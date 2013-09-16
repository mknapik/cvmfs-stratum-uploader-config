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

### `site.httpd.conf`

### `application.cfg`
