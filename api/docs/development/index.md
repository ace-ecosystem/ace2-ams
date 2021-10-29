# ACE2 GUI Development Guide
## Backend (FastAPI) commands
### Format code with Black
```
bin/format-backend-code.sh
```

### Run unit tests
```
bin/test-backend.sh
```

### Run specific unit tests
```
bin/test-backend.sh backend/app/tests/api/test/test_create.py
```

## Frontend (Vue.js) commands
### Compile and minify for production
```
docker-compose run frontend npm run build
```

### Run unit tests
```
docker-compose run frontend npm run test:unit
```

### Run end-to-end tests
```
docker-compose run frontend npm run test:e2e
```

### Lint and fix files
```
docker-compose run frontend npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).