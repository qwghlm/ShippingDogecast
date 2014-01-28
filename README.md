# Boilerplate

Boilerplate code for a Django project, the way we want it

## To convert to a "proper" project

Where the "app name" is the filesystem-friendly name of our app

1. Rename the `boilerplate` folder to the app name and `boilerplate/static/boilerplate` to the app name as well
2. Replace all instances of `dogecast` with the app name in lower-case
3. Replace all instances of `DOGECAST` with the app name in upper-case

For example, for an app called `test` the commands are:

    $ find . -type f -exec sed -i '' 's/dogecast/test/g' "{}" \;
    $ find . -type f -exec sed -i '' 's/DOGECAST/TEST/g' "{}" \;
