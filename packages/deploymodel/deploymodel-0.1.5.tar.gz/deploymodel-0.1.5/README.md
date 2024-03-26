# Dev

## Test the example with local deploymodel build
First build the deploymodel package using poetry and move it to `example` folder
```bash
cd backend/app/cli
export VERSION=$(awk -F '"' '/^version = "/{print $2}' pyproject.toml)
poetry build && cp ./dist/deploymodel-${VERSION}-py3-none-any.whl example
```

## Try building example
```bash
poetry run deploymodel build 123 -i example/Dockerfile
```