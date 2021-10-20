# frontend code

# Document
https://docs.google.com/document/d/1fLekhdrWLFf40RqKqk_gVcI-2o22fwGXew8y2aCkRqo/edit#heading=h.7q0lpxdflh4o

# Install nodeJS & npm
```
// Download from https://nodejs.org/en/
// follow instructions to install
// Check the install
node -v
npm -v
```
# Install dependencies
```
cd frontend
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Directories
`/src`: source code

`/public`: static html. No need to change.

`/dist`: to store final generations.

`/afterbuild.sh`: to move dist to ../backend/static to access from backend.


### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration for vue
See [Configuration Reference](https://cli.vuejs.org/config/).
