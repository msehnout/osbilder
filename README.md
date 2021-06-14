# OSBilder 🇩🇪

New, simplified user experience for osbuild-composer.

## Motivation
 * Users who want to build images from CLI don't need the features provided by osbuild-composer:
   * blueprint storage
   * sources manipulation
   * queueing 
 * `composer-cli` has features which are not strictly needed for advanced users:
   * modules lookup
    
## Idea
 * Drop composer from the CLI workflow
 * Right now `osbilder` uses `osbuild-pipeline` which is not built in any RPM, but once we have the depsolv workers, we 
can use it directly and thus bypass composer completely
 * `osbilder` should provide super simple interface to building OS images where all inputs (repositories, blueprints,
   image type, distro, architecture) is specified either in a "workspace" or as a command line argument
   
## Implementation
`osbilder` has two commands:
 1. `init` to create a directory structure like this:
```
--WORKSPACE--|--blueprints--|--blueprint.toml
             |              |--other-blueprint.toml
             |
             |--repositories--|--fedora-33.json
```
 2. `build` to build an image from the repos and blueprints specified in the workspace:
```
$ python3 main.py build --distro=fedora-33 --image-type=qcow2 --blueprint=test --workdir=test
```

See the `try-it.sh` script for example of `osbilder` usage. You can also run the script in a fresh VM (not recommended
running it on your own host system).