# [Jsonformer Demo App](https://jsonformer.rahul.gs/)

[Demo app](https://jsonformer.rahul.gs/) for [Jsonformer](https://github.com/1rgs/jsonformer).

## Developing

Once you've created a project and installed dependencies with npm install (or pnpm install or yarn), start a development server:

```
npm install
npm run dev
```

or start the server and open the app in a new browser tab

```
npm run dev -- --open
```

### Modal API

```
cd api
poetry install
poetry run modal serve main
```

## Building

To create a production version of your app:

```
npm run build
```

You can preview the production build with `npm run preview.`

To deploy your app, you may need to install an adapter for your target environment.

### Modal API

```
cd api
poetry install
poetry run modal deploy main
```
